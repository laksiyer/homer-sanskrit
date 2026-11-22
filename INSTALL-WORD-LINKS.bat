@echo off
cd /d "%~dp0"
python scripts\install_word_links.py
if errorlevel 1 (
 echo Installation stopped. Please copy the error message.
) else (
 echo Done. Open site\index.html and test Sanskrit word links.
)
pause
