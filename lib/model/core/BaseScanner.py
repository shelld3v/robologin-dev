class ScannerException(Exception):
    pass


class InvalidScannerException(ScannerException):
    pass


class BaseScanner:
    def __init__(self, settings, http_session, url, http_response):
        self.http_session = http_session
        self.settings = settings
        self.http_response = response
        self.url = url
        self._checked = None

    def check(self):
        """
        lazy initialize of __checked
        """
        if self._checked is None:
            self._checked = self._check_response_content()
        return self.__checked

    def build_fuzzer(self):
        if not self.check():
            raise InvalidScannerException()
        return self._get_fuzzer()


class HttpAuthScanner(BaseScanner):
    HTTP_AUTHS = {"digest": DigestHttpAuthFuzzer, "basic": BasicHttpAuthFuzzer}

    def __get_auth_header(self):
        return self.http_response.headers.get("www-authenticate").strip().lower()

    def __get_auth_type(self):
        return self.__get_auth_header().split(" ")[0]

    def _check_response_content(self):
        return http_response.status_code == 401
        and http_response.headers.get("www-authenticate") is not None
        and self.__get_auth_type() in self.HTTP_AUTHS.keys()

    def _get_fuzzer(self, http_response):
        return self.HTTP_AUTHS[self.__get_auth_type()](self.settings, self.http_session, self.url)
