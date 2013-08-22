:: UPLOADS FIRST LINE OF EACH HOURLY DATA FILE TO EDDY ON A DAILY BASIS
::
:: Written by Bruce Cook
:: Last modified: May 2006
:: NOTE: NEVER TESTED IN FIELD!!

@echo off
setlocal

:: SET WORKING DIRECTORY
cd \wlef\data\temp

:: RETRIEVE TIME STAMP (START OF INTERVAL BASED ON PC CLOCK)
FOR /F %%t IN (yyyymmdd.txt) do (set yyyymmdd=%%t)

:: CONCATONATE HEADERS AND LOGS INTO ONE FILE
cat c:\wlef\headers\top_fast.hdr top_fast.log c:\wlef\headers\top_slow.hdr top_slow.log > log 
cat c:\wlef\headers\mid_fast.hdr mid_fast.log c:\wlef\headers\mid_slow.hdr mid_slow.log > log 
cat c:\wlef\headers\bot_fast.hdr bot_fast.log c:\wlef\headers\bot_slow.hdr bot_slow.log > log 
cat c:\wlef\headers\trailer.hdr trailer.log > log
cat c:\wlef\headers\surf_met.hdr surf_met.log > log

:: CHANGE CASE, ADD TIME STAMP, AND ZIP FILES 
:: Note: an alternative is to use zip-7, which allows archieving and can be opened with unzip on linux; www.7-zip.org)
echo Renaming and zipping top files...
ren "LOG" log%yyyymmdd%
gzip log*

:: CONNECT TO INTERNET
rasdial "U of MN PPP Connection" cookx005 wuyang1

:: USE WINSCP TO UPLOAD LOG TO EDDY
winscp3.exe /console /script=ftpscript.txt

:: DISCONNECT FROM INTERNET
rasdial /disconnect

:: DELETE LOGS
del *.log
del log*.gz
