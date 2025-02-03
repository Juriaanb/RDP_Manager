@echo off
REM run.bat - Start the RDP Dashboard Flask app

REM Check if Python is available
python --version
if errorlevel 1 (
    echo "Python not found. Please install Python 3 first."
    pause
    exit /b 1
)

REM Install requirements (optional, can be removed)
echo Installing Python dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

REM Start the Flask app
echo Starting RDP Dashboard...
python app.py

pause
