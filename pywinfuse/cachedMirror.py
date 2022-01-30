import os, stat, errno
# pull in some spaghetti to make this stuff work without fuse-py being installed
try:
    import _find_fuse_parts
except ImportError:
    pass
import fuse
from fuse import Fuse


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

def getCacheInstance(server = 'dirCache'):
  try:
    from shove import Shove
    print('sqlite:///%s.sqlite'%server)
    dir_cache = Shove('sqlite:///%s.sqlite'%server)
    #ftpCache = Shove()
    print('use shove')
  except Exception as e:
    dir_cache = {}
    print('use dict')
  return dir_cache


class cachedMirrorFs(Fuse):
    def __init__(self, rootDir='c:/'):
      self.dirCache = getCacheInstance()
      self.baseFilesys = rootDir
      Fuse.__init__(self)
    def get_path(self, path):
      #print 'get path', path
      real_path = self.baseFilesys + path
      #print realP
      return real_path
    def getattr(self, path):
      #print 'get path attr', path
      st = MyStat()
      if path == '/':# or path == '.' or path == '..':
        st.st_mode = stat.S_IFDIR | 0o755
        st.st_nlink = 2
        return st
      try:
        return os.stat(self.get_path(path))
      except:
        #print 'no stat', self.getPath(path)
        return -errno.ENOENT

    def readdir(self, path, offset):
        #yield fuse.Direntry('a.txt')
        for r in  '.', '..':
            yield fuse.Direntry(r)
        try:
            cachedDir = self.dirCache[path]
            #print cachedDir
            for r in cachedDir:
                #print r
                yield fuse.Direntry(r)
            print('cached dir info')
        except KeyError:
            self.dirCache[path] = []
            for r in os.listdir(self.get_path(path)):
                self.dirCache[path].append(r)
                yield fuse.Direntry(r)
            print('real dir info')

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
        f = open(self.get_path(path), 'rb')
        f.seek(offset)
        buf = f.read(size)
        f.close()
        #print 'read len:', len(buf)
        return buf


import sys

def main():
    if len(sys.argv) < 2:
        rootDir = 'd:/'
    else:
        rootDir = sys.argv[1]
    fuseServer = cachedMirrorFs(rootDir = rootDir)
    fuseServer.main()

if __name__ == '__main__':
    main()
