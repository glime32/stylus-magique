#!/usr/bin/env python3
"""Fabrique stylus-telephone.user.css, à poser à côté de Stylus magique ou Stylus étude sur un téléphone.

    python3 tools/telephone.py

Au doigt, :hover reste collé après un appui : les règles de survol de Magique qui soulèvent,
penchent ou font tourner sont reprises sous @media (hover: none) avec les valeurs de repos.
L'enfoncement pendant l'appui (:active) reste. En plus : Gloock et Archivo, flash violet transparent.
"""

import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from etude import MAGIQUE, MOUVEMENT, decouper, lire, tout  # noqa: E402

CIBLE = MAGIQUE.parent / "stylus-telephone.user.css"
VERSION = "1.0.0"
SOULEVEE = re.compile(r"^-?\d+px 7px 0 (.+)$")
REPOS = {"translate": "none", "rotate": "none", "scale": "none", "transform": "none"}

ENTETE = f"""/* ==UserStyle==
@name           Stylus téléphone
@namespace      glime32.stylus-telephone
@version        {VERSION}
@description    À poser avec Stylus magique ou Stylus étude sur un téléphone : Gloock et Archivo, rien ne penche au doigt, flash violet transparent
@author         glime32
@license        MIT
@homepageURL    https://github.com/glime32/stylus-magique
@updateURL      https://raw.githubusercontent.com/glime32/stylus-magique/main/stylus-telephone.user.css
@preprocessor   default
==/UserStyle== */

/* Fabriqué par tools/telephone.py à partir de stylus-magique.user.css : ne pas modifier à la main. */
"""

PARTOUT = """@-moz-document url-prefix("http"), url-prefix("file:") {
@font-face {
  font-family: "Gloock"; font-style: normal; font-weight: 400; font-display: swap;
  src: local("Gloock"), local("Gloock-Regular"), url(https://fonts.gstatic.com/s/gloock/v8/Iurb6YFw84WUY4NJiBakJLRBjA.woff2) format("woff2");
}
@font-face {
  font-family: "Archivo"; font-style: normal; font-weight: 100 900; font-stretch: 62% 125%; font-display: swap;
  src: local("Archivo"), url(https://fonts.gstatic.com/s/archivo/v25/k3kQo8UDI-1M0wlSfdnoLmvDIaI.woff2) format("woff2");
}
html, html * { -webkit-tap-highlight-color: color-mix(in srgb, var(--sm-violet-vif, #d980ff) 30%, transparent) !important; }
}
"""


def renforce(selecteur):
    morceaux = []
    for s in decouper(selecteur):
        s = s.strip()
        i = s.find("::")
        morceaux.append(s + ":not(:active, #sm-tel)" if i < 0 else s[:i] + ":not(:active, #sm-tel)" + s[i:])
    return ", ".join(morceaux)


def nettoie(valeur):
    return re.sub(r"\s*!important\s*$", "", valeur).strip()


def fabriquer():
    t = MAGIQUE.read_text()
    debut = t.index("==/UserStyle== */") + len("==/UserStyle== */")
    noeuds = lire(t, debut, len(t))
    tous = [n for n in tout(noeuds) if n.sorte == "bloc"]
    voisins = {}
    for n in tous:
        voisins.setdefault((id(n.parent), n.tete.strip()), n)

    groupes = {}
    for n in tous:
        if n.tete.startswith("@") or ":hover" not in n.tete:
            continue
        mouvement = [d for d in n.decls() if d.nom in MOUVEMENT and nettoie(d.valeur) not in ("none", "0", "0deg", "1")]
        if not mouvement:
            continue
        repos = voisins.get((id(n.parent), n.tete.replace(":hover", "").strip()))
        base = {d.nom: nettoie(d.valeur) for d in repos.decls()} if repos else {}
        decls = [f"{d.nom}: {base.get(d.nom, REPOS[d.nom])} !important;" for d in mouvement]
        ombre = next((nettoie(d.valeur) for d in n.decls() if d.nom == "box-shadow"), None)
        if ombre and "box-shadow" in base:
            decls.append(f"box-shadow: {base['box-shadow']} !important;")
        elif ombre and SOULEVEE.match(ombre):
            decls.append(f"box-shadow: {SOULEVEE.sub(r'0 4px 0 \1', ombre)} !important;")
        regle = f"{renforce(n.tete)} {{ {' '.join(decls)} }}"
        p, autour, doc = n.parent, [], 'url-prefix("http"), url-prefix("file:")'
        while p is not None:
            if p.tete.startswith("@-moz-document"):
                doc = p.tete[len("@-moz-document"):].strip()
            elif p.tete.startswith("@"):
                autour.append(p.tete.strip())
            p = p.parent
        for a in autour:
            regle = f"{a} {{ {regle} }}"
        groupes.setdefault(doc, []).append(regle)

    sortie = [ENTETE, PARTOUT]
    for doc, regles in groupes.items():
        sortie.append(f"@-moz-document {doc} {{\n@media (hover: none) {{\n" + "\n".join(regles) + "\n}\n}\n")
    CIBLE.write_text("\n".join(sortie))
    print(f"{sum(map(len, groupes.values()))} règles de survol, {len(groupes)} blocs, {CIBLE.stat().st_size // 1024} Ko")


if __name__ == "__main__":
    fabriquer()
