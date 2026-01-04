import yt_dlp
import os
import sys
import platform
import subprocess
import shutil

# --- PATH CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "yt-dlp"])
                print("[+] Done.")
            except: pass
            input("Press Enter to continue...")
        
        elif choice == '2':
            print("\n[*] Updating libraries...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "pyperclip", "yt-dlp"])
                print("[+] Done.")
            except: pass
            input("Press Enter to continue...")

        elif choice == '3':
            print("\n[*] Starting update process...")
            # Using the specific link and replace logic you requested
            update_cmd = (
                f'start "Updater" cmd /c "cd /d "{BASE_DIR}" '
                f'&& curl -k -L -o projek.zip https://github.com/abdurrafiqz0304/mp4/archive/refs/heads/main.zip '
                f'&& tar -xf projek.zip '
                f'&& xcopy mp4-main\\* . /E /Y /Q '
                f'&& rmdir /s /q mp4-main '
                f'&& del projek.zip '
                f'&& call install.bat '
                f'&& echo. && echo [+] UPDATE COMPLETE! PLEASE RESTART. && pause"'
            )
            try:
                os.system(update_cmd)
                sys.exit()
            except: pass

# --- 2. FILE MANAGER (BATCH DELETE UPDATE) ---
def delete_specific_file(folder_path):
    while True:
        print("\n--- SELECT FILES TO DELETE ---")
        try:
            files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
            files.sort()
            
            if not files:
                print("[!] No files found.")
                return

            for i, f in enumerate(files, 1):
                size = os.path.getsize(os.path.join(folder_path, f)) / (1024 * 1024)
                print(f"{i}. {f} ({size:.2f} MB)")
            
            print("0. < BACK")
            print("TIP: You can enter multiple numbers (e.g., 1 2 5)") 
            
            sel_input = input("Select file number(s): ")
            if sel_input.strip() == '0': return

            # --- BATCH SELECTION LOGIC ---
            selections = sel_input.split()
            valid_files = []
            
            for s in selections:
                if s.isdigit():
                    idx = int(s) - 1
                    if 0 <= idx < len(files):
                        valid_files.append(files[idx])
            
            if not valid_files:
                print("[!] No valid file numbers selected.")
                input("Press Enter...")
                continue
            
            # Summary before deletion
            print(f"\n[WARNING] You selected {len(valid_files)} files to delete:")
            for vf in valid_files:
                print(f"- {vf}")
            
            confirm = input("Confirm delete ALL files above? (y/n): ")
            if confirm.lower() == 'y':
                for vf in valid_files:
                    try:
                        os.remove(os.path.join(folder_path, vf))
                        print(f"[+] Deleted: {vf}")
                    except Exception as e:
                        print(f"[!] Failed to delete {vf}: {e}")
                input("Done. Press Enter...")
            else:
                print("[*] Cancelled.")

        except Exception as e: 
            print(f"[!] Error: {e}")
            return

def manage_selected_folder(folder_name):
    path = os.path.join(BASE_DIR, folder_name)
    while True:
        if not os.path.exists(path):
            print("[!] Folder missing."); break
            
        cnt = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
        print("\n" + "-"*40)
        print(f"MANAGE FOLDER: {folder_name} [{cnt} files]")
        print("-" * 40)
        print("1. Open Folder (Explorer)")
        print("2. Delete Files (Select Single/Multiple)")
        print("3. DELETE ENTIRE FOLDER (Permanent)")
        print("0. < BACK")
        
        c = input("Option: ")
        if c == '0': break
        elif c == '1':
            if platform.system() == "Windows": os.startfile(path)
            else: subprocess.call(["open", path])
        elif c == '2': delete_specific_file(path)
        elif c == '3':
            if input(f"CONFIRM DELETE FOLDER '{folder_name}'? (Type 'YES'): ") == 'YES':
                try: 
                    shutil.rmtree(path)
                    print("[+] Folder deleted forever.")
                    break
                except: print("[!] Delete failed.")

def list_main_folders():
    while True:
        print("\n" + "="*50)
        print(f"{'FILE MANAGER - DELETE/MANAGE':^50}")
        print("="*50)
        try:
            folders = [f for f in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, f)) and not f.startswith('.')]
            folders.sort()
            
            if not folders: 
                print("[!] No folders found."); break
                
            for i, f in enumerate(folders, 1):
                count = len(os.listdir(os.path.join(BASE_DIR, f)))
                print(f"{i}. {f} ({count} items)")
                
            print("\n0. < MAIN MENU")
            print("Select folder number to manage/delete:")
            sel = input(">> ")
            if sel == '0': break
            
            try:
                idx = int(sel) - 1
                if 0 <= idx < len(folders): manage_selected_folder(folders[idx])
            except: pass
        except: break

# --- 3. DOWNLOADER ---
def run_download(urls, folder_path, format_type):
    ffmpeg_path = os.path.join(BASE_DIR, 'ffmpeg.exe')
    
    if format_type == '4':
        for sub in ['mp3', 'mp4']:
            p = os.path.join(folder_path, sub)
            if not os.path.exists(p): os.makedirs(p)
        print("\n[*] Processing MP3...")
        run_download(urls, os.path.join(folder_path, 'mp3'), '1')
        print("\n[*] Processing MP4...")
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
                except: print(f"[!] Failed: {url}")

# --- 4. SELECT FOLDER ---
def select_destination_folder():
    default = os.path.join(BASE_DIR, 'downloads')
    while True:
        print("\n--- SELECT FOLDER ---")
        print(f"1. Default ({default})")
        print("2. New Folder")
        print("3. Existing Folder")
        print("0. < BACK")
        c = input("Option: ")
        if c == '0': return None
        if c == '1':
            if not os.path.exists(default): os.makedirs(default)
            return default
        elif c == '2':
            name = input("New folder name: ").strip()
            if name:
                p = os.path.join(BASE_DIR, name)
                if not os.path.exists(p): os.makedirs(p)
                return p
        elif c == '3':
            folders = [f for f in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, f)) and not f.startswith('.')]
            if not folders: continue
            for i, f in enumerate(folders, 1): print(f"{i}. {f}")
            sel = input("Select: ")
            try: return os.path.join(BASE_DIR, folders[int(sel)-1])
            except: pass

# --- 5. MAIN MENU ---
def main_menu():
    while True:
        print("\n" + "="*50)
        print(f"{'MP3/MP4 TURBO V3.1 (ENGLISH EDITION)':^50}") 
        print("="*50)
        print("1. Download Single Link")
        print("2. Download Playlist")
        print("3. Bulk (.txt)")
        print("4. File Manager (Manage/Delete Folders)")
        print("5. UPDATE ENGINE")
        print("6. UPDATE APP CODE")
        print("7. Exit")
        
        choice = input("Select: ")
        
        if choice in ['1', '2', '3']:
            dest = select_destination_folder()
            if not dest: continue
            print("\nFormat:\n1. MP3 Only\n2. Raw Video (No Audio)\n3. Video Combined (Playable)\n4. Video & MP3 (Separated)\n0. Back")
            fmt = input("Select Format: ")
            if fmt == '0': continue
            while True:
                link = input("\nPaste Link (0 to Back): ")
                if link == '0': break
                run_download([link], dest, fmt)
                print("\n1.Continue 2.Open Folder 3.Main Menu")
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
