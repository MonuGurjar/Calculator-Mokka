#!/bin/bash
set -e

echo "Installing Calculator-mokka..."

# Check if we are running locally (files exist here) or via curl
if [ -f "main.py" ] && [ -f "style.qss" ]; then
    # Local install
    INSTALL_DIR="$(pwd)"
else
    # Curl install: clone to ~/.local/share/Calculator-Mokka
    INSTALL_DIR="$HOME/.local/share/Calculator-Mokka"
    echo "Downloading files from GitHub to $INSTALL_DIR..."
    
    if [ -d "$INSTALL_DIR/.git" ]; then
        echo "Updating existing installation..."
        cd "$INSTALL_DIR"
        git pull
    else
        mkdir -p "$HOME/.local/share"
        git clone https://github.com/MonuGurjar/Calculator-Mokka.git "$INSTALL_DIR"
        cd "$INSTALL_DIR"
    fi
fi

# 1. Ensure run.sh is executable
chmod +x "$INSTALL_DIR/run.sh"

# 2. Setup the virtual environment if it doesn't exist
if [ ! -d "$INSTALL_DIR/.venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$INSTALL_DIR/.venv"
    echo "Installing requirements..."
    "$INSTALL_DIR/.venv/bin/pip" install -r "$INSTALL_DIR/requirements.txt"
fi

# 3. Create the .desktop file content
DESKTOP_FILE="$HOME/.local/share/applications/garuda-mokka-calc.desktop"

echo "Creating desktop entry at $DESKTOP_FILE..."

# Ensure the applications directory exists
mkdir -p "$HOME/.local/share/applications"

cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Calculator-mokka
Comment=A sleek neon dark-mode calculator
Exec=$INSTALL_DIR/run.sh
Icon=$INSTALL_DIR/icon.png
Terminal=false
Categories=Utility;Calculator;
EOF

# 4. Update the desktop database
echo "Updating desktop database..."
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$HOME/.local/share/applications"
fi

echo "Installation complete! You can now find 'Calculator-mokka' in your application menu."
