import os
import time
import sys
from threading import Lock

MAYOR_VERSION = 0
MINOR_VERSION = 1
REVISION = 0
VERSION = {
    "MAYOR_VERSION": MAYOR_VERSION,
    "MINOR_VERSION": MINOR_VERSION,
    "REVISION": REVISION
}


class CommandLineController(object):
    def __init__(self, script_path, arguments, output):
        global VERSION
        PROGRAM_BANNER = open(FileUtils.buildPath(script_path, "lib", "controller", "banner.txt")).read().format(
            **VERSION)


    def start(self):


    def parse_arguments(self):
        raise NotImplemented

    def setup_report(self):
        raise NotImplemented

    def setup_session(self):
        raise NotImplemented

    def print_config(self):
        raise NotImplemented

    def match_callback(self, credentials):
        raise NotImplemented

    def error_callback(self):
        raise NotImplemented

    def critical_error_callback(self):
        raise NotImplemented

    def handler_interrupt(self):
        raise NotImplemented

    def wait(self):
        raise NotImplemented


