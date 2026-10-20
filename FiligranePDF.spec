from pathlib import Path
import sys

from PyInstaller.utils.hooks import collect_all

root = Path(SPECPATH)
dnd_datas, dnd_binaries, dnd_hiddenimports = collect_all('tkinterdnd2')
icon_name = 'icon.ico' if sys.platform == 'win32' else ('icon.icns' if sys.platform == 'darwin' else 'icon.png')
icon_path = root / icon_name
data_files = [(str(root / name), '.') for name in ('icon.png', 'icon.ico', 'icon.icns')]

a = Analysis(
    ['main.py'], pathex=[str(root)], binaries=dnd_binaries, datas=data_files + dnd_datas,
    hiddenimports=['fitz'] + dnd_hiddenimports, hookspath=[], hooksconfig={},
    runtime_hooks=[], excludes=[], noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz, a.scripts, a.binaries, a.datas, [], name='FiligranePDF',
    debug=False, bootloader_ignore_signals=False, strip=False, upx=True,
    console=False, icon=str(icon_path),
)
if sys.platform == 'darwin':
    app = BUNDLE(exe, name='Filigrane PDF.app', icon=str(icon_path), bundle_identifier='fr.filigranepdf.app')
