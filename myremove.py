import sys
import os

def rename(filename, stripword):
    newfilename = filename.split('/')
    print(newfilename[1])
    prefix = newfilename[1].split('.')
    newfilename[1] = prefix[0].strip(stripword) + '.' + prefix[1]
    newfilename = newfilename[0] + '/' + newfilename[1]
    print(f"The file {filename} has been renamed to {newfilename}")
    os.rename(filename,newfilename)

    
path = input("Please enter the directory name: ")
word = input("Please enter the prefix/postfix that need to be removed: ")

for root, dirnames, filenames in os.walk(path):
    for filename in filenames:
        if word in filename:
            full_com = root + "/" + filename
            rename(full_com, word)
