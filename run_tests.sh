#!/bin/bash -xe

root="test/source"
mountpoint="$(mktemp -d '/tmp/fuse-http-test.XXXXXXXX')"

python fuse-http.py "http://localhost:8000" $mountpoint &
fuse_pid=$!

cd $root
python -m SimpleHTTPServer &
httpd_pid=$!
cd -

trap "kill $fuse_pid $httpd_pid; sleep 0.5; rmdir $mountpoint" EXIT
 
sleep 1

test/test.sh $mountpoint

