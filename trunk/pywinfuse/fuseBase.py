from ctypes import *
from dokan import *


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

class Stat:
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


class fuseArgs:
  def __init__(self):
    pass
  def add(self, opt):
    pass

class Direntry:
  def __init__(self, name):
    self.name = name
  def getName(self):
    return self.name
    #return unicode(self.name).encode('utf-8')
    return self.name.replace('/','\\')


fuse_python_api = None

class fuseBase:
  fusage = 'no usage currently'
  def __init__(self, usage = '', dash_s_do = '', version = '', debug = 0):
    #The following is used to be compitable with Linux Fuse Python binding
    self.flags = 0
    self.multithreaded = 0
    self.allow_other = 0
    if debug != 1:
      self.debug = c_ubyte(0)
    else:
      self.debug = c_ubyte(1)
  def parse(self, errex = 0):
    pass
  
  '''
  The following functions are interface function defined in dokan.
  '''
  def CreateFileFunc(self, FileName, DesiredAccess, ShareMode, CreationDisposition, FlagsAndAttributes, pInfo):
    return 0# WINFUNCTYPE(c_int, LPCWSTR, DWORD, DWORD, DWORD, DWORD, PDOKAN_FILE_INFO)
  def OpenDirectoryFunc(self, FileName, pInfo):
    return 0# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)
  def CreateDirectoryFunc(self, pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''):
    return 0# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
  def CleanupFunc(self, pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''):
    return 0# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
  def CloseFileFunc(self, pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''):
    return 0# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
  def ReadFileFunc(self, FileName, Buffer, NumberOfBytesToRead, NumberOfBytesRead, Offset, pInfo):
    return 0# WINFUNCTYPE(c_int, LPCWSTR, LPVOID, DWORD, LPDWORD, LONGLONG, PDOKAN_FILE_INFO)),
  def WriteFileFunc(self, pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
    return 0# WINFUNCTYPE(c_int, LPCWSTR, LPCVOID, DWORD, LPDWORD, LONGLONG, PDOKAN_FILE_INFO)),
  def FlushFileBuffersFunc(self, pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
    return 0# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
  def GetFileInformationFunc(self, FileName, Buffer, pInfo):
    return 0# WINFUNCTYPE(c_int, LPCWSTR, LPBY_HANDLE_FILE_INFORMATION, PDOKAN_FILE_INFO)),
  def FindFilesFunc(self, PathName, PFillFindData, pInfo):
    return 0# WINFUNCTYPE(c_int, LPCWSTR, PFillFindData, PDOKAN_FILE_INFO)),
  def FindFilesWithPatternFunc(self, PathName, SearchPattern, PFillFindData, pInfo):
    return 0# WINFUNCTYPE(c_int, LPCWSTR, PFillFindData, PDOKAN_FILE_INFO)),
  def SetFileAttributesFunc(self, pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
    return 0# WINFUNCTYPE(c_int, LPCWSTR, DWORD, PDOKAN_FILE_INFO)),
  def SetFileTimeFunc(self, pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
    return 0# WINFUNCTYPE(c_int, LPCWSTR, POINTER(FILETIME), POINTER(FILETIME), POINTER(FILETIME), PDOKAN_FILE_INFO)),
  def DeleteFileFunc(self, pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
    return 0# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
  def DeleteDirectoryFunc(self, pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
    return 0# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
  def MoveFileFunc(self, pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
    return 0# WINFUNCTYPE(c_int, LPCWSTR, LPCWSTR, BOOL, PDOKAN_FILE_INFO)),
  def SetEndOfFileFunc(self, pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
    return 0# WINFUNCTYPE(c_int, LPCWSTR, LONGLONG, PDOKAN_FILE_INFO)),
  def LockFileFunc(self, pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
    return 0# WINFUNCTYPE(c_int, LPCWSTR, LONGLONG, LONGLONG, PDOKAN_FILE_INFO)),
  def UnlockFileFunc(self, pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
    return 0# WINFUNCTYPE(c_int, LPCWSTR, LONGLONG, LONGLONG, PDOKAN_FILE_INFO)),
  def GetDiskFreeSpaceFunc(self, FreeBytesAvailable, TotalNumberOfBytes, TotalNumberOfFreeBytes, pInfo):
    return 0# WINFUNCTYPE(c_int, PULONGLONG, PULONGLONG, PULONGLONG, PDOKAN_FILE_INFO)),
  def GetVolumeInformationFunc(self, VolumeNameBuffer, VolumeNameSize, VolumeSerialNumber, 
      MaximumComponentLength, FileSystemFlags, FileSystemNameBuffer, FileSystemNameSize, pInfo):
    return 0# WINFUNCTYPE(c_int, LPWSTR, DWORD, LPDWORD, LPDWORD, LPDWORD, LPWSTR, DWORD, PDOKAN_FILE_INFO)),
  def UnmountFunc(self, pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
    return 0# WINFUNCTYPE(c_int, PDOKAN_FILE_INFO)),


  def main(self):
    print windll.dokan
    operation = _DOKAN_OPERATIONS(
      CreateFileFuncType(self.CreateFileFunc),# WINFUNCTYPE(c_int, LPCWSTR, DWORD, DWORD, DWORD, DWORD, PDOKAN_FILE_INFO)),
      OpenDirectoryFuncType(self.OpenDirectoryFunc),# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
      CreateDirectoryFuncType(self.CreateDirectoryFunc),# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
      CleanupFuncType(self.CleanupFunc),# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
      CloseFileFuncType(self.CloseFileFunc),# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
      ReadFileFuncType(self.ReadFileFunc),# WINFUNCTYPE(c_int, LPCWSTR, LPVOID, DWORD, LPDWORD, LONGLONG, PDOKAN_FILE_INFO)),
      WriteFileFuncType(self.WriteFileFunc),# WINFUNCTYPE(c_int, LPCWSTR, LPCVOID, DWORD, LPDWORD, LONGLONG, PDOKAN_FILE_INFO)),
      FlushFileBuffersFuncType(self.FlushFileBuffersFunc),# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
      GetFileInformationFuncType(self.GetFileInformationFunc),# WINFUNCTYPE(c_int, LPCWSTR, LPBY_HANDLE_FILE_INFORMATION, PDOKAN_FILE_INFO)),
      FindFilesFuncType(self.FindFilesFunc),# WINFUNCTYPE(c_int, LPCWSTR, PFillFindData, PDOKAN_FILE_INFO)),
      FindFilesWithPatternFuncType(self.FindFilesWithPatternFunc),# WINFUNCTYPE(c_int, LPCWSTR, LPCWSTR, PFillFindData, PDOKAN_FILE_INFO)),
      SetFileAttributesFuncType(self.SetFileAttributesFunc),# WINFUNCTYPE(c_int, LPCWSTR, DWORD, PDOKAN_FILE_INFO)),
      SetFileTimeFuncType(self.SetFileTimeFunc),# WINFUNCTYPE(c_int, LPCWSTR, POINTER(FILETIME), POINTER(FILETIME), POINTER(FILETIME), PDOKAN_FILE_INFO)),
      DeleteFileFuncType(self.DeleteFileFunc),# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
      DeleteDirectoryFuncType(self.DeleteDirectoryFunc),# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
      MoveFileFuncType(self.MoveFileFunc),# WINFUNCTYPE(c_int, LPCWSTR, LPCWSTR, BOOL, PDOKAN_FILE_INFO)),
      SetEndOfFileFuncType(self.SetEndOfFileFunc),# WINFUNCTYPE(c_int, LPCWSTR, LONGLONG, PDOKAN_FILE_INFO)),
      LockFileFuncType(self.LockFileFunc),# WINFUNCTYPE(c_int, LPCWSTR, LONGLONG, LONGLONG, PDOKAN_FILE_INFO)),
      UnlockFileFuncType(self.UnlockFileFunc),# WINFUNCTYPE(c_int, LPCWSTR, LONGLONG, LONGLONG, PDOKAN_FILE_INFO)),
      GetDiskFreeSpaceFuncType(self.GetDiskFreeSpaceFunc),# WINFUNCTYPE(c_int, PULONGLONG, PULONGLONG, PULONGLONG, PDOKAN_FILE_INFO)),
      GetVolumeInformationFuncType(self.GetVolumeInformationFunc),# WINFUNCTYPE(c_int, LPWSTR, DWORD, LPDWORD, LPDWORD, LPDWORD, LPWSTR, DWORD, PDOKAN_FILE_INFO)),
      UnmountFuncType(self.UnmountFunc),# WINFUNCTYPE(c_int, PDOKAN_FILE_INFO)),
    )
    option = _DOKAN_OPTIONS(
    'K',#('DriveLetter', WCHAR),
    1,#('ThreadCount', USHORT),
    self.debug,#('DebugMode', UCHAR),
    self.debug,#('UseStdErr', UCHAR),
    0,#('UseAltStream', UCHAR),
    0,#('UseKeepAlive', UCHAR),
    0#('GlobalContext', ULONG64),
    )
    #from ctypesTest import *
    #dumpMem(addressof(self.debug), 4)
    #dumpMem(option, 15)
    self.fuse_args = fuseArgs
    windll.dokan.DokanMain(byref(option),byref(operation))


