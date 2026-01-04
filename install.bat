@echo off
setlocal
title MP3 TURBO INSTALLER

:: Dapatkan path folder sekarang
set "PROJ_PATH=%~dp0"
set "PROJ_PATH=%PROJ_PATH:~0,-1%"

echo [*] Menetapkan mp4.bat...
(
echo @echo off
echo python "%%~dp0main.py" %%*
) > "mp4.bat"

echo [*] Menambah folder ke Windows PATH...
:: Menggunakan PowerShell untuk update PATH tanpa merosakkan data sedia ada
powershell -Command ^
    "$path = [Environment]::GetEnvironmentVariable('Path', 'User');" ^
    "if($path -notlike '*%PROJ_PATH%*') {" ^
    "  [Environment]::SetEnvironmentVariable('Path', \"$path;%PROJ_PATH%\", 'User');" ^
    "  Write-Host '[+] PATH berjaya dikemaskini.' -ForegroundColor Green;" ^
    "} else { Write-Host '[*] Path sudah wujud.' -ForegroundColor Yellow; }"

echo.
echo ==========================================
echo [OK] Selesai! Sila buka CMD baru dan taip: mp4
echo ==========================================
pause