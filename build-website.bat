@echo off
setlocal
cd /d "%~dp0"
py -3 scripts\build.py
if errorlevel 1 (
  echo.
  echo Build failed. If the Python launcher is unavailable, try:
  echo python scripts\build.py
  pause
  exit /b 1
)
echo.
echo Website updated: site\index.html
pause
