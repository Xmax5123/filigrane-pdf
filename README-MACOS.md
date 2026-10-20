# Filigrane PDF pour macOS

Le fichier `.app` et le disque `.dmg` doivent être générés sur un Mac. PyInstaller ne fabrique pas une application macOS depuis Windows.

## Générer l’application et le `.dmg`

Sur macOS 12 ou plus récent, avec Python 3 installé, ouvrez Terminal dans le dossier extrait et lancez :

```bash
chmod +x build_macos.sh
./build_macos.sh
```

Le script crée `dist/Filigrane PDF.app` et `dist/FiligranePDF-macOS.dmg`. Ouvrez le `.dmg`, puis glissez l’application dans **Applications**.

La compilation doit être faite sur chaque architecture Mac visée (Apple Silicon ou Intel). L’application générée n’est pas signée ni notariée par Apple ; macOS peut afficher un avertissement lors du premier lancement. Pour une distribution publique sans cet avertissement, il faut signer et notarier l’application avec un compte développeur Apple.

## Lancer depuis les sources

```bash
python3 -m pip install -r requirements.txt
python3 main.py
```
