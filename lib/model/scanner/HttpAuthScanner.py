from lib.model.core.BaseScanner import BaseScanner
from lib.model.fuzzer.HttpAuthFuzzer import BasicHTTPAuthFuzzer, DigestHTTPAuthFuzzer


class HTTPAuthScanner(BaseScanner):
    __name__ = "HTTP Authentication"
    HTTP_AUTHS = {"digest": DigestHTTPAuthFuzzer, "basic": BasicHTTPAuthFuzzer}

    def __get_auth_header(self):
        return self.http_response.headers.get("www-authenticate").strip().lower()

    def __get_auth_type(self):
        return self.__get_auth_header().split(" ")[0]

    def _check_response_content(self):
        return self.http_response.status_code == 401 and \
               self.http_response.headers.get("www-authenticate") is not None \
               and self.__get_auth_type() in self.HTTP_AUTHS.keys()

    def _get_fuzzer(self):
        return self.HTTP_AUTHS[self.__get_auth_type()](self.settings, self.http_session, self.url)
