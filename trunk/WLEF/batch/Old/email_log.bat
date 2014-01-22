:: EMAILS LOG CONTAINING FIRST LINE OF EACH HOURLY DATA FILE TO EDDY ON A DAILY BASIS
:: EMAILS WARNINGS IF NO DATA FROM STATION
::
:: Written by Bruce Cook
:: Last modified: July 2007

@echo off
setlocal

:: SET WORKING DIRECTORY
cd \wlef\data\logs

:: RETRIEVE TIME STAMP (START OF INTERVAL BASED ON PC CLOCK)
FOR /F %%t IN (c:\wlef\data\temp\yyyymmdd.txt) do (set yyyymmdd=%%t)

:: CONCATONATE HEADERS AND LOGS INTO ONE FILE
:: Note: first echo will create new file (">"), while others will append (">>")
echo Concatonating records...
echo DATE:  %yyyymmdd% > log.txt
cat top_fast.hdr top_fast.log top_slow.hdr top_slow.log >> log.txt
cat mid_fast.hdr mid_fast.log mid_slow.hdr mid_slow.log >> log.txt 
cat bot_fast.hdr bot_fast.log bot_slow.hdr bot_slow.log >> log.txt
cat trailer.hdr trailer.log >> log.txt
cat surf_met.hdr surf_met.log >> log.txt

:: CHANGE CASE, ADD TIME STAMP
:: echo Renaming files...
:: ren "LOG" log%yyyymmdd%

:: CONNECT TO INTERNET, WAITING 60 SECS AND REDIALING UP TO 5X IF NECESSARY
:: rasup.exe is a C code that detects a ras connection, and must be in the system path
:: echo Connecting to internet...
date /t >> c:\wlef\programs\batch\internet.log
time /t >> c:\wlef\programs\batch\internet.log
:: rasdial "U of MN PPP Connection" cookx005 wuyang1! >> c:\wlef\programs\batch\internet.log
:: rasup
:: if %errorlevel% equ 1 goto done
:: rasdial /disconnect
:: sleep 30
:: rasdial "U of MN PPP Connection" cookx005 wuyang1! >> c:\wlef\programs\batch\internet.log
:: rasup
:: if %errorlevel% equ 1 goto done
:: rasdial /disconnect
:: sleep 30
:: rasdial "U of MN PPP Connection" cookx005 wuyang1! >> c:\wlef\programs\batch\internet.log
:: sleep 30
:: rasup
:: if %errorlevel% equ 1 goto done
:: rasdial /disconnect
:: sleep 30
:: rasdial "U of MN PPP Connection" cookx005 wuyang1! >> c:\wlef\programs\batch\internet.log
:: rasup
:: if %errorlevel% equ 1 goto done
:: rasdial /disconnect
:: sleep 30
:: rasdial "U of MN PPP Connection" cookx005 wuyang1! >> c:\wlef\programs\batch\internet.log
:: :done
:: 
:: USE MAILSEND TO SEND LOG TO METEO ACCOUNT
::mailsend15b -d umn.edu -smtp smtp.umn.edu -f cookx005@umn.edu -name WLEF -sub "WLEF Daily Report" -t cookx005@umn.edu,desai@aos.wisc.edu,jthom@ssec.wisc.edu,twh142@psu.edu +cc +bc -starttls -auth -user cookx005 -pass wuyang1! < c:\wlef\data\logs\log.txt
mailsend15b -d centurytel.net -smtp smtpauth.centurytel.net -f udcn@centurytel.net -name WLEF -sub "WLEF Daily Report" -t cookx005@umn.edu,desai@aos.wisc.edu,jthom@ssec.wisc.edu,twh142@psu.edu,bnsulman@wisc.edu +cc +bc -starttls -auth -user udcn -pass W1EFRl0G! < c:\wlef\data\logs\log.txt

:: EMAIL WARNINGS IF STATION ISN'T REPORTING
if not exist c:\wlef\data\archive\%yyyymmdd%\top*.gz (
::  mailsend15b -d umn.edu -smtp smtp.umn.edu -f cookx005@umn.edu -name WLEF -sub !WARNING! -t cookx005@umn.edu,desai@aos.wisc.edu,jthom@ssec.wisc.edu,twh142@psu.edu +cc +bc -starttls -auth -user cookx005 -pass wuyang1! -M "WLEF TOP BOX NOT REPORTING"
  mailsend15b -d centurytel.net -smtp smtpauth.centurytel.net -f udcn@centurytel.net -name WLEF -sub !WARNING! -t cookx005@umn.edu,desai@aos.wisc.edu,shelleyk@ssec.wisc.edu,jthom@ssec.wisc.edu,twh142@psu.edu,bnsulman@wisc.edu +cc +bc -starttls -auth -user udcn -pass W1EFRl0G! -M "WLEF TOP BOX NOT REPORTING"
)
if not exist c:\wlef\data\archive\%yyyymmdd%\mid*.gz (
 :: mailsend15b -d umn.edu -smtp smtp.umn.edu -f cookx005@umn.edu -name WLEF -sub !WARNING! -t cookx005@umn.edu,desai@aos.wisc.edu,jthom@ssec.wisc.edu,twh142@psu.edu +cc +bc -starttls -auth -user cookx005 -pass wuyang1! -M "WLEF MID BOX NOT REPORTING"
  mailsend15b -d centurytel.net -smtp smtpauth.centurytel.net -f udcn@centurytel.net -name WLEF -sub !WARNING! -t cookx005@umn.edu,desai@aos.wisc.edu,jthom@ssec.wisc.edu,twh142@psu.edu,bnsulman@wisc.edu +cc +bc -starttls -auth -user udcn -pass W1EFRl0G! -M "WLEF MID BOX NOT REPORTING"
)
if not exist c:\wlef\data\archive\%yyyymmdd%\bot*.gz (
 :: mailsend15b -d umn.edu -smtp smtp.umn.edu -f cookx005@umn.edu -name WLEF -sub !WARNING! -t cookx005@umn.edu,desai@aos.wisc.edu,jthom@ssec.wisc.edu,twh142@psu.edu +cc +bc -starttls -auth -user cookx005 -pass wuyang1! -M "WLEF BOT BOX NOT REPORTING"
  mailsend15b -d centurytel.net -smtp smtpauth.centurytel.net -f udcn@centurytel.net -name WLEF -sub !WARNING! -t cookx005@umn.edu,desai@aos.wisc.edu,jthom@ssec.wisc.edu,twh142@psu.edu,bnsulman@wisc.edu +cc +bc -starttls -auth -user udcn -pass W1EFRl0G! -M "WLEF BOT BOX NOT REPORTING"
)
if not exist c:\wlef\data\archive\%yyyymmdd%\trailer*.gz (
 :: mailsend15b -d umn.edu -smtp smtp.umn.edu -f cookx005@umn.edu -name WLEF -sub !WARNING! -t cookx005@umn.edu,desai@aos.wisc.edu,jthom@ssec.wisc.edu,twh142@psu.edu +cc +bc -starttls -auth -user cookx005 -pass wuyang1! -M "WLEF TRAILER LICORS NOT REPORTING"
  mailsend15b -d centurytel.net -smtp smtpauth.centurytel.net -f udcn@centurytel.net -name WLEF -sub !WARNING! -t cookx005@umn.edu,desai@aos.wisc.edu,jthom@ssec.wisc.edu,twh142@psu.edu,bnsulman@wisc.edu +cc +bc -starttls -auth -user udcn -pass W1EFRl0G! -M "WLEF TRAILER LICORS NOT REPORTING"
)
if not exist c:\wlef\data\archive\%yyyymmdd%\surf_met*.gz (
 :: mailsend15b -d umn.edu -smtp smtp.umn.edu -f cookx005@umn.edu -name WLEF -sub !WARNING! -t cookx005@umn.edu,desai@aos.wisc.edu,jthom@ssec.wisc.edu,twh142@psu.edu +cc +bc -starttls -auth -user cookx005 -pass wuyang1! -M "WLEF SURFACE MET NOT REPORTING"
  mailsend15b -d centurytel.net -smtp smtpauth.centurytel.net -f udcn@centurytel.net -name WLEF -sub !WARNING! -t cookx005@umn.edu,desai@aos.wisc.edu,jthom@ssec.wisc.edu,twh142@psu.edu,bnsulman@wisc.edu +cc +bc -starttls -auth -user udcn -pass W1EFRl0G! -M "WLEF SURFACE MET NOT REPORTING"
)

:: RESET COMPUTER CLOCK TO NIST SERVER
echo Setting pc to NIST clock...
net time /setsntp:time-a.nist.gov  >> c:\wlef\programs\batch\internet.log
net stop w32time >> c:\wlef\programs\batch\internet.log
w32tm /unregister >> c:\wlef\programs\batch\internet.log
w32tm /unregister >> c:\wlef\programs\batch\internet.log
w32tm /register >> c:\wlef\programs\batch\internet.log
net start w32time >> c:\wlef\programs\batch\internet.log

:: DISCONNECT FROM INTERNET
:: Note: 30 sec "sleep" is incorporated to allow Norton email scan and email processes to finish
:: sleep 60
:: echo Disconnecting from U OF MN PPP CONNECTION...
:: rasdial /disconnect

:: DELETE STATION LOGS
del *.log