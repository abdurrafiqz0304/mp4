@echo off
setlocal
title MP3 TURBO - UNINSTALLER

:: 1. Dapatkan Path Folder Sekarang
set "PROJ_PATH=%~dp0"
set "PROJ_PATH=%PROJ_PATH:~0,-1%"

echo ==========================================
echo      MP3 TURBO V2.1 - UNINSTALLER
echo ==========================================
echo.
echo [*] Lokasi dikesan: %PROJ_PATH%
echo.

:: 2. Padam fail mp4.bat
if exist "mp4.bat" (
    del "mp4.bat"
    echo [+] Fail 'mp4.bat' telah dipadam.
) else (
    echo [*] Fail 'mp4.bat' tidak dijumpai.
)

:: 3. Buang Folder dari Windows PATH (Clean-up)
echo [*] Membuang folder dari Environment PATH...
powershell -Command ^
    "$targetDir = '%PROJ_PATH%';" ^
    "$oldPath = [Environment]::GetEnvironmentVariable('Path', 'User');" ^
    "if ($oldPath -like '*$targetDir*') {" ^
    "  $pathList = $oldPath.Split(';', [System.StringSplitOptions]::RemoveEmptyEntries) | Where-Object { $_ -ne $targetDir };" ^
    "  $newPath = $pathList -join ';';" ^
    "  [Environment]::SetEnvironmentVariable('Path', $newPath, 'User');" ^
    "  Write-Host '[+] PATH telah dibersihkan.' -ForegroundColor Green;" ^
    "} else { Write-Host '[*] Path folder ini memang tiada dalam Registry.' -ForegroundColor Yellow; }"

:: 4. Selesai
echo.
echo ==========================================
echo [OK] UNINSTALL SELESAI!
echo ==========================================
echo Akses command 'mp4' telah dibuang.
echo Anda boleh memadam folder ini secara manual sekarang.
echo ==========================================
pause