#!/bin/bash
# Dapatkan folder semasa
DIR="$(cd "$(dirname "$0")" && pwd)"

# Setup shortcut 'mp4'
echo "Creating launcher..."
cat <<EOF > "$DIR/mp4"
#!/bin/bash
python3 "$DIR/main.py" "\$@"
EOF
chmod +x "$DIR/mp4"

# Tambah ke PATH (Auto-detect Zsh atau Bash)
RC_FILE="$HOME/.zshrc"
[ -n "$BASH_VERSION" ] && RC_FILE="$HOME/.bash_profile"

if grep -q "$DIR" "$RC_FILE"; then
    echo "Path already exists."
else
    echo "export PATH=\"\$PATH:$DIR\"" >> "$RC_FILE"
    echo "Path added!"
fi

# Cuba refresh terminal on-the-spot
source "$RC_FILE" > /dev/null 2>&1

echo "---------------------------------------"
echo " SUCCESS! Please Restart Terminal."
echo " Then type: mp4"
echo "---------------------------------------"