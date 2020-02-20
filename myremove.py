#!/usr/bin/env python3

import sys
import os

# A primitive implementation that use os.access
# This cannot avoid race condition:
#
#  1. Program checked using os.access that the new filename does not exist
#  2. Someone created that file ASAP after the check
#  3. Program called os.rename
def assertNotExist(root, oldfilename, newfilename):
    if os.access(root + "/" + newfilename, os.F_OK):
        print(f"Error when renaming {oldfilename} as {newfilename}:")
        print(f"    {newfilename} already exists in {root}!")
        sys.exit(1)

def onerror(error):
    raise error

# rename will not overwrite any existing file
def rename(dirname, filename, newfilename):
    assertNotExist(dirname, filename, newfilename)
    print(f"The file {filename} in {dirname} has been renamed to {newfilename}")
    os.rename(dirname + "/" + filename, dirname + "/" + newfilename)

def main():
    path = input("Please enter the directory name: ")
    word = input("Please enter the prefix/postfix that need to be removed: ")
    
    for root, dirnames, filenames in os.walk(path, onerror = onerror):
        for filename in filenames:
            if filename.startswith(word):
                newfilename = filename[len(word): ]
            elif filename.endswith(word):
                newfilename = filename[:-len(word)]
            else:
                continue
    
            rename(root, filename, newfilename)

# Catch OSError and print them to avoid traceback
# as OSError does not necessary mean bugs
# and is used more like a warning to the user
try:
    main()
except OSError as exception:
    print(exception)

