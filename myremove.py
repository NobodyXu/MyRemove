import sys
import os

def forking(command,filename,stripword):
    try:
        pid = os.fork()
    except:
        sys.exit("ERROR! FORKING FAILS!")

    if pid == 0:
        #child
        newfilename = filename.split('/')
        print(newfilename[1])
        prefix = newfilename[1].split('.')
        newfilename[1] = prefix[0].strip(stripword) + '.' + prefix[1]
        newfilename = newfilename[0] + '/' + newfilename[1]
        print(f"The file {filename} has been renamed to {newfilename}")
        os.rename(filename,newfilename)
        sys.exit()
        #normal exit
    else:
        exit_code = os.waitpid(pid,0)
        if exit_code[1] != 0:
            sys.exit("ERROR! EXITING WITH NON ZERO CODE!")

    
path = input("Please enter the directory name: ")
word = input("Please enter the prefix/postfix that need to be removed: ")

for root, dirnames, filenames in os.walk(path):
    for allfile in filenames:
        if word in allfile:
            full_com = root + "/" + allfile
            forking('mv',full_com,word)
