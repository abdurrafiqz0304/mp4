@echo off
title Ultimate Downloader Uninstaller
cls
color 0c

echo ==================================================
echo      ⚠️  PROGRAM UNINSTALLATION WIZARD  ⚠️
echo ==================================================
echo.
echo Script ini akan memadam keseluruhan folder ini dan
echo membersihkan setting Windows Path anda.
echo.

:ask_python
echo --------------------------------------------------
echo [1/3] PYTHON ENVIRONMENT
echo --------------------------------------------------
echo Adakah anda mahu uninstall library 'yt-dlp' dari Python?
echo (Pilih 'n' jika anda menggunakan library ini untuk projek lain)
echo.
set /p py_choice="Buang library yt-dlp? (y/n): "

if /i "%py_choice%"=="y" (
    echo.
    echo Menguninstall yt-dlp...
    pip uninstall yt-dlp -y
    echo [OK] Library berjaya dibuang.
) else (
    echo [INFO] Library Python dikekalkan.
)

echo.
echo --------------------------------------------------
echo [2/3] MEMBERSIHKAN WINDOWS PATH
echo --------------------------------------------------
echo Membuang folder ini dari system environment...

:: Gunakan PowerShell untuk remove path folder ini sahaja
powershell -Command "$path = [Environment]::GetEnvironmentVariable('Path', 'User'); $current = '%CD%'; $new = $path.Replace(';' + $current, '').Replace($current + ';', '').Replace($current, ''); [Environment]::SetEnvironmentVariable('Path', $new, 'User'); Write-Host '[SUCCESS] Path bersih.' -ForegroundColor Green"

echo.
echo --------------------------------------------------
echo [3/3] PEMADAMAN TOTAL (SELF-DESTRUCT)
echo --------------------------------------------------
echo.
echo ⚠️  AMARAN TERAKHIR ⚠️
echo Semua fail dalam folder ini (termasuk video yang didownload)
echo akan dipadamkan SEPENUHNYA.
echo.
set /p confirm="Adakah anda pasti? (y/n): "

if /i "%confirm%" neq "y" (
    echo [BATAL] Uninstallation dibatalkan. Tiada fail dipadam.
    pause
    exit
)

echo.
echo Selamat tinggal! Folder ini akan hilang dalam 3 saat...

:: --- TEKNIK SELF-DESTRUCT ---
:: Kita tak boleh delete folder ni semasa script ni tengah jalan di dalamnya.
:: Jadi kita buat script sementara di folder %TEMP% untuk buat kerja kotor.

set "SELF_DEL_SCRIPT=%TEMP%\clean_mp4_project.bat"
set "TARGET_DIR=%CD%"

(
    echo @echo off
    echo timeout /t 3 ^>nul
    echo rmdir /s /q "%TARGET_DIR%"
    echo del "%%~f0"
) > "%SELF_DEL_SCRIPT%"

:: Jalankan script hantu tu dan tutup script ini
start "" "%SELF_DEL_SCRIPT%"
exit