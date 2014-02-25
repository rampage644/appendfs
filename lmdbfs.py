#!/usr/bin/python
# -*- coding:utf8 -*-

import lmdb
import pickle
import logging

LOG_FILENAME = "LOG"
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG,)

DB_PATH = 'fsdb'

env = lmdb.open(DB_PATH, max_dbs=3)
try:
    meta_db = env.open_db(name='meta', create=False)
    data_db = env.open_db(name='data', create=False)
except lmdb.NotFoundError:
    meta_db = env.open_db(name='meta', create=True)
    data_db = env.open_db(name='data', create=True)


def write_file(path, stat, data):
    with env.begin(write=True, db=meta_db) as txn:
        txn.put(path, pickle.dumps(stat))
    with env.begin(write=True, db=data_db) as txn:
        txn.put(path, data)


def read_file(path):
    st, data = None, None
    with env.begin() as txn:
        meta = txn.get(path, db=meta_db)
        if meta:
            st = pickle.loads(meta)
    with env.begin() as txn:
        data = txn.get(path, db=data_db)
    return st, data

def exists(path):
    with env.begin() as txn:
        meta = txn.get(path, db=meta_db)
    return True if meta is not None else False

def files(path):
    files = []
    with env.begin() as txn:
        for k, v in txn.cursor(meta_db):
            files.append(k)

    return files
