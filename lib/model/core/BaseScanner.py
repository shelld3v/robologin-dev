class ScannerException(Exception):
    pass


class InvalidScannerException(ScannerException):
    pass

class BaseScanner:
    def __init__(self, settings, http_session, url, http_response):
        self.http_session = http_session
        self.settings = settings
        self.http_response = http_response
        self.url = url
        self._checked = None

    def check(self):
        """
        lazy initialize of __checked
        """
        if self._checked is None:
            self._checked = self._check_response_content()
        return self._checked

    def build_fuzzer(self):
        if not self.check():
            raise InvalidScannerException()
        return self._get_fuzzer()


