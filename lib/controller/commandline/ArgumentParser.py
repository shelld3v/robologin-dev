from optparse import OptionParser, OptionGroup

import oset

from lib.utils.FileUtils import File
from lib.utils.FileUtils import FileUtils
from lib.utils.DefaultConfigParser import DefaultConfigParser


class ArgumentParser(object):
    def __init__(self, script_path):
        self.script_path = script_path
        self.parse_config()
        options = self.parse_arguments()
        self.debug = options.debug
        if options.url == None:
            if options.url_list != None:
                with File(options.url_list) as url_list:
                    if not url_list.is_valid():
                        print("The file with URLs does not exist")
                        exit(0)
                    if not url_list.is_readable():
                        print('The input file cannot be read')
                        exit(0)
                    self.urlList = list(url_list.get_lines())
            elif options.url == None:
                print('URL target is missing, try using -u <url> ')
                exit(0)
        else:
            self.url_list = [options.url]

        with File(options.wordlist) as wordlist:
            if not wordlist.is_valid():
                print('The wordlist file does not exist')
                exit(0)
            if not wordlist.is_readable():
                print('The wordlist cannot be read')
                exit(0)

        if options.http_proxy is not None:
            if options.http_proxy.startswith('http://'):
                self.proxy = options.http_proxy
            else:
                self.proxy = 'http://{0}'.format(options.http_proxy)
        else:
            self.proxy = None

        if options.headers is not None:
            try:
                self.headers = dict((key.strip(), value.strip()) for (key, value) in (header.split(':', 1)
                                                                                      for header in options.headers))
            except Exception as e:
                print('Invalid headers')
                exit(0)
        else:
            self.headers = {}

        self.useragent = options.useragent
        self.use_random_agents = options.use_random_agents
        self.cookie = options.cookie
        if options.threads_count < 1:
            print('Threads number must be a number greater than zero')
            exit(0)
        self.threads_count = options.threads_count
        self.wordlist = options.wordlist
        self.delay = options.delay
        self.timeout = options.timeout

        self.max_retries = options.max_retries
        self.redirect = options.no_follow_redirects
        if (options.dns_cache and options.ip_addr) or (self.dns_cache and options.dns_cache):
            print("DNS Cache and IP address cannot be used together.")
            exit(0)
        self.dns_cache = options.dns_cache
        self.ip_addr = options.ip_addr


    def parse_config(self):
        config = DefaultConfigParser()
        config_path = FileUtils.build_path(self.script_path, "default.conf")
        config.read(config_path)

        # General
        self.threads_count = config.safe_getint("general", "threads", 10, list(range(1, 50)))
        self.redirect = config.safe_getboolean("general", "follow-redirects", False)
        # Dictionary


        self.wordlist = config.safe_get("dictionary", "wordlist",
                                        FileUtils.build_path(self.script_path, "db", "default.txt"))

        # Connection
        self.use_random_agents = config.safe_get("connection", "random-user-agents", False)
        self.useragent = config.safe_get("connection", "user-agent", None)
        self.delay = config.safe_get("connection", "delay", 0)
        self.timeout = config.safe_getint("connection", "timeout", 30)
        self.max_retries = config.safe_getint("connection", "max-retries", 5)
        self.proxy = config.safe_get("connection", "http-proxy", None)
        self.dns_cache = config.safe_get("connection", "dns-cache", False)

    def parse_arguments(self):
        usage = 'Usage: %prog [-u|--url] target [-e|--extensions] extensions [options]'
        parser = OptionParser(usage)
        # Mandatory arguments
        mandatory = OptionGroup(parser, 'Mandatory')
        mandatory.add_option('-u', '--url', help='URL target', action='store', type='string', dest='url', default=None)
        mandatory.add_option('-L', '--url-list', help='URL list target', action='store', type='string', dest='url_list',
                             default=None)

        connection = OptionGroup(parser, 'Connection Settings')
        connection.add_option('--timeout', action='store', dest='timeout', type='int',
                              default=self.timeout,
                              help='Connection timeout')
        connection.add_option('--ip', action='store', dest='ip_addr', default=None,
                              help='Resolve name to IP address')
        connection.add_option('--proxy', '--http-proxy', action='store', dest='http_proxy', type='string',
                              default=self.proxy, help='Http Proxy (example: localhost:8080')
        connection.add_option('--max-retries', action='store', dest='max_retries', type='int',
                              default=self.max_retries)
        connection.add_option('--dns-cache', help='Use a dns cache to speedup. Does not work on WAFs and CDNs.',
                              action='store_true', dest='dns_cache', default=False)
        connection.add_option('--delay', help='Delay between requests (float number)', action='store', dest='delay',
                              type='float', default=self.delay)

        # Dictionary settings
        dictionary = OptionGroup(parser, 'Dictionary Settings')
        dictionary.add_option('-w', '--wordlist', action='store', dest='wordlist',
                              default=self.wordlist)

        # Optional Settings
        general = OptionGroup(parser, 'General Settings')
        general.add_option('-d', '--debug', help='Enable debugging output', action='store_true', dest='debug',
                           default=False)

        general.add_option('-t', '--threads', help='Number of Threads', action='store', type='int', dest='threads_count'
                           , default=self.threads_count)
        general.add_option('-c', '--cookie', action='store', type='string', dest='cookie', default=None)
        general.add_option('--ua', '--user-agent', action='store', type='string', dest='useragent',
                           default=self.useragent)
        general.add_option('-F', '--follow-redirects', action='store_true', dest='no_follow_redirects'
                           , default=self.redirect)
        general.add_option('-H', '--header',
                           help='Headers to add (example: --header "Referer: example.com" --header "User-Agent: IE"',
                           action='append', type='string', dest='headers', default=None)
        general.add_option('--random-agents', '--random-user-agents', action="store_true", dest='use_random_agents')

        parser.add_option_group(mandatory)
        parser.add_option_group(dictionary)
        parser.add_option_group(general)
        parser.add_option_group(connection)
        options, arguments = parser.parse_args()
        return options
