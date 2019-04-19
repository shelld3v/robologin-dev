import time

from requests.packages import urllib3
from requests.sessions import Session
from requests.compat import OrderedDict, urlparse, urlunparse
from requests.models import PreparedRequest
from requests.exceptions import TooManyRedirects, ConnectionError, ConnectTimeout, ReadTimeout, Timeout

import copy
from http.client import IncompleteRead
import socket
from http.cookies import SimpleCookie


class BaseHandler:
    def __init__(self, value=None):
        self.value = value

    def fetch(self):
        return self.value

    def reset(self):
        pass


class CookieParser:
    def __init__(self, raw_cookie):
        self.cookie = SimpleCookie()
        cookie.load(raw_cookie)

        self.cookies = {}
        for key, morsel in cookie.items():
            cookies[key] = morsel

    def get_cookie_value(self, key):
        if cookies.get(key) is not None:
            return cookies.get(key).value
        else:
            return None


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


class RequestException(Exception):
    pass


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
                 max_retries=3,
                 timeout=30,
                 cookies=None,
                 headers=None,
                 dest_ip_address=None,
                 use_dns_cache=False,
                 delay=None,
                 dest_ip_addr=None,
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
        self.dest_ip_addr = dest_ip_addr

        if not max_retries:
            self.max_retries = 3
        else:
            self.max_retries = max_retries

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

    def _normalize_url(self, url):
        parsed_url = urlparse(url)

        if parsed_url.scheme not in ['http', 'https']:
            parsed_url = urlparse('http://{0}'.format(url))

        protocol = parsed_url.scheme
        host = parsed_url.netloc.split(':')[0]
        port = None

        try:
            port = parsed_url.netloc.split(':')[1]
        except IndexError:
            port = (443 if parsed_url.scheme == 'https' else 80)

        return protocol, host, port, parsed_url.path, parsed_url.query

    def _get_host_cache(self, host):
        ip = None
        if self._dns_cache.get(host):
            ip = self._dns_cache.get(host)
        else:
            try:
                ip = socket.gethostbyname(host)
            except socket.gaierror:
                raise RequestException("Could not resolve domain name")
        return ip

    def request(self, *args, **kwargs):
        method = args[0]
        protocol, host, port, path, query = self._normalize_url(args[1])

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

        dst_host = host
        host_header = host

        if 'dest_ip_addr' in kwargs:
            dst_host = kwargs['dest_ip_addr']
        elif self.dest_ip_addr:
            dst_host = self.dest_ip_addr
        elif self.use_dns_cache:
            dst_host = self.get_host_cache(host)

        if (protocol == 'http' and port != 80) or (protocol == 'https' and port != 443):
            dst_host += ':{0}'.format(port)
            host_header += ':{0}'.format(port)

        headers.update({'Host': host_header})

        url = urlunparse([protocol, dst_host, path, None, query, None])

        kwargs['headers'] = headers

        current_retry = 1
        result = None
        last_exception = None

        while current_retry <= self.max_retries:
            try:
                result = super().request(method, url, **kwargs)
                time.sleep(self.delay)
                break
            except TooManyRedirects as e:
                raise RequestException('Too many redirects: {0}'.format(e))
            except ConnectionError as e:
                if self.proxy_handler is not None:
                    raise RequestException('Error with the proxy: {0}')
                continue
            except (ConnectTimeout,
                    ReadTimeout,
                    Timeout,
                    IncompleteRead,
                    socket.timeout) as ex:
                last_exception = ex
                continue
            finally:
                current_retry += 1

        if current_retry > self.max_retries:
            raise (last_exception)

        return result

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
