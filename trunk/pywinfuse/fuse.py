#from pywinfuse import *
from ctypes import *
from dokan import *
#from myLogger import *
from tools import *
import inspect
from fuseBase import *
import win32file
import stat
import errno
import os
__version__ = '0.1'
# functions
def whoami():
    return inspect.stack()[1][3]
def whosdaddy():
    return inspect.stack()[2][3]

def log(a = '',b='',c='',d='',e='',f='',g='',h='',):
    print whosdaddy(),a,b,c,d,e

def dbg(*args):
  print whosdaddy()
  logStr = ''
  for i in args:
    logStr += str(i)
  print logStr

def dbgP(*args):
  #print whosdaddy()
  logStr = ''
  for i in args:
    logStr += str(i)+":"+str(type(i))
  print logStr


def cre(CreationDisposition):
  if CreationDisposition == win32file.CREATE_ALWAYS:
    print 'return 183'
    return win32file.ERROR_ALREADY_EXISTS
  if CreationDisposition == win32file.OPEN_ALWAYS:
    print win32file.ERROR_ALREADY_EXISTS
    return win32file.ERROR_ALREADY_EXISTS
  return 0


class Fuse(fuseBase):
  def setDirFlag(pInfo):
    pInfo.IsDirectory = 1
  def CreateFileFunc(self, FileName, DesiredAccess, ShareMode, CreationDisposition, FlagsAndAttributes, pInfo):
    #dbgP(FileName,DesiredAccess,ShareMode,CreationDisposition,FlagsAndAttributes, pInfo)
    unixFilename = FileName.replace('\\','/')
    if FileName == '\\':
      self.setDirFlag()
    if self.open(unixFilename, os.O_RDONLY) != -errno.ENOENT:
      print 'exist'
      return cre(CreationDisposition)
    else:
      return cre(CreationDisposition)
  def OpenDirectoryFunc(self, FileName, pInfo):
    unixFilename = FileName.replace('\\','/')
    if self.open(unixFilename, os.O_RDONLY) != -errno.ENOENT:
      return 0
    else:
      return 0
  def CreateDirectoryFunc(self, pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''):
    dbg()
    return 0# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
  def CleanupFunc(self, pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''):
    dbg()
    return 0# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
  def CloseFileFunc(self, pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''):
    dbg()
    return 0# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
  
  def ReadFileFunc(self, FileName, Buffer, NumberOfBytesToRead, NumberOfBytesRead, Offset, pInfo):
    #dbgP(FileName, Buffer, NumberOfBytesToRead, NumberOfBytesRead, Offset, pInfo)
    unixFilename = FileName.replace('\\','/')
    data = self.read(unixFilename, NumberOfBytesToRead, Offset)
    if data == -errno.ENOENT:
      print 'data not exist'
      return -2
    if data == '':
      print 'end of data'
      return -1
    length = len(data)
    memmove(Buffer, data, length)
    setDwordByPoint(NumberOfBytesRead, length)
    return 0# WINFUNCTYPE(c_int, LPCWSTR, LPVOID, DWORD, LPDWORD, LONGLONG, PDOKAN_FILE_INFO)),


  def WriteFileFunc(self, pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
    dbg()
    return 0# WINFUNCTYPE(c_int, LPCWSTR, LPCVOID, DWORD, LPDWORD, LONGLONG, PDOKAN_FILE_INFO)),
  def FlushFileBuffersFunc(self, pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
    dbg()
    return 0# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),

  def translateModeFromUnix(self, st):
    if st.st_mode & stat.S_IFDIR:
      #This element is a directory, set the correct attribute
      return win32file.FILE_ATTRIBUTE_DIRECTORY#16
    else:
      return win32file.FILE_ATTRIBUTE_ARCHIVE#32
    
  def GetFileInformationFunc(self, FileName, Buffer, pInfo):
    #log(FileName, Buffer, pInfo)
    unixFilename = FileName.replace('\\','/')
    st = self.getattr(unixFilename)
    if st != -errno.ENOENT:
      '''
      Buffer = _BY_HANDLE_FILE_INFORMATION(
        self.translateModeFromUnix(st),#('dwFileAttributes', DWORD),
        _FILETIME(0,0),#('ftCreationTime', FILETIME),2 DWORD
        _FILETIME(0,0),#('ftLastAccessTime', FILETIME),
        _FILETIME(0,0),#('ftLastWriteTime', FILETIME),
        0,#('dwVolumeSerialNumber', DWORD),
        st.st_size,#('nFileSizeHigh', DWORD),
        st.st_size,#('nFileSizeLow', DWORD),
        1,#('nNumberOfLinks', DWORD),
        0,#('nFileIndexHigh', DWORD),
        0#('nFileIndexLow', DWORD),
        )
      #Buffer.dwFileAttributes = self.translateModeFromUnix(st)
      #Buffer.nFileSizeLow = st.st_size
      print 'attr',Buffer.dwFileAttributes
      print 'size',Buffer.nFileSizeLow
      '''
      setDwordByPoint(Buffer, self.translateModeFromUnix(st))
      setDwordByPoint(Buffer+32, st.st_size>>32)#('nFileSizeHigh', DWORD),
      setDwordByPoint(Buffer+36, st.st_size&0xffffffff)#('nFileSizeLow', DWORD),
      setDwordByPoint(Buffer+40, 1)
      #Function always return 0 when success
      print 'success'
      return 0
    else:
      print 'returning -2'
      return -2
    return 0# WINFUNCTYPE(c_int, LPCWSTR, LPBY_HANDLE_FILE_INFORMATION, PDOKAN_FILE_INFO)),
  def FindFilesFunc(self, PathName, PFillFindData, pInfo):
    print 'finding files in: %s'%PathName
    unixFilename = PathName.replace('\\','/')
    offset = 0
    Buffer = _BY_HANDLE_FILE_INFORMATION(
      0,#('dwFileAttributes', DWORD),
      _FILETIME(0,0),#('ftCreationTime', FILETIME),
      _FILETIME(0,0),#('ftLastAccessTime', FILETIME),
      _FILETIME(0,0),#('ftLastWriteTime', FILETIME),
      0,#('dwVolumeSerialNumber', DWORD),
      0,#('nFileSizeHigh', DWORD),
      0,#('nFileSizeLow', DWORD),
      0,#('nNumberOfLinks', DWORD),
      0,#('nFileIndexHigh', DWORD),
      0#('nFileIndexLow', DWORD),
      )
    for entry in self.readdir(unixFilename, offset):
      #entry = self.readdir(unixFilename, offset)
      #if entry == None:
      #  break
      #if (entry.getName() == '.') or (entry.getName() == '..'):
      #  print 'continue'
      #  continue
      finalPath = os.path.join(PathName, entry.getName())
      print 'finalPath',finalPath
      unixFinal = finalPath.replace('\\','/')
      st = self.getattr(unixFinal)
      if st != -errno.ENOENT:
        Buffer.dwFileAttributes = self.translateModeFromUnix(st)
        Buffer.nFileSizeLow = st.st_size
        print 'attr',Buffer.dwFileAttributes
        print 'size',Buffer.nFileSizeLow
      else:
        continue
      print 'Buffer.nFileSizeLow', Buffer.nFileSizeLow
      he = _WIN32_FIND_DATAW(
        Buffer.dwFileAttributes,#('dwFileAttributes', DWORD),
        _FILETIME(0,0),#('ftCreationTime', FILETIME),
        _FILETIME(0,0),#('ftLastAccessTime', FILETIME),
        _FILETIME(0,0),#('ftLastWriteTime', FILETIME),
        0,#('nFileSizeHigh', DWORD),
        Buffer.nFileSizeLow,#('nFileSizeLow', DWORD),
        0,#('dwReserved0', DWORD),
        0,#('dwReserved1', DWORD),
        entry.getName(),#('cFileName', WCHAR * 260),
        entry.getName())#('cAlternateFileName', WCHAR * 14),)
      PFillFindData(pointer(he), pInfo)
    return 0# WINFUNCTYPE(c_int, LPCWSTR, PFillFindData, PDOKAN_FILE_INFO)),
  def FindFilesWithPatternFunc(self, PathName, SearchPattern, PFillFindData, pInfo):
    dbgP(PathName, SearchPattern, PFillFindData, pInfo)
    return self.FindFilesFunc(PathName, PFillFindData, pInfo)
    return 0# WINFUNCTYPE(c_int, LPCWSTR, PFillFindData, PDOKAN_FILE_INFO)),
  def SetFileAttributesFunc(self, pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
    dbg()
    return 0# WINFUNCTYPE(c_int, LPCWSTR, DWORD, PDOKAN_FILE_INFO)),
  def SetFileTimeFunc(self, pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
    dbg()
    return 0# WINFUNCTYPE(c_int, LPCWSTR, POINTER(FILETIME), POINTER(FILETIME), POINTER(FILETIME), PDOKAN_FILE_INFO)),
  def DeleteFileFunc(self, pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
    dbg()
    return 0# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
  def DeleteDirectoryFunc(self, pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
    dbg()
    return 0# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
  def MoveFileFunc(self, pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
    dbg()
    return 0# WINFUNCTYPE(c_int, LPCWSTR, LPCWSTR, BOOL, PDOKAN_FILE_INFO)),
  def SetEndOfFileFunc(self, pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
    dbg()
    return 0# WINFUNCTYPE(c_int, LPCWSTR, LONGLONG, PDOKAN_FILE_INFO)),
  def LockFileFunc(self, pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
    dbg()
    return 0# WINFUNCTYPE(c_int, LPCWSTR, LONGLONG, LONGLONG, PDOKAN_FILE_INFO)),
  def UnlockFileFunc(self, pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
    dbg()
    return 0# WINFUNCTYPE(c_int, LPCWSTR, LONGLONG, LONGLONG, PDOKAN_FILE_INFO)),
  def GetDiskFreeSpaceFunc(self, pFreeBytesAvailable, pTotalNumberOfBytes, pTotalNumberOfFreeBytes, pInfo):
    FreeBytesAvailable = 0x1234567L
    TotalNumberOfBytes = 0x10000000L#256M=256*1024*1024
    TotalNumberOfFreeBytes = 0x1234567L
    setLongLongByPoint(pFreeBytesAvailable, FreeBytesAvailable)
    setLongLongByPoint(pTotalNumberOfBytes, TotalNumberOfBytes)
    setLongLongByPoint(pTotalNumberOfFreeBytes, TotalNumberOfFreeBytes)
    return 0# WINFUNCTYPE(c_int, PULONGLONG, PULONGLONG, PULONGLONG, PDOKAN_FILE_INFO)),
  def GetVolumeInformationFunc(self, VolumeNameBuffer, VolumeNameSize, VolumeSerialNumber, 
      MaximumComponentLength, FileSystemFlags, FileSystemNameBuffer, FileSystemNameSize, pInfo):
    #log(VolumeNameBuffer, VolumeNameSize, VolumeSerialNumber, 
    #MaximumComponentLength, FileSystemFlags, FileSystemNameBuffer, FileSystemNameSize, pInfo)
    memmove(VolumeNameBuffer, u'my own volumne', min(VolumeNameSize, len(u'my own volumne')))
    VolumeSerialNumber = 0
    MaximumComponentLength = 0
    FileSystemFlags = 0
    memmove(FileSystemNameBuffer, u'wwj', min(FileSystemNameSize, 2*len(u'wwj')))
    return 0# WINFUNCTYPE(c_int, LPWSTR, DWORD, LPDWORD, LPDWORD, LPDWORD, LPWSTR, DWORD, PDOKAN_FILE_INFO)),
  def UnmountFunc(self, pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
    dbg()
    return 0# WINFUNCTYPE(c_int, PDOKAN_FILE_INFO)),

