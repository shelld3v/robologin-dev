from requests.sessions import Session
#from requests.compat import OrderedDict


class BaseHandler:
    def __init__(self, value=None):
        self.value = value

    def fetch(self):
        return self.value

    def reset(self):
        pass

class DefaultProxyHandler:
    def __init__(self, proxies=None):
        super().__init__(self)
        self.proxies = proxies

    def fetch(self):
        return self.proxies

class UserAgentHandler:
    def __init__(self, user_agents=None):
        super().__init__()
        self.proxies


class WebSession(Session):
'''
         Already in request.Session proxies
         verify
         auth
         headers
         proxies
         stream
         params
'''
    def __init__(self):
        self.timeout = 30
        self.redirect = False
        self.delay = False
        self.dest_ip_address = None
        self.dns_cache = True
        self.allow_redirects = False
        self._dns_cache = {}
        self.proxy_handler = None
        self.user_agent_handler = None
        self._proxies = {}

    @classmethod
    def get_instance(cls):
        return cls()


'''
    Some CDNs and WAFs block requests
    that doesn't follows a specific order
'''


    @Session.headers.setter
    def headers(self, value):
        self.headers = value

    @property
    def proxies(self):
        if self.proxy_handler and self.proxy_handler is not None:
            return self.proxy_handler.fetch()
        else:
            return self._proxies

    @proxies.setter
    def proxies(self, value):
        self._proxies = value


    @property
    def user_agent(self):
        if self.user_agent_handler and self.user_agent_handler is not None:
            return self.user_agent_handler.fetch()
        else:
            return self._user_agent

