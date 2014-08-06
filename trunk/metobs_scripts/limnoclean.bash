#!/usr/bin/env bash

WORKINGDIR=/mnt/data/ingest/limno_flux
DATE=$(date -d '-1 month' +%Y_%m)

cd $WORKINGDIR
# Create tar gzip file
ARCH="LimnologyFlux_${DATE}.dat.tar.gz"
if [ -e $ARCH ]; then
	echo "$PWD/$ARCH already exits!!"
	exit 1
fi
tar -zcvf LimnologyFlux_${DATE}.dat.tar.gz LimnologyFlux_*_${DATE}*.dat

# Delete files that are listed in the tar gzip we just created
for fn in $(tar -tvf LimnologyFlux_${DATE}*.gz | awk '{print $6}'); do 
	echo "removing $fn"
	rm -f $fn
done
