@echo off
cd /d "%~dp0"
python INSTALL-VAKA.py
if errorlevel 1 (pause & exit /b 1)
call build-website.bat
pause
