import yt_dlp
import os
import sys
import platform
import subprocess
import shutil

# --- CONFIG ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OS_TYPE = platform.system()

# --- 1. SYSTEM UPDATE CENTER ---
def update_center():
    while True:
        print("\n" + "="*50)
        print(f"{'SYSTEM UPDATE CENTER':^50}")
        print("="*50)
        print("1. UPDATE ENGINE (yt-dlp)")
        print("2. UPDATE LIBRARIES")
        print("3. UPDATE APP CODE (Replace Folder & Path)")
        print("0. < BACK")
        
        choice = input("\nSelect: ")
        if choice == '0': break

        if choice == '1':
            print("\n[*] Updating engine...")
            try: subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "yt-dlp"]); print("[+] Done.")
            except: pass
            input("Enter...")
        
        elif choice == '2':
            print("\n[*] Updating libraries...")
            try: subprocess.check_call([sys.executable, "-m", "pip", "install", "pyperclip", "yt-dlp"]); print("[+] Done.")
            except: pass
            input("Enter...")

        elif choice == '3':
            print("\n[*] Starting update...")
            
            # --- WINDOWS UPDATE COMMAND ---
            if OS_TYPE == "Windows":
                cmd = (
                    f'start "Updater" cmd /c "cd /d "{BASE_DIR}" '
                    f'&& curl -k -L -o projek.zip https://github.com/abdurrafiqz0304/mp4/archive/refs/heads/main.zip '
                    f'&& tar -xf projek.zip '
                    f'&& xcopy mp4-main\\* . /E /Y /Q '
                    f'&& rmdir /s /q mp4-main '
                    f'&& del projek.zip '
                    f'&& call install.bat '
                    f'&& echo [+] DONE! RESTART PROGRAM. && pause"'
                )
                try: os.system(cmd); sys.exit()
                except: pass
            
            # --- MAC/LINUX UPDATE COMMAND (ONE-LINER) ---
            else:
                # Teknik 'sh install.sh' elak permission issue
                print("[*] Downloading & Installing for Mac...")
                cmd = (
                    f'cd "{BASE_DIR}" && '
                    f'curl -k -L -o projek.zip https://github.com/abdurrafiqz0304/mp4/archive/refs/heads/main.zip && '
                    f'unzip -o projek.zip && '
                    f'cp -r mp4-main/* . && '
                    f'rm -rf mp4-main projek.zip && '
                    f'sh install.sh' 
                )
                try:
                    os.system(cmd)
                    print("\n[+] UPDATE COMPLETE! Please restart terminal.")
                    sys.exit()
                except: print("[!] Error.")

# --- 2. FILE MANAGER ---
def delete_specific_file(folder_path):
    while True:
        print("\n--- SELECT FILES TO DELETE ---")
        try:
            files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
            files.sort()
            if not files: print("[!] No files."); return

            for i, f in enumerate(files, 1):
                sz = os.path.getsize(os.path.join(folder_path, f))/(1024*1024)
                print(f"{i}. {f} ({sz:.2f} MB)")
            print("0. < BACK")
            print("TIP: Type numbers like: 1 2 5")
            
            sel = input("Select: ")
            if sel == '0': return
            
            nums = sel.split()
            targets = []
            for n in nums:
                if n.isdigit() and 0 <= int(n)-1 < len(files): targets.append(files[int(n)-1])
            
            if not targets: continue
            print(f"\n[!] Deleting {len(targets)} files.")
            if input("Confirm (y/n): ") == 'y':
                for t in targets: os.remove(os.path.join(folder_path, t))
                print("Done.")
        except: return

def manage_selected_folder(name):
    path = os.path.join(BASE_DIR, name)
    while True:
        if not os.path.exists(path): break
        cnt = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
        print(f"\n--- {name} ({cnt} files) ---")
        print("1. Open\n2. Delete Files\n3. DELETE FOLDER\n0. Back")
        c = input("Op: ")
        if c=='0': break
        elif c=='1':
            if OS_TYPE=="Windows": os.startfile(path)
            elif OS_TYPE=="Darwin": subprocess.call(["open", path])
            else: subprocess.call(["xdg-open", path])
        elif c=='2': delete_specific_file(path)
        elif c=='3':
            if input("TYPE 'YES' TO DELETE FOLDER: ")=='YES': shutil.rmtree(path); break

def list_main_folders():
    while True:
        print("\n=== FILE MANAGER ===")
        fs = [f for f in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, f)) and not f.startswith('.')]
        fs.sort()
        if not fs: print("No folders."); break
        for i, f in enumerate(fs, 1): print(f"{i}. {f}")
        print("0. Back")
        try:
            sel = int(input("Select folder: "))
            if sel==0: break
            if 0 < sel <= len(fs): manage_selected_folder(fs[sel-1])
        except: pass

# --- 3. DOWNLOADER ---
def run_download(urls, folder_path, format_type):
    ffmpeg_exe = 'ffmpeg.exe' if OS_TYPE == "Windows" else 'ffmpeg'
    ffmpeg_path = os.path.join(BASE_DIR, ffmpeg_exe)
    if not os.path.exists(ffmpeg_path): ffmpeg_path = None 

    if format_type == '4':
        for sub in ['mp3', 'mp4']:
            p = os.path.join(folder_path, sub)
            if not os.path.exists(p): os.makedirs(p)
        run_download(urls, os.path.join(folder_path, 'mp3'), '1')
        run_download(urls, os.path.join(folder_path, 'mp4'), '3')
        return

    opts = {
        'quiet': False, 'no_warnings': True, 'noplaylist': True,
        'outtmpl': f'{folder_path}/%(title)s.%(ext)s',
        'ffmpeg_location': ffmpeg_path
    }
    if format_type == '1': opts.update({'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '320'}]})
    elif format_type == '2': opts.update({'format': 'bestvideo'})
    elif format_type == '3': opts.update({'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best', 'merge_output_format': 'mp4'})
    
    with yt_dlp.YoutubeDL(opts) as ydl:
        for u in urls:
            if u.strip(): 
                try: ydl.download([u.strip()])
                except: print(f"Failed: {u}")

# --- 4. MAIN ---
def select_destination_folder():
    d = os.path.join(BASE_DIR, 'downloads')
    while True:
        print("\n1. Default\n2. New\n3. Existing\n0. Back")
        c = input("Choice: ")
        if c=='0': return None
        if c=='1': 
            if not os.path.exists(d): os.makedirs(d)
            return d
        elif c=='2':
            n = input("Name: ").strip()
            if n: 
                p = os.path.join(BASE_DIR, n)
                if not os.path.exists(p): os.makedirs(p)
                return p
        elif c=='3':
            fs = [f for f in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, f)) and not f.startswith('.')]
            if not fs: continue
            for i, f in enumerate(fs, 1): print(f"{i}. {f}")
            try: return os.path.join(BASE_DIR, fs[int(input("Sel: "))-1])
            except: pass

def main_menu():
    while True:
        print("\n" + "="*50)
        print(f"{'MP3/MP4 TURBO V3.3 (MAC/WIN ONE-CLICK)':^50}") 
        print("="*50)
        print("1. Single Link\n2. Playlist\n3. Bulk\n4. File Manager\n5. Update Engine\n6. Update App Code\n7. Exit")
        c = input("Select: ")
        if c in ['1','2','3']:
            d = select_destination_folder()
            if not d: continue
            fmt = input("1.MP3 2.Raw 3.Combined 4.Split\nFormat: ")
            if fmt not in ['1','2','3','4']: continue
            while True:
                l = input("Link (0 Back): ")
                if l=='0': break
                run_download([l], d, fmt)
                print("1.Cont 2.Open 3.Menu")
                if input(">> ")=='2':
                    if OS_TYPE=="Windows": os.startfile(d)
                    elif OS_TYPE=="Darwin": subprocess.call(["open", d])
                    else: subprocess.call(["xdg-open", d])
        elif c=='4': list_main_folders()
        elif c in ['5','6']: update_center()
        elif c=='7': sys.exit()

if __name__ == "__main__":
    try: main_menu()
    except: sys.exit()