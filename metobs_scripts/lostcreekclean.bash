#!/usr/bin/env bash

WORKINGDIR=/mnt/data/ingest/LostCreek
DATEIN=$(date -d '-1 month' +%Y_%m)
DATE=$(date -d '-1 month' +%Y%m)

echo $DATE
cd $WORKINGDIR
# Create tar gzip file
ARCH="LostCreek_${DATE}.dat.tar.gz"
if [ -e $ARCH ]; then
	echo "$PWD/$ARCH already exits!!"
	exit 1
fi
tar -zcvf LostCreek_${DATE}.dat.tar.gz LostCreek_*_${DATEIN}*.dat

# Delete files that are listed in the tar gzip we just created
for fn in $(tar -tvf LostCreek_${DATE}*.gz | awk '{print $6}'); do 
	echo "removing $fn"
	rm -f $fn
done
