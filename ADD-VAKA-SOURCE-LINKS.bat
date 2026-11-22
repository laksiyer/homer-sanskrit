@echo off
cd /d "%~dp0"
py -3 ADD-VAKA-SOURCE-LINKS.py
if errorlevel 1 python ADD-VAKA-SOURCE-LINKS.py
pause
