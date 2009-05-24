#!/usr/bin/env python

#    Copyright (C) 2006  Andrew Straw  <strawman@astraw.com>
#
#    This program can be distributed under the terms of the GNU LGPL.
#    See the file COPYING.
#

import os, stat, errno
# pull in some spaghetti to make this stuff work without fuse-py being installed
try:
    import _find_fuse_parts
except ImportError:
    pass
import fuse
from fuse import Fuse


if not hasattr(fuse, '__version__'):
    raise RuntimeError, \
        "your fuse-py doesn't know of fuse.__version__, probably it's too old."

fuse.fuse_python_api = (0, 2)

'''
hello_path = '/hello.txt'
hello_str = 'Hello World!\n'
'''

class MyStat(fuse.Stat):
    def __init__(self):
        self.st_mode = 0
        self.st_ino = 0
        self.st_dev = 0
        self.st_nlink = 0
        self.st_uid = 0
        self.st_gid = 0
        self.st_size = 0
        self.st_atime = 0
        self.st_mtime = 0
        self.st_ctime = 0

baseFilesys = "d:/"

class mirrorFs(Fuse):
    def getPath(self, path):
      #print 'get path', path
      realP = baseFilesys + path
      #print realP
      return realP
    def getattr(self, path):
      #print 'get path attr', path
      st = MyStat()
      if path == '/':# or path == '.' or path == '..':
        st.st_mode = stat.S_IFDIR | 0755
        st.st_nlink = 2
        return st
      try:
        return os.stat(self.getPath(path))
      except:
        #print 'no stat', self.getPath(path)
        return -errno.ENOENT

    def readdir(self, path, offset):
        #yield fuse.Direntry('a.txt')
        #for r in  '.', '..':
        #    yield fuse.Direntry(r)
        for r in os.listdir(self.getPath(path)):
            yield fuse.Direntry(r)

    def open(self, path, flags):
        #print 'calling open'
        if self.getattr(path) == -errno.ENOENT:
            return -errno.ENOENT
        accmode = os.O_RDONLY | os.O_WRONLY | os.O_RDWR
        if (flags & accmode) != os.O_RDONLY:
            return -errno.EACCES

    def read(self, path, size, offset):
        if self.getattr(path) == -errno.ENOENT:
            return -errno.ENOENT
        #print 'open file:',self.getPath(path)
        f = open(self.getPath(path),'rb')
        f.seek(offset)
        buf = f.read(size)
        f.close()
        #print 'read len:', len(buf)
        return buf
        

def main():
    usage="""
Userspace hello example

""" + Fuse.fusage
    server = mirrorFs(version="%prog " + fuse.__version__,
                     usage=usage,
                     dash_s_do='setsingle')

    server.parse(errex=1)
    server.main()

if __name__ == '__main__':
    main()
