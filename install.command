#!/bin/bash

# 1. Masuk ke folder di mana fail ini berada (PENTING untuk Mac)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "=========================================="
echo "      MP3/MP4 TURBO - MAC AUTO INSTALLER"
echo "=========================================="

# 2. Setup Permission untuk fail Python & Script
chmod +x main.py
echo "[*] Permission ditetapkan."

# 3. Cipta fail pemicu 'mp4'
echo "[*] Mencipta shortcut global 'mp4'..."
cat <<EOF > mp4
#!/bin/bash
python3 "$DIR/main.py" "\$@"
EOF

# Jadikan shortcut itu executable
chmod +x mp4

# 4. Tambah ke dalam PATH (Zsh / Bash)
SHELL_CONFIG="$HOME/.zshrc"
if [ -n "$BASH_VERSION" ]; then
    SHELL_CONFIG="$HOME/.bash_profile"
fi

if grep -q "$DIR" "$SHELL_CONFIG"; then
    echo "[!] Path sudah wujud. Tiada perubahan."
else
    echo "" >> "$SHELL_CONFIG"
    echo "# MP3 TURBO PATH" >> "$SHELL_CONFIG"
    echo "export PATH=\"\$PATH:$DIR\"" >> "$SHELL_CONFIG"
    echo "[+] Path ditambah ke $SHELL_CONFIG"
fi

# 5. Refresh Config (Cuba refresh on-the-spot)
source "$SHELL_CONFIG" > /dev/null 2>&1

echo ""
echo "=========================================="
echo " SIAP! SILA TUTUP TERMINAL INI."
echo " Buka Terminal baru dan taip: mp4"
echo "=========================================="
# Arahan supaya terminal tak terus tutup, user boleh baca log
read -p "Tekan Enter untuk keluar..."