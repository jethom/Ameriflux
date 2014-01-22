:@echo off

:: RETRIEVE TIME STAMP (START OF INTERVAL BASED ON PC CLOCK)
:FOR /F %%t IN (c:\wlef\data\temp\yyyymmdd.txt) do (set yyyymmdd=%%t)

:if not exist c:\wlef\data\archieve\%yyyymmdd%\mid*.gz (
:  echo !WARNING! WLEF TOP BOX NOT REPORTING
:)
: scp data to flux.aos.wisc.edu:/data/incoming/wlef
pscp -l jthom -pw "W1EFRl0G!" email_log.bat flux.aos.wisc.edu:/data/incoming/wlef/.