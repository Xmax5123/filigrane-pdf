#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "Ce script doit être exécuté sur macOS." >&2
  exit 1
fi
command -v hdiutil >/dev/null || { echo "hdiutil est introuvable." >&2; exit 1; }
python3 -m venv .buildvenv-macos
. .buildvenv-macos/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-build.txt
python -m PyInstaller --clean --noconfirm FiligranePDF.spec
hdiutil create -volname "Filigrane PDF" -srcfolder "dist/Filigrane PDF.app" -ov -format UDZO "dist/FiligranePDF-macOS.dmg"
echo "Application : dist/Filigrane PDF.app"
echo "Installateur à glisser dans Applications : dist/FiligranePDF-macOS.dmg"
