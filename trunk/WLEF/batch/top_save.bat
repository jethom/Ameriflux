:: SAVES HOURLY DATA FROM TOP BOX
::
:: Written by Bruce Cook
:: Last modified: May 2006

@echo off
setlocal

:: MOVE FILES
:: Note: Won't execute if logger is saving to files.
echo Moving top files...
move /Y c:\wlef\data\top*.* c:\wlef\data\temp

:: SET WORKING DIRECTORY
cd \wlef\data\temp

:: RETRIEVE TIME STAMP (START OF INTERVAL BASED ON PC CLOCK)
FOR /F %%t IN (yyyymmddhhnn.txt) do (set yyyymmddhhnn=%%t)
FOR /F %%t IN (yyyymmdd.txt) do (set yyyymmdd=%%t)

:: SPLIT FILES
:: Note: Can use Loggernet's tob32.exe -a [filename] to convert binary to ASCII only
echo Spliting top files...
splitr /M /H c:\wlef\programs\campbell\split\slow/Q top_slow.dat top_slow
splitr /M /H c:\wlef\programs\campbell\split\fast/Q top_fast.dat top_fast
del /F /Q top*.dat

:: SAVE FIRST LINE OF DATA TO LOG
set /p first_line=<top_fast.prn
echo %first_line% >> c:\wlef\data\logs\top_fast.log 
set /p first_line=<top_slow.prn
echo %first_line% >> c:\wlef\data\logs\top_slow.log 

:: CHANGE CASE, REMOVE EXTENSION, ADD TIME STAMP, AND ZIP FILES 
:: Note: an alternative is to use zip-7, which allows archieving and can be opened with unzip on linux; www.7-zip.org)
echo Renaming and zipping top files...
ren "TOP_FAST.PRN" top_fast%yyyymmddhhnn%
ren "TOP_SLOW.PRN" top_slow%yyyymmddhhnn%
gzip top*

:: COPY TO HD AND USB FLASH DRIVE
:: Notes: 
:: mkdir commands maybe redundant, as directories may already exist
:: will wait 120 seconds if can't find usb drive immediately (e.g., if being exchanged)  
:: allows removeable media with disk drive letter w:\ or z:\ (because cannot be same letter)
echo Transfering top files to archive and removable media...
if not exist w:\ sleep 60
mkdir w:\%yyyymmdd%
copy /Y top*.gz w:\%yyyymmdd%
if not exist z:\ sleep 60
mkdir z:\%yyyymmdd%
copy /Y top*.gz z:\%yyyymmdd%

: scp data to flux.aos.wisc.edu:/data/incoming/wlef
pscp -l jthom -pw "W1EFRl0G!" top*.gz flux.aos.wisc.edu:/data/incoming/wlef/.
mkdir c:\wlef\data\archive\%yyyymmdd%
move /Y top*.gz c:\wlef\data\archive\%yyyymmdd%
