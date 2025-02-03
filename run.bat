@echo off
REM run.bat - Start de RDP Dashboard Flask-app

REM Controleer of Python aanwezig is
python --version
if errorlevel 1 (
    echo "Python is niet gevonden. Installeer eerst Python 3."
    pause
    exit /b 1
)

REM Eventueel requirements installeren (optioneel, kun je ook weglaten)
echo Installing Python dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

REM Start de Flask-app
echo Starting RDP Dashboard...
python app.py

pause
