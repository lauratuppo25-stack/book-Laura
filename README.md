# Laura Tuppo — Portfolio

Portfolio dans la DA du CV : colonnes blanche et noire, rose poudré, nom en typo Art déco, titres en étiquettes arrondies. Communication & design graphique.

- `index.html` : le portfolio ; `cv.html` : la page CV (consultation et téléchargement).
- `assets/site.css`, `assets/site.js` : styles et animations communs aux deux pages.
- `cv/` : le CV en PDF et ses aperçus en image. Pour mettre à jour le CV, remplacer `cv/CV_Laura_Tuppo_2026.pdf` (et les deux images `cv-laura-tuppo*.jpg`).
- `images/` : tous les visuels des projets, plus `portrait-cutout.png` (portrait détouré du CV).

Ouvrir `index.html` dans un navigateur suffit. Pour le mettre en ligne gratuitement :
GitHub → *Settings* → *Pages* → *Deploy from a branch* → `main` / `root`.

## Ajouter ou modifier un projet

Les pages sont générées à partir du dossier `tools/` :

- `tools/template.html` (portfolio), `tools/cv.html` (page CV), `tools/site.css`, `tools/site.js` ;
- `tools/build.py` : la liste des projets (`P`), des expertises et du carnet d'images.

Pour ajouter un projet : déposer les images dans `images/`, ajouter une entrée dans la liste `P`
de `tools/build.py`, puis régénérer la page :

```
python3 tools/build.py .
```

(nécessite Python 3, Pillow et fontTools : `pip install pillow fonttools`)

### Typo Riesling

Le nom et les grands titres sont en **Riesling** (Bright Ideas, dafont). La police n'est pas publiée :
`tools/build.py` convertit ces textes en tracés SVG au moment de générer la page. Pour régénérer,
placer `riesling.ttf` dans `tools/` (le fichier est ignoré par git) ou indiquer son chemin :

```
RIESLING=/chemin/vers/riesling.ttf python3 tools/build.py .
```
