#!/bin/bash
#
# Runs the archive data in a screen
#
# If a screen session is already running with that name, exit, otherwise start
# a new detached screen session named 'ArchiveData'
#
. /home/flux/.bashrc
SCRN=$(/usr/bin/screen -list | /bin/grep ArchiveData | /usr/bin/awk '{print $1}')
workdir=$(eval /bin/echo ~)
pyscriptname="${workdir}/Documents/WLEF/scripts/loop2.py"
if [ -n "$SCRN" ]; then
/bin/echo Screen already running: $SCRN
else
/usr/bin/screen -S ArchiveData -d -m /home/flux/env/bin/python "${pyscriptname}"
/bin/echo Started in screen $(screen -list | grep ArchiveData | awk '{print $1}')
fi
