import os
import winreg # Library untuk edit Registry Windows
import ctypes # Untuk refresh environment variable tanpa restart PC

def create_batch_file():
    """
    Fungsi ini mencipta fail mp4.bat yang akan memanggil main.py
    """
    current_dir = os.getcwd()
    bat_filename = "mp4.bat"
    bat_path = os.path.join(current_dir, bat_filename)
    main_py_path = os.path.join(current_dir, "main.py")

    # Content bat file. 
    # %~dp0 bermaksud "lokasi fail bat ini berada".
    # Jadi dia akan cari main.py di folder yang sama dengan bat file.
    bat_content = f'@echo off\npython "{main_py_path}" %*'

    try:
        with open(bat_path, "w") as bat_file:
            bat_file.write(bat_content)
        print(f"[+] Berjaya cipta fail: {bat_filename}")
        return True
    except Exception as e:
        print(f"[!] Gagal cipta .bat file: {e}")
        return False

def add_to_path():
    """
    Fungsi ini menambah folder semasa ke dalam User PATH Environment Variable
    """
    current_dir = os.getcwd()
    
    # Registry Key untuk User Environment Variables
    key_path = r"Environment"
    
    try:
        # Buka Registry
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
        
        try:
            # Baca value PATH sedia ada
            existing_path_value, _ = winreg.QueryValueEx(reg_key, "Path")
        except FileNotFoundError:
            existing_path_value = ""

        # Check kalau folder dah ada dalam PATH
        if current_dir.lower() in existing_path_value.lower():
            print(f"[*] Folder ini sudah ada dalam PATH. Tidak perlu update.")
        else:
            # Tambah folder baru ke PATH (pisahkan dengan semicolon ;)
            new_path_value = existing_path_value + ";" + current_dir if existing_path_value else current_dir
            
            # Simpan semula ke Registry
            winreg.SetValueEx(reg_key, "Path", 0, winreg.REG_EXPAND_SZ, new_path_value)
            print(f"[+] Berjaya tambah folder ke Environment PATH.")
            
            # Refresh Windows Environment supaya tak payah logout
            # HWND_BROADCAST = 0xFFFF, WM_SETTINGCHANGE = 0x001A
            ctypes.windll.user32.SendMessageTimeoutW(
                0xFFFF, 0x001A, 0, "Environment", 0, 5000, None
            )
            print("[+] Windows Environment refreshed!")

        winreg.CloseKey(reg_key)
        return True

    except Exception as e:
        print(f"[!] Error mengubah Registry: {e}")
        print("[!] Sila run script ini sebagai Administrator jika perlu.")
        return False

if __name__ == "__main__":
    print("--- MP3 TURBO INSTALLER ---")
    print(f"[*] Lokasi sekarang: {os.getcwd()}")
    
    step1 = create_batch_file()
    step2 = add_to_path()
    
    if step1 and step2:
        print("\n" + "="*50)
        print("PEMASANGAN BERJAYA!")
        print("="*50)
        print("Sekarang awak boleh buka CMD baru dan taip 'mp4' di mana-mana sahaja.")
        print("Nota: Jika tak jadi, sila tutup CMD ini dan buka semula.")
    else:
        print("\n[!] Ada masalah semasa pemasangan.")
    
    input("\nTekan Enter untuk keluar...")