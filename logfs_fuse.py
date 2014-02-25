#!/usr/bin/python
# -*- coding:utf8 -*-

import stat
import errno
import fuse
import logging
import logfs

LOG_FILENAME = "LOG"
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG,)

DIRSIZE = 4096


class LogFileSystem(fuse.Fuse):
    def __init__(self, *args, ** kwargs):
        super(LogFileSystem, self).__init__(*args, **kwargs)
        self.files = {}

    def fsinit(self):
        logging.debug("fsinit")
        self.fs = logfs.LogFS('fslog', 'fsstruct')
        self.files = self.fs.read_files()

    def fsdestroy(self):
        logging.debug("fsdestroy")
        self.fs.write_files(self.files)

    def getattr(self, path):
        logging.debug("getattr %s" % (path))
        if path == "/":
            mode = stat.S_IFDIR | 0755
            ctx = fuse.FuseGetContext()
            st = fuse.Stat(st_mode=mode, st_size=4096, st_nlink=2,
                           st_uid=ctx['uid'], st_gid=ctx['gid'])
        elif path in self.files:
            offset = self.files[path].meta_offset
            length = self.files[path].meta_length
            st = self.fs.read_meta(offset, length)
        else:
            return -errno.ENOENT
        return st

    def truncate(self, path, size):
        logging.debug("truncate %s, %d" % (path, size))
        if path in self.files:
            ptr = self.files[path]
            st = self.fs.read_meta(ptr.meta_offset, ptr.meta_length)
            st.st_size = 0
            ptr.meta_offset, ptr.meta_length = self.fs.write_meta(st)
        return -errno.ENOENT

    def access(self, path, mode):
        logging.debug("access %s, %d" % (path, mode))
        return -errno.ENOSYS

    def readdir(self, path, offset):
        logging.debug("readdir %s, %d" % (path, offset))
        for entry in ('.', '..'):
            yield fuse.Direntry(entry)
        for entry in self.files:
            yield fuse.Direntry(entry[1:])

    def opendir(self, path):
        logging.debug("opendir: %s" % path)
        if path == '/':
            return 0
        else:
            return -errno.EACCES

    def open(self, path, flags):
        logging.debug("open %s, %s" % (path, hex(flags)))
        return None

    def write(self, path, buf, offset):
        logging.debug("write %s, %s, %d" % (path, buf, offset))
        if path in self.files:
            logging.debug(path)
            ptr = self.files[path]
            logging.debug("%d %d %d %d", ptr.meta_offset, ptr.meta_length,
                          ptr.data_offset, ptr.data_length)
            ptr.data_offset, ptr.data_length = self.fs.write_data(buf)
            logging.debug("%d %d %d %d", ptr.meta_offset, ptr.meta_length,
                          ptr.data_offset, ptr.data_length)
            st = self.fs.read_meta(ptr.meta_offset, ptr.meta_length)
            st.st_size = len(buf)
            ptr.meta_offset, ptr.meta_length = self.fs.write_meta(st)
            logging.debug("%d %d %d %d", ptr.meta_offset, ptr.meta_length,
                          ptr.data_offset, ptr.data_length)
            return st.st_size
        return -errno.ENOENT

    def read(self, path, size, offset):
        logging.debug("read %s, %d, %d" % (path, size, offset))
        if path in self.files:
            data = self.fs.read_data(self.files[path].data_offset,
                                     self.files[path].data_length)
            return data
        return -errno.ENOENT

    def mknod(self, path, mode, rdev):
        logging.debug("mknod: %s (mode %s, rdev %s)" % (path, oct(mode), rdev))
        ctx = fuse.FuseGetContext()
        st = fuse.Stat(st_mode=mode, st_nlink=1, st_size=0, st_uid=ctx['uid'],
                       st_gid=ctx['gid'])
        off, l = self.fs.write_meta(st)
        ptr = logfs.LogFSPointer(off, l, 0, 0)
        self.files[path] = ptr
        return 0


if __name__ == '__main__':
    fuse.fuse_python_api = (0, 2)
    server = LogFileSystem(version='%prog ' + fuse.__version__,
                           usage='',
                           dash_s_do='setsingle')
    server.parse(errex=1)
    server.main()
