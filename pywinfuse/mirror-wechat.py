#!/usr/bin/env python

#    Copyright (C) 2006  Andrew Straw  <strawman@astraw.com>
#
#    This program can be distributed under the terms of the GNU LGPL.
#    See the file COPYING.
#

import errno
import os
import stat
from mirror import MirrorFs
from itertools import cycle

# pull in some spaghetti to make this stuff work without fuse-py being installed
try:
    import _find_fuse_parts
except ImportError:
    pass
import fuse
from fuse import Fuse

if not hasattr(fuse, '__version__'):
    raise RuntimeError("your fuse-py doesn't know of fuse.__version__, probably it's too old.")

fuse.fuse_python_api = (0, 2)


class WeChatMirrorFs(MirrorFs):
    BASE_PATH = "D:"
    DECRYPT_KEY = None
    PIC_HEAD = [0xff, 0xd8, 0x89, 0x50, 0x47, 0x49]

    def translate_path(self, path):
        # print 'get path', path
        real_path = os.path.join(self.BASE_PATH, path)
        # print real_path
        return real_path

    def readdir(self, path, offset):
        # yield fuse.Direntry('a.txt')
        for r in '.', '..':
            yield fuse.Direntry(r)
        for r in os.listdir(self.translate_path(path)):
            # print("listing:", path)
            yield fuse.Direntry(r)

    def open(self, path, flags):
        # print('calling open')
        if self.getattr(path) == -errno.ENOENT:
            return -errno.ENOENT
        accmode = os.O_RDONLY | os.O_WRONLY | os.O_RDWR
        if (flags & accmode) != os.O_RDONLY:
            return -errno.EACCES
        return 0

    def read(self, path, size, offset):
        # print("reading:", path, size, offset)
        if self.getattr(path) == -errno.ENOENT:
            return -errno.ENOENT
        # print 'open file:',self.getPath(path)
        f = open(self.translate_path(path), 'rb')
        if self.is_wechat_image(path):
            if self.DECRYPT_KEY is None:
                dat_read = f.read(2)
                self.try_to_get_decrypt_key(dat_read)
        f.seek(offset)
        buf = f.read(size)
        if self.is_wechat_image(path):
            print(type(buf), len(buf))
            buf = bytes(a ^ b for a, b in zip(buf, cycle([self.DECRYPT_KEY])))
            # print(type(bufx), len(bufx))
        f.close()
        # print 'read len:', len(buf)
        return buf

    def is_wechat_image(self, path):
        return "FileStorage" in path and "Image" in path

    def try_to_get_decrypt_key(self, dat_read):
        # https://zhuanlan.zhihu.com/p/130314175
        # 图片字节头信息，[0][1]为jpg头信息[2][3]为png头信息[4][5]为gif头信息
        pic_head = [0xff, 0xd8, 0x89, 0x50, 0x47, 0x49]
        head_index = 0
        while head_index < len(pic_head):
            # 使用第一个头信息字节来计算加密码
            # 第二个字节来验证解密码是否正确
            code = dat_read[0] ^ pic_head[head_index]
            idf_code = dat_read[1] ^ code
            head_index = head_index + 1
            if idf_code == pic_head[head_index]:
                self.DECRYPT_KEY = code
                print("found head:", head_index, self.DECRYPT_KEY)
                return
            head_index = head_index + 1
        print("not jpg, png, gif")
        return


def main():
    usage = """
Userspace hello example

""" + Fuse.fusage
    server = WeChatMirrorFs(version="%prog " + fuse.__version__,
                            usage=usage,
                            dash_s_do='setsingle', debug=0)

    server.parse(errex=1)
    server.main()


if __name__ == '__main__':
    main()
