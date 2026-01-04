@echo off
setlocal
title Ultimate Downloader Installer (Setup Wizard)
color 0b
cls

echo ===============================================================================
echo                        ULTIMATE DOWNLOADER SETUP WIZARD
echo ===============================================================================
echo.
echo  [SYSTEM CHECK] Verifying system requirements...

:: --- PHASE 1: PYTHON DETECTION & AUTO-INSTALL ---
python --version >nul 2>&1
if %errorlevel% neq 0 (
    goto :python_missing
) else (
    echo  [CHECK] Python is already installed.
    goto :install_libs
)

:python_missing
color 0e
echo.
echo  [WARNING] Python was not found on this system.
echo  This software requires Python to function correctly.
echo.
echo  Would you like to automatically download and install Python now?
set /p py_consent=" [Y/N]: "

if /i "%py_consent%" neq "y" (
    color 0c
    echo.
    echo  [ERROR] Installation aborted. Python is required.
    pause
    exit /b
)

echo.
echo  [STEP 1/2] Downloading Python Installer...
:: Downloading Python 3.11 (Stable)
curl -L -o python_installer.exe https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe

echo.
echo  [STEP 2/2] Installing Python... (This window may pause, please wait)
echo  [INFO] Installing with 'Add to PATH' enabled...
:: /passive shows progress bar but requires no clicks. PrependPath=1 fixes the 'pip' error.
start /wait python_installer.exe /passive PrependPath=1

echo.
echo  [CLEANUP] Removing installer file...
del python_installer.exe

color 0a
echo.
echo ===============================================================================
echo   PYTHON INSTALLED SUCCESSFULLY!
echo ===============================================================================
echo.
echo  [IMPORTANT]
echo  Windows needs to refresh to recognize the new Python installation.
echo.
echo  PLEASE CLOSE THIS WINDOW AND RUN 'install.bat' AGAIN.
echo.
pause
exit

:: --- PHASE 2: LIBRARY INSTALLATION ---
:install_libs
color 0b
echo.
echo -------------------------------------------------------------------------------
echo  [PHASE 2] Installing Dependencies
echo -------------------------------------------------------------------------------
echo  [INFO] Installing 'yt-dlp' engine...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo  [ERROR] Failed to install libraries. Please try running as Administrator.
    pause
    exit /b
)

:: --- PHASE 3: FFMPEG SETUP ---
echo.
echo -------------------------------------------------------------------------------
echo  [PHASE 3] FFmpeg Configuration
echo -------------------------------------------------------------------------------

if exist ffmpeg.exe (
    echo  [CHECK] FFmpeg is already installed. Skipping...
) else (
    echo  [INFO] FFmpeg not found. Downloading latest build...
    curl -L -o ffmpeg_temp.zip https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
    
    echo  [INFO] Extracting files...
    tar -xf ffmpeg_temp.zip
    
    echo  [INFO] Configuring FFmpeg...
    cd ffmpeg-*-essentials\bin
    move ffmpeg.exe ..\..\ >nul
    cd ..\..\
    
    echo  [CLEANUP] Removing temporary files...
    del ffmpeg_temp.zip
    for /d %%d in (ffmpeg-*-essentials) do rmdir /s /q "%%d"
    echo  [SUCCESS] FFmpeg downloaded and configured.
)

:: --- PHASE 4: SHORTCUT & PATH ---
echo.
echo -------------------------------------------------------------------------------
echo  [PHASE 4] System Integration
echo -------------------------------------------------------------------------------

:: Remove old launcher if exists
if exist mp3.bat del mp3.bat

:: Create 'mp4' launcher
(
echo @echo off
echo python "%%~dp0main.py" %%*
) > mp4.bat
echo  [INFO] Global command 'mp4' created.

:: Add to Windows Path
echo  [INFO] Registering software to Windows Path...
powershell -Command "$oldPath = [Environment]::GetEnvironmentVariable('Path', 'User'); $currentDir = '%CD%'; if ($oldPath -notlike *"$currentDir"*) { [Environment]::SetEnvironmentVariable('Path', $oldPath + ';' + $currentDir, 'User'); Write-Host ' [SUCCESS] Path updated successfully.' -ForegroundColor Green } else { Write-Host ' [CHECK] Path already configured.' -ForegroundColor Yellow }"

:: --- FINALIZATION ---
color 0a
echo.
echo ===============================================================================
echo                        INSTALLATION COMPLETE
echo ===============================================================================
echo.
echo  How to use:
echo  1. Close this window.
echo  2. Open a new Command Prompt (CMD).
echo  3. Type 'mp4' anywhere to launch the tool.
echo.
pause

:: Done