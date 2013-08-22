:: SAVES HOURLY TRAILER LICOR DATA
:: Written by Bruce Cook
:: Last modified: May 2006

@echo off
setlocal

:: MOVE FILES
:: Note: Won't execute if logger is saving to files.
echo Moving trailer licor file...
move /Y c:\wlef\data\trailer.dat c:\wlef\data\temp

:: SET WORKING DIRECTORY
cd \wlef\data\temp

:: RETRIEVE TIME STAMP (START OF INTERVAL BASED ON PC CLOCK)
FOR /F %%t IN (yyyymmddhhnn.txt) do (set yyyymmddhhnn=%%t)
FOR /F %%t IN (yyyymmdd.txt) do (set yyyymmdd=%%t)

:: SPLIT FILES
:: Note: Can use Loggernet's tob32.exe -a [filename] to convert binary to ASCII only
echo Spliting trailer licor file...
splitr /M /H c:\wlef\programs\campbell\split\trailer/Q trailer.dat trailer.prn
del /F /Q trailer.dat

:: SAVE FIRST LINE OF DATA TO LOG
set /p first_line=<trailer.prn
echo %first_line% >> c:\wlef\data\logs\trailer.log 

:: CHANGE CASE/REMOVE EXTENSION AND ZIP FILES 
:: Note: an alternative is to use zip-7, which allows archieving and can be opened with unzip on linux; www.7-zip.org)
echo Renaming and zipping trailer licor file...
ren "trailer.PRN" trailer%yyyymmddhhnn%
gzip trailer*

:: COPY TO HD AND USB FLASH DRIVE
:: Note: mkdir commands maybe redundant, as directories may already exist
:: will wait 120 seconds if can't find usb drive immediately (e.g., if being exchanged)  
:: allows removeable media with disk drive letter w:\ or z:\ (because cannot be same letter) 
echo Transfering trailer licor file to archive and removable media...
if not exist w:\ sleep 60
mkdir w:\%yyyymmdd%
copy /Y trailer*.gz w:\%yyyymmdd%
if not exist z:\ sleep 60
mkdir z:\%yyyymmdd%
copy /Y trailer*.gz z:\%yyyymmdd%

: scp data to flux.aos.wisc.edu:/data/incoming/wlef
pscp -l jthom -pw "W1EFRl0G!" trailer*.gz flux.aos.wisc.edu:/data/incoming/wlef/.
mkdir c:\wlef\data\archive\%yyyymmdd%
move /Y trailer*.gz c:\wlef\data\archive\%yyyymmdd%