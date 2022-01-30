# from pywinfuse import *
from ctypes import *

# from myLogger import *
import inspect
import stat
import errno
import os
import re

from dokan import *
from tools import *
from fuseBase import *
from fuseOpen import *
from fuseUnlink import *
from fuse_debug import *
import logging
import myWin32file

__version__ = '0.1'


def feature_assert(section, feature):
    return True


@property
def FUSE_PYTHON_API_VERSION():
    return __version__.split('.')


def log(a='', b='', c='', d='', e='', f='', g='', h='', ):
    print(whosdaddy(), a, b, c, d, e)


def dbg(*args):
    return
    print(whosdaddy())
    logStr = ''
    for i in args:
        logStr += str(i)
    print(logStr)


def cre(CreationDisposition):
    if CreationDisposition == myWin32file.CREATE_ALWAYS:
        print('return 183')
        return myWin32file.ERROR_ALREADY_EXISTS
    if CreationDisposition == myWin32file.OPEN_ALWAYS:
        print(myWin32file.ERROR_ALREADY_EXISTS)
        return myWin32file.ERROR_ALREADY_EXISTS
    return 0


class Fuse(openSupport, unlinkSupport, writeSupport, fuseBase):
    def translateFileName(self, FileName):
        return FileName.replace('\\', '/')

    def OpenDirectoryFunc(self, FileName, pInfo):
        # dbgP(FileName, pInfo)
        unixFilename = FileName.replace('\\', '/')
        st = self.getattrWrapper(unixFilename)
        if st != -errno.ENOENT:
            return 0
        else:
            return -myWin32file.ERROR_FILE_NOT_FOUND

    def CleanupFunc(self, pInfo, a='', b='', c='', d='', e='', f='', g='', i='', j='', k=''):
        dbg()
        return 0  # WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),

    def release(self, path, flags):
        print('*** release', path, flags)
        return -errno.ENOSYS

    def CloseFileFunc(self, FileName, pInfo):
        dbg()
        unixFilename = FileName.replace('\\', '/')

        if self.checkError(self.getattrWrapper(unixFilename)) != 0:
            return -myWin32file.ERROR_FILE_NOT_FOUND

        return self.checkError(self.release_wrapper(unixFilename, pInfo))

    def ReadFileFunc(self, FileName, Buffer, NumberOfBytesToRead, NumberOfBytesRead, Offset, pInfo):
        dbgP(FileName, Buffer, NumberOfBytesToRead, NumberOfBytesRead, Offset, pInfo)
        # Why the directory is read?
        # Todo: find why, now, check if it is dir first
        unixFilename = FileName.replace('\\', '/')
        if self.getattr(unixFilename).st_mode & stat.S_IFDIR:
            return -myWin32file.ERROR_FILE_NOT_FOUND
        data = self.read_wrapper(unixFilename, NumberOfBytesToRead, Offset, pInfo)
        if data == -errno.ENOENT:
            print('data not exist', FileName)
            return -myWin32file.ERROR_FILE_NOT_FOUND
        if data == '':
            print('end of data')
            return -1
        length = len(data)
        memmove(Buffer, data, length)
        setDwordByPoint(NumberOfBytesRead, length)
        # NumberOfBytesRead = DWORD(length)
        return 0  # WINFUNCTYPE(c_int, LPCWSTR, LPVOID, DWORD, LPDWORD, LONGLONG, PDOKAN_FILE_INFO)),

    def FlushFileBuffersFunc(self, pInfo, a='', b='', c='', d='', e='', f='', g='', i='', j='', k=''):
        dbg()
        return 0  # WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),

    def translateModeFromUnix(self, st):
        if st.st_mode & stat.S_IFDIR:
            # This element is a directory, set the correct attribute
            return myWin32file.FILE_ATTRIBUTE_DIRECTORY  # 16
        else:
            return myWin32file.FILE_ATTRIBUTE_ARCHIVE  # 32

    def GetFileInformationFunc(self, FileName, Buffer, pInfo):
        # log(FileName, Buffer, pInfo)
        unixFilename = FileName.replace('\\', '/')
        st = self.getattrWrapper(unixFilename)

        if st != -errno.ENOENT:
            '''
      Buffer = BY_HANDLE_FILE_INFORMATION(
        self.translateModeFromUnix(st),#('dwFileAttributes', DWORD),
        FILETIME(0,0),#('ftCreationTime', FILETIME),2 DWORD
        FILETIME(0,0),#('ftLastAccessTime', FILETIME),
        FILETIME(0,0),#('ftLastWriteTime', FILETIME),
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
            # Some quick hack of setting ctypes
            setDwordByPoint(Buffer, self.translateModeFromUnix(st))
            setDwordByPoint(Buffer + 32, st.st_size >> 32)  # ('nFileSizeHigh', DWORD),
            setDwordByPoint(Buffer + 36, st.st_size & 0xffffffff)  # ('nFileSizeLow', DWORD),
            setDwordByPoint(Buffer + 40, 1)
            # Function always return 0 when success
            # print 'success'
            return 0
        else:
            print('returning -2')
            return -2
        return 0  # WINFUNCTYPE(c_int, LPCWSTR, LPBY_HANDLE_FILE_INFORMATION, PDOKAN_FILE_INFO)),

    def FindFilesFunc(self, PathName, PFillFindData, pInfo):
        print('finding files in: %s' % PathName)
        unixFilename = PathName.replace('\\', '/')
        offset = 0
        Buffer = BY_HANDLE_FILE_INFORMATION(
            0,  # ('dwFileAttributes', DWORD),
            FILETIME(0, 0),  # ('ftCreationTime', FILETIME),
            FILETIME(0, 0),  # ('ftLastAccessTime', FILETIME),
            FILETIME(0, 0),  # ('ftLastWriteTime', FILETIME),
            0,  # ('dwVolumeSerialNumber', DWORD),
            0,  # ('nFileSizeHigh', DWORD),
            0,  # ('nFileSizeLow', DWORD),
            0,  # ('nNumberOfLinks', DWORD),
            0,  # ('nFileIndexHigh', DWORD),
            0  # ('nFileIndexLow', DWORD),
        )
        for entry in self.readdir(unixFilename, offset):
            # entry = self.readdir(unixFilename, offset)
            # if entry == None:
            #  break
            if (entry.getName() == '.') or (entry.getName() == '..'):
                # print 'continue'
                continue
            finalPath = os.path.join(PathName, entry.getName())
            # print 'finalPath',finalPath
            unixFinal = finalPath.replace('\\', '/')
            st = self.getattrWrapper(unixFinal)
            if st != -errno.ENOENT:
                Buffer.dwFileAttributes = self.translateModeFromUnix(st)
                Buffer.nFileSizeLow = st.st_size
                # print 'attr',Buffer.dwFileAttributes
                # print 'size',Buffer.nFileSizeLow
            else:
                continue
            # print 'Buffer.nFileSizeLow', Buffer.nFileSizeLow
            he = WIN32_FIND_DATAW(
                Buffer.dwFileAttributes,  # ('dwFileAttributes', DWORD),#0
                FILETIME(0, 0),  # ('ftCreationTime', FILETIME),#4
                FILETIME(0, 0),  # ('ftLastAccessTime', FILETIME),#12
                FILETIME(0, 0),  # ('ftLastWriteTime', FILETIME),#20
                0,  # ('nFileSizeHigh', DWORD),#28
                Buffer.nFileSizeLow,  # ('nFileSizeLow', DWORD),#32
                0,  # ('dwReserved0', DWORD),#36
                0,  # ('dwReserved1', DWORD),#40
                'a.txt',
                # entry.getName(),#('cFileName', WCHAR * 260),#This can only be const string!!! if getName function called here, the result is not correct.
                '')  # ('cAlternateFileName', WCHAR * 14),)
            # print '---------------------',string_at(addressof(he)+44)
            # print '---------------------',string_at(addressof(he)+46)
            # memmove(addressof(he)+44, byref(c_char_p(u'a.txt')), len(entry.getName()))
            # print addressof(he)
            # setStringByPoint(addressof(he)+44, entry.getName(), 2*len(entry.getName())
            setStringByPoint(addressof(he) + 44, unicode(entry.getName()), myWin32file.MAX_PATH)
            # print addressof(he)
            # print '---------------------',string_at(addressof(he)+44)
            # print '---------------------name',he.cFileName
            PFillFindData(pointer(he), pInfo)
        return 0  # WINFUNCTYPE(c_int, LPCWSTR, PFillFindData, PDOKAN_FILE_INFO)),

    def FindFilesWithPatternFunc(self, PathName, SearchPattern, PFillFindData, pInfo):
        # print 'finding files in: %s'%PathName
        unixFilename = PathName.replace('\\', '/')
        offset = 0
        Buffer = BY_HANDLE_FILE_INFORMATION(
            0,  # ('dwFileAttributes', DWORD),
            FILETIME(0, 0),  # ('ftCreationTime', FILETIME),
            FILETIME(0, 0),  # ('ftLastAccessTime', FILETIME),
            FILETIME(0, 0),  # ('ftLastWriteTime', FILETIME),
            0,  # ('dwVolumeSerialNumber', DWORD),
            0,  # ('nFileSizeHigh', DWORD),
            0,  # ('nFileSizeLow', DWORD),
            0,  # ('nNumberOfLinks', DWORD),
            0,  # ('nFileIndexHigh', DWORD),
            0  # ('nFileIndexLow', DWORD),
        )

        for entry in self.readdir(unixFilename, offset):
            # entry = self.readdir(unixFilename, offset)
            # if entry == None:
            #  break
            if (entry.getName() == '.') or (entry.getName() == '..'):
                # print 'continue'
                continue
            regPat = SearchPattern.replace('*', '.*').replace('\\', '\\\\')
            if re.match(regPat, entry.getName()) == None:
                # print 'ignore %s'%entry.getName()
                continue
            finalPath = os.path.join(PathName, entry.getName())
            # print 'finalPath',finalPath
            unixFinal = finalPath.replace('\\', '/')

            st = self.getattrWrapper(unixFinal)
            if st != -errno.ENOENT:
                Buffer.dwFileAttributes = self.translateModeFromUnix(st)
                Buffer.nFileSizeLow = st.st_size
                # print 'attr',Buffer.dwFileAttributes
                # print 'size',Buffer.nFileSizeLow
            else:
                continue
            # print 'Buffer.nFileSizeLow', Buffer.nFileSizeLow
            he = WIN32_FIND_DATAW(
                Buffer.dwFileAttributes,  # ('dwFileAttributes', DWORD),#0
                FILETIME(0, 0),  # ('ftCreationTime', FILETIME),#4
                FILETIME(0, 0),  # ('ftLastAccessTime', FILETIME),#12
                FILETIME(0, 0),  # ('ftLastWriteTime', FILETIME),#20
                0,  # ('nFileSizeHigh', DWORD),#28
                Buffer.nFileSizeLow,  # ('nFileSizeLow', DWORD),#32
                0,  # ('dwReserved0', DWORD),#36
                0,  # ('dwReserved1', DWORD),#40
                'a.txt',
                # entry.getName(),#('cFileName', WCHAR * 260),#This can only be const string!!! if getName function called here, the result is not correct.
                '')  # ('cAlternateFileName', WCHAR * 14),)
            # print '---------------------',string_at(addressof(he)+44)
            # print '---------------------',string_at(addressof(he)+46)
            # memmove(addressof(he)+44, byref(c_char_p(u'a.txt')), len(entry.getName()))
            # print addressof(he)
            # setStringByPoint(addressof(he)+44, entry.getName(), 2*len(entry.getName())
            setStringByPoint(addressof(he) + 44, entry.getName(), myWin32file.MAX_PATH)
            # print addressof(he)
            # print '---------------------',string_at(addressof(he)+44)
            # print '---------------------name',he.cFileName
            PFillFindData(pointer(he), pInfo)
        return 0  # WINFUNCTYPE(c_int, LPCWSTR, PFillFindData, PDOKAN_FILE_INFO)),

    def SetFileAttributesFunc(self, pInfo, a='', b='', c='', d='', e='', f='', g='', i='', j='', k=''):
        dbg()
        return 0  # WINFUNCTYPE(c_int, LPCWSTR, DWORD, PDOKAN_FILE_INFO)),

    def SetFileTimeFunc(self, pInfo, a='', b='', c='', d='', e='', f='', g='', i='', j='', k=''):
        dbg()
        return 0  # WINFUNCTYPE(c_int, LPCWSTR, POINTER(FILETIME), POINTER(FILETIME), POINTER(FILETIME), PDOKAN_FILE_INFO)),

    def LockFileFunc(self, pInfo, a='', b='', c='', d='', e='', f='', g='', i='', j='', k=''):
        dbg()
        return 0  # WINFUNCTYPE(c_int, LPCWSTR, LONGLONG, LONGLONG, PDOKAN_FILE_INFO)),

    def UnlockFileFunc(self, pInfo, a='', b='', c='', d='', e='', f='', g='', i='', j='', k=''):
        dbg()
        return 0  # WINFUNCTYPE(c_int, LPCWSTR, LONGLONG, LONGLONG, PDOKAN_FILE_INFO)),

    def GetDiskFreeSpaceFunc(self, pFreeBytesAvailable, pTotalNumberOfBytes, pTotalNumberOfFreeBytes, pInfo):
        try:
            vfs = self.statfs()
            FreeBytesAvailable = vfs.f_bfree * vfs.f_bsize
            TotalNumberOfBytes = vfs.f_blocks * vfs.f_bsize
            TotalNumberOfFreeBytes = vfs.f_bfree * vfs.f_bsize

        except Exception as e:
            print(e)
            FreeBytesAvailable = 0x1000000000000
            TotalNumberOfBytes = 0x4000000000000  # 256M=256*1024*1024
            TotalNumberOfFreeBytes = 0x1000000000000

        setLongLongByPoint(pFreeBytesAvailable, FreeBytesAvailable)
        setLongLongByPoint(pTotalNumberOfBytes, TotalNumberOfBytes)
        setLongLongByPoint(pTotalNumberOfFreeBytes, TotalNumberOfFreeBytes)
        return 0  # WINFUNCTYPE(c_int, PULONGLONG, PULONGLONG, PULONGLONG, PDOKAN_FILE_INFO)),

    def GetVolumeInformationFunc(self, VolumeNameBuffer, VolumeNameSize, VolumeSerialNumber,
                                 MaximumComponentLength, FileSystemFlags, FileSystemNameBuffer,
                                 FileSystemNameSize, pInfo):
        # log(VolumeNameBuffer, VolumeNameSize, VolumeSerialNumber,
        # MaximumComponentLength, FileSystemFlags, FileSystemNameBuffer, FileSystemNameSize, pInfo)
        fsname = self.fsname
        memmove(VolumeNameBuffer, fsname, 2 * (len(fsname) + 1))
        VolumeSerialNumber = 0
        MaximumComponentLength = 0
        FileSystemFlags = 0
        memmove(FileSystemNameBuffer, u'PyWinFuse', 2 * (len(u'PyWinFuse') + 1))
        return 0  # WINFUNCTYPE(c_int, LPWSTR, DWORD, LPDWORD, LPDWORD, LPDWORD, LPWSTR, DWORD, PDOKAN_FILE_INFO)),

    def UnmountFunc(self, pInfo, a='', b='', c='', d='', e='', f='', g='', i='', j='', k=''):
        dbg()
        return 0  # WINFUNCTYPE(c_int, PDOKAN_FILE_INFO)),

    def checkError(self, ret):
        print("ret type:", type(ret))
        if ret is None or isinstance(ret, Stat):
            print('returning 0')
            return 0
        else:
            # print('returned value:', ret)
            print(inspect.stack()[1][3])
            return -myWin32file.ERROR_FILE_NOT_FOUND
