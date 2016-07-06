#!/bin/bash -xe

mountpoint=$1

grep '^fileA$' $mountpoint/nested/second_level/fileA
grep '^fileB$' $mountpoint/nonnested/fileB


