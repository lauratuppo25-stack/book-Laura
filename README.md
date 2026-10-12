# Laura Tuppo — Portfolio

Portfolio éditorial sur fond noir et crème, projets en couleur. Communication & design graphique.

- `index.html` : la page complète (HTML + CSS + JS, sans dépendance).
- `images/` : tous les visuels des projets.

Ouvrir `index.html` dans un navigateur suffit. Pour le mettre en ligne gratuitement :
GitHub → *Settings* → *Pages* → *Deploy from a branch* → `main` / `root`.

## Ajouter ou modifier un projet

`index.html` est généré à partir de deux fichiers du dossier `tools/` :

- `tools/template.html` : la mise en page (CSS, sections, scripts) ;
- `tools/build.py` : la liste des projets (`P`), des expertises et du carnet d'images.

Pour ajouter un projet : déposer les images dans `images/`, ajouter une entrée dans la liste `P`
de `tools/build.py`, puis régénérer la page :

```
python3 tools/build.py .
```

(nécessite Python 3 et Pillow : `pip install pillow`)
