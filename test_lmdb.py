#!/usr/bin/python
# -*- coding:utf8 -*-

import os
import unittest
import subprocess

# relative mount point
MOUNT_POINT = 'fs'


class LMDBFilesystemTest(unittest.TestCase):
    def testDirectoryListing(self):
        self.assertIn('.', os.listdir(MOUNT_POINT))
        self.assertIn('..', os.listdir(MOUNT_POINT))


if __name__ == '__main__':
    subprocess.check_output(['python', 'lmdb.py', MOUNT_POINT])
    try:
        unittest.main()
    finally:
        subprocess.check_call(['fusermount', '-u', MOUNT_POINT])
