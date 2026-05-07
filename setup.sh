#!/bin/bash

cd "$(dirname "$0")"

echo "🚀 YDM Installation is starting..."

python -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

APP_PATH=$(pwd)
DESKTOP_FILE="$HOME/.local/share/applications/ydm.desktop"

echo "[Desktop Entry]
Name=YDM
Comment=YouTube Download Manager
Exec=$APP_PATH/venv/bin/python $APP_PATH/main.py
Icon=$APP_PATH/icon.png
Terminal=false
Type=Application
Categories=Network;Utility;" > $DESKTOP_FILE

chmod +x $DESKTOP_FILE

if command -v kbuildsycoca6 &> /dev/null; then

    kbuildsycoca6 --noincremental

elif command -v update-desktop-database &> /dev/null; then

    update-desktop-database ~/.local/share/applications

fi

echo "✅ Installation complete! You can now find 'YDM' in your Application Menu."
