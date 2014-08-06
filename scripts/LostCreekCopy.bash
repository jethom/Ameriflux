#!/usr/bin/env bash

# copy yesterday's data
YYMMDD=$(date --date='yesterday' +%Y%m%d)
copyPath=/air/incoming/LostCreek/$YYMMDD
mkdir -p $copyPath
pattern=$(date --date='yesterday' +LostCreek*_%Y_%m_%d_*.dat)

/usr/bin/rsync -rltgoDuv --chmod=u+rw,g+r,o+r -e "ssh -tCx ash.ssec.wisc.edu ssh" metobs-vmhost:/mnt/data/ingest/LostCreek/${pattern} $copyPath

# copy today's data
YYMMDD=$(date +%Y%m%d)
copyPath=/air/incoming/LostCreek/$YYMMDD
mkdir -p $copyPath
pattern=$(date +LostCreek*_%Y_%m_%d_*.dat)
/usr/bin/rsync -rltgoDuv --chmod=u+rw,g+r,o+r -e "ssh -tCx ash.ssec.wisc.edu ssh" metobs-vmhost:/mnt/data/ingest/LostCreek/${pattern} $copyPath
#/usr/bin/rsync -rltgoDuv --chmod=u+rw,g+r,o+r -e "ssh -tCx -i /home/jthom/.ssh/id_dsa_jotnar ash.ssec.wisc.edu ssh" metobs-vmhost:/mnt/data/ingest/LostCreek/${pattern} $copyPath

# copy the diagnostic file
copyPath=/air/incoming/LostCreek/Diagnostics
/usr/bin/rsync -rltgoDuv --chmod=u+rw,g+r,o+r -e "ssh -tCx ash.ssec.wisc.edu ssh" metobs-vmhost:/mnt/data/ingest/LostCreek/LostCreek_dailydiag*.dat $copyPath
#/usr/bin/rsync -rltgoDuv --chmod=u+rw,g+r,o+r -e "ssh -tCx -i /home/jthom/.ssh/id_dsa_jotnar ash.ssec.wisc.edu ssh" metobs-vmhost:/mnt/data/ingest/LostCreek/LostCreek_dailydiag*.dat $copyPath
