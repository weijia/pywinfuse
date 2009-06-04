import os, stat, errno
import fuse
from fuse import Fuse
import uuid


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

from ftplib import FTP

cachePath = "d:/cache/"
from simpleFtpClient import *

def getCacheInstance(server):
  try:
    from shove import Shove
    print 'sqlite:///%s.sqlite'%server
    ftpCache = Shove('sqlite:///%s.sqlite'%server)
    #ftpCache = Shove()
    print 'use shove'
  except:
    ftpCache = {}
    print 'use dict'
  return ftpCache

class ftpFs(Fuse):
    def __init__(self, server='localhost', user = "anonymous", passwd = "ftplib-example-2"):
      self.cacheList = {}
      self.client = simpleFtpClient(server, user, passwd)
      self.ftpCache = getCacheInstance(server)
      Fuse.__init__(self)
    def getPath(self, path):
      #print 'get path', path
      realP = cachePath + path
      #print realP
      return realP
    def getattr(self, path):
      #print 'get path attr', path
      st = MyStat()
      if path == '/':# or path == '.' or path == '..':
        st.st_mode = stat.S_IFDIR | 0755
        st.st_nlink = 2
        return st
      #print path
      dirName, filename = path.rsplit('/',1)
      #print dirName, filename
      dirName = dirName + '/'
      try:
          d = self.ftpCache[dirName]
          for i in d:
              if i[9] == filename:
                  print i[9],i[1]
                  if i[1][0] == 'd':
                      st.st_mode = stat.S_IFDIR | 0755
                      st.st_nlink = 2
                      return st
                  else:
                      st.st_mode = stat.S_IFREG | 0444
                      st.st_nlink = 1
                      st.st_size = int(i[5])
                      return st
      except KeyError:
          pass
      return -errno.ENOENT

    def readdir(self, path, offset):
        #yield fuse.Direntry('a.txt')
        for r in  '.', '..':
            yield fuse.Direntry(r)
        try:
            cachedDir = self.ftpCache[path]
        except KeyError:
            self.ftpCache[path] = self.client.getDir(path)##########################################Reading ftp server
            cachedDir = self.ftpCache[path]
        #print self.ftpCache[path]
        for r in cachedDir:
            print r[9]
            yield fuse.Direntry(r[9])

    def open(self, path, flags):
        #print 'calling open'
        if self.getattr(path) == -errno.ENOENT:
            return -errno.ENOENT
        accmode = os.O_RDONLY | os.O_WRONLY | os.O_RDWR
        if (flags & accmode) != os.O_RDONLY:
            return -errno.EACCES

    def read(self, path, size, offset):
        #Check existance first
        if self.getattr(path) == -errno.ENOENT:
            return -errno.ENOENT
        #If it is downloaded?
        if not self.cacheList.has_key(path):
            #Didn't cached, download the remote file
            cached = self.cacheFile(path)
            self.cacheList[path] = cached
            print 'caching file:%s'%path
        else:
            cached = self.cacheList[path]
            print 'can use cache:%s:'%cached
        f = open(cached,'rb')
        f.seek(offset)
        buf = f.read(size)
        f.close()
        #print 'read len:', len(buf)
        return buf
        
    def cacheFile(self, path):
        #Generate local file path
        cached = self.getPath(str(uuid.uuid4()))
        wf = open(cached, 'wb')
        self.client.get(path, wf)##########################################Reading ftp server
        wf.close()
        return cached
        
def main():
    #server = ftpFs(user='wwj',passwd='wwj')
    import sys
    fuseServer = ftpFs(server = sys.argv[1], user = sys.argv[2], passwd = sys.argv[3])
    fuseServer.main()

if __name__ == '__main__':
    main()
