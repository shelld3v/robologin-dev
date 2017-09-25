class PlainTextWordlist(BaseWordlist):
	def __init__(self, fields, separator):
		self.fields = fields
		self.separator = separator

    def _check_file_access(self, path):
        return FileUtil.is_readable(path)

	def _parse_content(self, path):
	    for line in FileUtils.get_lines(path)

    def process_wordlist(self):
        if self._check_file_access(target):
            self._parse_content(target)


class PlainText