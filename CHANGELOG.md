# Notes de version

Stylus n'installe une mise à jour que si le numéro `@version` change. Il monte à chaque modification :
le dernier chiffre pour une correction, celui du milieu pour une nouveauté.

## Claude rapide 1.0.0 · Question rapide · 13 novembre 2026

Nouveau style `claude-rapide.user.css`, seulement pour claude.ai ouvert en fenêtre appli (`--app=https://claude.ai/new`) :
- plus que la zone de texte, centrée sur la page d'accueil, et le choix du modèle à droite ;
- cachés : barre latérale, barre du haut (incognito, titre, Partager), salutation, artéfacts récents, « Projet », « Auto », trombone, micro, mode vocal, « Claude est une IA et peut commettre des erreurs » ;
- pas d'étoile devant les titres, rien ne penche au survol, même si Stylus magique est allumé sur claude.ai ;
- les onglets ne changent pas (`@media (display-mode: standalone)`).

## Stylus étude 1.1.0 · Repos des yeux · 12 novembre 2026

Nouveau :
- Formules de Wikipédia et graphiques de Desmos et GeoGebra au gris du texte (ils étaient blanc pur) ; pareil pour les pages que le thème inverse (sites sans mode sombre, mails HTML de Gmail).
- YouTube : miniatures en gris, la couleur revient au survol de la vidéo.
- Les animations qui tournent en boucle sur les sites (bandeaux, cases grises qui clignotent, etc.) s'arrêtent après un tour ; les ronds de chargement continuent.
- Texte 10 % plus grand sur Wikipédia et les autres wikis, ArchWiki, la doc Python et Moodle.

## Stylus étude 1.0.1 · J'aime · 12 novembre 2026

Corrigé :
- YouTube : J'aime et Je n'aime pas formaient deux boutons séparés, le bord d'une seule moitié s'allumait au survol. Ils redeviennent une seule pastille grise avec un trait fin au milieu, dont tout le bord s'éclaircit au survol.

## Stylus étude 1.0.0 · Premier jet · 12 novembre 2026

Nouveau thème `stylus-etude.user.css`, fabriqué à partir de Stylus magique par `tools/etude.py` :
- couleurs « Encre » : texte gris clair, traits gris, liens lavande, violet seulement sur le bouton principal, icônes grises comme le texte ;
- plus de relief, de bascule ni d'étoiles ; au survol, seul le bord s'éclaircit ; polices des sites ;
- rouge seulement pour le curseur de texte, les erreurs et le danger ;
- images à 70 %, normales au survol ; compteurs en pastilles grises discrètes ;
- YouTube : plus de vidéos proposées ni de Shorts, la playlist et le chat restent ;
- interligne 1,7 sur Wikipédia, ArchWiki et la doc Python ; Stack Exchange : 80 caractères par ligne et interligne 1,7.

## Lecteur PDF · Languettes · 11 novembre 2026

Changé (`pdfjs/magique-pdfjs.css`, arrive tout seul par le timer) :
- La barre du haut est coupée en deux languettes accrochées au bord : à gauche le volet, la recherche, les pages et le zoom ; à droite les outils, télécharger, imprimer et ». Le milieu reste libre pour la barre d'Helium.
- Chaque languette dépasse de quelques pixels et descend seulement quand la souris arrive dans les 40 px du haut de son côté (avant : dès les 88 px du haut, sur toute la largeur).
- Tout à la même hauteur : boutons de 32 px, numéro de page et zoom en petites pastilles.
- « Zoom automatique » s'affiche « Auto » (la liste garde les noms complets).
- Télécharger passe à gauche de l'imprimante.

## 1.2.2 · Démarrage · 9 novembre 2026

Corrigé :
- WhatsApp : l'écran de démarrage était blanc (il s'affiche avant que le thème sombre soit chargé). Il est noir, avec une ✦ qui scintille à la place du logo et une barre violette.

## 1.2.1 · Compteur · 9 novembre 2026

Corrigé :
- WhatsApp : le nombre de messages non lus était blanc sur l'étiquette claire, donc invisible ; il est maintenant foncé.

## 1.2.0 · Salons · 9 novembre 2026

Nouveau :
- Instagram : 3 ✦ violet clair à la place des 3 points « en train d'écrire », elles gardent leur rebond.

Changé :
- Discord : plus de # devant les salons textuels ; dans les salons vocaux, le haut-parleur passe juste après le nom.

## 1.1.0 · Les étoiles · 9 novembre 2026

Nouveau :
- Les étoiles du portfolio : ✦ devant les gros titres, dans les étiquettes, dans un carré violet devant la rubrique en cours.
- Grande étoile à 8 branches au coin des boutons principaux et des cartes, environ un survol sur trois.
- ✦ qui scintille à la place des roues de chargement et des écrans de démarrage (Gmail, WhatsApp, Discord, Google Messages).
- 3 ✦ à la place des 3 points « en train d'écrire » (Discord, Google Messages, WhatsApp).

Changé :
- Gmail : mails non lus en gras avec une fine barre violette à gauche, sans cadre.
- WhatsApp : chiffre du compteur de non lus lisible, avec une ✦ dans l'étiquette.
- Carré de la rubrique en cours : carré violet, bord fin, vraie ✦ aqua au centre.
- Titres dont le texte est en bloc : l'étoile suit l'alignement du texte (titres centrés).

Corrigé :
- Instagram : nom du compte en haut des messages coupé, étoile au-dessus au lieu d'à gauche.
- YouTube : l'ombre des boutons J'aime / Partager mordait sur la description.
- Pas d'étoile sur les titres invisibles, les icônes, les logos, la recherche, les bandeaux du haut, ni les petits titres (Discord, LinkedIn, Agenda, Traduction, Amazon…).

À part, le lecteur PDF (`pdfjs/magique-pdfjs.css`, mis à jour par son timer) : fond violet et bord rouge comme Xournal, barre du haut en capsule, mot trouvé visible sous la barre de recherche.

## 1.0.0 · Premier style · 8 novembre 2026

- Noir OLED, violet et bleu, titres en Gloock : le style du Nouvel onglet sur plus de 250 sites.
- Passes site par site : Gmail, YouTube, Discord, Moodle, ADE, claude.ai, Gemini, Keep, DuckDuckGo, Wikipédia, GitHub, SoundCloud, anime-sama, chess.com, messageries.
- Volet violet entre deux pages d'un même site, dans un style à part (`volet.user.css`).
