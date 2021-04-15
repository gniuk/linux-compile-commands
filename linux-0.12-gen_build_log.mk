SUBDIRS = kernel/math kernel/blk_drv kernel/chr_drv kernel mm fs lib

all:
	for i in ${SUBDIRS}; do LANGUAGE=en make -C $$i V=1 -j1 --dry-run; done
	LANGUAGE=en make V=1 -j1 --dry-run init/main.o
