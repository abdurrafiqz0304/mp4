@echo off
title Ultimate Downloader Installer
cls

echo ==================================================
echo   ULTIMATE DOWNLOADER AUTO-INSTALLER
echo ==================================================
echo.

:: 1. Install Python Library
echo [1/3] Menginstall library Python (yt-dlp)...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Gagal install pip. Pastikan Python sudah diinstall.
    pause
    exit /b
)

:: 2. Cek FFmpeg
if exist ffmpeg.exe (
    echo [INFO] ffmpeg.exe sudah wujud. Skip download.
    goto :finish
)

:: 3. Download & Extract FFmpeg (Jika tiada)
echo.
echo [2/3] FFmpeg tiada. Sedang DOWNLOAD dari server (Mungkin lama sikit)...
echo Link: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
echo.

:: Download guna CURL
curl -L -o ffmpeg_temp.zip https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip

echo.
echo [3/3] Sedang EXTRACT fail...
:: Extract guna TAR (Built-in Windows 10/11)
tar -xf ffmpeg_temp.zip

:: Pindahkan ffmpeg.exe ke folder utama
:: Folder dalam zip biasanya nama panjang, kita guna wildcard (*)
cd ffmpeg-*-essentials\bin
move ffmpeg.exe ..\..\
cd ..\..\

:: 4. Cleanup (Buang sampah)
echo [CLEANUP] Membuang fail sementara...
del ffmpeg_temp.zip
for /d %%d in (ffmpeg-*-essentials) do rmdir /s /q "%%d"

:finish
echo.
echo ==================================================
echo    SIAP! SEMUA DAH COMPLETE.
echo ==================================================
echo.
echo Anda boleh taip 'python main.py' untuk mula.
pause