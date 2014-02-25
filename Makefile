MOUNTPOINT=fs

test_lmdb:
	mkdir $(MOUNTPOINT) || true
	rm LOG || true
	python lmdb_fuse.py $(MOUNTPOINT) -s
	python test_lmdb.py || true
	fusermount -u $(MOUNTPOINT)

test_log:
	mkdir $(MOUNTPOINT) || true
	rm LOG || true
	python logfs_fuse.py $(MOUNTPOINT) -s
	python test_lmdb.py || true
	fusermount -u $(MOUNTPOINT)