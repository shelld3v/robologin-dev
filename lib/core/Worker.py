class Worker:
	def __init__(self, requester, dictionary, engine):
		self.requester = requester
		self.dictionary = dictionary
		self.engine = engine

	def start(self):
		raise NotImplemented

	def stop(self):
		raise NotImplemented

	def pause(self):
		raise NotImplemented

	def wait(self):
		raise NotImplemented

	def is_running(self):
		raise NotImplemented

	def _brute(self, entry):
		raise NotImplemented

	def _thread_proc(self):
		raise NotImplemented