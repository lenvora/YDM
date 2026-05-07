# Maintainer: Lenvora
pkgname=ydm-git
pkgver=1.0.0
pkgrel=1
pkgdesc="YouTube Download Manager by Lenvora"
arch=('any')
url="https://github.com/lenvora/YDM"
license=('MIT')
depends=('pyside6' 'yt-dlp' 'python')
source=("git+https://github.com/lenvora/YDM.git")
md5sums=('SKIP')

package() {
  cd "$srcdir/YDM"
  
  install -d "$pkgdir/usr/share/ydm"
  install -d "$pkgdir/usr/share/pixmaps"
  install -d "$pkgdir/usr/share/applications"
  install -d "$pkgdir/usr/bin"
  
  cp -r * "$pkgdir/usr/share/ydm/"
  cp icon_2.png "$pkgdir/usr/share/pixmaps/ydm.png"
  
  echo -e "#!/bin/bash\npython /usr/share/ydm/main.py \"\$@\"" > "$pkgdir/usr/bin/ydm"
  chmod +x "$pkgdir/usr/bin/ydm"

  echo -e "[Desktop Entry]\nName=YDM\nComment=YouTube Download Manager\nExec=/usr/bin/ydm\nIcon=ydm\nTerminal=false\nType=Application\nCategories=Network;Video;" > "$pkgdir/usr/share/applications/ydm.desktop"
}
