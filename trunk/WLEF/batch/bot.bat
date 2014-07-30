@echo off
setlocal

if %time:~0,2% lss 10 (
if %time:~3,2% lss 30 (
set dtF=%date:~-4%_%date:~4,2%\%date:~7,2%\0%time:~1,1%00
) else (
set dtF=%date:~-4%_%date:~4,2%\%date:~7,2%\0%time:~1,1%30
)
) else (
if %time:~3,2% lss 30 (
set dtF=%date:~-4%_%date:~4,2%\%date:~7,2%\%time:~0,2%00
) else (
set dtF=%date:~-4%_%date:~4,2%\%date:~7,2%\%time:~0,2%30
)
)
cd c:\Campbellsci\Loggernet

mkdir C:\Users\Flux\Documents\WLEF\ArchiveData\FluxData\%dtF%\bot

move bot*.dat C:\Users\Flux\Documents\WLEF\ArchiveData\FluxData\%dtF%\bot
 

rem cd C:\Users\Flux\Documents\WLEF\ArchiveData\FluxData\%dtF%\bot\.

rem start /wait 7z a -ttar bot_slow_%dtF%.tar bot_slow*.dat
rem start /wait 7z a -tgzip bot_slow_%dtF%.tar.gz bot_slow_%dtF%.tar
rem start /wait 7z a -ttar bot_fast_%dtF%.tar bot_fast*.dat
rem start /wait 7z a -tgzip bot_fast_%dtF%.tar.gz bot_fast_%dtF%.tar
 


