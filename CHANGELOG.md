# Notes de version

Stylus n'installe une mise à jour que si le numéro `@version` change. Il monte à chaque modification :
le dernier chiffre pour une correction, celui du milieu pour une nouveauté.

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
