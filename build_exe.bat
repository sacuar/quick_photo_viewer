@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title Quick Photo Viewer - Windows Build
if not exist "app.py" (
 echo ERROR: app.py is missing from %CD%
 goto :failed
)
if not exist "requirements-build.txt" (
 echo ERROR: requirements-build.txt missing. Extract the entire ZIP.
 goto :failed
)
set "PY_CMD=py -3"
py -3 --version >nul 2>&1
if errorlevel 1 (
 set "PY_CMD=python"
 python --version >nul 2>&1
 if errorlevel 1 goto :failed
)
%PY_CMD% -m pip install -r "%~dp0requirements-build.txt"
if errorlevel 1 goto :failed
%PY_CMD% "%~dp0build_exe.py"
if errorlevel 1 goto :failed
echo Build completed in Documents\QuickPhotoViewerBuild.
pause
exit /b 0
:failed
echo Build failed. See error above.
pause
exit /b 1
