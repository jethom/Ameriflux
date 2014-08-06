#!/usr/bin/env bash
DATE=201406
echo $DATE
WORKINGDIR=/mnt/data/ingest/LostCreek
echo $WORKINGDIR

cd $WORKINGDIR
pwd
for fn in $(tar -tvf LostCreek_${DATE}*.gz | awk '{print $6}'); do
	echo "removing $fn"
	rm -f $fn
done
