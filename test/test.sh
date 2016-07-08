#!/bin/bash -xe

mountpoint=$1

grep '^fileA$' $mountpoint/fileA
grep '^fileA$' $mountpoint/subdirectory/fileA

