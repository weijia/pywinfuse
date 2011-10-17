import myWin32file
import errno
from tools import *
import stat
import ctypes

class unlinkSupport:
  def unlink(self, path):
    print '*** unlink', path
    return -errno.ENOSYS
  def rmdir(self, path):
    print '*** rmdir', path
    return -errno.ENOSYS
    
  def DeleteFileFunc(self, FileName, pInfo):# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO))
    unixFilename = self.translateFileName(FileName)
    st = self.getattrWrapper(unixFilename)
    if st != -errno.ENOENT:
      if st.st_mode & stat.S_IFDIR:
        #Is DIR rmdir
        return self.checkError(self.rmdir(unixFilename))
      else:
        print 'removing:',unixFilename
        return self.checkError(self.unlink(unixFilename))
    return -myWin32file.ERROR_FILE_NOT_FOUND

  def DeleteDirectoryFunc(self, FileName, pInfo): 
    #dbg()
    unixFilename = self.translateFileName(FileName)
    cl('Filename:', unixFilename)
    return self.checkError(self.rmdir(unixFilename))


class writeSupport:
  def write(self, path, buf, offset):
    print '*** write', path, buf, offset
    return -errno.ENOSYS

  def ftruncate(self, path, offset):
    print '*** truncate', path, offset
    return -errno.ENOSYS

  def WriteFileFunc(self, FileName, Buffer, NumberOfBytesToWrite, NumberOfBytesWritten, Offset, pInfo): 
    #dbg()
    unixFilename = self.translateFileName(FileName)
    realBuf = ctypes.string_at(Buffer, NumberOfBytesToWrite)
    writtenLen = self.write_wrapper(unixFilename, realBuf, Offset, pInfo)

    if writtenLen < 0:
      return -myWin32file.ERROR_FILE_NOT_FOUND
    setDwordByPoint(NumberOfBytesWritten, writtenLen)
    return 0# WINFUNCTYPE(c_int, LPCWSTR, LPCVOID, DWORD, LPDWORD, LONGLONG, PDOKAN_FILE_INFO)),

  def SetEndOfFileFunc(self, FileName, offset, pInfo):
    # dbg()
    unixFilename = self.translateFileName(FileName)
    if offset == 0:
        return self.ftruncate_wrapper(unixFilename, offset, pInfo)

    return 0# WINFUNCTYPE(c_int, LPCWSTR, LONGLONG, PDOKAN_FILE_INFO)),

