@echo off
setlocal EnableExtensions
cd /d "%~dp0"
call "%~dp0build_exe.bat" /nopause
if errorlevel 1 goto :failed
set "BUILD=%USERPROFILE%\Documents\QuickPhotoViewerBuild\dist\QuickPhotoViewer"
if not exist "%BUILD%\QuickPhotoViewer.exe" (
 echo ERROR: Missing application executable in %BUILD%
 goto :failed
)
set "ISCC=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if not exist "%ISCC%" set "ISCC=%ProgramFiles%\Inno Setup 6\ISCC.exe"
if not exist "%ISCC%" (
 echo ERROR: Inno Setup 6 compiler not found. Install Inno Setup first.
 goto :failed
)
"%ISCC%" /DBuildOutput="%BUILD%" "%~dp0installer\QuickPhotoViewer.iss"
if errorlevel 1 goto :failed
echo.
echo Installer created in %~dp0installer\output
if /i "%~1"=="/nopause" exit /b 0
pause
exit /b 0
:failed
echo.
echo Installer build failed; nothing was installed or registered.
if /i "%~1"=="/nopause" exit /b 1
pause
exit /b 1
