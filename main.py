import yt_dlp
import os
import sys
import platform
import subprocess

# --- KONFIGURASI PATH ---
# Memastikan program sentiasa merujuk kepada folder aplikasi utama
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- 1. SYSTEM UPDATE CENTER ---
def update_center():
    while True:
        print("\n" + "="*50)
        print(f"{'SYSTEM UPDATE CENTER':^50}")
        print("="*50)
        print("1. UPDATE ENGINE (yt-dlp)")
        print("2. UPDATE LIBRARIES (Dependencies)")
        print("3. UPDATE APP CODE (Ganti Folder & Path)")
        print("0. < KEMBALI")
        
        choice = input("\nPilih: ")
        if choice == '0': break

        if choice == '1':
            print("\n[*] Mengemaskini engine muat turun...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "yt-dlp"])
            input("\nSelesai! Tekan Enter...")
        
        elif choice == '2':
            print("\n[*] Mengemaskini library...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyperclip", "yt-dlp"])
            input("\nSelesai! Tekan Enter...")

        elif choice == '3':
            print("\n[*] Menjalankan kemas kini aplikasi...")
            print("[*] Sila tunggu, CMD baru akan dibuka untuk menggantikan fail.")
            
            # Logik kemas kini: Download -> Extract -> XCopy (Replace) -> Install.bat
            update_cmd = (
                f'start "Updater" cmd /c "cd /d "{BASE_DIR}" '
                f'&& curl -k -L -o projek.zip https://github.com/abdurrafiqz0304/mp4/archive/refs/heads/main.zip '
                f'&& tar -xf projek.zip '
                f'&& xcopy mp4-main\\* . /E /Y /Q '
                f'&& rmdir /s /q mp4-main '
                f'&& del projek.zip '
                f'&& call install.bat '
                f'&& echo [+] UPDATE BERJAYA! SILA RESTART PROGRAM. & pause"'
            )
            try:
                os.system(update_cmd)
                sys.exit() # Tutup program asal supaya fail boleh diganti
            except Exception as e:
                print(f"[!] Ralat kemas kini: {e}")

# --- 2. FILE MANAGER (OPTION 4) ---
def list_main_folders():
    while True:
        print("\n" + "="*50)
        print(f"{'FILE MANAGER - SENARAI FOLDER':^50}")
        print("="*50)
        try:
            # Hanya scan folder dalam direktori aplikasi
            folders = [f for f in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, f)) and not f.startswith('.')]
            folders.sort()
            if not folders:
                print("[!] Tiada folder dijumpai.")
            else:
                for i, folder in enumerate(folders, 1):
                    count = len(os.listdir(os.path.join(BASE_DIR, folder)))
                    print(f"{i}. {folder} ({count} fail)")
        except Exception as e:
            print(f"[!] Ralat: {e}")
        print("\n0. < KEMBALI")
        if input("Pilih: ") == '0': break

# --- 3. DOWNLOADER (FIXED AUDIO CODEC) ---
def run_download(urls, folder_path, format_type):
    ffmpeg_path = os.path.join(BASE_DIR, 'ffmpeg.exe')
    
    # Asingkan MP3 dan MP4 ke sub-folder jika dipilih
    if format_type == '4':
        for sub in ['mp3', 'mp4']:
            p = os.path.join(folder_path, sub)
            if not os.path.exists(p): os.makedirs(p)
        run_download(urls, os.path.join(folder_path, 'mp3'), '1')
        run_download(urls, os.path.join(folder_path, 'mp4'), '3')
        return

    ydl_opts = {
        'quiet': False,
        'outtmpl': f'{folder_path}/%(title)s.%(ext)s',
        'ffmpeg_location': ffmpeg_path if os.path.exists(ffmpeg_path) else None,
        'noplaylist': True, # Mengelakkan muat turun playlist secara tidak sengaja
    }

    if format_type == '1':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '320'}],
        })
    elif format_type == '3': # Membetulkan ralat audio Opus
        ydl_opts.update({
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
            'postprocessors': [{'key': 'FFmpegVideoConvertor','preferedformat': 'mp4'}],
        })
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in urls:
            if url.strip(): ydl.download([url.strip()])

# --- 4. PEMILIHAN FOLDER (image_f392a8.png) ---
def select_destination_folder():
    default_folder = os.path.join(BASE_DIR, 'downloads')
    while True:
        print("\n--- PILIH FOLDER ---")
        print(f"1. 'downloads' (Default)")
        print("2. Folder Baru")
        print("3. Folder Sedia Ada")
        print("0. < KEMBALI")
        
        c = input("Pilihan: ")
        if c == '0': return None
        if c == '1':
            if not os.path.exists(default_folder): os.makedirs(default_folder)
            return default_folder
        elif c == '2':
            name = input("Nama folder baru: ").strip()
            if name:
                p = os.path.join(BASE_DIR, name)
                if not os.path.exists(p): os.makedirs(p)
                return p
        elif c == '3':
            folders = [f for f in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, f)) and not f.startswith('.')]
            if not folders: continue
            for i, f in enumerate(folders, 1): print(f"{i}. {f}")
            sel = input("Pilih (0=Back): ")
            try: return os.path.join(BASE_DIR, folders[int(sel)-1])
            except: pass

# --- 5. MAIN MENU ---
def main_menu():
    while True:
        print("\n" + "="*50)
        print(f"{'MP3 & MP4 TURBO V2.1 (SELF-UPDATER)':^50}")
        print("="*50)
        print("1. Download Single Link")
        print("2. Download Playlist")
        print("3. Bulk (.txt)")
        print("4. File Manager (Senarai Folder)")
        print("5. UPDATE ENGINE")
        print("6. UPDATE APP CODE")
        print("7. Keluar")
        
        choice = input("Pilih: ")
        
        if choice in ['1', '2', '3']:
            dest = select_destination_folder()
            if not dest: continue

            print("\nFormat:")
            print("1. MP3 Only")
            print("3. Video Combined (Boleh Play)")
            print("4. Video & MP3 (Separated Sub-folders)")
            print("0. < KEMBALI")
            fmt = input("Pilih: ")
            if fmt == '0': continue
            
            while True:
                link = input("\nSila paste link (0 untuk Back): ")
                if link == '0': break
                run_download([link], dest, fmt)
                
                print("\n1.Teruskan Link 2.Buka Folder 3.Menu Utama")
                act = input(">> ")
                if act == '2':
                    if platform.system() == "Windows": os.startfile(dest)
                    else: subprocess.call(["open", dest])
                elif act == '3': break
        
        elif choice == '4':
            list_main_folders()
        elif choice in ['5', '6']:
            update_center()
        elif choice == '7':
            sys.exit()

if __name__ == "__main__":
    try: main_menu()
    except KeyboardInterrupt: sys.exit()