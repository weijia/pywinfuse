import myWin32file
import errno
from fuseBase import *
'''
opTranslate = {myWin32file.OPEN_EXISTING:,
myWin32file.TRUNCATE_EXISTING:,
myWin32file.CREATE_NEW:}
'''

import sys, traceback


class openSupport:
  def create(*args):
    pass
  '''
  def setDirFlag(pInfo):
    pInfo.IsDirectory = 1
  def CreateFileFunc(self, FileName, DesiredAccess, ShareMode, CreationDisposition, FlagsAndAttributes, pInfo):
    #dbgP(FileName,DesiredAccess,ShareMode,CreationDisposition,FlagsAndAttributes, pInfo)
    unixFilename = FileName.replace('\\','/')
    if FileName == '\\':
      self.setDirFlag()
    if self.getattr(unixFilename) != -errno.ENOENT:
      print 'exist'
      return cre(CreationDisposition)
    else:
      return cre(CreationDisposition)
  '''
  def CreateFileFunc(self, FileName, DesiredAccess, ShareMode, CreationDisposition, FlagsAndAttributes, pInfo):
    #dbgP(FileName,DesiredAccess,ShareMode,CreationDisposition,FlagsAndAttributes, pInfo)
    #print 'new create file fun called'
    unixFilename = FileName.replace('\\','/')
    if FileName == '/':
      pInfo.IsDirectory = 1
    #print unixFilename
    #Check the existance of the file
    if self.checkError(self.getattrWrapper(unixFilename)) == 0:
      #File exist, check if we need to fail when the file exists
      if (myWin32file.CREATE_NEW == CreationDisposition):
        return -myWin32file.ERROR_FILE_NOT_FOUND
    else:
      if (myWin32file.OPEN_EXISTING == CreationDisposition) or\
        (myWin32file.TRUNCATE_EXISTING == CreationDisposition):
        return -myWin32file.ERROR_FILE_NOT_FOUND
      #Create the file if required
      if (myWin32file.CREATE_NEW == CreationDisposition) or\
        (myWin32file.CREATE_ALWAYS == CreationDisposition) or\
        (myWin32file.OPEN_ALWAYS == CreationDisposition) or\
        (mymyWin32file.TRUNCATE_EXISTING == CreationDisposition):
        return self.checkError(self.create_wrapper(unixFilename))
    return 0
  
  def getattrWrapper(self, path):
    '''#Is this needed? gmailfs will not handle '/'?
    st = Stat()
    if path == '/':# or path == '.' or path == '..':
      st.st_mode = stat.S_IFDIR | 0755
      st.st_nlink = 2
      return st
    '''
    try:
      return self.getattr(path)
    except:
      print 'exception detected when getting attr:', path
      traceback.print_exc(file=sys.stdout)
    return -errno.ENOENT

  def mkdir(self, path, mode):
    print '*** mkdir', path, oct(mode)
    return -errno.ENOSYS
  def CreateDirectoryFunc(self, FileName, pInfo):# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
    #dbg()
    res = self.mkdir(self.translateFileName(FileName), 777)
    return self.checkError(res)
    
      
  def rename(self, oldPath, newPath):
    print '*** rename', oldPath, newPath
    return -errno.ENOENT
  def MoveFileFunc(self, FileName, NewFileName, ReplaceIfExisting, pInfo):
    res = self.rename(self.translateFileName(FileName), self.translateFileName(NewFileName))
    return self.checkError(res)
