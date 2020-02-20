#!/usr/bin/env python3

import sys
import os

def usage(argv0, msg, exit_code):
    print(f"{msg}Usage: {argv0}: [flag] <optional args...>")
    print(f"[flag]:")
    print(f"    -v/--verbose to adjust verbosity")
    print(f"    -h/--help    to print this help")
    print(f"<optional args...>:")
    print(f"    path to dir")
    print(f"    prefix/postfix that needs to be removed")
    sys.exit(exit_code)

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
def rename(dir_fd, filename, newfilename, verbose):
    rename_impl1(dir_fd, filename, newfilename)
    if verbose:
        print(f"The file {filename} has been renamed to {newfilename}")

def parse_argv(argv):
    # Parse argv
    verbose = False

    for i in range(1, len(argv)):
        if argv[i] in ["-v", "--verbose"]:
            verbose = True
            argv.pop(index = i)
        elif argv[i] in ["-h", "--help"]:
            usage(argv[0], "", 0)
        elif argv[i].startswith("-"):
            usage(argv[0], f"Unrecognized option {argv[i]}\n\n", 1)

    path = None
    word = None
    if len(argv) > 3:
        usage(argv[0], "Too many parameters!\n", 1)
    if len(argv) >= 2:
        path = argv[1]
    if len(argv) == 3:
        word = argv[2]

    return (verbose, path, word)
 
def main(argv):
    verbose, path, word = parse_argv(argv)

    if path is None:
        path = input("Please enter the directory name: ")
    if word is None:
        word = input("Please enter the prefix/postfix that need to be removed: ")
    
    for root, dirnames, filenames, dir_fd in os.fwalk(path, onerror = onerror):
        print(f"In dir {root}")
        for filename in filenames:
            if filename.startswith(word):
                rename(dir_fd, filename, filename[len(word): ], verbose)
            elif filename.endswith(word):
                rename(dir_fd, filename, filename[:-len(word)], verbose)
    

# Catch OSError and print them to avoid traceback
# as OSError does not necessary mean bugs
# and is used more like a warning to the user
try:
    main(sys.argv)
except OSError as exception:
    print(exception)

