#!/bin/bash -xe

root="test/source"
httpd_path="../testHTTPServer.py" #relative to $root
mountpoint="$(mktemp -d '/tmp/fuse-http-test.XXXXXXXX')"

python fuse-http.py "http://localhost:8000" $mountpoint &
fuse_pid=$!

cd $root
python $httpd_path &
httpd_pid=$!
cd -

trap "kill $fuse_pid $httpd_pid; sleep 0.5; rmdir $mountpoint" EXIT
 
sleep 1

test/test.sh $mountpoint

