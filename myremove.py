#!/usr/bin/env python3

import sys
import os

def rename(dirname, filename, newfilename):
    print(f"The file {filename} in {dirname} has been renamed to {newfilename}")
    os.rename(dirname + "/" + filename, dirname + "/" + newfilename)

path = input("Please enter the directory name: ")
word = input("Please enter the prefix/postfix that need to be removed: ")

for root, dirnames, filenames in os.walk(path):
    for filename in filenames:
        if filename.startswith(word):
            newfilename = filename[len(word): ]
        elif filename.endswith(word):
            newfilename = filename[:-len(word)]
        else:
            continue

        rename(root, filename, newfilename)
