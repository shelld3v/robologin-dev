import urllib.parse
import copy

import requests.utils


class FormData:
    def __init__(self):
        self.url = None
        self.get_fields = []
        self.post_fields = []
        self.get_tokens = []
        self.post_tokens = []
        self.method = "POST"
        self.headers = {}
        self.content_type = 'application/x-www-form-urlencoded'
        self.password_field_location = 'post'
        self.password_field_name = None
        self.username_field_location = 'post'
        self.username_field_name = None
        self.url = None

    def set_method(self, method='POST'):
        self.method = method

    def set_url(self, url):
        self.url = url

    def set_content_type(self, content_type):
        self.content_type = content_type

    def add_post_field(self, name, value):
        self.post_fields.append((name, value,))

    def add_get_field(self, name, value):
        self.get_fields.append((name, value,))

    def set_username_field_post(self, name):
        self.username_field_location = 'post'
        self.username_field_name = name

    def set_username_field_get(self, name):
        self.user_field_location = 'get'
        self.username_field_name = name

    def set_password_field_post(self, name):
        self.password_field_location = 'post'
        self.password_field_name = name

    def set_password_field_get(self, name):
        self.password_field_location = 'get'
        self.password_field_name = name

    def set_token_field_get(self, name):
        self.get_tokens.append(name)

    def set_token_field_post(self, name):
        self.post_tokens.append(name)

    def get_data(self, credentials):
        headers = copy.copy(self.headers)
        get_fields = copy.copy(self.get_fields)
        post_fields = copy.copy(self.post_fields)

        if self.password_field_location == 'get':
            get_fields.append((self.password_field_name, credentials.password,))
        else:
            post_fields.append((self.password_field_name, credentials.password,))

        if self.username_field_location == 'get':
            get_fields.append((self.username_field_name, credentials.username,))
        else:
            post_fields.append((self.username_field_name, credentials.username,))

        return {'method':self.method,
                'url':self.url,
                'headers':self.headers,
                'get_fields':get_fields,
                'post_fields': post_fields,
                }

    def __str__(self):
        return "URL: {0}, HEADERS: {1}, GET: {2}, POST: {3}".format(self.url, \
                                                                    self.headers,
                                                                    self.get_fields, self.post_fields)


class FormDataParser:
    def __init__(self, url, form):
        self.url = url
        self.form = form
        self.__setted_params = None

    def build_form_data(self):
        form_data = FormData()
        form_data.set_method(self._get_method())
        action = self._resolve_action()
        url, get_params = self._parse_url(action)
        form_data.set_url(url)
        form_data.set_content_type = self._get_content_type()
        password_field = self.form.find('input', attrs={'name': True, 'type': 'password'})
        username_field = self._detect_username_field(self.form, password_field)
        if self._get_method() is 'GET':
            form_data.set_password_field_get(password_field['name'])
            form_data.set_username_field_get(username_field['name'])
        else:
            form_data.set_password_field_post(password_field['name'])
            form_data.set_username_field_post(username_field['name'])

        for key in get_params.keys():
            for value in get_params[key]:
                form_data.add_get_field(key, value)
        form_fields = self.get_all_setted_params()
        for key in form_fields.keys():
            for value in form_fields[key]:
                if self._get_method() is 'GET':
                    form_data.add_get_field(key, value)
                else:
                    form_data.add_post_field(key, value)
        return form_data

    def _detect_username_field(self, form, password_field):
        previous = password_field.find_previous_sibling('input', attrs={'name': True, 'value': False, 'type': 'text'})
        first = form.find('input', attrs={'name': True, 'value': False, 'type': 'text'})
        if previous and first == previous:
            return first

        email = form.find('input', attrs={'type': 'email', 'value': False})

        if email:
            return email

        return form.find('input', attrs={'name': True, 'type': 'text'})


    def __parse_params_form_action(self, form_func):
        lambda x: x.fi

    def __parse_params_by_attrs(self, type, attrs):
        params = {}
        form_fields = self.form.find_all(type, attrs=attrs)
        for field in form_fields:
            if params.get(field['name']) is None:
                params[field['name']] = []
            params[field['name']].append(field['value'])

        return params


    def get_all_setted_params(self):
        if not self.__setted_params:
            self.__setted_params = self.__parse_params_by_attrs('input',
                                        {'name': True, 'value': True})
        return self.__setted_params

    def _parse_url(self, url):

        parsed = urllib.parse.urlsplit(url)
        url = '{0}://{1}{2}'.format(parsed.scheme, parsed.netloc, parsed.path)
        params = urllib.parse.parse_qs(parsed.query)
        return url, params

    def _get_method(self):
        return (self.form["method"] if self.form.get("method") \
                    else "GET").upper()

    def _get_content_type(self):
        return self.form["Content-Type"] if self.form.get("Content-Type") \
            else "application/x-www-form-urlencoded"

    def _resolve_action(self):
        parsed = urllib.parse.urlsplit(self.form['action'])
        url = None
        if not parsed.netloc:
            url = urllib.parse.urljoin(self.url, requests.utils.requote_uri(self.form['action']))
        else:
            url = requests.utils.requote_uri(self.url)

        return url

    def xpath_soup(element):
        """
        https://gist.github.com/ergoithz/6cf043e3fdedd1b94fcf#file-xpath_soup-py
        Generate xpath of soup element
        :param element: bs4 text or node
        :return: xpath as string
        """
        components = []
        child = element if element.name else element.parent
        for parent in child.parents:
            """
            @type parent: bs4.element.Tag
            """
            previous = itertools.islice(parent.children, 0, parent.contents.index(child))
            xpath_tag = child.name
            xpath_index = sum(1 for i in previous if i.name == xpath_tag) + 1
            components.append(xpath_tag if xpath_index == 1 else '%s[%d]' % (xpath_tag, xpath_index))
            child = parent
        components.reverse()
        return '/%s' % '/'.join(components)
