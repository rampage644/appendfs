#!/usr/bin/python
# -*- coding:utf8 -*-

import unittest
import subprocess

MOUNT_POINT = 'fs'


class LMDBFilesystemTest(unittest.TestCase):
    def testDirectoryListing(self):
        self.fail()


if __name__ == '__main__':
    subprocess.check_output(['python', 'lmdb.py', MOUNT_POINT])
    unittest.main()
    subprocess.check_call(['fusermount', '-u', MOUNT_POINT])
