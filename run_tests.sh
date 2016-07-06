#!/bin/bash -xe

root="test/source"
mountpoint="test/mountpoint"
mkdir -p $mountpoint

python loopback.py $root $mountpoint

sleep 1

test/test.sh $mountpoint

fusermount -u $mountpoint || umount $mountpoint
