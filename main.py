import yt_dlp
import os
import platform
import subprocess
import sys
import shutil

# --- CONFIGURATION ---
FFMPEG_FILENAME = 'ffmpeg.exe'

# --- FUNGSI BANTUAN ---
def open_folder_window(path):
    try:
        if not os.path.exists(path):
            print(f"❌ Folder '{path}' tidak wujud.")
            return
        if platform.system() == "Windows": os.startfile(path)
        else: subprocess.call(["open" if platform.system() == "Darwin" else "xdg-open", path])
        print(f"📂 Folder dibuka: '{path}'")
    except Exception as e: print(f"❌ Error buka folder: {e}")

def get_ffmpeg_path():
    # 1. Cek Local
    script_dir = os.path.dirname(os.path.abspath(__file__))
    local_ffmpeg = os.path.join(script_dir, 'ffmpeg.exe')
    if os.path.exists(local_ffmpeg): return local_ffmpeg
    # 2. Cek Global
    system_ffmpeg = shutil.which('ffmpeg')
    if system_ffmpeg: return system_ffmpeg
    return None

# --- SYSTEM: FILE MANAGER (DELETE SELECTED/FOLDER) ---
def delete_files_interactive(folder_path):
    """Style mp4tomp3: Pilih nombor fail untuk delete"""
    while True:
        # Scan semua fail
        all_files = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, folder_path)
                all_files.append((rel_path, full_path))
        
        all_files.sort(key=lambda x: x[0])

        if not all_files:
            print("\n(Folder kosong / Tiada fail)")
            input("[Enter] untuk kembali")
            return

        print(f"\n--- PADAM FAIL DALAM: '{folder_path}' ---")
        for i, (name, path) in enumerate(all_files, 1):
            try: size_mb = os.path.getsize(path) / (1024 * 1024)
            except: size_mb = 0
            print(f"{i}. {name} ({size_mb:.2f} MB)")
        print("0. Kembali")

        print("\nCara Pilih: Taip nombor (contoh: 1,3,5) untuk delete fail tersebut.")
        print("Atau taip 'all' untuk delete semua.")
        choice = input("Pilihan: ").strip()
        
        if choice == '0': return
        
        to_delete = []
        if choice.lower() == 'all':
            if input(f"⚠️ AMARAN: Padam SEMUA {len(all_files)} fail? (y/n): ").lower() == 'y':
                to_delete = all_files
        else:
            try:
                indices = [int(x.strip()) for x in choice.split(',')]
                for idx in indices:
                    if 1 <= idx <= len(all_files):
                        to_delete.append(all_files[idx-1])
            except:
                print("❌ Input salah. Guna koma (,) untuk asingkan nombor.")
                continue
        
        if to_delete:
            print(f"\nMemadam {len(to_delete)} fail...")
            for name, path in to_delete:
                try: 
                    os.remove(path)
                    print(f"🗑️ Deleted: {name}")
                except Exception as e: print(f"❌ Error: {e}")
            input("\n[Enter] untuk Refresh List")

def file_manager_menu():
    while True:
        # Scan folder sedia ada
        folders = [d for d in os.listdir('.') if os.path.isdir(d) and not d.startswith('.') and not d.startswith('__')]
        
        print("\n" + "="*40); print("    📁 PENGURUS FAIL (FILE MANAGER)    "); print("="*40)
        
        if not folders:
            print("(Tiada folder dijumpai)")
            if input("0. Kembali (Enter): "): return
            return

        for i, d in enumerate(folders, 1): print(f"{i}. {d}")
        print("0. Kembali")

        try:
            c = int(input("\nPilih Folder untuk Urus: "))
            if c == 0: return
            selected_folder = folders[c-1]
        except: continue

        while True:
            print(f"\n--- MENGURUS: '{selected_folder}' ---")
            print("1. Buka Folder (Explorer)")
            print("2. Pilih & Padam Video (Selected Delete)")
            print("3. PADAM FOLDER INI (Delete Entire Folder)")
            print("0. Kembali")
            
            act = input("Pilihan: ").strip()
            
            if act == '0': break
            if act == '1': open_folder_window(selected_folder)
            if act == '2': delete_files_interactive(selected_folder)
            if act == '3':
                confirm = input(f"⚠️ ADKAH ANDA PASTI nak buang folder '{selected_folder}'? (yes/no): ")
                if confirm.lower() == 'yes':
                    try: 
                        shutil.rmtree(selected_folder)
                        print("✅ Folder berjaya dibuang.")
                        break # Keluar dari menu ni sebab folder dah hilang
                    except Exception as e: print(f"❌ Error: {e}")

# --- SYSTEM: FOLDER SELECTOR (NEW FEATURE) ---
def select_folder_menu(default_name):
    while True:
        print(f"\n--- PILIH FOLDER SIMPANAN ---")
        print(f"1. Guna Default ('{default_name}')")
        print(f"2. Buat Folder Baru (Custom Name)")
        print(f"3. Pilih Folder Sedia Ada (List Existing)")
        print("0. Kembali")
        
        c = input("Pilihan: ").strip()
        if c == '0': return None
        if c == '1': return default_name
        
        if c == '2':
            name = input("Masukkan nama folder baru: ").strip()
            return name if name else default_name
            
        if c == '3':
            # Scan folder untuk dipilih
            folders = [d for d in os.listdir('.') if os.path.isdir(d) and not d.startswith('.') and not d.startswith('__')]
            if not folders:
                print("❌ Tiada folder lain dijumpai.")
                continue
                
            print("\n--- FOLDER SEDIA ADA ---")
            for i, d in enumerate(folders, 1):
                print(f"{i}. {d}")
            print("0. Cancel")
            
            try:
                idx = int(input("Pilih nombor: "))
                if idx == 0: continue
                return folders[idx-1]
            except:
                print("❌ Pilihan tidak sah.")

# --- CORE DOWNLOAD ENGINE ---
def run_downloader(urls, format_mode, quality_opt, base_folder):
    if not os.path.exists(base_folder): os.makedirs(base_folder)
    
    ffmpeg_loc = get_ffmpeg_path()
    if not ffmpeg_loc:
        print(f"\n❌ CRITICAL: FFmpeg tak jumpa. Sila run install.bat!")
        return

    path_mp3 = base_folder
    path_mp4 = base_folder
    
    if format_mode == 'both':
        path_mp3 = os.path.join(base_folder, "Audio_MP3")
        path_mp4 = os.path.join(base_folder, "Video_MP4")
        if not os.path.exists(path_mp3): os.makedirs(path_mp3)
        if not os.path.exists(path_mp4): os.makedirs(path_mp4)

    opts_list = [] 
    res = 2160 if quality_opt == 'high' else (1080 if quality_opt == 'mid' else 480)
    kbps = '320' if quality_opt == 'high' else '128'
    
    common_opts = {
        'ffmpeg_location': ffmpeg_loc, 'quiet': False, 'no_warnings': True,
        'noplaylist': False, 'ignoreerrors': True,
    }

    if format_mode in ['mp3', 'both']:
        mp3_opts = common_opts.copy()
        mp3_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': kbps}],
            'outtmpl': f'{path_mp3}/%(title)s.%(ext)s', 
        })
        opts_list.append(("🎵 AUDIO (MP3)", mp3_opts))

    if format_mode in ['mp4', 'both']:
        mp4_opts = common_opts.copy()
        mp4_opts.update({
            'format': f"bestvideo[height<={res}]+bestaudio/best[height<={res}]",
            'merge_output_format': 'mp4',
            'postprocessor_args': {'merger': ['-c:a', 'aac']}, # Fix Opus Issue
            'outtmpl': f'{path_mp4}/%(title)s.%(ext)s',
        })
        opts_list.append(("🎬 VIDEO (MP4)", mp4_opts))

    if format_mode == 'mute':
        mute_opts = common_opts.copy()
        mute_opts.update({
            'format': f"bestvideo[height<={res}]",
            'merge_output_format': 'mp4',
            'outtmpl': f'{base_folder}/%(title)s [NOSOUND].%(ext)s',
        })
        opts_list.append(("🔇 VIDEO (NO SOUND)", mute_opts))

    print("\n" + "="*50)
    print(f"   MEMPROSES... ({len(urls)} Link)   ")
    print(f"   📂 Target: {base_folder}")
    print("="*50)

    for label, options in opts_list:
        print(f"\n⬇️  SEDANG DOWNLOAD: {label}...")
        with yt_dlp.YoutubeDL(options) as ydl:
            for url in urls:
                try: ydl.download([url.strip()])
                except Exception as e: print(f"❌ Error: {e}")

# --- MAIN MENU ---
def update_engine():
    print("\n[SYSTEM] Mengemaskini yt-dlp...")
    try: subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"]); print("✅ Updated.")
    except: print("❌ Failed.")
    input("[Enter]")

def main_menu():
    while True:
        print("\n" + "="*50); print("   🔥 ULTIMATE DOWNLOADER V7 (MANAGER) 🔥   "); print("="*50)
        print("1. MP3 Sahaja")
        print("2. MP4 Sahaja (Auto Fix Audio)")
        print("3. COMBO (Split Folders)")
        print("4. VIDEO BISU (No Sound)")
        print("5. FILE MANAGER (Delete Files/Folders)")
        print("6. Update System")
        print("0. Keluar")
        
        pilih = input("\nPilihan: ").strip()

        if pilih == '0': break
        if pilih == '6': update_engine(); continue
        if pilih == '5': file_manager_menu(); continue # Menu Delete kat sini
        
        mode = ''; def_folder = 'Downloads'
        if pilih == '1': mode = 'mp3'; def_folder = 'Downloads_Music'
        elif pilih == '2': mode = 'mp4'; def_folder = 'Downloads_Video'
        elif pilih == '3': mode = 'both'; def_folder = 'Downloads_Combo' 
        elif pilih == '4': mode = 'mute'; def_folder = 'Downloads_RawFootage'
        else: continue

        print(f"\n--- KUALITI ---")
        print("1. High (4K / 320kbps)")
        print("2. Medium (1080p / 128kbps)")
        print("3. Low (480p)")
        print("0. Back")
        q = input("Pilihan: ").strip()
        if q == '0': continue
        qual = 'high' if q == '1' else ('low' if q == '3' else 'mid')

        # NEW: Select Existing Folder Logic
        target_folder = select_folder_menu(def_folder)
        if target_folder is None: continue

        print("\n--- SUMBER ---")
        print("1. Paste Link")
        print("2. Bulk (.txt)")
        print("0. Back")
        s = input("Pilihan: ").strip()
        if s == '0': continue
        
        links = []
        if s == '2':
            fn = input("Nama file txt: ")
            if os.path.exists(fn): 
                with open(fn) as f: links = f.readlines()
        else:
            raw = input("Link: ")
            if raw: links = [raw]

        if links:
            run_downloader(links, mode, qual, target_folder)
            print("\n✅ Siap.")
            if input("Buka folder? (y/n): ").lower() == 'y': open_folder_window(target_folder)

if __name__ == "__main__":
    main_menu()