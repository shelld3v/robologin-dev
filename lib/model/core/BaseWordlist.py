class WordlistException(Exception):
    pass


class NotReadableWordlistException(WordlistException):
    pass


class NotExistsWordlistException(WordlistException):
    pass


class BaseWordlist:
    def process(self):
        raise NotImplemented
