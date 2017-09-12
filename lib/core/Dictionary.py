import threading
from lib.utils.FileUtils import FileUtils
from oset import oset

class Dictionary:
	def __init__(self):
		self.entries = []
		self.condition = threading.Lock()
		self.current = 0
		self.wordlist_parser = self._default_wordlist_parser

	def append_from_file(self, path, wordlist_parser=None):
		entries = None
		if line_parser is None:
			entries = self.wordlist_parser(path)
		else:
			entries = wordlist_parser(path)
		self.entries = list(oset(self.entries + entries))

	def get_with_index(self):
		self.condition.acquire()
		current = None
		result = None
        try:
            result = self.entries[self.current]
        except IndexError:
            self.condition.release()
            raise StopIteration
        else:
        	self.current = self.current + 1
        	current = self.current
        	return current, result
        finally:
        	self.condition.release()

    def reset(self):
    	self.condition.acquire()
    	self.current = 0
    	self.condition.release()

    def get(self):
    	_, result = self.get_with_index()
    	return result

    def __next__(self):
    	return self.get()
    	
	def _wordlist_parser(self, path):
		return FileUtils.get_lines(path)

	def __len__(self):
		return self.entries