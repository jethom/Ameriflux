#!/usr/bin/env bash
#
# Runs the archive data in a screen
#
# If a screen session is already running with that name, exit, otherwise start
# a new detached screen session named 'ArchiveData'
#
SCRN=$(/usr/bin/screen -list | /bin/grep ArchiveData | /usr/bin/awk '{print $1}')
workdir=$(eval /bin/echo ~)
pyscriptname="${workdir}/Documents/WillowCreek/scripts/loop2.py"
if [ -n "$SCRN" ]; then
echo Screen already running: $SCRN
else
/usr/bin/screen -S ArchiveData -d -m /home/flux/env/bin/python "${pyscriptname}"
echo Started in screen $(/usr/bin/screen -list | /bin/grep ArchiveData | /usr/bin/awk '{print $1}')
fi
