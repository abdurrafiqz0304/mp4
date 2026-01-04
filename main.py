import yt_dlp
import os
import sys
import platform
import subprocess
import shutil

# --- KONFIGURASI PATH ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- 1. SYSTEM UPDATE CENTER ---
def update_center():
    while True:
        print("\n" + "="*50)
        print(f"{'SYSTEM UPDATE CENTER':^50}")
        print("="*50)
        print("1. UPDATE ENGINE (yt-dlp)")
        print("2. UPDATE LIBRARIES")
        print("3. UPDATE APP CODE (Ganti Folder & Path)")
        print("0. < KEMBALI")
        
        choice = input("\nPilih: ")
        if choice == '0': break

        if choice == '1':
            print("\n[*] Updating engine...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "yt-dlp"])
                print("[+] Selesai.")
            except: pass
            input("Enter untuk sambung...")
        
        elif choice == '2':
            print("\n[*] Updating libraries...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "pyperclip", "yt-dlp"])
                print("[+] Selesai.")
            except: pass
            input("Enter untuk sambung...")

        elif choice == '3':
            print("\n[*] Memulakan proses update...")
            update_cmd = (
                f'start "Updater" cmd /c "cd /d "{BASE_DIR}" '
                f'&& curl -k -L -o projek.zip https://github.com/abdurrafiqz0304/mp4/archive/refs/heads/main.zip '
                f'&& tar -xf projek.zip '
                f'&& xcopy mp4-main\\* . /E /Y /Q '
                f'&& rmdir /s /q mp4-main '
                f'&& del projek.zip '
                f'&& call install.bat '
                f'&& echo. && echo [+] UPDATE SIAP! SILA RESTART. && pause"'
            )
            try:
                os.system(update_cmd)
                sys.exit()
            except: pass

# --- 2. FILE MANAGER (DELETE & MANAGE) ---
def delete_specific_file(folder_path):
    while True:
        print("\n--- PILIH FAIL UNTUK DIPADAM ---")
        try:
            files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
            files.sort()
            
            if not files:
                print("[!] Tiada fail.")
                return

            for i, f in enumerate(files, 1):
                size = os.path.getsize(os.path.join(folder_path, f)) / (1024 * 1024)
                print(f"{i}. {f} ({size:.2f} MB)")
            print("0. < KEMBALI")
            
            sel = input("Nombor fail: ")
            if sel == '0': return

            idx = int(sel) - 1
            if 0 <= idx < len(files):
                target = os.path.join(folder_path, files[idx])
                if input(f"Padam '{files[idx]}'? (y/n): ") == 'y':
                    os.remove(target)
                    print("[+] Terpadam.")
        except: return

def manage_selected_folder(folder_name):
    path = os.path.join(BASE_DIR, folder_name)
    while True:
        if not os.path.exists(path):
            print("[!] Folder hilang."); break
            
        cnt = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
        print("\n" + "-"*40)
        print(f"URUS FOLDER: {folder_name} [{cnt} files]")
        print("-" * 40)
        print("1. Buka Folder (Explorer)")
        print("2. Padam Fail Dalam Folder")
        print("3. PADAM ENTIRE FOLDER (Semua hilang)")
        print("0. < KEMBALI")
        
        c = input("Pilihan: ")
        if c == '0': break
        elif c == '1':
            if platform.system() == "Windows": os.startfile(path)
            else: subprocess.call(["open", path])
        elif c == '2': delete_specific_file(path)
        elif c == '3':
            if input(f"CONFIRM PADAM FOLDER '{folder_name}'? (Taip 'YES'): ") == 'YES':
                try: 
                    shutil.rmtree(path)
                    print("[+] Folder dah hilang selamanya.")
                    break
                except: print("[!] Gagal padam.")

def list_main_folders():
    while True:
        print("\n" + "="*50)
        print(f"{'FILE MANAGER - DELETE/MANAGE':^50}")
        print("="*50)
        folders = [f for f in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, f)) and not f.startswith('.')]
        folders.sort()
        
        if not folders: 
            print("[!] Tiada folder."); break
            
        for i, f in enumerate(folders, 1):
            print(f"{i}. {f}")
            
        print("\n0. < MENU UTAMA")
        print("Pilih nombor folder untuk masuk menu delete/urus:")
        sel = input(">> ")
        if sel == '0': break
        try:
            if 0 <= int(sel)-1 < len(folders): manage_selected_folder(folders[int(sel)-1])
        except: pass

# --- 3. DOWNLOADER ---
def run_download(urls, folder_path, format_type):
    ffmpeg_path = os.path.join(BASE_DIR, 'ffmpeg.exe')
    
    if format_type == '4':
        for sub in ['mp3', 'mp4']:
            p = os.path.join(folder_path, sub)
            if not os.path.exists(p): os.makedirs(p)
        run_download(urls, os.path.join(folder_path, 'mp3'), '1')
        run_download(urls, os.path.join(folder_path, 'mp4'), '3')
        return

    ydl_opts = {
        'quiet': False, 'no_warnings': True, 'noplaylist': True,
        'outtmpl': f'{folder_path}/%(title)s.%(ext)s',
        'ffmpeg_location': ffmpeg_path if os.path.exists(ffmpeg_path) else None
    }

    if format_type == '1':
        ydl_opts.update({'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '320'}]})
    elif format_type == '2':
        ydl_opts.update({'format': 'bestvideo'})
    elif format_type == '3':
        ydl_opts.update({'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', 'merge_output_format': 'mp4'})
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in urls:
            if url.strip(): 
                try: ydl.download([url.strip()])
                except: print(f"[!] Gagal: {url}")

# --- 4. SELECT FOLDER ---
def select_destination_folder():
    default = os.path.join(BASE_DIR, 'downloads')
    while True:
        print("\n--- PILIH FOLDER ---")
        print(f"1. Default ({default})")
        print("2. Folder Baru")
        print("3. Folder Sedia Ada")
        print("0. < KEMBALI")
        c = input("Pilih: ")
        if c == '0': return None
        if c == '1':
            if not os.path.exists(default): os.makedirs(default)
            return default
        elif c == '2':
            name = input("Nama: ").strip()
            if name:
                p = os.path.join(BASE_DIR, name)
                if not os.path.exists(p): os.makedirs(p)
                return p
        elif c == '3':
            folders = [f for f in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, f)) and not f.startswith('.')]
            if not folders: continue
            for i, f in enumerate(folders, 1): print(f"{i}. {f}")
            sel = input("Pilih: ")
            try: return os.path.join(BASE_DIR, folders[int(sel)-1])
            except: pass

# --- 5. MAIN MENU ---
def main_menu():
    while True:
        print("\n" + "="*50)
        # SAYA UBAH TAJUK KAT SINI SUPAYA AWAK NAMPAK BEZA
        print(f"{'MP3/MP4 TURBO V3.0 (SUPER MANAGER)':^50}") 
        print("="*50)
        print("1. Download Single Link")
        print("2. Download Playlist")
        print("3. Bulk (.txt)")
        print("4. File Manager (Urus/Padam Folder)")
        print("5. UPDATE ENGINE")
        print("6. UPDATE APP CODE")
        print("7. Keluar")
        
        choice = input("Pilih: ")
        
        if choice in ['1', '2', '3']:
            dest = select_destination_folder()
            if not dest: continue
            print("\nFormat:\n1. MP3\n2. Raw Video\n3. Video Combined\n4. Video & MP3 (Asing)\n0. Back")
            fmt = input("Pilih: ")
            if fmt == '0': continue
            while True:
                link = input("\nLink (0 Back): ")
                if link == '0': break
                run_download([link], dest, fmt)
                print("\n1.Sambung 2.Buka Folder 3.Menu")
                act = input(">> ")
                if act == '2':
                    if platform.system() == "Windows": os.startfile(dest)
                    else: subprocess.call(["open", dest])
                elif act == '3': break
        
        elif choice == '4':
            list_main_folders() # Ini akan bawa ke menu baru
        elif choice in ['5', '6']:
            update_center()
        elif choice == '7':
            sys.exit()

if __name__ == "__main__":
    try: main_menu()
    except KeyboardInterrupt: sys.exit()