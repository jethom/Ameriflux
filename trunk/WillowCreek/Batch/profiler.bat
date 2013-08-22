:: March 12, 2010
:: profiler.bat will move, rename and compress data files from the different CSI stations at WillowCreek
:: this will be run at the end of each day

@echo off
setlocal

:: move to the primary data directory
cd c:\Documents and Settings\Willow Creek\Desktop\Data\profiler

if %time:~0,2% lss 10 (
set dtF=%date:~-4%%date:~4,2%%date:~7,2%0%time:~1,1%00
) else (
set dtF=%date:~-4%%date:~4,2%%date:~7,2%%time:~0,2%00
)

md %dtF%

:: move C:\Campbellsci\Loggernet\Profile*.dat %dtF%\.

start "ProfilerCopy" /MIN pscp -p -r %dtF% jthom@flux.aos.wisc.edu:/data/incoming/WillowCreek/current/profiler/.

