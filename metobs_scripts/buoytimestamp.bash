#!/usr/bin/env bash
#
# script to move mendota date files to daily files
#
workingdir=/mnt/data/ingest/mendota_buoy/
pat_ld=$(date --date='yesterday' +MendotaBuoy_limnodata_%Y%m%d.dat)
pat_md=$(date --date='yesterday' +MendotaBuoy_metdata_%Y%m%d.dat)
pat_sys=$(date --date='yesterday' +MendotaBuoy_system_%Y%m%d.dat)

# pause loggernet data collection
/opt/CampbellSci/LoggerNet/cora_cmd < /mnt/data/ingest/programs/buoy/PauseOn.SCR
mv ${workingdir}/MendotaBuoy_metdata.dat ${workingdir}/${pat_md}
mv ${workingdir}/MendotaBuoy_limnodata.dat ${workingdir}/${pat_ld}
mv ${workingdir}/MendotaBuoy_system.dat ${workingdir}/${pat_sys}
#cp ${workingdir}/MendotaBuoy_metdata.dat ${workingdir}/${pat_md}
#cp ${workingdir}/MendotaBuoy_limnodata.dat ${workingdir}/${pat_ld}
#cp ${workingdir}/MendotaBuoy_system.dat ${workingdir}/${pat_sys}
# resume loggernet data collection
/opt/CampbellSci/LoggerNet/cora_cmd < /mnt/data/ingest/programs/buoy/PauseOff.SCR
