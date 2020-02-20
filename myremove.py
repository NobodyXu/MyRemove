#!/usr/bin/env python3

import sys
import os

def onerror(error):
    raise error

# This implementation use link + unlink to rename
# 
# Potential race case:
# 
#     Process get terminated before unlink, therefore
#     both filename and newfilename exists in the filesystem
def rename_impl1(dir_fd, filename, newfilename):
    try:
        os.link(filename, newfilename, src_dir_fd = dir_fd, dst_dir_fd = dir_fd)
    except FileExistsError:
        print(f"Error when renaming {filename} as {newfilename}:")
        print(f"    {newfilename} already exists!")
        sys.exit(1)
    os.unlink(filename, dir_fd = dir_fd)

# rename will not overwrite any existing file
def rename(dir_fd, filename, newfilename):
    rename_impl1(dir_fd, filename, newfilename)
    print(f"The file {filename} has been renamed to {newfilename}")

def main():
    path = input("Please enter the directory name: ")
    word = input("Please enter the prefix/postfix that need to be removed: ")
    
    for root, dirnames, filenames, dir_fd in os.fwalk(path, onerror = onerror):
        print(f"In dir {root}")
        for filename in filenames:
            if filename.startswith(word):
                rename(dir_fd, filename, filename[len(word): ])
            elif filename.endswith(word):
                rename(dir_fd, filename, filename[:-len(word)])
    

# Catch OSError and print them to avoid traceback
# as OSError does not necessary mean bugs
# and is used more like a warning to the user
try:
    main()
except OSError as exception:
    print(exception)

