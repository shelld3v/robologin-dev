from lib.model.core.BaseScanner import BaseScanner, ScannerException
from lib.model.parser.HtmlParser import HTMLParser
from lib.model.parser.FormData import FormDataParser
from lib.model.fuzzer.FormDataFuzzer import FormDataFuzzer,QuickRatioWebFormRecognition
from lib.model.wordlist.PlainTextWordlist import Credentials
from lib.utils.RatioDiffCalc import RatioDiffCalc
from lib.utils.RandomUtils import RandomUtils

import logging

class FormDataScannerException(ScannerException):
    pass


class CSRFHandler(object):
    def __init__(self, settings,http_session,url):
        self.settings = settings
        self.http_session = http_session
        self.token_params = []
        self.logger = logging.getLogger("csrf-handler")

    def add_token_param(self, param_name):
        self.logger.debug("POSSIBLE CSRF TOKEN DETECTED: {0}".format(param_name))
        self.token_params.append(param_name)


class FormDataScanner(BaseScanner):
    __name__ = "Form Data Authentication"
    csrf_dictionary = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._login_forms = None
        self.logger = logging.getLogger("form-data-scanner")

    def _parse_login_forms(self,http_reponse_content):
        parser = HTMLParser(http_reponse_content)
        return parser.get_login_forms()

    def _get_login_forms(self):
        if self._login_forms is None:
            self._login_forms = self._parse_login_forms(self.http_response.content)
        return self._login_forms

    def _check_response_content(self):
        return len(self._get_login_forms()) >= 1

    def _get_fuzzer(self):
        login_form = self._get_login_forms()[0]
        form_data_parser = FormDataParser(self.url, login_form)
        form_data = form_data_parser.build_form_data()
        self.logger.debug('Form data method: {0}'.format(form_data.method))


        first_faildata_usr = RandomUtils.rand_string(8)
        first_faildata_pwd = RandomUtils.rand_string(8)
        first_credentials = Credentials(first_faildata_usr, first_faildata_pwd)

        self.logger.debug('First comparison credentials: {0}'.format(first_credentials))
        first_data = form_data.get_data(first_credentials)

        first_response = self.http_session.request(first_data['method'], first_data['url'],
                params=first_data['get_fields'], data=first_data['post_fields'], headers=first_data['headers'])


        csrf_handler = None
        if len(form_data_parser.get_all_setted_params()) > 0:
            csrf_handler = self._get_csrf_handler(form_data_parser, first_data, first_credentials)
            pass


        self.logger.debug('Second comparison credentials: {0}'.format(first_credentials))
        second_faildata_usr = RandomUtils.rand_string(8, omit=first_faildata_usr)
        second_faildata_pwd = RandomUtils.rand_string(8, omit=first_faildata_pwd)
        second_credentials = Credentials(second_faildata_usr, second_faildata_pwd)

        second_data = form_data.get_data(second_credentials)

        second_response = self.http_session.request(second_data['method'], second_data['url'],
                params=second_data['get_fields'], data=second_data['post_fields'], headers=second_data['headers'])


        if first_response.status_code != second_response.status_code:
            raise FormDataScannerException('Status codes differs in initial response scanning')

        differ = RatioDiffCalc()
        ratio = differ.get_quick_ratio(first_response.content, second_response.content)

        self.logger.debug('Initial Web Form Scan ratio {0}'.format(ratio))

        recognition_engine = None

        dynamic_marks = []
        if ratio >= 0.98:
            recognition_engine = QuickRatioWebFormRecognition(0.98, first_response)
        else:
            dynamic_marks = differ.find_marks_from_diff(first_response.content, second_response.content)
            if dynamic_marks and len(dynamic_marks) > 1:
                clean_first_body = differ.remove_marks(first_response.content)
                clean_second_body = differ.remove_marks(seconde_response.content)
                if differ.get_quick_ratio(clean_first_body, clean_second_body) >= 0.98:
                    recognition_engine = QuickRatioWebFormRecognition(0.98, first_response)

        return FormDataFuzzer(self.settings, self.http_session,first_data['url'], form_data, recognition_engine)


    def _setup_parser(self, first_page, second_page):
        self.dynamic_parser = DynamicContentParser(first_page, second_page)
        base_ratio = float("{0:.2f}".format(self.dynamic_parser.comparisonRatio))  # Rounding to 2 decimals
        # If response length is small, adjust ratio

        if len(first_page) < 2000:
            base_ratio -= 0.1
        self.scan_ratio = self.default_ratio
        if base_ratio < self.default_ratio:
            self.scan_ratio = base_ratio


    def _get_csrf_handler(self,form_data_parser, previous_data, credentials):
        setted_params = form_data_parser.get_all_setted_params()
        form_data = form_data_parser.build_form_data()

        csrf_handler = CSRFHandler(self.settings,self.http_session,self.url)

        for param_name in setted_params:
            if param_name in self.csrf_dictionary:
                csrf_handler.add_token_param(param_name)

        data = form_data.get_data(credentials)
        second_response = self.http_session.get(data['url'])
        second_login_form = self._parse_login_forms(second_response.content)[0]
        second_form_data_parser = FormDataParser(self.url, second_login_form)
        second_data = second_form_data_parser.build_form_data().get_data(credentials)

        for param_name in self.__find_diff_token('get_fields', previous_data, second_data):
            csrf_handler.add_token_param(param_name)

        for param_name in self.__find_diff_token('post_fields', previous_data, second_data):
            csrf_handler.add_token_param(param_name)

        return csrf_handler


    def __find_diff_token(self, field_type, first_data, second_data):
            diff_result = []
            for t1 in first_data[field_type]:
                for t2 in second_data[field_type]:
                    if t1[0] == t2[0] and t1[1] != t2[1]:
                        diff_result.append(t1[0])
            for t1 in second_data[field_type]:
                for t2 in first_data[field_type]:
                    if t1[0] == t2[0] and t1[1] != t2[1]:
                        diff_result.append(t1[0])
            return list(set(diff_result))





"""


class WebFormFuzzerBuilder(object):
    def __init__(self, url, form):
        self.url = url
        self.form = form
        self.headers = headers
        self.redirect_status = [301, 302, 307]
        self.default_ratio = 0.98
        self.scan_ratio = None
        self.redirect_regexp = None

    def setup(self):
            try:
                self.headers['Content-type'] = self.form['content_type']
            except:
                self.headers['Content-type'] = "application/x-www-form-urlencoded"

            first_faildata_usr = rand_string(8)
            first_faildata_pwd = rand_string(8)
        second_faildata_usr = rand_string(8, omit=first_faildata_usr)
        second_faildata_pwd = rand_string(8, omit=first_faildata_pwd)
        first_response = self.get_response(first_faildata_usr, first_faildata_pwd)
        second_response = self.get_response(second_faildata_usr, second_faildata_pwd)

        # Analyze response redirects
        if first_response.status_code in self.redirect_status and first_response.headers['location'] and \
                second_response.headers['location']:
            self.redirect_regexp = self.get_redirect_regexp(first_response.headers['location'], \
                                                            second_response.headers['location'])
        # Analyze response bodies
        self.setup_parser(first_response.content, second_response.content)




    def test_login(self, user, password):
        response = self.get_response(user, password)
        invalid_redirect = False
        if self.redirect_regexp is not None and response.headers['location'] is not None:
            invalid_redirect = re.match(self.redirect_regexp, response.headers['location']) is not None
            # If redirection doesn't match the rule, mark as found
            if not invalid_redirect: return True, None

        ratio = self.dynamic_parser.compareTo(response.content)
        if ratio >= self.scan_ratio:
            return False, ratio
        elif invalid_redirect and ratio >= (self.scan_ratio - 0.15):
            return False, ratio

        return True, ratio

    def setup_parser(self, first_page, second_page):
        self.dynamic_parser = DynamicContentParser(first_page, second_page)
        base_ratio = float("{0:.2f}".format(self.dynamic_parser.comparisonRatio))  # Rounding to 2 decimals
        # If response length is small, adjust ratio

        if len(first_page) < 2000:
            base_ratio -= 0.1
        self.scan_ratio = self.default_ratio
        if base_ratio < self.default_ratio:
            self.scan_ratio = base_ratio


    def get_redirect_regexp(self, first_location, second_location):
        if first_location is None or second_location is None:
            return None

        sm = SequenceMatcher(None, first_location, second_location)
        marks = []
        for blocks in sm.get_matching_blocks():
            i = blocks[0]
            n = blocks[2]
            # empty block
            if n == 0:
                continue
            mark = first_location[i:i + n]
            marks.append(mark)
        regexp = '^.*{0}.*$'.format('.*'.join(map(re.escape, marks)))

        return regexp
"""