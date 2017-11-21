class FuzzerException(Exception):
    pass


class BaseFuzzer:
    def __init__(self, settings, http_session, url):
        self.url = url
        self.settings = settings
        self.http_session = http_session

    def test_credentials(self, credentials):
        raise NotImplemented
