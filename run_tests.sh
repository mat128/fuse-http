#!/bin/bash -xe

root="test/source"
mountpoint="test/mountpoint"
mkdir -p $mountpoint

python loopback.py $root $mountpoint &
fuse_pid=$!

sleep 1

test/test.sh $mountpoint

kill $fuse_pid
