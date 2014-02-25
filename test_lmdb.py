#!/usr/bin/python
# -*- coding:utf8 -*-

import os
import unittest

# relative mount point
MOUNT_POINT = 'fs'


class LMDBFilesystemTest(unittest.TestCase):
    def testFileCreation(self):
        with open(os.path.join(MOUNT_POINT, 'testfile'), 'w') as wfile:
            pass
        self.assertIn('testfile', os.listdir(MOUNT_POINT))

    def testFileWriting(self):
        data = 'balbalbal'
        with open(os.path.join(MOUNT_POINT, 'testfile2'), 'w') as wfile:
            wfile.write(data)

        with open(os.path.join(MOUNT_POINT, 'testfile2'), 'r') as rfile:
            data_r = rfile.read()
            self.assertEqual(data_r, data)


if __name__ == '__main__':
    unittest.main()
