import os
import sys
import subprocess

# --- FUNGSI 1: SYSTEM UPDATE (GIT PULL) ---
# Ini untuk feature "6. UPDATE APP CODE" dalam gambar
def update_app_code():
    print("\n--- UPDATE APP CODE ---")
    print("[*] Checking for updates...")
    try:
        result = subprocess.run(["git", "pull"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[+] Git Output:\n{result.stdout}")
            print("[+] App updated successfully! Sila restart tool ini.")
        else:
            print(f"[!] Update Error:\n{result.stderr}")
            print("[!] Pastikan git installed.")
    except Exception as e:
        print(f"[!] Error: {e}")
    input("\nTekan Enter untuk kembali...")

# --- FUNGSI 2: LOGIC FOLDER SEDIA ADA ---
# Ini yang akan listkan folder macam dalam gambar ke-3
def pilih_folder_sedia_ada():
    # Dapatkan senarai semua folder dalam directory sekarang (.)
    # Kita filter supaya ambil folder sahaja (isdir) dan abaikan folder tersembunyi (.)
    all_items = os.listdir('.')
    folders = [f for f in all_items if os.path.isdir(f) and not f.startswith('.')]
    folders.sort() # Susun ikut abjad

    if not folders:
        print("\n[!] Tiada folder lain dijumpai di sini.")
        return None

    while True:
        # Paparkan list folder dengan nombor
        # Rujukan Gambar 3: List folder dipaparkan (cth: 1. DAN DA DAN...)
        print("\n--- PILIH FOLDER SEDIA ADA ---")
        for index, folder_name in enumerate(folders, 1):
            print(f"{index}. {folder_name}")
        print("0. < KEMBALI")

        choice = input("Pilih: ") # Rujukan Gambar 3

        if choice == '0':
            return None
        
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(folders):
                selected = folders[choice_idx]
                print(f"[*] Folder dipilih: {selected}")
                return selected
            else:
                print("[!] Nombor tidak sah.")
        except ValueError:
            print("[!] Sila masukkan nombor.")

# --- FUNGSI 3: MENU PILIH FOLDER ---
def select_destination_folder():
    default_folder = 'downloads'
    
    while True:
        # Tiru style Gambar 1
        print("\n--- PILIH FOLDER ---")
        print(f"1. '{default_folder}' (Default)")
        print("2. Folder Baru")
        print("3. Folder Sedia Ada")
        print("0. < KEMBALI")
        
        choice = input("Pilihan: ") # Rujukan Gambar 1
        
        selected_folder = ""
        
        if choice == '1':
            selected_folder = default_folder
            break
            
        elif choice == '2':
            custom_name = input("Nama Folder Baru: ")
            if custom_name.strip():
                selected_folder = custom_name
                break
            else:
                print("[!] Nama folder tidak boleh kosong.")

        elif choice == '3':
            # Panggil fungsi khas untuk listkan folder
            existing = pilih_folder_sedia_ada()
            if existing:
                selected_folder = existing
                break
            # Jika user tekan 0 (Back) dalam menu folder, loop akan ulang menu utama folder
                
        elif choice == '0':
            return None
            
        else:
            print("[!] Pilihan tidak sah.")

    # Logic Create/Check Folder
    if selected_folder:
        if not os.path.exists(selected_folder):
            try:
                os.makedirs(selected_folder)
                print(f"[+] Folder '{selected_folder}' berjaya dicipta.")
            except OSError as e:
                print(f"[!] Error create folder: {e}")
                return None
            
    return selected_folder

# --- FUNGSI 4: MENU UTAMA (HOME) ---
def main_menu():
    while True:
        # Tiru style Gambar 2 (MP3 TURBO)
        print("\n" + "="*50)
        print("   MP3 TURBO V2.1 (SELF-UPDATER)")
        print("="*50)
        print("1. Download Single Link")
        print("2. Download Playlist")
        print("3. Bulk (.txt)")
        print("4. File Manager")
        print("5. UPDATE ENGINE (Fix Slow Speed)") # Dummy feature
        print("6. UPDATE APP CODE (Dapatkan Feature Baru)") # Rujukan Gambar 2
        print("7. Keluar")
        
        choice = input("Pilih: ")
        
        if choice in ['1', '2', '3']:
            # Langkah 1: Pilih folder dulu
            dest = select_destination_folder()
            
            if dest:
                # Langkah 2: Logic download (placeholder)
                print(f"\n[INFO] Memulakan proses dalam folder: '{dest}'")
                # Jika user pilih quality (Gambar 3 bawah), boleh tambah logic di sini
                # quality_menu() ...
                input("Tekan Enter untuk sambung demo...")

        elif choice == '6':
            update_app_code() # Jalankan git pull

        elif choice == '7':
            print("Keluar...")
            sys.exit()
            
        else:
            print("[!] Pilihan belum siap atau tidak sah.")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nForce Quit.")