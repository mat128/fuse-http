#!/bin/bash -xe

root="test/source"
mountpoint="test/mountpoint"

python loopback.py $root $mountpoint

sleep 1

test/test.sh $mountpoint

umount $mountpoint
