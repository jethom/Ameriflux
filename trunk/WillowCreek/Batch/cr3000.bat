:: March 12, 2010
:: movefiles.bat will move, rename and compress data files from the different CSI stations at WillowCreek
:: this will be run at the end of each day

@echo off
setlocal

:: move to the primary data directory
cd "c:\Documents and Settings\Willow Creek\Desktop\Data\CR3000"

if %time:~0,2% lss 10 (
set dtF=%date:~-4%%date:~4,2%%date:~7,2%0%time:~1,1%%time:~3,2%
) else (
set dtF=%date:~-4%%date:~4,2%%date:~7,2%%time:~0,2%%time:~3,2%
)

mkdir "%dtF%"

::move C:\Campbellsci\Loggernet\CR3000*.dat "%dtF%\."

start "CR3000Copy" /MIN pscp -p -r "%dtF%" jthom@flux.aos.wisc.edu:/data/incoming/WillowCreek/current/CR3000/.

 
