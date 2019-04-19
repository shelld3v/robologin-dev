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


"""def extract_form_fields(soup):
    "Turn a BeautifulSoup form in to a dict of fields and default values"
    fields = {}
    for input in soup.findAll('input'):
        # ignore submit/image with no name attribute
        if input['type'] in ('submit', 'image') and not 'name' in input:
            continue

        # single element nome/value fields
        if input['type'] in ('text', 'hidden', 'password', 'submit', 'image'):
            value = ''
            if 'value' in input:
                value = input['value']
            fields[input['name']] = value
            continue

        # checkboxes and radios
        if input['type'] in ('checkbox', 'radio'):
            value = ''
            if input.has_attr("checked"):
                if input.has_attr('value'):
                    value = input['value']
                else:
                    value = 'on'
            if 'name' in input and value:
                fields[input['name']] = value

            if not 'name' in input:
                fields[input['name']] = value

            continue

        assert False, 'input type %s not supported' % input['type']

    # textareas
    for textarea in soup.findAll('textarea'):
        fields[textarea['name']] = textarea.string or ''

    # select fields
    for select in soup.findAll('select'):
        value = ''
        options = select.findAll('option')
        is_multiple = select.has_key('multiple')
        selected_options = [
            option for option in options
            if option.has_key('selected')
        ]

        # If no select options, go with the first one
        if not selected_options and options:
            selected_options = [options[0]]

        if not is_multiple:
            assert(len(selected_options) < 2)
            if len(selected_options) == 1:
                value = selected_options[0]['value']
        else:
            value = [option['value'] for option in selected_options]

        fields[select['name']] = value

    return fields"""