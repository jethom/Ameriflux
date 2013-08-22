@echo off
setlocal

:: MOVE FILES
:: Note: Won't execute if logger is saving to files.
echo Moving bot files...
move /Y c:\wlef\data\bot*.* c:\wlef\data\temp

:: SET WORKING DIRECTORY
cd \wlef\data\temp

FOR /F %%t IN (yyyymmddhhnn.txt) do (set yyyymmddhhnn=%%t)
FOR /F %%t IN (yyyymmdd.txt) do (set yyyymmdd=%%t)

:: SPLIT FILES
:: Note: Can use Loggernet's tob32.exe -a [filename] to convert binary to ASCII only
echo Spliting bot files...
splitr /M /H c:\wlef\programs\campbell\split\slow/Q bot_slow.dat bot_slow
splitr /M /H c:\wlef\programs\campbell\split\fast/Q bot_fast.dat bot_fast
del /F /Q bot*.dat

:: SAVE FIRST LINE OF DATA TO LOG
set /p first_line=<bot_fast.prn
echo %first_line% >> c:\wlef\data\logs\bot_fast.log 
set /p first_line=<bot_slow.prn
echo %first_line% >> c:\wlef\data\logs\bot_slow.log 

:: CHANGE CASE/REMOVE EXTENSION AND ZIP FILES 
:: Note: an alternative is to use zip-7, which allows archieving and can be opened with unzip on linux; www.7-zip.org)
echo Renaming and zipping bot files...
ren "bot_FAST.PRN" bot_fast%yyyymmddhhnn%
ren "bot_SLOW.PRN" bot_slow%yyyymmddhhnn%
gzip bot*

:: COPY TO HD AND USB FLASH DRIVE
:: Note: mkdir commands maybe redundant, as directories may already exist
:: will wait 120 seconds if can't find usb drive immediately (e.g., if being exchanged)  
:: allows removeable media with disk drive letter w:\ or z:\ (because cannot be same letter)  
echo Transfering bot files to archive and removable media...
if not exist w:\ sleep 60
mkdir w:\%yyyymmdd%
copy /Y bot*.gz w:\%yyyymmdd%
if not exist z:\ sleep 60
mkdir z:\%yyyymmdd%
copy /Y bot*.gz z:\%yyyymmdd%
: scp files to flux.aos.wisc.edu:/data/incoming/wlef
pscp -l jthom -pw "W1EFRl0G!" bot*.gz flux.aos.wisc.edu:/data/incoming/wlef/.
: save files to archive on C:\
mkdir c:\wlef\data\archive\%yyyymmdd%
move /Y bot*.gz c:\wlef\data\archive\%yyyymmdd%
