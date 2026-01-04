import yt_dlp
import os
import sys
import platform
import subprocess
import shutil  # Penting untuk fungsi padam folder

# --- KONFIGURASI PATH ---
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
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "yt-dlp"])
                print("\n[+] Engine berjaya dikemaskini!")
            except Exception as e:
                print(f"[!] Ralat: {e}")
            input("Tekan Enter untuk sambung...")
        
        elif choice == '2':
            print("\n[*] Mengemaskini library...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "pyperclip", "yt-dlp"])
                print("\n[+] Library berjaya dikemaskini!")
            except Exception as e:
                print(f"[!] Ralat: {e}")
            input("Tekan Enter untuk sambung...")

        elif choice == '3':
            print("\n[*] Menjalankan kemas kini aplikasi...")
            print("[*] CMD baru akan dibuka untuk proses muat turun dan penggantian fail.")
            
            update_cmd = (
                f'start "Updater" cmd /c "cd /d "{BASE_DIR}" '
                f'&& curl -k -L -o projek.zip https://github.com/abdurrafiqz0304/mp4/archive/refs/heads/main.zip '
                f'&& tar -xf projek.zip '
                f'&& xcopy mp4-main\\* . /E /Y /Q '
                f'&& rmdir /s /q mp4-main '
                f'&& del projek.zip '
                f'&& call install.bat '
                f'&& echo. && echo [+] UPDATE SELESAI! SILA RESTART PROGRAM. && pause"'
            )
            
            try:
                os.system(update_cmd)
                sys.exit()
            except Exception as e:
                print(f"[!] Ralat kemas kini: {e}")

# --- 2. LOGIK FILE MANAGER BARU ---

def delete_specific_file(folder_path):
    while True:
        print("\n--- PILIH FAIL UNTUK DIPADAM ---")
        try:
            files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
            files.sort()
            
            if not files:
                print("[!] Folder kosong atau tiada fail.")
                return

            for i, f in enumerate(files, 1):
                size = os.path.getsize(os.path.join(folder_path, f)) / (1024 * 1024)
                print(f"{i}. {f} ({size:.2f} MB)")
            
            print("0. < KEMBALI")
            
            sel = input("Pilih nombor fail: ")
            if sel == '0': return

            idx = int(sel) - 1
            if 0 <= idx < len(files):
                file_to_del = os.path.join(folder_path, files[idx])
                confirm = input(f"Adakah anda pasti mahu memadam '{files[idx]}'? (y/n): ")
                if confirm.lower() == 'y':
                    os.remove(file_to_del)
                    print("[+] Fail berjaya dipadam.")
            else:
                print("[!] Pilihan tidak sah.")
                
        except Exception as e:
            print(f"[!] Ralat: {e}")
            return

def manage_selected_folder(folder_name):
    folder_path = os.path.join(BASE_DIR, folder_name)
    
    while True:
        if not os.path.exists(folder_path):
            print("[!] Folder ini sudah tidak wujud.")
            break

        # Kira jumlah fail
        try:
            file_count = len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])
        except: file_count = 0

        print("\n" + "-"*40)
        print(f"PENGURUSAN FOLDER: {folder_name} ({file_count} fail)")
        print("-"*40)
        print("1. Buka Folder (Explorer)")
        print("2. Padam Fail Spesifik (Select File)")
        print("3. PADAM ENTIRE FOLDER (Delete All)")
        print("0. < KEMBALI")

        c = input("Pilihan: ")
        
        if c == '0': break
        
        elif c == '1': # Buka Folder
            if platform.system() == "Windows": os.startfile(folder_path)
            else: subprocess.call(["open", folder_path])
            
        elif c == '2': # Padam Fail
            delete_specific_file(folder_path)
            
        elif c == '3': # Padam Folder
            confirm = input(f"\n[AMARAN] Adakah anda pasti mahu memadam folder '{folder_name}' dan SEMUA isinya? (y/n): ")
            if confirm.lower() == 'y':
                try:
                    shutil.rmtree(folder_path)
                    print(f"[+] Folder '{folder_name}' telah dipadam sepenuhnya.")
                    break # Keluar dari menu folder sebab folder dah tak ada
                except Exception as e:
                    print(f"[!] Gagal memadam folder: {e}")

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
                input("Tekan Enter untuk kembali...")
                break
            else:
                for i, folder in enumerate(folders, 1):
                    count = len(os.listdir(os.path.join(BASE_DIR, folder)))
                    print(f"{i}. {folder} ({count} fail)")
                
                print("\n0. < KEMBALI KE MENU UTAMA")
                print("Pilih nombor folder untuk uruskan (Buka/Padam):")
                
                sel = input(">> ")
                if sel == '0': break
                
                try:
                    idx = int(sel) - 1
                    if 0 <= idx < len(folders):
                        manage_selected_folder(folders[idx])
                    else:
                        print("[!] Nombor tidak sah.")
                except ValueError:
                    print("[!] Sila masukkan nombor.")
                    
        except Exception as e:
            print(f"[!] Ralat scan: {e}")
            break

# --- 3. DOWNLOADER ---
def run_download(urls, folder_path, format_type):
    ffmpeg_path = os.path.join(BASE_DIR, 'ffmpeg.exe')
    
    if format_type == '4':
        for sub in ['mp3', 'mp4']:
            p = os.path.join(folder_path, sub)
            if not os.path.exists(p): os.makedirs(p)
        print("\n[*] Memproses MP3...")
        run_download(urls, os.path.join(folder_path, 'mp3'), '1')
        print("\n[*] Memproses MP4...")
        run_download(urls, os.path.join(folder_path, 'mp4'), '3')
        return

    ydl_opts = {
        'quiet': False,
        'outtmpl': f'{folder_path}/%(title)s.%(ext)s',
        'ffmpeg_location': ffmpeg_path if os.path.exists(ffmpeg_path) else None,
        'noplaylist': True,
    }

    if format_type == '1': # MP3 Only
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '320'}],
        })
    elif format_type == '2': # Video Raw
        ydl_opts.update({'format': 'bestvideo'})
    elif format_type == '3': # Video Combined
        ydl_opts.update({
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
            'postprocessors': [{'key': 'FFmpegVideoConvertor','preferedformat': 'mp4'}],
        })
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in urls:
            if url.strip(): 
                try: ydl.download([url.strip()])
                except Exception as e: print(f"[!] Gagal: {e}")

# --- 4. PEMILIHAN FOLDER ---
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

# --- 5. MENU UTAMA ---
def main_menu():
    while True:
        print("\n" + "="*50)
        print(f"{'MP3 & MP4 TURBO V2.1 (SELF-UPDATER)':^50}")
        print("="*50)
        print("1. Download Single Link")
        print("2. Download Playlist")
        print("3. Bulk (.txt)")
        print("4. File Manager (Urus/Padam Folder)")
        print("5. UPDATE ENGINE (Fix Slow Speed)")
        print("6. UPDATE APP CODE (Dapatkan Feature Baru)")
        print("7. Keluar")
        
        choice = input("Pilih: ")
        
        if choice in ['1', '2', '3']:
            dest = select_destination_folder()
            if not dest: continue

            print("\nFormat:")
            print("1. MP3 Only")
            print("2. Video Raw sahaja (Tiada Audio)")
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