# Laura Tuppo — Portfolio

Portfolio sur fond noir, interface épurée, projets en couleur. Communication & design graphique.

- `index.html` : la page complète (HTML + CSS + JS, sans dépendance).
- `images/` : tous les visuels des projets.

Ouvrir `index.html` dans un navigateur suffit. Pour le mettre en ligne gratuitement :
GitHub → *Settings* → *Pages* → *Deploy from a branch* → `main` / `root`.

## Ajouter un projet

Copier un bloc `<article class="project">` existant, puis :

1. déposer les images dans `images/` ;
2. pour chaque image, renseigner `--ar` (largeur ÷ hauteur), `width`, `height` et `alt` ;
3. ajouter la ligne correspondante dans l'index (`.index`), avec le même `data-cat`
   (`graphisme`, `communication` ou `photo`), et mettre à jour les compteurs du filtre.

