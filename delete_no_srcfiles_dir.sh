#!/bin/bash

# Use it after delete_not_compiled_files.py to delete unrelated source directories

TARGET_DIRS=(block certs crypto drivers fs include init ipc kernel lib mm net security sound virt)

for rootdir in ${TARGET_DIRS[@]}; do
    all_dirs=$(find $rootdir -type d | sort -r)
    # echo $all_dirs
    for subdir in ${all_dirs}; do
        # echo $subdir
        has_src=$(ls $subdir | grep -E "\.c$|\.h$|\.S$|\.tbl$")
        if [ "$has_src" == "" ]; then
            has_subdir=$(find $subdir -type d | egrep -v "${subdir}\b$")
            if [ "$has_subdir" == "" ]; then
                echo -n "REMOVE [no source files and subdirs in]: "
                echo "$subdir"
                rm -rf "$subdir"
            fi
        fi
    done
done
