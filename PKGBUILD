# Maintainer: Lenvora
pkgname=ydm-git
pkgver=1.0.0
pkgrel=2
pkgdesc="YouTube Download Manager by Lenvora"
arch=('any')
url="https://github.com/lenvora/YDM"
license=('MIT')
depends=('pyside6' 'yt-dlp' 'python')
source=("git+https://github.com/lenvora/YDM.git")
md5sums=('SKIP')

package() {
  cd "$srcdir/YDM"
  
  # Klasörleri oluştur
  mkdir -p "$pkgdir/usr/bin"
  mkdir -p "$pkgdir/usr/share/ydm"
  mkdir -p "$pkgdir/usr/share/pixmaps"
  
  # Kodları ve ikonu kopyala (venv hariç her şeyi)
  cp main.py "$pkgdir/usr/share/ydm/"
  cp icon.png "$pkgdir/usr/share/pixmaps/ydm.png"
  
  # Çalıştırma scriptini düzelt (Sistem python'ını kullanacak şekilde)
  echo -e "#!/bin/bash\npython /usr/share/ydm/main.py \"\$@\"" > "$pkgdir/usr/bin/ydm"
  chmod +x "$pkgdir/usr/bin/ydm"
}
