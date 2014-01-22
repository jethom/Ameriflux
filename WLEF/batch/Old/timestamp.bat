:: CREATE DAILY DIRECTORY AND RECORD INTERVAL START USING PC DATE/TIME
:: This program is invoked at the start of the 30 min data acquisition
:: Written by Bruce Cook
:: Last modified May 2006

@echo off
setlocal

:: SET WORKING DIRECTORY
cd \wlef\data\temp

:: RAW INPUTS
echo yyyy = %date:~10,4%
echo mm = %date:~4,2% 
echo dd = %date:~7,2% 
echo hh = %time:~0,2%
echo min = %time:~3,2%

:: MOVE PREVIOUS TIME STAMP FILES 
:: Note: Previous time stamps will be used to rename files
move /Y current_yyyymmdd.txt yyyymmdd.txt
move /Y current_yyyymmddhhnn.txt yyyymmddhhnn.txt

:: MAKE DAILY DIRECTORY AND SAVE TIME STAMP TO FILE
mkdir c:\wlef\data\archive\%date:~10,4%%date:~4,2%%date:~7,2%
mkdir w:\%date:~10,4%%date:~4,2%%date:~7,2%
echo %date:~10,4%%date:~4,2%%date:~7,2% >> current_yyyymmdd.txt

:: SAVE FILE TIME STAMP TO FILE
:: Note: hour range from 0 to 23 (1 and 2 digit)
if %time:~0,2% lss 10 (
  echo %date:~10,4%%date:~4,2%%date:~7,2%0%time:~1,1%%time:~3,2% >> current_yyyymmddhhnn.txt
) else (
  echo %date:~10,4%%date:~4,2%%date:~7,2%%time:~0,2%%time:~3,2% >> current_yyyymmddhhnn.txt
)