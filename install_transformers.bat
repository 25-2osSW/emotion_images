@echo off
REM Set the current directory to the script's location
REM This ensures it runs correctly regardless of where the user installs WebUI
cd /d "%~dp0"

echo ========================================================
echo [System] Starting PyTorch (CPU) installation...
echo (This may take a few minutes depending on internet speed)
echo ========================================================

REM Check if the portable environment exists
if not exist "portable_env\python.exe" (
    echo [Error] 'portable_env' folder not found!
    echo Current Path: %cd%
    echo.
    echo [Solution] Please make sure this file is placed in the
    echo ROOT folder of Text Generation WebUI.
    echo (It should be next to 'start_windows.bat')
    pause
    exit
)

REM Install PyTorch (CPU version) to save space and ensure compatibility
echo [Installing] Installing torch (CPU version)...
"portable_env\python.exe" -m pip install torch --index-url https://download.pytorch.org/whl/cpu

REM Update Transformers library
echo [Installing] Updating transformers library...
"portable_env\python.exe" -m pip install transformers

echo.
echo ========================================================
echo [Success] Installation complete!
echo You can now close this window and run start_windows.bat
echo ========================================================
pause