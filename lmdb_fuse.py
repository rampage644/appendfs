#!/usr/bin/python
# -*- coding:utf8 -*-

import os
import stat
import errno
import fuse
import logging

import lmdbfs

LOG_FILENAME = "LOG"
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG,)

DIRSIZE = 4096


class LMDBStat(fuse.Stat):

    def __init__(self):
        self.st_mode = 0
        self.st_ino = 0
        self.st_dev = 0
        self.st_nlink = 0
        self.st_uid = os.getuid()
        self.st_gid = os.getgid()
        self.st_size = 0
        self.st_atime = 0
        self.st_mtime = 0
        self.st_ctime = 0


class LMDBFileSystem(fuse.Fuse):

    def __init__(self, *args, **kwargs):
        super(LMDBFileSystem, self).__init__(*args, **kwargs)

    def getattr(self, path):
        logging.debug("getattr %s" % (path))
        ret = LMDBStat()
        if path == '/':
            ret.st_mode = stat.S_IFDIR | 0755
            ret.st_nlink = 2
            ret.st_size = DIRSIZE
            return ret
        else:
            meta, _ = lmdbfs.read_file(path)
            if meta:
                return meta
            else:
                return -errno.ENOENT

    def truncate(self, path, size):
        logging.debug("truncate %s, %d" % (path, size))
        if lmdbfs.exists(path):
            st, data = lmdbfs.read_file(path)
            st.st_size = size
            data = data[:size]
            lmdbfs.write_file(path, st, data)
            return 0
        return -errno.ENOENT

    def access(self, path, mode):
        logging.debug("access %s, %d" % (path, mode))
        return -errno.ENOSYS

    def readdir(self, path, offset):
        logging.debug("readdir %s, %d" % (path, offset))
        for entry in ('.', '..'):
            yield fuse.Direntry(entry)
        for entry in lmdbfs.files(path):
            logging.debug("readdir %s" % (entry[1:]))
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
        if lmdbfs.exists(path):
            st, data = lmdbfs.read_file(path)
            st.st_size = len(buf)
            lmdbfs.write_file(path, st, buf)
            return len(buf)
        return -errno.ENOENT

    def read(self, path, size, offset):
        logging.debug("read %s, %d, %d" % (path, size, offset))
        if lmdbfs.exists(path):
            _, data = lmdbfs.read_file(path)
            return data[offset:offset+size]
        return -errno.ENOENT

    def mknod(self, path, mode, rdev):
        logging.debug("mknod: %s (mode %s, rdev %s)" % (path, oct(mode), rdev))
        st = LMDBStat()
        st.st_mode = mode
        st.st_nlink = 1
        lmdbfs.write_file(path, st, "")
        return 0


if __name__ == '__main__':
    fuse.fuse_python_api = (0, 2)
    server = LMDBFileSystem(version='%prog ' + fuse.__version__,
                            usage='',
                            dash_s_do='setsingle')
    server.parse(errex=1)
    server.main()
