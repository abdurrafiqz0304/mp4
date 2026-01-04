@echo off
setlocal
title Ultimate Downloader Installer (Global Setup)
cls

echo ==================================================
echo   ULTIMATE DOWNLOADER AUTO-INSTALLER
echo ==================================================
echo.

:: --- 1. INSTALL LIBRARY PYTHON ---
echo [1/4] Menginstall library Python (yt-dlp)...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Gagal install pip. Pastikan Python sudah diinstall.
    pause
    exit /b
)

:: --- 2. SETUP FFMPEG (AUTO DOWNLOAD) ---
if exist ffmpeg.exe (
    echo [INFO] ffmpeg.exe sudah wujud. Skip download.
) else (
    echo.
    echo [2/4] FFmpeg tiada. Sedang DOWNLOAD...
    curl -L -o ffmpeg_temp.zip https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
    
    echo [INFO] Extracting FFmpeg...
    tar -xf ffmpeg_temp.zip
    cd ffmpeg-*-essentials\bin
    move ffmpeg.exe ..\..\
    cd ..\..\
    
    echo [CLEANUP] Membersihkan fail sampah...
    del ffmpeg_temp.zip
    for /d %%d in (ffmpeg-*-essentials) do rmdir /s /q "%%d"
)

:: --- 3. CREATE LAUNCHER (mp4.bat SAHAJA) ---
echo.
echo [3/4] Membuat shortcut command 'mp4'...

:: Buang mp3.bat lama jika ada (cleanup)
if exist mp3.bat (
    del mp3.bat
    echo [INFO] Command lama 'mp3' telah dipadam.
)

:: Buat command 'mp4'
(
echo @echo off
echo python "%%~dp0main.py" %%*
) > mp4.bat
echo [OK] Command 'mp4' berjaya dicipta.

:: --- 4. ADD TO WINDOWS PATH ---
echo.
echo [4/4] Menambah folder ini ke Windows PATH...
echo Path Sekarang: %CD%

:: Powershell script untuk tambah Path dengan selamat
powershell -Command "$oldPath = [Environment]::GetEnvironmentVariable('Path', 'User'); $currentDir = '%CD%'; if ($oldPath -notlike *"$currentDir"*) { [Environment]::SetEnvironmentVariable('Path', $oldPath + ';' + $currentDir, 'User'); Write-Host '[SUCCESS] Path berjaya ditambah!' -ForegroundColor Green } else { Write-Host '[INFO] Folder ini sudah ada dalam Path.' -ForegroundColor Yellow }"

echo.
echo ==================================================
echo    INSTALLATION SELESAI!
echo ==================================================
echo.
echo Cara Guna:
echo 1. Tutup window ini.
echo 2. Buka CMD baru (di mana-mana folder).
echo 3. Taip 'mp4'
echo.
pause