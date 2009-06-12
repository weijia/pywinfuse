import myWin32file
import errno
from tools import *
import stat

class unlinkSupport:
  def unlink(self, path):
    print '*** unlink', path
    return -errno.ENOSYS
  def rmdir(self, path):
    print '*** rmdir', path
    return -errno.ENOENT
    
  def DeleteFileFunc(self, FileName, pInfo):# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO))
    unixFilename = self.translateFileName(FileName)
    st = self.getattr(unixFilename)
    if st.st_mode & stat.S_IFDIR:
      #Is DIR rmdir
      return self.checkError(self.rmdir(unixFilename))
    else:
      print 'removing:',unixFilename
      return self.checkError(self.unlink(unixFilename))



class writeSupport:
  def write(self, path, buf, offset):
    print '*** write', path, buf, offset
    return -errno.ENOSYS
  def WriteFileFunc(self, FileName, Buffer, NumberOfBytesToWrite, NumberOfBytesWritten, Offset, pInfo): 
    #dbg()
    unixFilename = self.translateFileName(FileName)
    realBuf = Buffer[:NumberOfBytesToWrite]
    writtenLen = self.write(unixFilename, realBuf, Offset)
    if writtenLen < 0:
      return -myWin32file.ERROR_FILE_NOT_FOUND
    setDwordByPoint(NumberOfBytesWritten, writtenLen)
    return 0# WINFUNCTYPE(c_int, LPCWSTR, LPCVOID, DWORD, LPDWORD, LONGLONG, PDOKAN_FILE_INFO)),
