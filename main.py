import yt_dlp
import os
import sys
import platform
import subprocess

# --- KONFIGURASI PATH ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- FUNGSI LIST FOLDER (OPTION 4) ---
def list_main_folders():
    while True:
        print("\n" + "="*50)
        print(f"{'FILE MANAGER - SENARAI FOLDER':^50}")
        print("="*50)
        try:
            folders = [f for f in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, f)) and not f.startswith('.')]
            folders.sort()
            if not folders:
                print("[!] Tiada folder dijumpai dalam mp4-main.")
            else:
                print(f"Lokasi: {BASE_DIR}\n")
                for i, folder in enumerate(folders, 1):
                    count = len(os.listdir(os.path.join(BASE_DIR, folder)))
                    print(f"{i}. {folder} ({count} fail)")
        except Exception as e:
            print(f"[!] Ralat scan: {e}")
        print("\n0. < KEMBALI")
        if input("Pilih: ") == '0': break

# --- FUNGSI DOWNLOADER (FIXED CODECS) ---
def run_download(urls, folder_path, format_type):
    ffmpeg_path = os.path.join(BASE_DIR, 'ffmpeg.exe')
    
    # Logik untuk Video & MP3 Asing (Sub-folders)
    if format_type == '4':
        mp3_dir = os.path.join(folder_path, 'mp3')
        mp4_dir = os.path.join(folder_path, 'mp4')
        for p in [mp3_dir, mp4_dir]:
            if not os.path.exists(p): os.makedirs(p)
        print("[*] Memproses muat turun berasingan (MP3 & MP4)...")
        run_download(urls, mp3_dir, '1')
        run_download(urls, mp4_dir, '3')
        return

    ydl_opts = {
        'quiet': False,
        'no_warnings': True,
        'outtmpl': f'{folder_path}/%(title)s.%(ext)s',
        'ffmpeg_location': ffmpeg_path if os.path.exists(ffmpeg_path) else None,
        'noplaylist': True,
    }

    if format_type == '1': # MP3 Only
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '320'}],
        })
    elif format_type == '2': # Video Raw (No Audio)
        ydl_opts.update({'format': 'bestvideo'})
    elif format_type == '3': # Video Combined (FIXED FOR MEDIA PLAYER)
        ydl_opts.update({
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
        })
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in urls:
            url_clean = url.strip()
            if not url_clean: continue
            try: 
                print(f"\n[*] Memproses: {url_clean}")
                ydl.download([url_clean])
            except Exception as e: 
                print(f"[!] Gagal: {e}")

# --- PEMILIHAN FOLDER ---
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
            folders.sort()
            if not folders: continue
            print("\n--- SENARAI FOLDER ---")
            for i, f in enumerate(folders, 1): print(f"{i}. {f}")
            print("0. < KEMBALI")
            sel = input("Pilih: ")
            if sel == '0': continue
            try: return os.path.join(BASE_DIR, folders[int(sel)-1])
            except: pass

# --- MENU UTAMA ---
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
            print("\n[*] Menuju ke pemilihan folder...")
            dest = select_destination_folder()
            if not dest: continue

            print("\nFormat:")
            print("1. MP3 Only")
            print("2. Video Raw (No Audio)")
            print("3. Video Combined (Boleh Play)")
            print("4. Video & MP3 (Separated Sub-folders)")
            print("0. < KEMBALI")
            fmt = input("Pilih format: ")
            if fmt == '0': continue
            
            while True:
                link = input("\nSila paste link (0 untuk Back ke Menu): ")
                if link == '0': break
                
                run_download([link], dest, fmt)
                
                print("\nSeterusnya?")
                print("1. Teruskan Paste Link")
                print("2. Buka Folder")
                print("3. Kembali ke Menu Utama")
                act = input("Pilihan: ")
                
                if act == '2':
                    if platform.system() == "Windows": os.startfile(dest)
                    else: subprocess.call(["open", dest])
                elif act == '3':
                    return # Kembali ke loop menu utama
        
        elif choice == '4':
            list_main_folders()
            
        elif choice == '7':
            sys.exit()

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nForce Quit.")