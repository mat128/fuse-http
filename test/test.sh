#!/bin/bash -xe

mountpoint=$1

grep '^fileA$' $mountpoint/fileA
grep '^fileA$' $mountpoint/subdirectory/fileA
grep '^fileA$' $mountpoint/no_content_length_for_directories/fileA
