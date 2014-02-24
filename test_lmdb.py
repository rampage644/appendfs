#!/usr/bin/python
# -*- coding:utf8 -*-

import os
import unittest

# relative mount point
MOUNT_POINT = os.path.join(os.getcwd(), 'fs')


class LMDBFilesystemTest(unittest.TestCase):
    def testDirectoryListing(self):
        self.assertIn('.', os.listdir(MOUNT_POINT))
        self.assertIn('..', os.listdir(MOUNT_POINT))


if __name__ == '__main__':
    unittest.main()
