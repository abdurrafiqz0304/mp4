# 🔥 Ultimate YouTube Downloader (MP3 & MP4)

A powerful, all-in-one Python tool to download YouTube videos, playlists, and albums.
**Version:** V6 (Git-Ready Edition)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![FFmpeg](https://img.shields.io/badge/Dependency-FFmpeg-green)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen)

## ✨ Key Features
* 🚀 **Global Command:** Just type `mp4` in CMD to launch the tool from anywhere!
* 🎵 **MP3 Mode:** Extract high-quality audio (320kbps).
* 🎬 **MP4 Mode:** Download videos with **Auto-AAC Fix** (Fixes "Opus format not supported" error on Windows Media Player).
* 📦 **Combo Mode:** Download BOTH MP3 and MP4 automatically sorted into sub-folders (`Audio_MP3` & `Video_MP4`).
* 🔇 **Mute Mode:** Download raw video footage without sound (great for editing).
* 📋 **Bulk Download:** Support downloading multiple links from a text file (`list.txt`).
* 📁 **File Manager:** Built-in tool to delete files or clean up folders.
* 🧹 **Clean Uninstaller:** Includes `uninstaller.bat` to remove the tool and clean up system paths.

---

## 🚀 Quick Installation (Automated)

The installer will automatically install Python libraries, download FFmpeg, and add the `mp4` command to your Windows Path.

### Option 1: Git Clone (Recommended)
```bash
git clone https://github.com/abdurrafiqz0304/mp4tomp3.git && cd mp4tomp3 && install.bat
```

### Option 2: CMD
```bash
curl -k -L -o projek.zip https://github.com/abdurrafiqz0304/mp4tomp3/archive/refs/heads/main.zip && tar -xf projek.zip && cd mp4tomp3-main && install.bat
```

### Option 3: PowerShell
```bash
Invoke-WebRequest -Uri "https://github.com/abdurrafiqz0304/mp4tomp3/archive/refs/heads/main.zip" -OutFile "projek.zip"; Expand-Archive -Path "projek.zip" -DestinationPath "."; cd mp4tomp3-main; .\install.bat
```