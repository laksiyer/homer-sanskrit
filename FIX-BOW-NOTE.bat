@echo off
cd /d "%~dp0"
py -3 scripts\fix_bow_note.py
if errorlevel 1 (
  echo.
  echo The repair did not complete. Please send the error shown above.
  pause
  exit /b 1
)
echo.
echo Success! Commit and Push origin using GitHub Desktop.
pause
