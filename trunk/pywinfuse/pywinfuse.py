from ctypes import *
from dokan import *
#from myLogger import *
from tools import *
import inspect
# functions
def whoami():
    return inspect.stack()[1][3]
def whosdaddy():
    return inspect.stack()[2][3]

def log(a = '',b='',c='',d='',e='',f='',g='',h='',):
    print whosdaddy(),a,b,c,d,e

def dbg(*args):
  #print whosdaddy()
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

option = _DOKAN_OPTIONS(
    'K',#('DriveLetter', WCHAR),
    0,#('ThreadCount', USHORT),
    1,#('DebugMode', UCHAR),
    1,#('UseStdErr', UCHAR),
    1,#('UseAltStream', UCHAR),
    0,#('UseKeepAlive', UCHAR),
    0#('GlobalContext', ULONG64),
)

CreateFileFuncType = WINFUNCTYPE(c_int, LPCWSTR, DWORD, DWORD, DWORD, DWORD, PDOKAN_FILE_INFO)
OpenDirectoryFuncType = WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)
CreateDirectoryFuncType = WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)
CleanupFuncType = WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)
CloseFileFuncType = WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)
ReadFileFuncType = WINFUNCTYPE(c_int, LPCWSTR, LPVOID, DWORD, LPVOID, LONGLONG, PDOKAN_FILE_INFO)
WriteFileFuncType = WINFUNCTYPE(c_int, LPCWSTR, LPCVOID, DWORD, LPDWORD, LONGLONG, PDOKAN_FILE_INFO)
FlushFileBuffersFuncType = WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)
GetFileInformationFuncType = WINFUNCTYPE(c_int, LPCWSTR, LPBY_HANDLE_FILE_INFORMATION, PDOKAN_FILE_INFO)
FindFilesFuncType = WINFUNCTYPE(c_int, LPCWSTR, PFillFindData, PDOKAN_FILE_INFO)
FindFilesWithPatternFuncType = WINFUNCTYPE(c_int, LPCWSTR, LPCWSTR, PFillFindData, PDOKAN_FILE_INFO)
SetFileAttributesFuncType = WINFUNCTYPE(c_int, LPCWSTR, DWORD, PDOKAN_FILE_INFO)
SetFileTimeFuncType = WINFUNCTYPE(c_int, LPCWSTR, POINTER(FILETIME), POINTER(FILETIME), POINTER(FILETIME), PDOKAN_FILE_INFO)
DeleteFileFuncType = WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)
DeleteDirectoryFuncType = WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)
MoveFileFuncType = WINFUNCTYPE(c_int, LPCWSTR, LPCWSTR, BOOL, PDOKAN_FILE_INFO)
SetEndOfFileFuncType = WINFUNCTYPE(c_int, LPCWSTR, LONGLONG, PDOKAN_FILE_INFO)
LockFileFuncType = WINFUNCTYPE(c_int, LPCWSTR, LONGLONG, LONGLONG, PDOKAN_FILE_INFO)
UnlockFileFuncType = WINFUNCTYPE(c_int, LPCWSTR, LONGLONG, LONGLONG, PDOKAN_FILE_INFO)
GetDiskFreeSpaceFuncType = WINFUNCTYPE(c_int, PULONGLONG, PULONGLONG, PULONGLONG, PDOKAN_FILE_INFO)
GetVolumeInformationFuncType = WINFUNCTYPE(c_int, LPWSTR, DWORD, LPDWORD, LPDWORD, LPDWORD, LPWSTR, DWORD, PDOKAN_FILE_INFO)
UnmountFuncType = WINFUNCTYPE(c_int, PDOKAN_FILE_INFO)




def dummyFunc(a='', b='', c='', d='', e='', f='',g='',h='',i='',j=''):
    print a, b, c, d, e, f, g, h, i, j
    return 0
'''
_DOKAN_OPERATIONS(\
    CreateFileFuncType(dummyFunc),#('CreateFile', WINFUNCTYPE(c_int, LPCWSTR, DWORD, DWORD, DWORD, DWORD, PDOKAN_FILE_INFO)),
    CreateFileFuncType(dummyFunc),#('OpenDirectory', WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
    CreateFileFuncType(dummyFunc),#('CreateDirectory', WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
    CreateFileFuncType(dummyFunc),#('Cleanup', WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
    CreateFileFuncType(dummyFunc),#('CloseFile', WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
    CreateFileFuncType(dummyFunc),#('ReadFile', WINFUNCTYPE(c_int, LPCWSTR, LPVOID, DWORD, LPDWORD, LONGLONG, PDOKAN_FILE_INFO)),
    CreateFileFuncType(dummyFunc),#('WriteFile', WINFUNCTYPE(c_int, LPCWSTR, LPCVOID, DWORD, LPDWORD, LONGLONG, PDOKAN_FILE_INFO)),
    CreateFileFuncType(dummyFunc),#('FlushFileBuffers', WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
    CreateFileFuncType(dummyFunc),#('GetFileInformation', WINFUNCTYPE(c_int, LPCWSTR, LPBY_HANDLE_FILE_INFORMATION, PDOKAN_FILE_INFO)),
    CreateFileFuncType(dummyFunc),#('FindFiles', WINFUNCTYPE(c_int, LPCWSTR, PFillFindData, PDOKAN_FILE_INFO)),
    CreateFileFuncType(dummyFunc),#('FindFilesWithPattern', WINFUNCTYPE(c_int, LPCWSTR, LPCWSTR, PFillFindData, PDOKAN_FILE_INFO)),
    CreateFileFuncType(dummyFunc),#('SetFileAttributes', WINFUNCTYPE(c_int, LPCWSTR, DWORD, PDOKAN_FILE_INFO)),
    CreateFileFuncType(dummyFunc),#('SetFileTime', WINFUNCTYPE(c_int, LPCWSTR, POINTER(FILETIME), POINTER(FILETIME), POINTER(FILETIME), PDOKAN_FILE_INFO)),
    CreateFileFuncType(dummyFunc),#('DeleteFile', WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
    CreateFileFuncType(dummyFunc),#('DeleteDirectory', WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
    CreateFileFuncType(dummyFunc),#('MoveFile', WINFUNCTYPE(c_int, LPCWSTR, LPCWSTR, BOOL, PDOKAN_FILE_INFO)),
    CreateFileFuncType(dummyFunc),#('SetEndOfFile', WINFUNCTYPE(c_int, LPCWSTR, LONGLONG, PDOKAN_FILE_INFO)),
    CreateFileFuncType(dummyFunc),#('LockFile', WINFUNCTYPE(c_int, LPCWSTR, LONGLONG, LONGLONG, PDOKAN_FILE_INFO)),
    CreateFileFuncType(dummyFunc),#('UnlockFile', WINFUNCTYPE(c_int, LPCWSTR, LONGLONG, LONGLONG, PDOKAN_FILE_INFO)),
    CreateFileFuncType(dummyFunc),#('GetDiskFreeSpace', WINFUNCTYPE(c_int, PULONGLONG, PULONGLONG, PULONGLONG, PDOKAN_FILE_INFO)),
    CreateFileFuncType(dummyFunc),#('GetVolumeInformation', WINFUNCTYPE(c_int, LPWSTR, DWORD, LPDWORD, LPDWORD, LPDWORD, LPWSTR, DWORD, PDOKAN_FILE_INFO)),
    CreateFileFuncType(dummyFunc),#('Unmount', WINFUNCTYPE(c_int, PDOKAN_FILE_INFO)),
)
'''

import win32file

def cre(CreationDisposition):
  if CreationDisposition == 2:#CREATE_ALWAYS
    print 'return 183'
    return 183 #win32file.ERROR_ALREADY_EXISTS
  if CreationDisposition == 4:#OPEN_ALWAYS
    print 183 #win32file.ERROR_ALREADY_EXISTS
    return 183
  return 0

def CreateFileFunc(FileName, DesiredAccess, ShareMode, CreationDisposition, FlagsAndAttributes, pInfo):
  print 'create file'
  dbgP(FileName,DesiredAccess,ShareMode,CreationDisposition,FlagsAndAttributes, pInfo)
  print CreationDisposition
  if FileName.lower() == '\\hello.txt':
    print 'return 0'
    return cre(CreationDisposition)
   
  if FileName == '\\':# and not pInfo.IsDirectory:
    print 'set is dir'
    #pInfo.IsDirectory = True
    return cre(CreationDisposition)
  '''
  if CreationDisposition == win32file.OPEN_ALWAYS:
    print 'return 183'
    return 183#win32file.ERROR_ALREADY_EXISTS
  '''
  print 'return -2'
  return -2
def OpenDirectoryFunc(FileName, pInfo):
  #log(FileName, pInfo)
  if FileName == 'helloworld':
    return 1
  return 0
def CreateDirectoryFunc(pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''):
  dbg()
  return 0# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
def CleanupFunc(pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''):
  dbg()
  return 0# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
def CloseFileFunc(pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''):
  dbg()
  return 0# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),



def ReadFileFunc(FileName, Buffer, NumberOfBytesToRead, NumberOfBytesRead, Offset, pInfo):
  dbgP(FileName, Buffer, NumberOfBytesToRead, NumberOfBytesRead, Offset, pInfo)
  data = 'hello world'
  print type(Buffer)
  if Offset > len(data):
    #Read from behind the data
    setDwordByPoint(NumberOfBytesRead, 0)
    return 0
  if len(data) < Offset + NumberOfBytesToRead:
    #Read end exceed data
    memmove(Buffer, data[Offset:], len(data)-Offset)
    r = len(data)-Offset
    setDwordByPoint(NumberOfBytesRead, r)
  else:
    memmove(Buffer, data, NumberOfBytesToRead)
    r = NumberOfBytesToRead
    setDwordByPoint(NumberOfBytesRead, r)
  memmove(Buffer, data, 4)
  print string_at(Buffer)
  real = 11
  setDwordByPoint(NumberOfBytesRead, real)
  return 0# WINFUNCTYPE(c_int, LPCWSTR, LPVOID, DWORD, LPDWORD, LONGLONG, PDOKAN_FILE_INFO)),


def WriteFileFunc(pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
  dbg()
  return 0# WINFUNCTYPE(c_int, LPCWSTR, LPCVOID, DWORD, LPDWORD, LONGLONG, PDOKAN_FILE_INFO)),
def FlushFileBuffersFunc(pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
  dbg()
  return 0# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
def GetFileInformationFunc(FileName, Buffer, pInfo):
  #log(FileName, Buffer, pInfo)
  if FileName == '\\':
    #print '--------------------------------------------\\'
    Buffer = _BY_HANDLE_FILE_INFORMATION(
        16,#('dwFileAttributes', DWORD),
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
    return 1
  if FileName == '\\hello.txt':
    print '--------------------------------------------\\hello.txt'
    Buffer = _BY_HANDLE_FILE_INFORMATION(
        128,#('dwFileAttributes', DWORD),
      _FILETIME(0,0),#('ftCreationTime', FILETIME),
      _FILETIME(0,0),#('ftLastAccessTime', FILETIME),
      _FILETIME(0,0),#('ftLastWriteTime', FILETIME),
      0,#('dwVolumeSerialNumber', DWORD),
      0,#('nFileSizeHigh', DWORD),
      0,#('nFileSizeLow', DWORD),
      0,#('nNumberOfLinks', DWORD),
      0,#('nFileIndexHigh', DWORD),
      0,#('nFileIndexLow', DWORD),
      )
    return 1
  return 0# WINFUNCTYPE(c_int, LPCWSTR, LPBY_HANDLE_FILE_INFORMATION, PDOKAN_FILE_INFO)),
def FindFilesFunc(PathName, PFillFindData, pInfo):
  #log(PathName, PFillFindData, pInfo)
  he = _WIN32_FIND_DATAW(
    128,#('dwFileAttributes', DWORD),
    _FILETIME(0,0),#('ftCreationTime', FILETIME),
    _FILETIME(0,0),#('ftLastAccessTime', FILETIME),
    _FILETIME(0,0),#('ftLastWriteTime', FILETIME),
    0,#('nFileSizeHigh', DWORD),
    len('hello world'),#('nFileSizeLow', DWORD),
    0,#('dwReserved0', DWORD),
    0,#('dwReserved1', DWORD),
    'hello.txt',#('cFileName', WCHAR * 260),
    '')#('cAlternateFileName', WCHAR * 14),)
  PFillFindData(pointer(he), pInfo)
  #print '---------------------------------------------------',he
  #print '---------------------------------------------------',pInfo
  return 1# WINFUNCTYPE(c_int, LPCWSTR, PFillFindData, PDOKAN_FILE_INFO)),
def FindFilesWithPatternFunc(PathName, SearchPattern, PFillFindData, pInfo):
  FindFilesFunc(PathName, PFillFindData, pInfo)
  return 1# WINFUNCTYPE(c_int, LPCWSTR, PFillFindData, PDOKAN_FILE_INFO)),
def SetFileAttributesFunc(pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
  dbg()
  return 0# WINFUNCTYPE(c_int, LPCWSTR, DWORD, PDOKAN_FILE_INFO)),
def SetFileTimeFunc(pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
  dbg()
  return 0# WINFUNCTYPE(c_int, LPCWSTR, POINTER(FILETIME), POINTER(FILETIME), POINTER(FILETIME), PDOKAN_FILE_INFO)),
def DeleteFileFunc(pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
  dbg()
  return 0# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
def DeleteDirectoryFunc(pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
  dbg()
  return 0# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
def MoveFileFunc(pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
  dbg()
  return 0# WINFUNCTYPE(c_int, LPCWSTR, LPCWSTR, BOOL, PDOKAN_FILE_INFO)),
def SetEndOfFileFunc(pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
  dbg()
  return 0# WINFUNCTYPE(c_int, LPCWSTR, LONGLONG, PDOKAN_FILE_INFO)),
def LockFileFunc(pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
  dbg()
  return 0# WINFUNCTYPE(c_int, LPCWSTR, LONGLONG, LONGLONG, PDOKAN_FILE_INFO)),
def UnlockFileFunc(pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
  dbg()
  return 0# WINFUNCTYPE(c_int, LPCWSTR, LONGLONG, LONGLONG, PDOKAN_FILE_INFO)),
def GetDiskFreeSpaceFunc(pFreeBytesAvailable, pTotalNumberOfBytes, pTotalNumberOfFreeBytes, pInfo):
  '''
  FreeBytesAvailable = 0x123456789abcdef0L
  TotalNumberOfBytes = 0x10000000L#256M=256*1024*1024
  TotalNumberOfFreeBytes = 0x1000L
  setLongLongByPoint(pFreeBytesAvailable, FreeBytesAvailable)
  setLongLongByPoint(pTotalNumberOfBytes, TotalNumberOfBytes)
  setLongLongByPoint(pTotalNumberOfFreeBytes, TotalNumberOfFreeBytes)
  '''
  return 0# WINFUNCTYPE(c_int, PULONGLONG, PULONGLONG, PULONGLONG, PDOKAN_FILE_INFO)),
def GetVolumeInformationFunc(VolumeNameBuffer, VolumeNameSize, VolumeSerialNumber, 
    MaximumComponentLength, FileSystemFlags, FileSystemNameBuffer, FileSystemNameSize, pInfo):
  #log(VolumeNameBuffer, VolumeNameSize, VolumeSerialNumber, 
  #MaximumComponentLength, FileSystemFlags, FileSystemNameBuffer, FileSystemNameSize, pInfo)
  memmove(VolumeNameBuffer, u'my own volumne', min(VolumeNameSize, len(u'my own volumne')))
  VolumeSerialNumber = 0
  MaximumComponentLength = 0
  FileSystemFlags = 0
  memmove(FileSystemNameBuffer, 'wwj', min(FileSystemNameSize, len('wwj')))
  return 0# WINFUNCTYPE(c_int, LPWSTR, DWORD, LPDWORD, LPDWORD, LPDWORD, LPWSTR, DWORD, PDOKAN_FILE_INFO)),
def UnmountFunc(pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
  dbg()
  return 0# WINFUNCTYPE(c_int, PDOKAN_FILE_INFO)),

operation = _DOKAN_OPERATIONS(
  CreateFileFuncType(CreateFileFunc),# WINFUNCTYPE(c_int, LPCWSTR, DWORD, DWORD, DWORD, DWORD, PDOKAN_FILE_INFO)),
  OpenDirectoryFuncType(OpenDirectoryFunc),# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
  CreateDirectoryFuncType(CreateDirectoryFunc),# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
  CleanupFuncType(CleanupFunc),# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
  CloseFileFuncType(CloseFileFunc),# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
  ReadFileFuncType(ReadFileFunc),# WINFUNCTYPE(c_int, LPCWSTR, LPVOID, DWORD, LPDWORD, LONGLONG, PDOKAN_FILE_INFO)),
  WriteFileFuncType(WriteFileFunc),# WINFUNCTYPE(c_int, LPCWSTR, LPCVOID, DWORD, LPDWORD, LONGLONG, PDOKAN_FILE_INFO)),
  FlushFileBuffersFuncType(FlushFileBuffersFunc),# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
  GetFileInformationFuncType(GetFileInformationFunc),# WINFUNCTYPE(c_int, LPCWSTR, LPBY_HANDLE_FILE_INFORMATION, PDOKAN_FILE_INFO)),
  FindFilesFuncType(FindFilesFunc),# WINFUNCTYPE(c_int, LPCWSTR, PFillFindData, PDOKAN_FILE_INFO)),
  FindFilesWithPatternFuncType(FindFilesWithPatternFunc),# WINFUNCTYPE(c_int, LPCWSTR, LPCWSTR, PFillFindData, PDOKAN_FILE_INFO)),
  SetFileAttributesFuncType(SetFileAttributesFunc),# WINFUNCTYPE(c_int, LPCWSTR, DWORD, PDOKAN_FILE_INFO)),
  SetFileTimeFuncType(SetFileTimeFunc),# WINFUNCTYPE(c_int, LPCWSTR, POINTER(FILETIME), POINTER(FILETIME), POINTER(FILETIME), PDOKAN_FILE_INFO)),
  DeleteFileFuncType(DeleteFileFunc),# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
  DeleteDirectoryFuncType(DeleteDirectoryFunc),# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
  MoveFileFuncType(MoveFileFunc),# WINFUNCTYPE(c_int, LPCWSTR, LPCWSTR, BOOL, PDOKAN_FILE_INFO)),
  SetEndOfFileFuncType(SetEndOfFileFunc),# WINFUNCTYPE(c_int, LPCWSTR, LONGLONG, PDOKAN_FILE_INFO)),
  LockFileFuncType(LockFileFunc),# WINFUNCTYPE(c_int, LPCWSTR, LONGLONG, LONGLONG, PDOKAN_FILE_INFO)),
  UnlockFileFuncType(UnlockFileFunc),# WINFUNCTYPE(c_int, LPCWSTR, LONGLONG, LONGLONG, PDOKAN_FILE_INFO)),
  GetDiskFreeSpaceFuncType(GetDiskFreeSpaceFunc),# WINFUNCTYPE(c_int, PULONGLONG, PULONGLONG, PULONGLONG, PDOKAN_FILE_INFO)),
  GetVolumeInformationFuncType(GetVolumeInformationFunc),# WINFUNCTYPE(c_int, LPWSTR, DWORD, LPDWORD, LPDWORD, LPDWORD, LPWSTR, DWORD, PDOKAN_FILE_INFO)),
  UnmountFuncType(UnmountFunc),# WINFUNCTYPE(c_int, PDOKAN_FILE_INFO)),
)


from ctypes import *
print windll.dokan
windll.dokan.DokanMain(byref(option),byref(operation))
