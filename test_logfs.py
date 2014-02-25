#!/usr/bin/python
# -*- coding:utf8 -*-

import logfs
import fuse
import unittest


DATA_FILE_PATH = 'logfs.bin'
META_FILE_PATH = 'logfsx.bin'

fs = logfs.LogFS(DATA_FILE_PATH, META_FILE_PATH)


class LogFSTest(unittest.TestCase):
    def testMeta(self):
        st1 = fuse.Stat(st_mode=1, st_nlink=2, st_size=100)
        off1, len1 = fs.write_meta(st1)
        st2 = fuse.Stat(st_mode=3, st_nlink=4, st_size=102)
        off2, len2 = fs.write_meta(st2)
        st3 = fuse.Stat(st_mode=5, st_nlink=6, st_size=104)
        off3, len3 = fs.write_meta(st3)

        rst2 = fs.read_meta(off2, len2)
        rst1 = fs.read_meta(off1, len1)
        rst3 = fs.read_meta(off3, len3)

        self.assertEqual(st1.st_mode, rst1.st_mode)
        self.assertEqual(st2.st_nlink, rst2.st_nlink)
        self.assertEqual(st3.st_size, rst3.st_size)

    def testData(self):
        data = 'blabla' * 4
        off, length = fs.write_data(data)

        rdata = fs.read_data(off, length)

        self.assertEqual(data, rdata)
        self.assertEqual(len(data), length)

    def testStruct(self):
        dictionary = {}
        dictionary['/file1'] = logfs.LogFSPointer(0, 10, 10, 20)
        dictionary['/file2'] = logfs.LogFSPointer(30, 10, 40, 20)

        fs.write_files(dictionary)
        rdict = fs.read_files()

        self.assertEqual(len(rdict), len(dictionary))
        self.assertEqual(rdict, dictionary)


if __name__ == '__main__':
    unittest.main()
