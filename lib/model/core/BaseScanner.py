

class BaseScanner:
    def __init__(self, settings, http_session):
        self.http_session = http_session
        self.settings = settings

    def scan_url(self, url):
        NotImplemented


