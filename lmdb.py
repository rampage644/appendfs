#!/usr/bin/python
# -*- coding:utf8 -*-

import errno
import fuse
import logging

LOG_FILENAME = "LOG"
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO,)


class MyStat(fuse.Stat):
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


class LMDBFileSystem(fuse.Fuse):
    def __init__(self, *args, **kwargs):
        super(LMDBFileSystem, self).__init__(*args, **kwargs)

    def getattr(self, path):
        return -errno.ENOSYS

    def access(self, path, mode):
        return -errno.ENOSYS

    def readdir(self, path, offset):
        logging.info("readdir %s, %d" % (path, offset))
        yield fuse.Direntry('.')
        yield fuse.Direntry('..')

    def open(self, path, flags):
        logging.info("open %s, %d" % (path, flags))
        return -errno.ENOSYS

    def write(self, path, buf, offset):
        return -errno.ENOSYS

    def read(self, path, size, offset):
        return -errno.ENOSYS


if __name__ == '__main__':
    fuse.fuse_python_api = (0, 2)
    server = LMDBFileSystem()
    server.parse(errex=1)
    server.main()
