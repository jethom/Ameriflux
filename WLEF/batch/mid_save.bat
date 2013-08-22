@echo off
setlocal

:: MOVE FILES
:: Note: Won't execute if logger is saving to files.
echo Moving mid files...
move /Y c:\wlef\data\mid*.* c:\wlef\data\temp

:: SET WORKING DIRECTORY
cd \wlef\data\temp

FOR /F %%t IN (yyyymmddhhnn.txt) do (set yyyymmddhhnn=%%t)
FOR /F %%t IN (yyyymmdd.txt) do (set yyyymmdd=%%t)

:: SPLIT FILES
:: Note: Can use Loggernet's tob32.exe -a [filename] to convert binary to ASCII only
echo Spliting mid files...
splitr /M /H c:\wlef\programs\campbell\split\slow/Q mid_slow.dat mid_slow
splitr /M /H c:\wlef\programs\campbell\split\fast/Q mid_fast.dat mid_fast
del /F /Q mid*.dat

:: SAVE FIRST LINE OF DATA TO LOG
set /p first_line=<mid_fast.prn
echo %first_line% >> c:\wlef\data\logs\mid_fast.log 
set /p first_line=<mid_slow.prn
echo %first_line% >> c:\wlef\data\logs\mid_slow.log 

:: CHANGE CASE/REMOVE EXTENSION AND ZIP FILES 
:: Note: an alternative is to use zip-7, which allows archieving and can be opened with unzip on linux; www.7-zip.org)
echo Renaming and zipping mid files...
ren "mid_FAST.PRN" mid_fast%yyyymmddhhnn%
ren "mid_SLOW.PRN" mid_slow%yyyymmddhhnn%
gzip mid*

:: COPY TO HD AND USB FLASH DRIVE
:: Note: mkdir commands maybe redundant, as directories may already exist
:: will wait 120 seconds if can't find usb drive immediately (e.g., if being exchanged)
:: allows removeable media with disk drive letter w:\ or z:\ (because cannot be same letter)    
echo Transfering mid files to archive and removable media...
if not exist w:\ sleep 60
mkdir w:\%yyyymmdd%
copy /Y mid*.gz w:\%yyyymmdd%
if not exist z:\ sleep 60
mkdir z:\%yyyymmdd%
copy /Y mid*.gz z:\%yyyymmdd%

: scp data to flux.aos.wisc.edu:/data/incoming/wlef
pscp -l jthom -pw "W1EFRl0G!" mid*.gz flux.aos.wisc.edu:/data/incoming/wlef/.
mkdir c:\wlef\data\archive\%yyyymmdd%
move /Y mid*.gz c:\wlef\data\archive\%yyyymmdd%
