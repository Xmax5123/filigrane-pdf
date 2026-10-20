#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$(readlink -f "$0")")"
if [[ "$(uname -s)" != "Linux" ]]; then
  echo "Ce script doit être exécuté sur Ubuntu/Linux." >&2
  exit 1
fi
for command in dpkg-deb dpkg python3; do
  command -v "$command" >/dev/null || { echo "Commande manquante: $command" >&2; exit 1; }
done

python3 -m venv .buildvenv-linux
. .buildvenv-linux/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-build.txt
python -m PyInstaller --clean --noconfirm FiligranePDF.spec

stage="build/deb-root"
rm -rf "$stage"
mkdir -p "$stage/DEBIAN" "$stage/opt/filigrane-pdf" "$stage/usr/share/applications" "$stage/usr/share/icons/hicolor/256x256/apps"
install -m 755 dist/FiligranePDF "$stage/opt/filigrane-pdf/filigrane-pdf"
install -m 644 icon.png "$stage/usr/share/icons/hicolor/256x256/apps/filigrane-pdf.png"
cat > "$stage/usr/share/applications/filigrane-pdf.desktop" <<'EOF'
[Desktop Entry]
Type=Application
Name=Filigrane PDF
Comment=Ajouter un filigrane répété à des documents PDF
Exec=/opt/filigrane-pdf/filigrane-pdf
Icon=filigrane-pdf
Terminal=false
Categories=Office;Utility;
EOF
arch="$(dpkg --print-architecture)"
cat > "$stage/DEBIAN/control" <<EOF
Package: filigrane-pdf
Version: 1.0.0
Section: graphics
Priority: optional
Architecture: ${arch}
Maintainer: Filigrane PDF
Description: Application de filigrane pour PDF
 Outil graphique pour traiter un ou plusieurs PDF avec un filigrane répété.
EOF
mkdir -p dist
dpkg-deb --root-owner-group --build "$stage" "dist/FiligranePDF_1.0.0_${arch}.deb"
echo "Paquet créé : dist/FiligranePDF_1.0.0_${arch}.deb"
