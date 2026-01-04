@echo off
title MP3 TURBO INSTALLER
color 0A

:: Paparan Intro
echo ==========================================
echo      MP3 TURBO V2.1 - INSTALLATION
echo ==========================================
echo.
echo [*] Sedang mengesan Python...

:: Check kalau user ada Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [!] ERROR: Python tidak dijumpai!
    echo [!] Sila install Python dahulu sebelum guna tool ini.
    echo.
    pause
    exit
)

:: Jalankan script install.py yang power tadi
echo [*] Python dikesan. Memulakan setup environment...
echo.
python install.py

echo.
echo ==========================================
echo [OK] Setup Selesai! Boleh tutup window ini.
echo ==========================================
pause