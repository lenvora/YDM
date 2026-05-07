#!/bin/bash

echo "🚀 YDM Installation is starting..."

# Install dependencies
pip install -r requirements.txt

# Create .desktop file for the Application Menu
cat <<EOF > $HOME/.local/share/applications/ydm.desktop
[Desktop Entry]
Name=YDM (YouTube Downloader)
Comment=Professional YouTube Downloader by Lenvora
Exec=python3 $(pwd)/main.py
Icon=download
Terminal=false
Type=Application
Categories=Network;Video;
EOF

chmod +x $HOME/.local/share/applications/ydm.desktop

echo "✅ Installation complete! You can now find 'YDM' in your Application Menu."
