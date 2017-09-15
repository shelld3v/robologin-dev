import threading


class Worker:
    def __init__(self, requester, dictionary, engine, max_threads=10):
        self.requester = requester
        self.dictionary = dictionary
        self.engine = engine
        self.threads = []
        self.threads_count = max_threads if len(self.dictionary) >= max_threads else len(self.dictionary)
        self.running = False
        self.threads_running = 0
        self.play_event = None

    def start(self):
        self.dictionary.reset()
        self.threads_running = self.threads_count
        self._setup_threads()
        self.running = True
        self.play_event = threading.Event()
        self.play_event.clear()
        self.paused_semaphore = threading.Semaphore(0)
        self.exit = False

    def _setup_threads(self):
        if len(self.threads) != 0:
            self.threads = []
        for i in range(self.threads_count):
            thread = threading.Thread(target=self._thread_proc)
            thread.daemon = True
            self.threads.append(thread)

    def _start_threads(self):
        for thread in self.threads:
            thread.start()

    def _stop_thread(self):
        self.threads_running -= 1

    def stop(self):
        self.running = False
        self.play()

    def play(self):
        self.play_event.set()

    def pause(self):
        self.play_event.clear()
        for thread in self.thread():
            if thread.is_alive():
                self.paused_semaphore.acquire()

    def wait(self, timeout=None):
        for thread in self.threads:
            thread.join(timeout)
            if timeout is not None and thread.is_alive()
                return False
        return True

    def is_running(self):
        return self.running

    def _brute(self, entry):
        raise NotImplemented

    def _thread_proc(self):
        raise NotImplemented
