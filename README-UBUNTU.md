# Filigrane PDF pour Ubuntu

Le paquet Ubuntu doit être construit depuis Ubuntu (PyInstaller ne produit pas un exécutable Linux depuis Windows).

## Générer le paquet `.deb`

Sur Ubuntu 22.04 ou plus récent, ouvrez un terminal dans le dossier extrait et exécutez :

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip python3-tk dpkg-dev
chmod +x build_ubuntu.sh
./build_ubuntu.sh
```

Le fichier `.deb` sera créé dans `dist/`. Installez-le avec :

```bash
sudo apt install ./dist/FiligranePDF_1.0.0_*.deb
```

L’application apparaîtra dans le menu des applications sous **Filigrane PDF**. Le script construit le paquet pour l’architecture Ubuntu de l’ordinateur qui le lance (amd64 ou arm64, selon le cas). Pour distribuer aux autres, créez séparément le paquet sur chaque architecture visée.

## Lancer depuis les sources

```bash
python3 -m pip install -r requirements.txt
python3 main.py
```
