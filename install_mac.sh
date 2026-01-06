#!/bin/bash

# Dapatkan directory folder ini
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
echo "[*] Detected Directory: $BASE_DIR"

# 1. Cipta file launcher 'mp4' (tanpa .bat)
echo "[*] Creating launcher..."
cat <<EOF > "$BASE_DIR/mp4"
#!/bin/bash
python3 "$BASE_DIR/main.py" "\$@"
EOF

# Jadikan ia executable
chmod +x "$BASE_DIR/mp4"

# 2. Tambah ke PATH (Support Zsh & Bash)
SHELL_CONFIG=""
if [ -n "$ZSH_VERSION" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_CONFIG="$HOME/.bash_profile"
else
    # Default ke .zshrc untuk macOS baru
    SHELL_CONFIG="$HOME/.zshrc"
fi

echo "[*] Updating Shell Config: $SHELL_CONFIG"

# Check if path already exists
if grep -q "$BASE_DIR" "$SHELL_CONFIG"; then
    echo "[!] Path already exists in config."
else
    echo "export PATH=\"\$PATH:$BASE_DIR\"" >> "$SHELL_CONFIG"
    echo "[+] Path added successfully!"
fi

echo ""
echo "=========================================="
echo " INSTALLATION COMPLETE!"
echo "=========================================="
echo "Please RESTART your terminal, then type: mp4"
echo "=========================================="