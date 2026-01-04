@echo off
setlocal enabledelayedexpansion
title MP3 TURBO INSTALLER

echo ==========================================
echo      MP3 TURBO V2.1 - AUTO INSTALLER
echo ==========================================
echo.

:: 1. Dapatkan Path Folder Sekarang
set "CURRENT_DIR=%~dp0"
:: Buang backslash di hujung path
set "CURRENT_DIR=%CURRENT_DIR:~0,-1%"

:: 2. Cipta mp4.bat (Overwrite jika sedia ada)
echo [*] Mencipta mp4.bat di lokasi semasa...
(
echo @echo off
echo python "%CURRENT_DIR%\main.py" %%*
) > "mp4.bat"

:: 3. Update Environment Variable PATH (REPLACE/FORCE)
:: Kita guna PowerShell sebab lebih selamat untuk edit Registry PATH
echo [*] Mengemaskini Environment Variable PATH...
powershell -Command ^
    "$currentDir = '%CURRENT_DIR%';" ^
    "$oldPath = [Environment]::GetEnvironmentVariable('Path', 'User');" ^
    "$pathList = $oldPath.Split(';', [System.StringSplitOptions]::RemoveEmptyEntries) | Where-Object { $_ -ne $currentDir };" ^
    "$newPath = ($pathList + $currentDir) -join ';';" ^
    "[Environment]::SetEnvironmentVariable('Path', $newPath, 'User');"

if %errorlevel% equ 0 (
    echo [+] PATH berjaya dikemaskini.
) else (
    echo [!] Gagal mengemaskini PATH. Sila run sebagai Admin jika perlu.
)

:: 4. Selesai
echo.
echo ==========================================
echo [OK] INSTALLATION SELESAI!
echo ==========================================
echo 1. Sila TUTUP CMD ini.
echo 2. Buka CMD baru dan taip 'mp4'.
echo ==========================================
pause