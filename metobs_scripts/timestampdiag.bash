#!/usr/bin/env bash
#
# script to move diagnostic file for Lost Creek daily diagnostic file to a file with 
# a time stamp.
#
workingdir=/mnt/data/ingest/LostCreek/
pattern=$(date +LostCreek_dailydiag_%Y%m%d.dat)

/opt/CampbellSci/LoggerNet/cora_cmd < /mnt/data/ingest/programs/buoy/PauseOn.SCR
mv ${workingdir}/LostCreek_dailydiag.dat ${workingdir}/${pattern}
#cp ${workingdir}/LostCreek_dailydiag.dat ${workingdir}/${pattern}
/opt/CampbellSci/LoggerNet/cora_cmd < /mnt/data/ingest/programs/buoy/PauseOff.SCR
