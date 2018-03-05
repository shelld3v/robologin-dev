import threading
import datetime
import traceback
import datetime

from lib.model.core.BaseFuzzer import FuzzerException


class Worker:
    def __init__(self, http_session, dictionary, fuzzer, logger, max_threads=10,
                 success_callbacks=[], failed_callbacks=[], error_callbacks=[]):
        self.http_session = http_session
        self.logger = logger
        self.dictionary = dictionary
        self.fuzzer = fuzzer
        self.success_callbacks = success_callbacks
        self.failed_callbacks = failed_callbacks
        self.error_callbacks = error_callbacks
        self.child_threads = []

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
        self.play()
        self._start_threads()

    def _setup_threads(self):
        if len(self.child_threads) != 0:
            self.child_threads = []
        for i in range(self.threads_count):
            thread_name = "robologin-worker-child-thread-{0}".format(i)
            thread = threading.Thread(target=self._thread_proc, name=thread_name)
            thread.daemon = True
            self.child_threads.append(
                {
                    "name": thread_name,
                    "thread": thread,
                    "start_time": None,
                    "running": False,
                    "last_report_time": None
                }
            )

    def _start_threads(self):
        for thread in self.child_threads:
            thread["start_time"] = datetime.datetime.now()
            thread["running"] = True
            thread["thread"].start()

    def _stop_thread(self):
        for i, thread in enumerate(self.child_threads):
            if thread["thread"] == threading.current_thread():
                self.logger.debug("Stopping thread {0}".format(thread["name"]))
                thread["running"] = False
                self.threads_running -= 1
                break

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
        start = datetime.datetime.now()
        def elapsed_time():
            return (datetime.datetime.now() - start).microseconds / 1000000

        for thread in self.child_threads:
            while thread["thread"].is_alive():
                delay = None
                if timeout:
                    if timeout - elapsed_time() < 0:
                        return False
                    delay = timeout - elapsed_time()
                thread["thread"].join(delay if delay and delay >=0 else 0)
        return True

    def is_running(self):
        return self.running

    def _get_current_thread(self):
        pass

    def _thread_proc(self):
        while not self.play_event.wait(0.1):
            pass
        try:
            credentials = next(self.dictionary)
            while self.running:
                try:
                    success = self.fuzzer.test_credentials(credentials)
                    for callback in (self.success_callbacks if success else self.failed_callbacks):
                        callback(credentials)
                except (RequestException, FuzzerException) as e:
                    for callback in self.error_callbacks:
                        callback(credentials, e)
                except Exception as e:
                    self.logger.error(str(e))
                    self.logger.error(traceback.format_exc())
                finally:
                    if not self.play_event.is_set():
                        self.paused_semaphore.release()
                        slef.play_event.wait()
                    credentials = next(self.dictionary)
        except StopIteration as e:

            return
        finally:
            self._stop_thread()


"""
    def check_threads(self):
        raise NotImplemented

    def _thread_monitor(self):
        raise NotImplemented
"""
