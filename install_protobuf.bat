@echo off
REM Set the current directory to the script's location
cd /d "%~dp0"

echo ========================================================
echo [System] Installing dependencies for Emotion Analysis
echo (Target: protobuf, sentencepiece)
echo ========================================================

REM Check if the portable environment exists
if exist "portable_env\python.exe" (
    echo [Check] WebUI environment found.
    echo [Installing] Installing libraries... Please wait.
    
    REM Install the required packages
    "portable_env\python.exe" -m pip install protobuf sentencepiece
    
    echo.
    echo ========================================================
    echo [Success] Installation complete!
    echo You can now close this window and run start_windows.bat
    echo ========================================================
) else (
    echo [Error] 'portable_env' folder not found!
    echo.
    echo [Solution] Please make sure this file is placed in the
    echo ROOT folder of Text Generation WebUI.
    echo (It should be next to 'start_windows.bat')
)

pause