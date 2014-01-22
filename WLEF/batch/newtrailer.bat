@echo off
setlocal

cd C:\Campbellsci\Loggernet

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

mkdir C:\Users\Flux\Documents\WLEF\ArchiveData\FluxData\%dtF%\newtrailer
dir

::rename trailer_final_storage_1.dat trailer_final_storage_%dtF%.dat

move newtrailer_*.dat C:\Users\Flux\Documents\WLEF\ArchiveData\FluxData\%dtF%\newtrailer


::cd C:\Users\Flux\Documents\WLEF\ArchiveData\FluxData\%dtF%\trailer

:: start /wait 7z a -tgzip trailer_final_storage_%dtF%.dat.gz trailer_final_storage_%dtF%.dat


:: del trailer*.dat