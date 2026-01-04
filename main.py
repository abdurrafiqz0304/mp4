import os

def select_destination_folder():
    default_folder = 'Downloads_Video'
    
    while True:
        # 1. Paparkan Menu (Print interface)
        print("\n--- SELECT DESTINATION FOLDER ---")
        print(f"1. Use Default ('{default_folder}')")
        print("2. Create / Use Custom Folder Name")
        print("0. Back")
        
        # 2. Minta Input Pengguna
        choice = input(">> ") # Atau boleh guna 'Choice: '
        
        selected_folder = ""
        
        # 3. Proses Pilihan (Logic)
        if choice == '1':
            selected_folder = default_folder
            print(f"[*] Default folder selected: {selected_folder}")
            break
            
        elif choice == '2':
            custom_name = input("Enter custom folder name: ")
            # Buang whitespace jika ada
            if custom_name.strip(): 
                selected_folder = custom_name
                print(f"[*] Custom folder selected: {selected_folder}")
                break
            else:
                print("[!] Folder name cannot be empty.")
                
        elif choice == '0':
            print("[*] Going back...")
            return None  # Kembali ke menu sebelumnya
            
        else:
            print("[!] Invalid selection. Please try again.")
    
    # 4. Cipta Folder jika belum wujud (Create directory)
    if selected_folder:
        if not os.path.exists(selected_folder):
            try:
                os.makedirs(selected_folder)
                print(f"[+] Folder '{selected_folder}' created successfully.")
            except OSError as e:
                print(f"[!] Error creating folder: {e}")
        else:
            print(f"[*] Using existing folder: '{selected_folder}'")
            
    return selected_folder

# --- Main Execution ---
if __name__ == "__main__":
    # Jalankan fungsi
    folder = select_destination_folder()