#!/usr/bin/env python
from __future__ import print_function, absolute_import, division

import logging
from errno import ENOENT
from sys import argv
from time import time, mktime, strptime

from fuse import FUSE, FuseOSError, Operations, LoggingMixIn
from stat import S_IFDIR, S_IFREG

if not hasattr(__builtins__, 'bytes'):
    bytes = str

import requests


class HttpFilesystem(LoggingMixIn, Operations):
    def __init__(self, base_url):
        self.base_url = base_url
        super(HttpFilesystem, self).__init__()
        self.session = requests.Session()

    def read(self, path, size, offset, fh):
        response = self.session.get(self.base_url + path)
        return response.content[offset:offset+size]

    def getattr(self, path, fh=None):
        mtime = time()
        if path.endswith('/'):
            return dict(st_mode=(S_IFDIR | 0o755), st_ctime=mtime, st_mtime=mtime, st_atime=mtime, st_nlink=2)
        response = self.session.head(self.base_url + path)
        if response.status_code == 301:
            return self.getattr(response.headers['location'], fh)

        if response.status_code != 200:
            raise FuseOSError(ENOENT)

        size = int(response.headers['content-length'])
        try:
            mtime = mktime(strptime(response.headers['last-modified'],
                                    "%a, %d %b %Y %H:%M:%S GMT"))
        except KeyError:
            pass

        return dict(st_mode=(S_IFREG), st_nlink=1, st_size=size, st_ctime=mtime, st_mtime=mtime, st_atime=time())


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    fuse = FUSE(HttpFilesystem(argv[1]), argv[2], foreground=True)
