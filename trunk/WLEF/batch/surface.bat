@echo off
setlocal

cd C:\Campbellsci\Loggernet

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

:: rename surface_final_storage_1.dat surface_final_storage_%dtF%.dat
mkdir C:\Users\Flux\Documents\WLEF\ArchiveData\FluxData\%dtF%\surface

move surface_final_storage_1.dat C:\Users\Flux\Documents\WLEF\ArchiveData\FluxData\%dtF%\surface

cd C:\Users\Flux\Documents\WLEF\ArchiveData\FluxData\%dtF%\surface

:: start /wait 7z a -tgzip surface_final_storage_%dtF%.dat.gz surface_final_storage_%dtF%.dat

rem start pscp -p surface_final_storage_%dtF%.dat.gz jthom@flux.aos.wisc.edu:/data/incoming/WLEF_IN/surface/.

:: del surface*.dat