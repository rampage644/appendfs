#!/usr/bin/python
# -*- coding:utf8 -*-

import errno
import fuse
import logging

LOG_FILENAME = "LOG"
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG,)

DIRSIZE = 4096


class LogFileSystem(fuse.Fuse):

    def getattr(self, path):
        logging.debug("getattr %s" % (path))
        return -errno.ENOENT

    def truncate(self, path, size):
        logging.debug("truncate %s, %d" % (path, size))
        return -errno.ENOENT

    def access(self, path, mode):
        logging.debug("access %s, %d" % (path, mode))
        return -errno.ENOSYS

    def readdir(self, path, offset):
        logging.debug("readdir %s, %d" % (path, offset))
        for entry in ('.', '..'):
            yield fuse.Direntry(entry)

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
        return -errno.ENOENT

    def read(self, path, size, offset):
        logging.debug("read %s, %d, %d" % (path, size, offset))
        return -errno.ENOENT

    def mknod(self, path, mode, rdev):
        logging.debug("mknod: %s (mode %s, rdev %s)" % (path, oct(mode), rdev))
        return -errno.ENOSYS


if __name__ == '__main__':
    fuse.fuse_python_api = (0, 2)
    server = LogFileSystem(version='%prog ' + fuse.__version__,
                           usage='',
                           dash_s_do='setsingle')
    server.parse(errex=1)
    server.main()
