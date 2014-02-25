#!/usr/bin/python
# -*- coding:utf8 -*-

import os
import pickle

class LogFSPointer(object):
    def __init__(self, meta_offset, meta_length,
                 data_offset, data_length):
        self.meta_offset = meta_offset
        self.meta_length = meta_length
        self.data_offset = data_offset
        self.data_length = data_length

    def __eq__(self, other):
        return (self.meta_length == other.meta_length and
                self.meta_offset == other.meta_offset and
                self.data_length == other.data_length and
                self.data_offset == other.data_offset)

class LogFS(object):
    def __init__(self, datafile, structfile):
        self.data_f = open(datafile, 'a+')
        self.struct_f = open(structfile, 'a+')

    def __del__(self):
        self.data_f.close()
        self.struct_f.close()

    def _read_binary(self, offset, length):
        self.data_f.seek(offset, os.SEEK_SET)
        return self.data_f.read(length)

    def _write_binary(self, data):
        self.data_f.seek(0, os.SEEK_END)
        off = self.data_f.tell()
        self.data_f.write(data)
        return off, len(data)

    def read_meta(self, offset, length):
        return pickle.loads(self._read_binary(offset, length))

    def read_data(self, offset, length):
        return self._read_binary(offset, length)

    def read_files(self):
        self.struct_f.seek(0, os.SEEK_SET)
        return pickle.loads(self.struct_f.read())

    def write_meta(self, st):
        return self._write_binary(pickle.dumps(st))

    def write_data(self, data):
        return self._write_binary(data)

    def write_files(self, dictionary):
        self.struct_f.seek(0, os.SEEK_SET)
        self.struct_f.write(pickle.dumps(dictionary))
        self.struct_f.flush()
