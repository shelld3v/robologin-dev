from bs4 import BeautifulSoup


class HTMLParser(BeautifulSoup):
    def __init__(self, *args, **kwargs):
        args += ('lxml',)
        super().__init__(*args, **kwargs)
        self._fixed_types = False
        self.fix_types()

    #def has_iframes(self):



    #def fill_iframes(self):


    def get_password_fields(self):
        return self.find_all('input', {'type': 'password', 'name': True})

    def fix_types(self):
        if self._fixed_types:
            return
        for tag in self.find_all('input', {'type': False}):
            tag.attrs['type'] = 'text'
        self._fixed_types = True

    def get_login_forms(self):
        detected_forms = []
        for form in self.find_all('form'):

            password_fields = form.find_all('input', {'type': 'password', 'name': True})

            if len(password_fields) == 1 and len(form.find_all('input')) >= 2:
                detected_forms.append(form)
        return detected_forms