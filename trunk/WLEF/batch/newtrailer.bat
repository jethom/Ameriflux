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

mkdir C:\Users\Flux\Documents\WLEF\ArchiveData\Data\%dtF%
dir

::rename trailer_final_storage_1.dat trailer_final_storage_%dtF%.dat

move newtrailer_*.dat C:\Users\Flux\Documents\WLEF\ArchiveData\Data\%dtF%


::cd C:\Users\Flux\Documents\WLEF\ArchiveData\FluxData\%dtF%\trailer

:: start /wait 7z a -tgzip trailer_final_storage_%dtF%.dat.gz trailer_final_storage_%dtF%.dat


:: del trailer*.dat