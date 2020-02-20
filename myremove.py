#!/usr/bin/env python3

import sys
import os

# A primitive implementation that use os.access
# This cannot avoid race condition:
#
#  1. Program checked using os.access that the new filename does not exist
#  2. Someone created that file ASAP after the check
#  3. Program called os.rename
def assertNotExist(dir_fd, oldfilename, newfilename):
    if os.access(newfilename, os.F_OK, dir_fd = dir_fd):
        print(f"Error when renaming {oldfilename} as {newfilename}:")
        print(f"    {newfilename} already exists!")
        sys.exit(1)

def onerror(error):
    raise error

# rename will not overwrite any existing file
def rename(dir_fd, filename, newfilename):
    assertNotExist(dir_fd, filename, newfilename)
    print(f"The file {filename} has been renamed to {newfilename}")
    os.rename(filename, newfilename, src_dir_fd = dir_fd, dst_dir_fd = dir_fd)

def main():
    path = input("Please enter the directory name: ")
    word = input("Please enter the prefix/postfix that need to be removed: ")
    
    for root, dirnames, filenames, dir_fd in os.fwalk(path, onerror = onerror):
        print(f"In dir {root}")
        for filename in filenames:
            if filename.startswith(word):
                newfilename = filename[len(word): ]
            elif filename.endswith(word):
                newfilename = filename[:-len(word)]
            else:
                continue
    
            rename(dir_fd, filename, newfilename)

# Catch OSError and print them to avoid traceback
# as OSError does not necessary mean bugs
# and is used more like a warning to the user
try:
    main()
except OSError as exception:
    print(exception)

