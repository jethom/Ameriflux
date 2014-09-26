#!/usr/bin/env bash

WORKINGDIR=/home/flux/Documents/data
ARCHIVEDIR=/home/flux/Documents/archive
DATE=$(date -d '-1 month' +%Y%m)
echo "DATE = $DATE"

echo $DATE
cd $WORKINGDIR
# Create tar gzip file
ARCH="${ARCHIVEDIR}/${DATE}.tar.gz"
echo "$ARCH"
if [ -e $ARCH ]; then
	echo "$PWD/$ARCH already exits!!"
	exit 1
fi
tar -zcvf ${ARCH} ${DATE}*

# Delete files that are listed in the tar gzip we just created
for fn in $(tar -tvf $ARCH | grep drw | awk '{print $6}'); do 
	echo "removing $fn"
	rm -rf $fn
done
