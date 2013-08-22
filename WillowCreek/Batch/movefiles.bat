:: March 12, 2010
:: movefiles.bat will move, rename and compress data files from the different CSI stations at WillowCreek
:: this will be run at the end of each day

@echo off
setlocal

:: move to the primary data directory
cd c:\Documents and Settings\Willow Creek\Desktop\Data

:: get the date information to rename files 
set yyyy=%date:~10,4%
set mm=%date:~4,2%
set dd=%date:~7,2%
set /a ddm1=%dd% - 1

:: Move the data files to the Data directory
move /y C:\CampbellSci\Loggernet\*.dat .


:: Rename the files

::profile
ren Profile_final_storage_1.dat Profile1_%yyyy%%mm%%ddm1%.dat
ren Profile_final_storage_2.dat Profile2_%yyyy%%mm%%ddm1%.dat

:: Flux data files
ren Flux_final_storage_1.dat Flux1_%yyyy%%mm%%ddm1%.dat
ren Flux_final_storage_2.dat Flux2_%yyyy%%mm%%ddm1%.dat

:: Handar data File
ren Handar_final_storage_1.dat Handar_%yyyy%%mm%%ddm1%.dat

:: GZIP the files
::gzip -afqv1 Profile1_%yyyy%%mm%%ddm1%.dat
::gzip -afqv1 Profile2_%yyyy%%mm%%ddm1%.dat

::gzip -afqv1 Flux1_%yyyy%%mm%%ddm1%.dat
::gzip -afqv1 Flux2_%yyyy%%mm%%ddm1%.dat

::gzip -afqv1 Handar_%yyyy%%mm%%ddm1%.dat



