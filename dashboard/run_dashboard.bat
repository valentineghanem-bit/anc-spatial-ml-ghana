@echo off
REM Windows launcher -- ANC Fertility Dashboard
cd /d "%~dp0"
echo Starting ANC Fertility Dashboard...
echo Open http://127.0.0.1:8050 in your browser
start "" "http://127.0.0.1:8050"
timeout /t 1 /nobreak >nul
python app.py
pause
