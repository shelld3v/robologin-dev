#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os

if sys.version_info < (3, 0):
    sys.stdout.write("Sorry, dirsearch requires Python 3.x\n")
    sys.exit(1)

from lib.controller import *


class Program(object):
    def __init__(self):
        self.script_path = (os.path.dirname(os.path.realpath(__file__)))
        self.controller = Controller(self.script_path)


if __name__ == '__main__':
    main = Program()
