#!/usr/bin/env bash
#
# Runs the archive data in a screen
#
# If a screen session is already running with that name, exit, otherwise start
# a new detached screen session named 'ArchiveData'
#
SCRN=$(screen -list | grep ArchiveData | awk '{print $1}')
workdir=$(eval echo ~)
pyscriptname="${workdir}/Documents/WLEF/scripts/loop2.py"
if [ -n "$SCRN" ]; then
echo Screen already running: $SCRN
else
screen -S ArchiveData -d -m python "${pyscriptname}"
echo Started in screen $(screen -list | grep ArchiveData | awk '{print $1}')
fi
