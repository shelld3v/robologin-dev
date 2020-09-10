from lib.model.core.BaseWordlist import BaseWordlist
from lib.utils.FileUtils import FileUtils


class Credentials:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __hash__(self):
        return hash(self.username) ^ hash(self.password)

    def __str__(self):
        return "{0}:{1}".format(self.username, self.password)


class BasePlainTextWordlist(BaseWordlist):
    def __init__(self, separator, path):
        self.separator = separator
        self.path = path

    def _check_file_access(self, path):
        if not FileUtils.is_file(path):
            raise NotExistsWordlistException(path)
        if not FileUtils.is_readable(path):
            raise NotReadableWordlistException(path)

    def _parse_content(self, path):
        result = []
        for line in FileUtils.get_lines(path):
            username, password = line.split(self.separator, 1)
            result.append(Credentials(username, password))
        return result

    def process(self):
        self._check_file_access(self.path)
        return self._parse_content(self.path)


class DefaultPlainTextWordlist(BasePlainTextWordlist):
    def __init__(self, path):
        super().__init__(':', path)
