#!/bin/bash

_subdirs=(kernel/math kernel/blk_drv kernel/chr_drv kernel mm fs lib)

for _dir in ${_subdirs[@]}; do
  LANGUAGE=en make -C ${_dir} V=1 -j1 --dry-run |& tee -a build-log.txt
done
LANGUAGE=en make V=1 -j1 --dry-run init/main.o |& tee -a build-log.txt

# compiledb needs the make[N] style of Entering and Leaving directory.
# make[N] is automatically set when these commands are executed in Makefile target. See gen_build_log.mk
sed -i 's|make|make[1]|g' build-log.txt
