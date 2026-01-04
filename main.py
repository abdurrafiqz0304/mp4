import os
import subprocess # Diperlukan untuk run command git
import sys

# --- FUNGSI 1: SYSTEM UPDATE (GIT PULL) ---
def system_update():
    print("\n--- SYSTEM UPDATE ---")
    print("[*] Checking for updates from author...")
    try:
        # Menjalankan command 'git pull'
        result = subprocess.run(["git", "pull"], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"[+] Output:\n{result.stdout}")
            print("[+] System updated successfully! Please restart the tool.")
        else:
            print(f"[!] Git Error:\n{result.stderr}")
            print("[!] Make sure git is installed and this is a cloned repository.")
            
    except Exception as e:
        print(f"[!] Error: {e}")
    
    input("\nPress Enter to return to Home...")

# --- FUNGSI 2: PILIH DESTINATION FOLDER ---
def select_destination_folder():
    default_folder = 'Downloads_Video'
    
    while True:
        print("\n--- SELECT DESTINATION FOLDER ---")
        print(f"1. Use Default ('{default_folder}')")
        print("2. Use Current Folder (Save here)")  # <-- OPSI BARU
        print("3. Create / Use Custom Folder Name")
        print("0. Back")
        
        choice = input(">> ")
        
        selected_folder = ""
        
        if choice == '1':
            selected_folder = default_folder
            break
            
        elif choice == '2':
            # '.' bermaksud current directory
            selected_folder = "." 
            print("[*] Selected current folder.")
            break
            
        elif choice == '3':
            custom_name = input("Enter custom folder name: ")
            if custom_name.strip():
                selected_folder = custom_name
                break
            else:
                print("[!] Folder name cannot be empty.")
                
        elif choice == '0':
            return None
            
        else:
            print("[!] Invalid selection.")

    # Logic Create Folder (Kecuali jika user pilih Current Folder '.')
    if selected_folder and selected_folder != ".":
        if not os.path.exists(selected_folder):
            try:
                os.makedirs(selected_folder)
                print(f"[+] Folder '{selected_folder}' created.")
            except OSError as e:
                print(f"[!] Error creating folder: {e}")
                return None
        else:
            print(f"[*] Using existing folder: '{selected_folder}'")
            
    return selected_folder

# --- FUNGSI 3: MENU UTAMA (HOME) ---
def main_menu():
    while True:
        # Clear screen sikit bagi kemas (optional)
        # os.system('cls' if os.name == 'nt' else 'clear')
        
        print("\n=== MAIN MENU (HOME) ===")
        print("1. Start Downloader (Select Destination)")
        print("2. System Update (Git Pull)") # <-- MENU BARU
        print("0. Exit")
        
        choice = input(">> ")
        
        if choice == '1':
            folder = select_destination_folder()
            if folder:
                # Masukkan logic downloader awak di sini nanti
                print(f"\n[SUCCESS] Ready to download into: {folder}")
                # downloader_function(folder) ...
        
        elif choice == '2':
            system_update()
            
        elif choice == '0':
            print("Exiting...")
            sys.exit()
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nForce Quit.")