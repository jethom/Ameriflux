@echo off
setlocal

if %time:~0,2% lss 10 (
if %time:~3,2% lss 30 (
set dtF=%date:~-4%_%date:~4,2%_%date:~7,2%_0%time:~1,1%_00
) else (
set dtF=%date:~-4%_%date:~4,2%_%date:~7,2%_0%time:~1,1%_30
)
) else (
if %time:~3,2% lss 30 (
set dtF=%date:~-4%_%date:~4,2%_%date:~7,2%_%time:~0,2%_00
) else (
set dtF=%date:~-4%_%date:~4,2%_%date:~7,2%_%time:~0,2%_30
)
)

cd C:\Campbellsci\Loggernet
mkdir C:\Users\Flux\Documents\WLEF\ArchiveData\FluxData\%dtF%\top


move top*.dat C:\Users\Flux\Documents\WLEF\ArchiveData\FluxData\%dtF%\top

rem cd C:\Users\Flux\Documents\WLEF\ArchiveData\FluxData\%dtF%\top\.

rem start /wait 7z a -ttar top_slow_%dtF%.tar top_slow*.dat
rem start /wait 7z a -tgzip top_slow_%dtF%.tar.gz top_slow_%dtF%.tar
rem start /wait 7z a -ttar top_fast_%dtF%.tar top_fast*.dat
rem start /wait 7z a -tgzip top_fast_%dtF%.tar.gz top_fast_%dtF%.tar
 

