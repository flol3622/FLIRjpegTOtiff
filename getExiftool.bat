@echo off
REM download exiftool from https://exiftool.org/
powershell -Command "& { (New-Object Net.WebClient).DownloadFile('https://exiftool.org/exiftool-12.79.zip', 'exiftool-12.79.zip') }"


REM extract exiftool(-k).exe to the same folder as this batch file
powershell -command "& { Expand-Archive -Path ExifTool-12.79.zip -DestinationPath . -Force }"

REM and rename it to exiftool.exe
rename "exiftool(-k).exe" "exiftool.exe"
del ExifTool-12.79.zip
