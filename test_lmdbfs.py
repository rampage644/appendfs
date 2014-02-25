#!/usr/bin/python
# -*- coding:utf8 -*-

import lmdbfs
import fuse
import unittest


class LMDBFilesystemTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test(self):
        st = fuse.Stat()
        st.st_nlink = 1
        st.st_mode = 0
        data = 'file1datadatadata'
        lmdbfs.write_file('file1', st, data)

        st_r, data_r = lmdbfs.read_file('file1')
        self.assertEqual(data, data_r)
        self.assertEquals(st.st_nlink, st_r.st_nlink)

    def testNonExistentRead(self):
        st_r, data_r = lmdbfs.read_file('file2')
        self.assertIsNone(st_r)
        self.assertIsNone(data_r)

    def testFileExistence(self):
        self.assertTrue(lmdbfs.exists('file1'))
        self.assertFalse(lmdbfs.exists('file2'))

    def testListFiles(self):
        data = 'blba'
        st = fuse.Stat(st_size = len(data), st_nlink = 1)
        lmdbfs.write_file('file3', st, data)
        lmdbfs.write_file('file4', st, data)

        self.assertIn('file3', lmdbfs.files('/'))
        self.assertIn('file4', lmdbfs.files('/'))
        self.assertNotIn('file5', lmdbfs.files('/'))


if __name__ == '__main__':
    unittest.main()
