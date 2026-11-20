#!/usr/bin/env python3
"""Fabrique stylus-telephone.user.css : Stylus étude pour le Galaxy A54 (Titanium), à installer seul.

    python3 tools/telephone.py        (après tools/etude.py)

Stylus étude sans le bloc qui habille les pages de Stylus (fait pour l'interface du PC,
illisible sur celle du téléphone), plus un flash violet transparent au toucher.
"""

import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from etude import CIBLE as ETUDE, lire  # noqa: E402

CIBLE = ETUDE.parent / "stylus-telephone.user.css"
VERSION = "2.0.4"

ENTETE = f"""/* ==UserStyle==
@name           Stylus téléphone
@namespace      glime32.stylus-telephone
@version        {VERSION}
@description    Stylus étude pour le Galaxy A54 (Titanium) : à installer seul, sans Magique ni Étude
@author         glime32
@license        MIT
@homepageURL    https://github.com/glime32/stylus-magique
@updateURL      https://raw.githubusercontent.com/glime32/stylus-magique/main/stylus-telephone.user.css
@preprocessor   default
==/UserStyle== */

/* Fabriqué par tools/telephone.py à partir de stylus-etude.user.css : ne pas modifier à la main. */
"""

TOUCHER = """
/*@@ telephone @@*/
@-moz-document url-prefix("http") {
html, html * { -webkit-tap-highlight-color: color-mix(in srgb, var(--sm-violet-vif, #d980ff) 30%, transparent) !important; }
}
"""


def fabriquer():
    t = ETUDE.read_text()
    debut = t.index("==/UserStyle== */") + len("==/UserStyle== */")
    retirer = [(n.debut, n.fin) for n in lire(t, debut, len(t))
               if n.sorte == "bloc" and n.tete.startswith('@-moz-document url-prefix("chrome-extension://')]
    corps, pos = [], debut
    for a, b in retirer:
        corps.append(t[pos:a])
        pos = b
    corps.append(t[pos:])
    texte = re.sub(r"\n{3,}", "\n\n", "".join(corps)).strip("\n")
    CIBLE.write_text(ENTETE + "\n" + texte + "\n" + TOUCHER)
    print(f"{len(retirer)} bloc(s) des pages de Stylus retiré(s), {CIBLE.stat().st_size // 1024} Ko")


if __name__ == "__main__":
    fabriquer()
