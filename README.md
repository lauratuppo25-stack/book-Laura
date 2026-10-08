# Laura Tuppo — Portfolio

Portfolio groovy et minimaliste en noir & blanc : graphisme, communication et photographie.

- `index.html` : la page complète (HTML + CSS + JS, sans dépendance).
- `images/` : tous les visuels des projets.

Ouvrir `index.html` dans un navigateur suffit. Pour le mettre en ligne gratuitement :
GitHub → *Settings* → *Pages* → *Deploy from a branch* → `main` / `root`.

## Ajouter un projet

Copier un bloc `<article class="project">` existant dans la bonne section
(`#graphisme`, `#communication` ou `#photographie`), puis :

1. déposer les images dans `images/` ;
2. pour chaque image, renseigner `--ar` (largeur ÷ hauteur), `width`, `height` et `alt` ;
3. ajouter une ligne correspondante dans le sommaire (`.index-list`).

Les visuels s'affichent en noir & blanc par défaut et passent en couleur au survol
ou via l'interrupteur « Couleur » de la barre de navigation.
