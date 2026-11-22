@echo off
cd /d "%~dp0"
py -3 fix-bow-note.py
if errorlevel 1 python fix-bow-note.py
pause
