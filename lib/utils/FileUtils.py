# -*- coding: utf-8 -*-
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  Author: Mauro Soria

import os
import os.path


class File(object):
    def __init__(self, *path_components):
        self._path = FileUtils.build_path(*path_components)
        self.content = None

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        raise NotImplemented

    def is_valid(self):
        return FileUtils.is_file(self.path)

    def exists(self):
        return FileUtils.exists(self.path)

    def is_readable(self):
        return FileUtils.is_readable(self.path)

    def is_writable(self):
        return FileUtils.is_writable(self.path)

    def read(self):
        return FileUtils.read(self.path)

    def update(self):
        self.content = self.read()

    def content(self):
        if not self.content:
            self.content = FileUtils.read()
        return self.content()

    def getLines(self):
        for line in FileUtils.getLines(self.path):
            yield line

    def __cmp__(self, other):
        if not isinstance(other, File):
            raise NotImplemented
        return cmp(self.content(), other.content())

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        pass


class FileUtils(object):
    @staticmethod
    def build_path(*path_components):
        if path_components:
            path = os.path.join(*path_components)
        else:
            path = ''
        return path

    @staticmethod

    @staticmethod
    def is_readable(file_path):
        if not os.access(file_path, os.R_OK):
            return False
        try:
            with open(file_path):
                pass
        except IOError:
            return False
        return True

    @staticmethod
    def is_writable(file_path):
        return os.access(file_path, os.W_OK)

    @staticmethod
    def read(file_path):
        result = ''
        with open(file_path, 'r') as fd:
            for line in fd.readlines():
                result += line
        return result

    @staticmethod
    def get_lines(file_path):
        with open(file_path, 'r', errors="replace") as fd:
            return fd.read().splitlines()

    @staticmethod
    def is_dir(file_path):
        return os.path.isdir(file_path)

    @staticmethod
    def is_file(file_path):
        return os.path.isfile(file_path)

    @staticmethod
    def create_directory(directory):
        if not FileUtils.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def size_human(num):
        base = 1024
        for x in ['B ', 'KB', 'MB', 'GB']:
            if num < base and num > -base:
                return "%3.0f%s" % (num, x)
            num /= base
        return "%3.0f %s" % (num, 'TB')

    @staticmethod
    def write_lines(file_path, lines):
        content = None
        if type(lines) is list:
            content = "\n".join(lines)
        else:
            content = lines
        with open(file_path, "w") as f:
            f.writelines(content)