import sys
import logging
import gc
import threading
import select

from lib.controller.commandline.ArgumentParser import ArgumentParser
from lib.utils.FileUtils import FileUtils
from lib.model.core.Dictionary import Dictionary
from lib.model.core.Worker import Worker
from lib.model.connection.HttpSession import HttpSession
from lib.model.wordlist.PlainTextWordlist import DefaultPlainTextWordlist
from lib.model.scanner.HttpAuthScanner import HttpAuthScanner
from lib.model.scanner.FormDataScanner import FormDataScanner

MAYOR_VERSION = 0
MINOR_VERSION = 1
REVISION = 0
VERSION = {
    "MAYOR_VERSION": MAYOR_VERSION,
    "MINOR_VERSION": MINOR_VERSION,
    "REVISION": REVISION
}


class Controller(object):
    def __init__(self, script_path):

        global VERSION
        self.script_path = script_path
        self.arguments = self.parse_arguments()
        self.scanners = [HTTPAuthScanner, FormDataScanner]
        self.running = False
        self.setup_logger()
        PROGRAM_BANNER = open(
            FileUtils.build_path(script_path, "lib", "controller", "commandline", "banner.txt")).read().format(
            **VERSION)
        print(PROGRAM_BANNER)
        self.exit = False
        self.dictionary = Dictionary()
        self.parse_settings()
        self.print_lock = threading.Lock()
        for wordlist in self.get_wordlists():
            self.dictionary.append_from_wordlist(wordlist)
        self.start_loop()
        self.logger.info("FINISH")

    def setup_logger(self):
        self.logger = logging.getLogger("robologin")
        formatter = None
        if self.arguments.debug:
            self.logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        else:
            self.logger.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(message)s')
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def get_wordlists(self):
        return [DefaultPlainTextWordlist(self.arguments.wordlist)]

    def scan_site(self, url):
        http_session = self.get_http_session()
        initial_response = http_session.get(url)
        for CurrentScanner in self.scanners:
            scanner = CurrentScanner(self.settings, http_session, url, initial_response)
            self.logger.debug("Scanning with {0}".format(scanner.__name__))
            if scanner.check():
                return scanner.build_fuzzer()
        return False

    def parse_settings(self):
        self.settings = {}

    def get_http_session(self):
        return HttpSession(proxies={'http':self.arguments.proxy, 'https' : self.arguments.proxy})

    def start_loop(self):
        #try:
        for url in self.arguments.url_list:

            gc.collect()
            self.logger.info("Analyzing target: {0}".format(url))
            self.success_credentials = []
            fuzzer = self.scan_site(url)
            if not fuzzer:
                self.logger.info("No bruteforcing method for site {0} found =(".format(url))
                continue
            self.logger.info("Using method {0}".format(fuzzer.__name__))
            self.tested_credentials = 0
            worker = Worker(self.get_http_session(), self.dictionary, fuzzer, self.logger,
                            self.arguments.threads_count,
                            [self.success_callback], [self.failed_callback], [self.error_callback])
            worker.start()
            worker.wait()
            result_line = ''
            if len(self.success_credentials) > 0:
                result_line += "\nCredentials found!!!!!!!!!\n"
                result_line += "\n"

                for i, cred in enumerate(self.success_credentials):
                    result_line += "{0})  {1}\n".format(i, str(cred))
            else:
                result_line += "\n\nNo luck =(\n"
            self.logger.info(result_line)

    def parse_arguments(self):
        return ArgumentParser(self.script_path)

    def setup_report(self):
        raise NotImplemented

    def setup_session(self):
        raise NotImplemented

    def print_config(self):
        raise NotImplemented

    def report_credential(self, credentials):
        with self.print_lock:
            percentage = lambda x, y: float(x) / float(y) * 100
            before = percentage(self.tested_credentials, len(self.dictionary))
            self.tested_credentials += 1
            after = percentage(self.tested_credentials, len(self.dictionary))
            if int(before) < int(after):
                last_digit = int(after) % 10
                p = None
                if int(after) < 10:
                    p = int(after)
                elif last_digit >= 5:
                    p = int(str(int(after))[:-1] + '5')
                else:
                    p = int(str(int(after))[:-1] + '0')

                if p > before:
                    self.logger.info("{0}% - Last credentials processed {1}".format(p, str(credentials)))


    def success_callback(self, credentials):
        self.report_credential(credentials)
        self.success_credentials.append(credentials)
        self.logger.info("********** {0} ********** SUCCESS !!!!!! =D".format(credentials))

    def failed_callback(self, credentials):
        self.report_credential(credentials)
        self.logger.debug("Testing credentials {0}".format(credentials))

    def error_callback(self, credentials, e):
        self.report_credential(credentials)
        self.logger.error("Error testing credentials {0}: {1}".format(credentials, str(e)))

    def critical_error_callback(self):
        raise NotImplemented

    def handler_interrupt(self):
        raise NotImplemented

    def wait(self):
        raise NotImplemented
