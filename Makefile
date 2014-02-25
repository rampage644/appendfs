MOUNTPOINT=fs

test:
	mkdir $(MOUNTPOINT) || true
	rm LOG || true
	python lmdb_fuse.py $(MOUNTPOINT)
	python test_lmdb.py || true
	fusermount -u $(MOUNTPOINT)
