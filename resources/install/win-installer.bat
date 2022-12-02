@echo off

echo "Building for windows"
COPY  "install\win\installer.cfg" "win-build.tmp"
pynsist.exe "win-build.tmp"

@REM  read installer_name value from installer.cfg
FOR /F "tokens=2 delims==" %%a IN ('findstr /i "installer_name" "win-build.tmp"') DO SET installer_name=%%a
mkdir "out\"

@REM copy installer to dist folder
move "build\nsis\%installer_name%" "out\%installer_name%"
call install\win\sha256.bat "out\%installer_name%" sha256
echo %sha256% > "out\%installer_name%.sha256.txt"
DEL  "win-build.tmp"
