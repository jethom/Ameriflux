#!/usr/bin/env bash

# copy yesterday's data
YYMMDD=$(date --date='yesterday' +%Y%m%d)
copyPath=/air/incoming/LimnologyFlux/$YYMMDD
mkdir -p $copyPath
pattern=$(date --date='yesterday' +LimnologyFlux*_%Y_%m_%d_*.dat)

#/usr/bin/rsync -rltgoDuv --chmod=u+rw,g+r,o+r -e "ssh -i $HOME/.ssh/id_dsa_jotnar" buoy@jotnar.ssec.wisc.edu:/cygdrive/c/Data/LimnologyFlux/${pattern} $copyPath

/usr/bin/rsync -rltgoDuv --chmod=u+rw,g+r,o+r -e "ssh -tCx ash.ssec.wisc.edu ssh" metobs-vmhost:/mnt/data/ingest/limno_flux/${pattern} $copyPath

# copy today's data
YYMMDD=$(date +%Y%m%d)
copyPath=/air/incoming/LimnologyFlux/$YYMMDD
mkdir -p $copyPath
pattern=$(date +LimnologyFlux*_%Y_%m_%d_*.dat)
#/usr/bin/rsync -rltgoDuv --chmod=u+rw,g+r,o+r -e "ssh -i $HOME/.ssh/id_dsa_jotnar" buoy@jotnar.ssec.wisc.edu:/cygdrive/c/Data/LimnologyFlux/${pattern} $copyPath
/usr/bin/rsync -rltgoDuv --chmod=u+rw,g+r,o+r -e "ssh -tCx ash.ssec.wisc.edu ssh" metobs-vmhost:/mnt/data/ingest/limno_flux/${pattern} $copyPath
