#!/usr/bin/python3

# Delete files that are not compiled
# Used for ccls indexed source
# Usage:
# 0. Subdirs in arch/ and include/ which are specific to uninterested architectures may deleted manually before carrying on.
# 1. Choose the directories in delRegex below carefully! Files in these dirs shall be deleted safely.
# me=$(whoami); cd ~/osdev/linux-2.0.27/.ccls-cache/@home@${me}@osdev@linux-2.0.27
# python3 ../../delete_not_compiled_files.py

import os
import re

delRegex = re.compile(r"(^drivers/|^fs/|^net/)")

reg = re.compile(r".*\.[chS]$")

def all_files(targetDir):
    files = os.listdir(targetDir)
    return files

def src_code_files(allFiles):
    srcCodeFiles = [f for f in allFiles if reg.match(f)]
    return srcCodeFiles

def replace_at(files):
    compiledFiles = [f.replace('@', '/') for f in files]
    return compiledFiles

# ==================================================

def walk_through_root(rootdir):
    o = os.walk(rootdir)
    allFiles = []
    for root, subdirs, files in o:
        for filename in files:
            filePath = os.path.join(root, filename)
            allFiles.append(filePath)

    return allFiles

def meet_deletion_cond(filepath):
    if delRegex.match(filepath):
        return True
    return False

def delete_files(toBeDeletedFiles):
    for f in toBeDeletedFiles:
        os.remove(f)

if __name__ == '__main__':
    # Get compiled files
    targetDir = "."
    allFiles = all_files(targetDir)
    # print(allFiles)
    srcCodeFiles = src_code_files(allFiles)
    # print(srcCodeFiles)
    compiledFiles = replace_at(srcCodeFiles)
    # print(compiledFiles)
    print(len(compiledFiles))
    # ========================================

    # Get all source files
    olddir = os.path.curdir
    os.chdir("../../")

    allFiles = walk_through_root(".")
    filteredSrcFiles = []
    for f in allFiles:
        if "ccls-cache" in f:
            continue
        if not reg.match(f):
            continue
        newf = f.replace("./", "")
        filteredSrcFiles.append(newf)
    # print(filteredSrcFiles)
    print(len(filteredSrcFiles))
    # ========================================

    # Before doing the following deletion, we manually deleted subdirs in
    # "arch" and "include" associated with other ARCHs.
    # Get all excluded files, we remove uncompiled files in drivers, fs and net.
    toBeDeletedFiles = []
    for f in filteredSrcFiles:
        if f not in compiledFiles and meet_deletion_cond(f):
            toBeDeletedFiles.append(f)
    # print(toBeDeletedFiles)
    print(len(toBeDeletedFiles))
    # ========================================

    # Now delete files in toBeDeletedFiles
    delete_files(toBeDeletedFiles)
