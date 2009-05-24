import win32file
import errno
'''
opTranslate = {win32file.OPEN_EXISTING:,
win32file.TRUNCATE_EXISTING:,
win32file.CREATE_NEW:}
'''



class openSupport:
  def create(fn):
    pass
  def CreateFileFunc(self, FileName, DesiredAccess, ShareMode, CreationDisposition, FlagsAndAttributes, pInfo):
    #dbgP(FileName,DesiredAccess,ShareMode,CreationDisposition,FlagsAndAttributes, pInfo)
    #print 'new create file fun called'
    unixFilename = FileName.replace('\\','/')
    if FileName == '/':
      pInfo.IsDirectory = 1
    #print unixFilename
    #Check the existance of the file
    if self.getattr(unixFilename) != -errno.ENOENT:
      #File exist, check if we need to fail when the file exists
      if (win32file.CREATE_NEW == CreationDisposition):
        return -win32file.ERROR_FILE_NOT_FOUND
    else:
      if (win32file.OPEN_EXISTING == CreationDisposition) or\
        (win32file.TRUNCATE_EXISTING == CreationDisposition):
        return -win32file.ERROR_FILE_NOT_FOUND
      #Create the file if required
      if (win32file.CREATE_NEW == CreationDisposition) or\
        (win32file.CREATE_ALWAYS == CreationDisposition) or\
        (win32file.OPEN_ALWAYS == CreationDisposition) or\
        (win32file.TRUNCATE_EXISTING == CreationDisposition):
        self.create(unixFilename)
    
    return 0
        
