from requests.auth import HTTPBasicAuth, HTTPDigestAuth

from lib.model.core.BaseFuzzer import BaseFuzzer


class BaseHTTPAuthFuzzer(BaseFuzzer):
    def __init__(self, settings, http_session, url):
        super().__init__(settings, http_session, url)
        self.unauthorized_status_code = 401

    def test_credentials(self, credentials):
        response = self.http_session.get(self.url, auth=self._get_auth_type(credentials))
        return response.status_code != self.unauthorized_status_code

    def _get_auth_type(self, credentials):
        raise NotImplemented


class BasicHTTPAuthFuzzer(BaseHTTPAuthFuzzer):
    __name__ = "Basic HTTP Authentication"

    def _get_auth_type(self, credentials):
        return HTTPBasicAuth(credentials.username, credentials.password)


class DigestHTTPAuthFuzzer(BaseHTTPAuthFuzzer):
    __name__ = "Digest HTTP Authentication"

    def _get_auth_type(self, credentials):
        return HTTPDigestAuth(credentials.username, credentials.password)
