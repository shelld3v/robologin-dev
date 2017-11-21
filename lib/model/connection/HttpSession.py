import copy

from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

from requests.packages import urllib3
from requests.sessions import Session
from requests.compat import OrderedDict
from requests.models import PreparedRequest


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


"""
         Already in request.Session proxies
         verify
         auth
         headers
         proxies
         stream
         params
"""


class HttpSession(Session):
    custom_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Keep-Alive': '300',
        'Cache-Control': 'max-age=0',
    }

    headers_order = [
        'Host',
        'User-Agent',
        'Accept',
        'Accept-Language',
        'Accept-Encoding',
        'Referer',
        'Cookie',
        'Connection',
        'Content-Type'
    ]

    def __init__(self,
                 proxies=None,
                 verify=False,
                 allow_redirects=False,
                     user_agent=None,
                 max_retries=5,
                 timeout=30,
                 cookies=None,
                 headers=None,
                 dest_ip_address=None,
                 use_dns_cache=False,
                 delay=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        urllib3.disable_warnings()
        self.timeout = 30 if timeout is None else timeout
        self.delay = delay if delay else 0.0
        self.dest_ip_address = dest_ip_address if dest_ip_address else None
        self.allow_redirects = False
        self.use_dns_cache = use_dns_cache
        self._dns_cache = {}
        self.proxy_handler = None
        self.user_agent_handler = None
        self.verify = verify
        if cookies:
            self.cookies = cookies
        self.headers.update(self.custom_headers)
        if headers:
            self.headers.update(headers)
        if user_agent:
            self.headers['User-Agent'] = user_agent
        if proxies:
            self._proxies = proxies
        if allow_redirects:
            self.allow_redirects = allow_redirects
        if max_retries:
            pass
            retries = Retry(total=int(max_retries),backoff_factor=0.1,status_forcelist=[ 500, 502, 503, 504 ])
            self.mount('http://', HTTPAdapter(max_retries=retries))
            self.mount('https://', HTTPAdapter(max_retries=retries))
        PreparedRequest.prepare_headers = HttpSession._prepare_headers

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    @property
    def proxies(self):
        if self.proxy_handler and self.proxy_handler is not None:
            return self.proxy_handler.fetch()
        else:
            return self._proxies

    def request(self, *args, **kwargs):
        if not 'proxies' in kwargs:
            kwargs.update({'proxies': self.proxies})

        if not 'allow_redirects' in kwargs:
            kwargs.update({'allow_redirects': self.allow_redirects})

        if not 'timeout' in kwargs:
            kwargs['timeout'] = self.timeout

        if not 'verify' in kwargs:
            kwargs['verify'] = self.verify

        headers = copy.copy(self.headers)

        if 'headers' in kwargs:
            headers.update(kwargs['headers'])

        if 'user_agent' in kwargs:
            headers.update({'User-Agent': kwargs['user_agent']})

        kwargs['headers'] = headers

        return super().request(*args, **kwargs)

    '''
        Some CDNs and WAFs block requests
        that doesn't follows a specific order
    '''

    def _prepare_headers(self, headers):
        headers_order = [
            'Host',
            'User-Agent',
            'Accept',
            'Accept-Language',
            'Accept-Encoding',
            'Referer',
            'Cookie',
            'Connection',
            'Content-Type'
        ]

        self.headers = OrderedDict()
        if headers:
            for header_name in filter(lambda x: x in headers, headers_order):
                self.headers[header_name] = headers.get(header_name)
            for header_name in filter(lambda x: x not in self.headers, headers):
                self.headers[header_name] = headers.get(header_name)

    @proxies.setter
    def proxies(self, value):
        self._proxies = value

    @property
    def user_agent(self):
        if self.user_agent_handler and self.user_agent_handler is not None:
            return self.user_agent_handler.fetch()
        else:
            return self._user_agent
