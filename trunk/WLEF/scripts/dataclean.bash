#!/usr/bin/env bash
. /home/jthom/.bashrc

WORKINGDIR=/home/flux/Documents/data
ARCHIVEDIR=/home/flux/Documents/archive
DATE=$(/bin/date -d '-1 month' +%Y%m)
/bin/echo "DATE = $DATE"

/bin/echo $DATE
cd $WORKINGDIR
# Create tar gzip file
ARCH="${ARCHIVEDIR}/${DATE}.tar.gz"
/bin/echo "$ARCH"
if [ -e $ARCH ]; then
	/bin/echo "$PWD/$ARCH already exits!!"
	exit 1
fi
/bin/tar -zcvf ${ARCH} ${DATE}*

# Delete files that are listed in the tar gzip we just created
for fn in $(/bin/tar -tvf $ARCH | /bin/grep drw | /usr/bin/awk '{print $6}'); do 
	/bin/echo "removing $fn"
	rm -rf $fn
done
