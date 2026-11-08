@echo off
setlocal EnableExtensions
cd /d "%~dp0"
if not exist "%~dp0app.py" (echo ERROR: app.py missing & goto :failed)
if not exist "%~dp0requirements-build.txt" (echo ERROR: requirements-build.txt missing & goto :failed)
set "PY=py -3"
py -3 --version >nul 2>&1
if errorlevel 1 (
    set "PY=python"
    python --version >nul 2>&1
    if errorlevel 1 (echo ERROR: Python not found & goto :failed)
)
%PY% -m pip install -r "%~dp0requirements-build.txt"
if errorlevel 1 goto :failed
%PY% "%~dp0build_exe.py"
if errorlevel 1 goto :failed
echo Windows EXE folder created in Documents\QuickPhotoViewerBuild\dist\QuickPhotoViewer
if /i "%~1"=="/nopause" exit /b 0
pause
exit /b 0
:failed
if /i "%~1"=="/nopause" exit /b 1
pause
exit /b 1
