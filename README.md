# Filigrane PDF

Application de bureau pour ajouter un filigrane à plusieurs PDF en même temps. Les documents peuvent être déposés directement dans la liste ; la touche **Suppr** retire les éléments sélectionnés. Les fichiers sont traités localement.

## Télécharger une version compilée

Le workflow GitHub Actions `Build desktop packages` génère un ZIP Windows, un paquet `.deb` pour Ubuntu 22.04+, et un `.dmg` macOS. Il se lance manuellement depuis l’onglet Actions ou à la publication d’une balise `v*`.

## Construire localement

Installez Python 3.9 ou plus récent. Sur l’ordinateur correspondant au système visé, installez les dépendances puis lancez le script de compilation de cette plateforme :

- Windows : `python -m pip install -r requirements-build.txt`, puis `python -m PyInstaller --clean --noconfirm FiligranePDF.spec`
- Ubuntu : `bash build_ubuntu.sh` (produit un `.deb`)
- macOS : `bash build_macos.sh` (produit un `.dmg`)

PyInstaller construit les applications pour le système sur lequel il tourne ; les paquets Linux et macOS doivent donc être générés sur leurs plateformes respectives.

## Lancer les sources

```bash
python -m pip install -r requirements.txt
python main.py
```
