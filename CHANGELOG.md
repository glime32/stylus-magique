# Notes de version

Stylus n'installe une mise à jour que si le numéro `@version` change. Il monte à chaque modification :
le dernier chiffre pour une correction, celui du milieu pour une nouveauté.

## Stylus téléphone 2.0.2, 1.2.9 et Stylus étude 1.1.7 · Cinq sites de plus · 20 novembre 2026

Nouveau :
- duck.ai, Supercell (compte et boutique), Uniqlo, Samsung et Pages Jaunes passent en noir avec les couleurs du thème.
- Pages Jaunes : le haut de page jaune (posé sur un ::before ou en !important) passe en noir, son texte redevient lisible.
- Uniqlo : le bandeau d'offre et les onglets Femme/Homme, posés sur la photo claire, ont un fond noir.

## Stylus téléphone 2.0.1, 1.2.8 et Stylus étude 1.1.6 · Le style de l'A54 · 20 novembre 2026

Changé :
- Stylus téléphone devient Stylus étude pour le Galaxy A54, à installer seul (sans Magique ni Étude). Il n'habille plus les pages de Stylus, qui restaient illisibles sur le téléphone, et garde le flash violet au toucher.

Corrigé :
- YouTube version téléphone : le cadre « Votre historique YouTube est désactivé » était gris ; il passe en noir à bord violet.

## Stylus téléphone 1.0.0 · Au doigt · 20 novembre 2026

Nouveau style, à poser à côté de Stylus magique ou de Stylus étude sur un téléphone :
- les polices Gloock (gros titres) et Archivo (petits titres) se téléchargent une fois, le téléphone ne les a pas ;
- au doigt, les boutons ne restent plus soulevés et penchés après un appui : seul l'enfoncement pendant l'appui reste ;
- le flash quand on touche un lien ou un bouton devient violet transparent.

Fabriqué par `tools/telephone.py` à partir de Magique.

## 1.2.7 et Stylus étude 1.1.5 · YouTube sur téléphone · 20 novembre 2026

Corrigé :
- YouTube version téléphone (m.youtube.com) : les barres du haut et du bas, le panneau d'infos et le menu étaient gris très foncé. Ils passent en noir pur, comme sur ordinateur.

## 1.2.6 et Stylus étude 1.1.4 · Adresse Amazon · 20 novembre 2026

Corrigé :
- Amazon : les questions repliables (instructions de livraison, « Avons-nous besoin d'un code d'accès… ») étaient des cadres blancs au texte pâle, presque illisible. Elles passent en noir avec un bord violet (lavande dans Étude) et un texte clair.
- Amazon, passage en caisse et carnet d'adresses : les puces « Maison / Appartement / Entreprise / Autre » et les boutons comme « Ajouter instr. de livraison » prennent l'aspect des boutons du thème, et la puce choisie ressort en violet.

## 1.2.5 et Stylus étude 1.1.3 · J'aime SoundCloud · 15 novembre 2026

Corrigé :
- SoundCloud : un morceau aimé ou republié, un compte suivi ne se voyaient plus (le thème effaçait l'orange de SoundCloud). Le cœur, le nombre et le bord passent en violet clair dans Magique, en lavande dans Étude.

## Keep rapide 1.2.0 · Plus de notes vides · 15 novembre 2026

Corrigé :
- La fenêtre s'ouvrait sur `keep.new`, qui enregistre une note dès qu'elle s'ouvre, même vide : chaque ouverture laissait une note vide. Le style remplit maintenant la fenêtre avec la zone « Créer une note… » du haut de Keep, qui ne crée une note que si on écrit dedans. Fenêtre à ouvrir avec `--app=https://keep.google.com/`.

## Keep rapide 1.1.0 · Note vide · 15 novembre 2026

- Plus de phrase grise dans la note (« Créer une note… ») : elle reste vide jusqu'à ce qu'on écrive.

## Keep rapide 1.0.0 · Note rapide · 15 novembre 2026

Nouveau style `keep-rapide.user.css`, seulement pour Google Keep ouvert en fenêtre appli (`--app=https://keep.new`) :
- plus que la note ouverte, qui remplit la fenêtre ;
- cachés : barre du haut, menu, « Créer une note », les autres notes, le titre de la note, l'épingle, « Modification : … », et en bas mise en forme, collaborateur, archiver, annuler et rétablir ;
- les onglets ne changent pas (`@media (display-mode: standalone)`).

## Claude rapide 1.3.0 · Sans bandeau · 14 novembre 2026

- Plus de bandeau au-dessus de la zone de texte, comme « Vous avez utilisé 83 % de votre limite hebdomadaire · Obtenir plus d'utilisation ».

## Claude rapide 1.2.2 · Chargement propre · 13 novembre 2026

- Pendant les 3-4 s où claude.ai se charge, on ne voit plus la fausse barre latérale avec « Claude », la salutation ni la phrase grise : seulement la zone de texte, au milieu, avec la même bordure que la vraie. On peut déjà y écrire, claude.ai garde le texte.

## Claude rapide 1.1.0 · Zone de texte vide · 13 novembre 2026

- Plus de phrase grise dans la zone de texte (« Comment puis-je vous aider aujourd'hui ? », « Répondre… ») : la zone reste vide jusqu'à ce qu'on écrive.

## Claude rapide 1.0.0 · Question rapide · 13 novembre 2026

Nouveau style `claude-rapide.user.css`, seulement pour claude.ai ouvert en fenêtre appli (`--app=https://claude.ai/new`) :
- plus que la zone de texte, centrée sur la page d'accueil, et le choix du modèle à droite ;
- cachés : barre latérale, barre du haut (incognito, titre, Partager), salutation, artéfacts récents, « Projet », « Auto », trombone, micro, mode vocal, « Claude est une IA et peut commettre des erreurs » ;
- pas d'étoile devant les titres, rien ne penche au survol, même si Stylus magique est allumé sur claude.ai ;
- les onglets ne changent pas (`@media (display-mode: standalone)`).

## 1.2.4 et Stylus étude 1.1.2 · Curseur en bloc · 14 novembre 2026

Changé :
- Le curseur de texte des champs est un bloc rouge fixe (au lieu d'une barre fine), sur tous les sites.

## 1.2.3 et Stylus étude 1.1.1 · Curseur · 13 novembre 2026

Corrigé :
- Le curseur de texte était violet et fin sur les sites qui imposent leur propre couleur (champs de messagerie, éditeurs). Il est rouge et fixe dans tous les champs, sur tous les sites.

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
