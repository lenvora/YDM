# Maintainer: Lenvora
pkgname=ydm-git
pkgver=1.0.0
pkgrel=1
pkgdesc="YouTube Download Manager by Lenvora"
arch=('any')
url="https://github.com/lenvora/YDM"
license=('MIT')
depends=('pyside6' 'yt-dlp')
source=("git+https://github.com/lenvora/YDM.git")
md5sums=('SKIP')

package() {
  cd "$srcdir/YDM"
  mkdir -p "$pkgdir/usr/bin"
  mkdir -p "$pkgdir/usr/share/ydm"
  
  cp -r * "$pkgdir/usr/share/ydm/"
  
  # Çalıştırma kısayolu oluştur (Mail falan yok burada)
  echo -e "#!/bin/bash\n/usr/share/ydm/venv/bin/python /usr/share/ydm/main.py \"\$@\"" > "$pkgdir/usr/bin/ydm"
  chmod +x "$pkgdir/usr/bin/ydm"
}
