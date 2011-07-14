from ctypes import *

WSTRING = c_wchar_p


WCHAR = c_wchar
PWCHAR = WSTRING
USHORT = c_ushort
ULONG64 = c_ulonglong
PULONGLONG = c_void_p#POINTER(ULONG64)
PUCHAR = POINTER(c_ubyte)
UCHAR = c_ubyte
BOOL = c_int
PBOOL = POINTER(c_int)
LPBOOL = POINTER(c_int)
PULONG = POINTER(c_ulong)
ULONG = c_ulong
PDWORD = POINTER(c_ulong)
DWORD = c_ulong
LPDWORD = POINTER(c_ulong)
LPCWSTR = WSTRING
LPWSTR = c_void_p#WSTRING
PWSTR = WSTRING
LPVOID = c_void_p
LPCVOID = c_void_p
INT64 = c_longlong
LONGLONG = INT64
class _FILETIME(Structure):
    pass
_FILETIME._fields_ = [
    ('dwLowDateTime', DWORD),
    ('dwHighDateTime', DWORD),
]
PFILETIME = POINTER(_FILETIME)
FILETIME = _FILETIME
class _BY_HANDLE_FILE_INFORMATION(Structure):
    pass
_BY_HANDLE_FILE_INFORMATION._fields_ = [
    ('dwFileAttributes', DWORD),
    ('ftCreationTime', FILETIME),
    ('ftLastAccessTime', FILETIME),
    ('ftLastWriteTime', FILETIME),
    ('dwVolumeSerialNumber', DWORD),
    ('nFileSizeHigh', DWORD),
    ('nFileSizeLow', DWORD),
    ('nNumberOfLinks', DWORD),
    ('nFileIndexHigh', DWORD),
    ('nFileIndexLow', DWORD),
]
LPBY_HANDLE_FILE_INFORMATION = c_void_p#POINTER(_BY_HANDLE_FILE_INFORMATION)
BY_HANDLE_FILE_INFORMATION = _BY_HANDLE_FILE_INFORMATION
class _WIN32_FIND_DATAW(Structure):
    pass
_WIN32_FIND_DATAW._fields_ = [
    ('dwFileAttributes', DWORD),
    ('ftCreationTime', FILETIME),
    ('ftLastAccessTime', FILETIME),
    ('ftLastWriteTime', FILETIME),
    ('nFileSizeHigh', DWORD),
    ('nFileSizeLow', DWORD),
    ('dwReserved0', DWORD),
    ('dwReserved1', DWORD),
    ('cFileName', WCHAR * 260),
    ('cAlternateFileName', WCHAR * 14),
	#('extra', WCHAR * 4),
]
PWIN32_FIND_DATAW = POINTER(_WIN32_FIND_DATAW)
WIN32_FIND_DATAW = _WIN32_FIND_DATAW
LPWIN32_FIND_DATAW = POINTER(_WIN32_FIND_DATAW)
class _DOKAN_OPTIONS(Structure):
    pass
_DOKAN_OPTIONS._pack_ = 4
_DOKAN_OPTIONS._fields_ = [
        ('Version', USHORT),
        ('ThreadCount', USHORT),
        ('Options', ULONG),
        ('GlobalContext', ULONG64),
        ('MountPoint', LPCWSTR),
    ]

DOKAN_OPTIONS = _DOKAN_OPTIONS
PDOKAN_OPTIONS = POINTER(_DOKAN_OPTIONS)
class _DOKAN_FILE_INFO(Structure):
    pass
_DOKAN_FILE_INFO._pack_ = 4
_DOKAN_FILE_INFO._fields_ = [
    ('Context', ULONG64),
    ('DokanContext', ULONG64),
    ('ProcessId', ULONG),
    ('IsDirectory', UCHAR),
    ('DeleteOnClose', UCHAR),
    ('DokanOptions', PDOKAN_OPTIONS),
]
PDOKAN_FILE_INFO = POINTER(_DOKAN_FILE_INFO)
DOKAN_FILE_INFO = _DOKAN_FILE_INFO
PFillFindData = WINFUNCTYPE(c_int, PWIN32_FIND_DATAW, PDOKAN_FILE_INFO)
class _DOKAN_OPERATIONS(Structure):
    pass
_DOKAN_OPERATIONS._fields_ = [
    ('CreateFile', WINFUNCTYPE(c_int, LPCWSTR, DWORD, DWORD, DWORD, DWORD, PDOKAN_FILE_INFO)),
    ('OpenDirectory', WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
    ('CreateDirectory', WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
    ('Cleanup', WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
    ('CloseFile', WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
    ('ReadFile', WINFUNCTYPE(c_int, LPCWSTR, LPVOID, DWORD, LPVOID, LONGLONG, PDOKAN_FILE_INFO)),
    #PMPP('WriteFile', WINFUNCTYPE(c_int, LPCWSTR, LPCVOID, DWORD, LPDWORD, LONGLONG, PDOKAN_FILE_INFO)),
    ('WriteFile', WINFUNCTYPE(c_int, LPCWSTR, LPCVOID, DWORD, LPDWORD, LONGLONG, PDOKAN_FILE_INFO)),
    ('FlushFileBuffers', WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
    ('GetFileInformation', WINFUNCTYPE(c_int, LPCWSTR, LPBY_HANDLE_FILE_INFORMATION, PDOKAN_FILE_INFO)),
    ('FindFiles', WINFUNCTYPE(c_int, LPCWSTR, PFillFindData, PDOKAN_FILE_INFO)),
    ('FindFilesWithPattern', WINFUNCTYPE(c_int, LPCWSTR, LPCWSTR, PFillFindData, PDOKAN_FILE_INFO)),
    ('SetFileAttributes', WINFUNCTYPE(c_int, LPCWSTR, DWORD, PDOKAN_FILE_INFO)),
    ('SetFileTime', WINFUNCTYPE(c_int, LPCWSTR, POINTER(FILETIME), POINTER(FILETIME), POINTER(FILETIME), PDOKAN_FILE_INFO)),
    ('DeleteFile', WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
    ('DeleteDirectory', WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
    ('MoveFile', WINFUNCTYPE(c_int, LPCWSTR, LPCWSTR, BOOL, PDOKAN_FILE_INFO)),
    ('SetEndOfFile', WINFUNCTYPE(c_int, LPCWSTR, LONGLONG, PDOKAN_FILE_INFO)),
    ('SetAllocationSize', WINFUNCTYPE(c_int, LPCWSTR, LONGLONG, PDOKAN_FILE_INFO)),
    ('LockFile', WINFUNCTYPE(c_int, LPCWSTR, LONGLONG, LONGLONG, PDOKAN_FILE_INFO)),
    ('UnlockFile', WINFUNCTYPE(c_int, LPCWSTR, LONGLONG, LONGLONG, PDOKAN_FILE_INFO)),
    ('GetDiskFreeSpace', WINFUNCTYPE(c_int, PULONGLONG, PULONGLONG, PULONGLONG, PDOKAN_FILE_INFO)),
    ('GetVolumeInformation', WINFUNCTYPE(c_int, LPWSTR, DWORD, LPDWORD, LPDWORD, LPDWORD, LPWSTR, DWORD, PDOKAN_FILE_INFO)),
    ('Unmount', WINFUNCTYPE(c_int, PDOKAN_FILE_INFO)),
    ('GetFileSecurity', WINFUNCTYPE(c_int, LPWSTR, LPVOID, LPVOID, PULONG, ULONG, PDOKAN_FILE_INFO)),
    ('SetFileSecurity', WINFUNCTYPE(c_int, LPWSTR, LPVOID, LPVOID, ULONG, PDOKAN_FILE_INFO)),
]
PDOKAN_OPERATIONS = POINTER(_DOKAN_OPERATIONS)
DOKAN_OPERATIONS = _DOKAN_OPERATIONS
__all__ = ['LONGLONG', 'LPWIN32_FIND_DATAW',
           '_BY_HANDLE_FILE_INFORMATION', 'PFillFindData', 'PDWORD',
           'FILETIME', 'PWIN32_FIND_DATAW', 'DOKAN_FILE_INFO',
           'PULONGLONG', 'DWORD', 'LPBOOL', '_FILETIME',
           '_WIN32_FIND_DATAW', 'LPBY_HANDLE_FILE_INFORMATION',
           'ULONG', 'PWCHAR', '_DOKAN_FILE_INFO', 'ULONG64',
           'BY_HANDLE_FILE_INFORMATION', '_DOKAN_OPERATIONS',
           'PUCHAR', 'PFILETIME', 'PDOKAN_OPTIONS',
           'WIN32_FIND_DATAW', 'PBOOL', 'UCHAR', 'LPCVOID', 'LPCWSTR',
           'PDOKAN_OPERATIONS', 'DOKAN_OPTIONS', 'LPWSTR', 'INT64',
           'PDOKAN_FILE_INFO', 'PWSTR', 'DOKAN_OPERATIONS', 'USHORT',
           'LPVOID', 'LPDWORD', 'BOOL', 'PULONG', 'WCHAR',
           '_DOKAN_OPTIONS']
