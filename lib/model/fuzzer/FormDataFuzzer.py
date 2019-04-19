from lib.model.core.BaseFuzzer import BaseFuzzer
from lib.utils.RatioDiffCalc import RatioDiffCalc
import logging

class FormDataFuzzer(BaseFuzzer):
    __name__ = "Form Data Authentication"

    def __init__(self, settings, http_session, url, form_data, recognition_engine):
        super().__init__(settings, http_session, url)
        self.recognition_engine = recognition_engine
        self.form_data = form_data

    def test_credentials(self, credentials):
        data = self.form_data.get_data(credentials)
        response = self.http_session.request(data['method'], data['url'],
                params=data['get_fields'], data=data['post_fields'], headers=data['headers'])

        result = self.recognition_engine.match(response)
        return result


class BaseWebFormRecognition:
    def match(self, response):
        raise NotImplemented


class QuickRatioWebFormRecognition(BaseWebFormRecognition):
    def __init__(self, min_ratio, initial_response, dynamic_marks=None):
        self.min_ratio = min_ratio
        self.differ = RatioDiffCalc()
        self.initial_response = initial_response
        self.dynamic_marks = dynamic_marks
        if dynamic_marks and len(dynamic_marks >= 1):
            self.initial_response.content = self.differ.remove_marks(initial_response.content, dynamic_marks)

        self.logger = logging.getLogger("quick-ratio-webform-recon")

    def _match_headers(self, response):
        pass


    def _match_status_code(self, response):
        pass

    def _match_json_data(self, response):
        pass

    def match(self, response):
        clean_response_body = response.content
        if self.initial_response.status_code != response.status_code:
            return True
        if self.dynamic_marks:
            clean_response_body = self.differ.remove_marks(response.content)
        content_ratio = self.differ.get_quick_ratio(self.initial_response.content, clean_response_body)
        self.logger.debug('Comparison Page Ratio: {0}'.format(content_ratio))

        return content_ratio < self.min_ratio

