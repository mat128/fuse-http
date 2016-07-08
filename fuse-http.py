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

    def read(self, path, size, offset, fh):
      response = requests.get(self.base_url + path)
      value = response.content[offset:offset+size]
      return value

    def getattr(self, path, fh=None):
      response = requests.head(self.base_url + path)
      if response.status_code != 200:
        raise FuseOSError(ENOENT)
      size = int(response.headers['content-length'])
      try:
        mtime = mktime(strptime(response.headers['last-modified'],
                                "%a, %d %b %Y %H:%M:%S GMT"))
      except KeyError:
        mtime=time()

      if path.endswith('/'): #directories
        value = dict(st_mode=(S_IFDIR | 0o755), st_ctime=mtime,
                    st_mtime=mtime, st_atime=mtime, st_nlink=2)
      else:
        value = dict(st_mode=(S_IFREG), st_nlink=1,
                     st_size=size, st_ctime=mtime, st_mtime=mtime,
                     st_atime=time())

      return value

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    fuse = FUSE(HttpFilesystem(argv[1]), argv[2], foreground=True)
