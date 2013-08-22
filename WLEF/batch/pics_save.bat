:: SAVES HOURLY PICS
::
:: Written by Bruce Cook
:: Last modified: May 2006

@echo off
setlocal

:: RETRIEVE TIME STAMP (START OF INTERVAL BASED ON PC CLOCK)
FOR /F %%t IN (c:\wlef\data\temp\yyyymmddhhnn.txt) do (set yyyymmddhhnn=%%t)
FOR /F %%t IN (c:\wlef\data\temp\yyyymmdd.txt) do (set yyyymmdd=%%t)

:: SET WORKING DIRECTORY
cd \wlef\pics\unfiled

:: RENAME FILES
:: Note that midnight is missing for some unknown reason
ren *_12_00_*AM.jpg %yyyymmdd%00.jpg
ren *_01_00_*AM.jpg %yyyymmdd%01.jpg
ren *_02_00_*AM.jpg %yyyymmdd%02.jpg
ren *_03_00_*AM.jpg %yyyymmdd%03.jpg
ren *_04_00_*AM.jpg %yyyymmdd%04.jpg
ren *_05_00_*AM.jpg %yyyymmdd%05.jpg
ren *_06_00_*AM.jpg %yyyymmdd%06.jpg
ren *_07_00_*AM.jpg %yyyymmdd%07.jpg
ren *_08_00_*AM.jpg %yyyymmdd%08.jpg
ren *_09_00_*AM.jpg %yyyymmdd%09.jpg
ren *_10_00_*AM.jpg %yyyymmdd%10.jpg
ren *_11_00_*AM.jpg %yyyymmdd%11.jpg
ren *_12_00_*PM.jpg %yyyymmdd%12.jpg
ren *_01_00_*PM.jpg %yyyymmdd%13.jpg
ren *_02_00_*PM.jpg %yyyymmdd%14.jpg
ren *_03_00_*PM.jpg %yyyymmdd%15.jpg
ren *_04_00_*PM.jpg %yyyymmdd%16.jpg
ren *_05_00_*PM.jpg %yyyymmdd%17.jpg
ren *_06_00_*PM.jpg %yyyymmdd%18.jpg
ren *_07_00_*PM.jpg %yyyymmdd%19.jpg
ren *_08_00_*PM.jpg %yyyymmdd%20.jpg
ren *_09_00_*PM.jpg %yyyymmdd%21.jpg
ren *_10_00_*PM.jpg %yyyymmdd%22.jpg
ren *_11_00_*PM.jpg %yyyymmdd%23.jpg

:: ZIP FILES
echo Zipping pics...
gzip *.jpg

:: COPY TO HD AND USB FLASH DRIVE
:: Note: mkdir commands maybe redundant, as directories may already exist
:: will wait 120 seconds if can't find usb drive immediately (e.g., if being exchanged)  
:: allows removeable media with disk drive letter w:\ or z:\ (because cannot be same letter)  
echo Transfering pictures to archive and removable media...
if not exist w:\ sleep 60
mkdir w:\%yyyymmdd%
copy /Y *.jpg.gz w:\%yyyymmdd%
if not exist z:\ sleep 60
mkdir z:\%yyyymmdd%
copy /Y *.jpg.gz z:\%yyyymmdd%

: scp data to flux.aos.wisc.edu:/data/incoming/wlef
pscp -l jthom -pw "W1EFRl0G!" *.jpg.gz flux.aos.wisc.edu:/data/incoming/wlef/.
mkdir c:\wlef\data\archive\%yyyymmdd%
move /Y *.jpg.gz c:\wlef\data\archive\%yyyymmdd%

