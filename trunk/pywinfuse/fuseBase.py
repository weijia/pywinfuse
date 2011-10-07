
import os
import sys

from ctypes import *
from dokan import *

from fuseparts.subbedopts import SubOptsHive, SubbedOptFormatter
from fuseparts.subbedopts import SubbedOptIndentedFormatter, SubbedOptParse
from fuseparts.subbedopts import SUPPRESS_HELP, OptParseError
from fuseparts.setcompatwrap import set

CreateFileFuncType = WINFUNCTYPE(c_int, LPCWSTR, DWORD, DWORD, DWORD, DWORD, PDOKAN_FILE_INFO)
OpenDirectoryFuncType = WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)
CreateDirectoryFuncType = WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)
CleanupFuncType = WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)
CloseFileFuncType = WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)
ReadFileFuncType = WINFUNCTYPE(c_int, LPCWSTR, LPVOID, DWORD, LPVOID, LONGLONG, PDOKAN_FILE_INFO)
WriteFileFuncType = WINFUNCTYPE(c_int, LPCWSTR, LPCVOID, DWORD, LPVOID, LONGLONG, PDOKAN_FILE_INFO)
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
SetAllocationSizeFuncType = WINFUNCTYPE(c_int, LPCWSTR, LONGLONG, PDOKAN_FILE_INFO)
LockFileFuncType = WINFUNCTYPE(c_int, LPCWSTR, LONGLONG, LONGLONG, PDOKAN_FILE_INFO)
UnlockFileFuncType = WINFUNCTYPE(c_int, LPCWSTR, LONGLONG, LONGLONG, PDOKAN_FILE_INFO)
GetDiskFreeSpaceFuncType = WINFUNCTYPE(c_int, PULONGLONG, PULONGLONG, PULONGLONG, PDOKAN_FILE_INFO)
GetVolumeInformationFuncType = WINFUNCTYPE(c_int, LPWSTR, DWORD, LPDWORD, LPDWORD, LPDWORD, LPWSTR, DWORD, PDOKAN_FILE_INFO)
UnmountFuncType = WINFUNCTYPE(c_int, PDOKAN_FILE_INFO)
GetFileSecurityFuncType = WINFUNCTYPE(c_int, LPWSTR, LPVOID, LPVOID, PULONG, ULONG, PDOKAN_FILE_INFO)
SetFileSecurityFuncType = WINFUNCTYPE(c_int, LPWSTR, LPVOID, LPVOID, ULONG, PDOKAN_FILE_INFO)

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


##########
###
###  Parsing for FUSE.
###
###  Code imported from http://fuse.sourceforge.net/
###
##########


class FuseArgs(SubOptsHive):
    """
    Class representing a FUSE command line.
    """

    fuse_modifiers = {'showhelp': '-ho',
                      'showversion': '-V',
                      'foreground': '-f'}

    def __init__(self):

        SubOptsHive.__init__(self)

        self.modifiers = {}
        self.mountpoint = None

        for m in self.fuse_modifiers:
            self.modifiers[m] = False

    def __str__(self):
        return '\n'.join(['< on ' + str(self.mountpoint) + ':',
                          '  ' + str(self.modifiers), '  -o ']) + \
               ',\n     '.join(self._str_core()) + \
               ' >'

    def getmod(self, mod):
        return self.modifiers[mod]

    def setmod(self, mod):
        self.modifiers[mod] = True

    def unsetmod(self, mod):
        self.modifiers[mod] = False

    def mount_expected(self):
        if self.getmod('showhelp'):
            return False
        if self.getmod('showversion'):
            return False
        return True

    def assemble(self):
        """Mangle self into an argument array"""

        self.canonify()
        args = [sys.argv and sys.argv[0] or "python"]
        if self.mountpoint:
            args.append(self.mountpoint)
        for m, v in self.modifiers.iteritems():
            if v:
                args.append(self.fuse_modifiers[m])

        opta = []
        for o, v in self.optdict.iteritems():
                opta.append(o + '=' + v)
        opta.extend(self.optlist)

        if opta:
            args.append("-o" + ",".join(opta))

        return args


class FuseFormatter(SubbedOptIndentedFormatter):

    def __init__(self, **kw):
        if not 'indent_increment' in kw:
            kw['indent_increment'] = 4
        SubbedOptIndentedFormatter.__init__(self, **kw)

    def store_option_strings(self, parser):
        SubbedOptIndentedFormatter.store_option_strings(self, parser)
        # 27 is how the lib stock help appears
        self.help_position = max(self.help_position, 27)
        self.help_width = self.width - self.help_position


class FuseOptParse(SubbedOptParse):
    """
    This class alters / enhances `SubbedOptParse` so that it's
    suitable for usage with FUSE.

    - When adding options, you can use the `mountopt` pseudo-attribute which
      is equivalent with adding a subopt for option ``-o``
      (it doesn't require an option argument).

    - FUSE compatible help and version printing.

    - Error and exit callbacks are relaxed. In case of FUSE, the command
      line is to be treated as a DSL [#]_. You don't wanna this module to
      force an exit on you just because you hit a DSL syntax error.

    - Built-in support for conventional FUSE options (``-d``, ``-f`, ``-s``).
      The way of this can be tuned by keyword arguments, see below.

    .. [#] http://en.wikipedia.org/wiki/Domain-specific_programming_language

    Keyword arguments for initialization
    ------------------------------------

    standard_mods
      Boolean [default is `True`].
      Enables support for the usual interpretation of the ``-d``, ``-f``
      options.

    fetch_mp
      Boolean [default is `True`].
      If it's True, then the last (non-option) argument
      (if there is such a thing) will be used as the FUSE mountpoint.

    dash_s_do
      String: ``whine``, ``undef``, or ``setsingle`` [default is ``whine``].
      The ``-s`` option -- traditionally for asking for single-threadedness --
      is an oddball: single/multi threadedness of a fuse-py fs doesn't depend
      on the FUSE command line, we have direct control over it.

      Therefore we have two conflicting principles:

      - *Orthogonality*: option parsing shouldn't affect the backing `Fuse`
        instance directly, only via its `fuse_args` attribute.

      - *POLS*: behave like other FUSE based fs-es do. The stock FUSE help
        makes mention of ``-s`` as a single-threadedness setter.

      So, if we follow POLS and implement a conventional ``-s`` option, then
      we have to go beyond the `fuse_args` attribute and set the respective
      Fuse attribute directly, hence violating orthogonality.

      We let the fs authors make their choice: ``dash_s_do=undef`` leaves this
      option unhandled, and the fs author can add a handler as she desires.
      ``dash_s_do=setsingle`` enables the traditional behaviour.

      Using ``dash_s_do=setsingle`` is not problematic at all, but we want fs
      authors be aware of the particularity of ``-s``, therefore the default is
      the ``dash_s_do=whine`` setting which raises an exception for ``-s`` and
      suggests the user to read this documentation.

    dash_o_handler
      Argument should be a SubbedOpt instance (created with
      ``action="store_hive"`` if you want it to be useful).
      This lets you customize the handler of the ``-o`` option. For example,
      you can alter or suppress the generic ``-o`` entry in help output.
    """

    def __init__(self, *args, **kw):

        self.mountopts = []

        self.fuse_args = \
            'fuse_args' in kw and kw.pop('fuse_args') or FuseArgs()
        dsd = 'dash_s_do' in kw and kw.pop('dash_s_do') or 'whine'
        if 'fetch_mp' in kw:
            self.fetch_mp = bool(kw.pop('fetch_mp'))
        else:
            self.fetch_mp = True
        if 'standard_mods' in kw:
            smods = bool(kw.pop('standard_mods'))
        else:
            smods = True
        if 'fuse' in kw:
            self.fuse = kw.pop('fuse')
        if not 'formatter' in kw:
            kw['formatter'] = FuseFormatter()
        doh = 'dash_o_handler' in kw and kw.pop('dash_o_handler')

        SubbedOptParse.__init__(self, *args, **kw)

        if doh:
            self.add_option(doh)
        else:
            self.add_option('-o', action='store_hive',
                            subopts_hive=self.fuse_args, help="mount options",
                            metavar="opt,[opt...]")

        if smods:
            self.add_option('-f', action='callback',
                            callback=lambda *a: self.fuse_args.setmod('foreground'),
                            help=SUPPRESS_HELP)
            self.add_option('-d', action='callback',
                            callback=lambda *a: self.fuse_args.add('debug'),
                            help=SUPPRESS_HELP)

        if dsd == 'whine':
            def dsdcb(option, opt_str, value, parser):
                raise RuntimeError, """

! If you want the "-s" option to work, pass
!
!   dash_s_do='setsingle'
!
! to the Fuse constructor. See docstring of the FuseOptParse class for an
! explanation why is it not set by default.
"""

        elif dsd == 'setsingle':
            def dsdcb(option, opt_str, value, parser):
                self.fuse.multithreaded = False

        elif dsd == 'undef':
            dsdcb = None
        else:
            raise ArgumentError, "key `dash_s_do': uninterpreted value " + str(dsd)

        if dsdcb:
            self.add_option('-s', action='callback', callback=dsdcb,
                            help=SUPPRESS_HELP)


    def exit(self, status=0, msg=None):
        if msg:
            sys.stderr.write(msg)

    def error(self, msg):
        SubbedOptParse.error(self, msg)
        raise OptParseError, msg

    def print_help(self, file=sys.stderr):
        SubbedOptParse.print_help(self, file)
        print >> file
        self.fuse_args.setmod('showhelp')

    def print_version(self, file=sys.stderr):
        SubbedOptParse.print_version(self, file)
        self.fuse_args.setmod('showversion')

    def parse_args(self, args=None, values=None):
        o, a = SubbedOptParse.parse_args(self, args, values)
        if a and self.fetch_mp:
            self.fuse_args.mountpoint = os.path.realpath(a.pop())
        return o, a

    def add_option(self, *opts, **attrs):
        if 'mountopt' in attrs:
            if opts or 'subopt' in attrs:
                raise OptParseError(
                  "having options or specifying the `subopt' attribute conflicts with `mountopt' attribute")
            opts = ('-o',)
            attrs['subopt'] = attrs.pop('mountopt')
            if not 'dest' in attrs:
                attrs['dest'] = attrs['subopt']

        SubbedOptParse.add_option(self, *opts, **attrs)


class Direntry:
    def __init__(self, name):
        self.name = name
    def getName(self):
        return self.name
        #return unicode(self.name).encode('utf-8')
        return self.name.replace('/','\\')

class fuseOptDict:
    def __init__(self):
        pass
    def copy(self):
        pass
        
fuse_python_api = None

class fuseBase:
    fusage = 'no usage currently'
    def __init__(self, usage = '', dash_s_do = '', version = '', debug = 0):
        #The following is used to be compitable with Linux Fuse Python binding
        self.flags = 0
        self.multithreaded = 0
        self.allow_other = 0
        self.optdict = fuseOptDict()
        self.fuse_args = FuseArgs()
        self.parser = FuseOptParse()
        if debug != 1:
            self.debug = c_ubyte(0)
        else:
            self.debug = c_ubyte(1)

    def parse(self, *args, **kw):
        """Parse command line, fill `fuse_args` attribute."""

        ev = 'errex' in kw and kw.pop('errex')
        if ev and not isinstance(ev, int):
            raise TypeError, "error exit value should be an integer"

        try:
            self.cmdline = self.parser.parse_args(*args, **kw)
        except OptParseError:
          if ev:
              sys.exit(ev)
          raise

        return self.fuse_args

    def GetContext(self):
        # os.lstat always return 0 as uid and gid on windows.
        return { 'pid' : os.getpid(), 'uid' : 0, 'gid' : 0 }

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
        return 0# WINFUNCTYPE(c_int, LPCWSTR, LPCVOID, DWORD, LPVOID, LONGLONG, PDOKAN_FILE_INFO)),
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
    def SetAllocationSizeFunc(self, pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
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
    def GetFileSecurityFunc(self, pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
        return 0# WINFUNCTYPE(c_int, PDOKAN_FILE_INFO)),
    def SetFileSecurityFunc(self, pInfo, a='',b='',c='',d='',e='',f='',g='',i='',j='',k=''): 
        return 0# WINFUNCTYPE(c_int, PDOKAN_FILE_INFO)),


    def main(self, args=None):
        if not self.fuse_args.mountpoint:
            self.fuse_args.mountpoint = u"K"

        print windll.dokan
        operation = _DOKAN_OPERATIONS(
            CreateFileFuncType(self.CreateFileFunc),# WINFUNCTYPE(c_int, LPCWSTR, DWORD, DWORD, DWORD, DWORD, PDOKAN_FILE_INFO)),
            OpenDirectoryFuncType(self.OpenDirectoryFunc),# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
            CreateDirectoryFuncType(self.CreateDirectoryFunc),# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
            CleanupFuncType(self.CleanupFunc),# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
            CloseFileFuncType(self.CloseFileFunc),# WINFUNCTYPE(c_int, LPCWSTR, PDOKAN_FILE_INFO)),
            ReadFileFuncType(self.ReadFileFunc),# WINFUNCTYPE(c_int, LPCWSTR, LPVOID, DWORD, LPDWORD, LONGLONG, PDOKAN_FILE_INFO)),
            WriteFileFuncType(self.WriteFileFunc),# WINFUNCTYPE(c_int, LPCWSTR, LPCVOID, DWORD, LPVOID, LONGLONG, PDOKAN_FILE_INFO)),
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
            SetAllocationSizeFuncType(self.SetAllocationSizeFunc),# WINFUNCTYPE(c_int, LPCWSTR, LONGLONG, PDOKAN_FILE_INFO)),
            LockFileFuncType(self.LockFileFunc),# WINFUNCTYPE(c_int, LPCWSTR, LONGLONG, LONGLONG, PDOKAN_FILE_INFO)),
            UnlockFileFuncType(self.UnlockFileFunc),# WINFUNCTYPE(c_int, LPCWSTR, LONGLONG, LONGLONG, PDOKAN_FILE_INFO)),
            GetDiskFreeSpaceFuncType(self.GetDiskFreeSpaceFunc),# WINFUNCTYPE(c_int, PULONGLONG, PULONGLONG, PULONGLONG, PDOKAN_FILE_INFO)),
            GetVolumeInformationFuncType(self.GetVolumeInformationFunc),# WINFUNCTYPE(c_int, LPWSTR, DWORD, LPDWORD, LPDWORD, LPDWORD, LPWSTR, DWORD, PDOKAN_FILE_INFO)),
            UnmountFuncType(self.UnmountFunc),# WINFUNCTYPE(c_int, PDOKAN_FILE_INFO)),
            GetFileSecurityFuncType(self.GetFileSecurityFunc),
            SetFileSecurityFuncType(self.SetFileSecurityFunc),
        )
        option = _DOKAN_OPTIONS(
            600,#('Version', USHORT),
            1,#('ThreadCount', USHORT),
            0,#('Options', ULONG),
            0,#('GlobalContext', ULONG64),
            self.fuse_args.mountpoint,#('MountPoint', LPCWSTR),
        )
        #from ctypesTest import *
        #dumpMem(addressof(self.debug), 4)
        #dumpMem(option, 15)
        
        windll.dokan.DokanMain(byref(option),byref(operation))


