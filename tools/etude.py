#!/usr/bin/env python3
"""Fabrique stylus-etude.user.css à partir de stylus-magique.user.css et d'etude/etude.css.

    python3 tools/etude.py           écrit le fichier puis affiche le relevé
    python3 tools/etude.py --releve  relevé seul, sur le fichier déjà écrit
    python3 tools/etude.py --retires liste aussi les règles retirées hors des blocs d'étoiles
"""

import re
import sys
from bisect import bisect
from pathlib import Path

ICI = Path(__file__).resolve().parent.parent
MAGIQUE = ICI / "stylus-magique.user.css"
SOURCE = ICI / "etude" / "etude.css"
CIBLE = ICI / "stylus-etude.user.css"

SANS_JETON = {"--sm-serif", "--sm-etroite", "--sm-snap", "--sm-etoile", "--sm-etoile8", "--sm-tuile"}
ETAT = re.compile(r":(?:hover|active|focus(?:-visible|-within)?)\b")
PSEUDO = re.compile(r"::?(?:before|after)\b")
MOUVEMENT = {"rotate", "translate", "scale", "transform"}
ETOILE = re.compile(r"var\(--sm-(?:etoile8?|tuile)\)|--sm-e8|M12 0c\.75 6\.6")
POLICE = re.compile(r"var\(--sm-(?:serif|etroite)\)")
AVEC_POLICE = {"font-stretch", "font-variation-settings", "font-weight", "font-size",
               "letter-spacing", "text-transform", "line-height"}
GARDE_ROUGE = re.compile(r"error|invalid|danger|destructive|problem|alert|progress|swatch|brand-red", re.I)
BLANC = re.compile(r"#fff(?:fff)?\b|\bwhite\b|rgb\(\s*255\s*,\s*255\s*,\s*255\s*\)", re.I)
VIOLET = re.compile(r"var\(--sm-violet\)|#610089\b", re.I)

SECTIONS_ETOILES = {"etoiles-magique", "etoiles-exceptions"}
GARDE_ETOILES = re.compile(
    r'ytd-multi-page-menu-renderer #header|^div\.bxwGjd$|^#loader$|\[class\*="linkTop_"\]'
    r'|^html, body$|^\[data-testid="wa-web-loading-screen"\](?! > div:first-child)')
# ce qui n'existe que pour faire de la place au carré étoilé, à l'ombre ou à la carte qui penche
COMPAGNONS = re.compile(
    r'^\.scrollBarStyled:has\(> \.as-carte\)$|^ytd-watch-metadata #bottom-row$'
    r'|^ytd-guide-entry-renderer\[active\] yt-icon\.guide-icon$|^\.aim \.TO\.nZ \.qj$'
    r'|^\[role="tab"\]\.PvRhvb-ibnC6b\.gk6SMd \.PvRhvb-ibnC6b-V67aGc$'
    r'|^a\[data-component="NavList\.Item"\]\[aria-current\]:not\(\[aria-current="false"\]\) \[data-component="ActionList\.Item\.Label"\]$'
    r'|^:is\(h1, h2\):has\(> span:first-child\)')


class Note:
    sorte = "note"

    def __init__(self, debut, fin):
        self.debut, self.fin = debut, fin


class Decl:
    sorte = "decl"

    def __init__(self, t, debut, bout):
        self.debut = debut
        self.fin = debut + len(t[debut:bout].rstrip())
        self.pv = bout < len(t) and t[bout] == ";"
        self.texte = t[debut:self.fin]
        nom, _, valeur = self.texte.partition(":")
        self.nom = nom.strip()
        self.important = bool(re.search(r"!\s*important\s*$", valeur, re.I))
        self.valeur = re.sub(r"\s*!\s*important\s*$", "", valeur, flags=re.I).strip()

    def avec(self, valeur):
        tete = re.match(r"\s*[^:]+:\s*", self.texte).group(0)
        fin = re.search(r"\s*!\s*important\s*$", self.texte, re.I)
        return tete + valeur + (fin.group(0) if fin else "")


class Bloc:
    sorte = "bloc"

    def __init__(self, t, debut, ouvre, fin):
        self.debut, self.ouvre, self.fin = debut, ouvre, fin
        self.tete = " ".join(t[debut:ouvre].split())
        self.enfants = []

    def decls(self):
        return [n for n in self.enfants if n.sorte == "decl"]


def chaine(t, i):
    q, i = t[i], i + 1
    while t[i] != q:
        i += 2 if t[i] == "\\" else 1
    return i + 1


def saut(t, i):
    if t.startswith("/*", i):
        return t.index("*/", i + 2) + 2
    if t[i] in "\"'":
        return chaine(t, i)
    return None


def fermeture(t, i):
    prof = 0
    while True:
        j = saut(t, i)
        if j is not None:
            i = j
            continue
        if t[i] == "{":
            prof += 1
        elif t[i] == "}":
            prof -= 1
            if prof == 0:
                return i + 1
        i += 1


def lire(t, a, b, parent=None):
    enfants, i = [], a
    while True:
        while i < b and t[i].isspace():
            i += 1
        if i >= b:
            return enfants
        if t.startswith("/*", i):
            n = Note(i, t.index("*/", i + 2) + 2)
            suite = n.fin
        else:
            j, prof = i, 0
            while j < b:
                k = saut(t, j)
                if k is not None:
                    j = k
                    continue
                if t[j] == "(":
                    prof += 1
                elif t[j] == ")":
                    prof -= 1
                elif prof == 0 and t[j] in "{;":
                    break
                j += 1
            if j < b and t[j] == "{":
                n = Bloc(t, i, j, fermeture(t, j))
                n.enfants = lire(t, j + 1, n.fin - 1, n)
                suite = n.fin
            else:
                n = Decl(t, i, j)
                suite = j + 1
        n.parent = parent
        enfants.append(n)
        i = suite


def tout(noeuds):
    for n in noeuds:
        yield n
        if n.sorte == "bloc":
            yield from tout(n.enfants)


def decouper(valeur, sep=","):
    morceaux, prof, debut = [], 0, 0
    for i, c in enumerate(valeur):
        if c == "(":
            prof += 1
        elif c == ")":
            prof -= 1
        elif c == sep and prof == 0:
            morceaux.append(valeur[debut:i])
            debut = i + 1
    morceaux.append(valeur[debut:])
    return [m.strip() for m in morceaux]


def sans_fonctions(texte):
    while True:
        nouveau = re.sub(r"[\w-]*\([^()]*\)", " ", texte)
        if nouveau == texte:
            return texte
        texte = nouveau


def en_relief(ombre):
    mots = sans_fonctions(ombre).split()
    if "inset" in mots:
        return False
    nombres = [m for m in mots if re.fullmatch(r"-?(?:\d+\.?\d*|\.\d+)(?:px|em|rem)?", m)]
    if len(nombres) < 2:
        return False
    x, y = (float(re.sub(r"[a-z]+", "", n)) for n in nombres[:2])
    flou = float(re.sub(r"[a-z]+", "", nombres[2])) if len(nombres) > 2 else 0
    return flou == 0 and (x, y) != (0, 0)


def sans_relief(valeur):
    ombres = decouper(valeur)
    gardees = [o for o in ombres if not en_relief(o)]
    if len(gardees) == len(ombres):
        return valeur
    return ", ".join(gardees) or "none"


def etendue(t, n):
    a = n.debut
    b = n.fin + (1 if n.sorte == "decl" and n.pv else 0)
    ligne = t.rfind("\n", 0, a) + 1
    reste = re.compile(r"[ \t]*(?:/\*[^\n]*?\*/)?[ \t]*(?:\n|$)").match(t, b)
    if not t[ligne:a].strip() and reste:
        return ligne, reste.end()
    while b < len(t) and t[b] == " ":
        b += 1
    return a, b


def lire_source():
    s = SOURCE.read_text()
    entete = s[:s.index("==/UserStyle== */") + len("==/UserStyle== */")]
    noeuds = lire(s, len(entete), len(s))
    racine = next(n for n in noeuds if n.sorte == "bloc" and n.tete == ":root")
    jetons = {d.nom: d.valeur for d in racine.decls()}
    return entete, jetons, s[racine.fin:].strip("\n")


def fabriquer():
    t = MAGIQUE.read_text()
    entete, jetons, ajouts = lire_source()
    debut = t.index("==/UserStyle== */") + len("==/UserStyle== */")
    noeuds = lire(t, debut, len(t))
    suppr, rempl, tetes, inconnus = set(), {}, {}, []

    section = None
    for n in noeuds:
        if n.sorte == "note":
            m = re.match(r"/\*@@ (.+?) @@\*/", t[n.debut:n.fin])
            if m:
                section = m.group(1)
                continue
        n.section = section
        for e in tout([n]):
            e.section = section

    for n in tout(noeuds):
        if n.sorte == "note":
            if not t.startswith("/*@@", n.debut):
                suppr.add(n)
            continue
        if n.sorte != "bloc":
            continue
        if n.tete.startswith("@keyframes sm-"):
            suppr.add(n)
            continue
        if n.tete.startswith("@"):
            continue
        decls = n.decls()
        if any(d.nom == "--sm-texte" for d in decls):
            racine_jetons(n, jetons, suppr, rempl, inconnus)
            continue
        if n.section in SECTIONS_ETOILES and not GARDE_ETOILES.search(n.tete) or COMPAGNONS.search(n.tete):
            suppr.add(n)
            continue
        if n.parent is not None and n.parent.sorte == "bloc" and n.parent.tete.startswith("@keyframes"):
            continue
        regle(n, suppr, rempl)
        if n.tete.startswith("html:root :is(") and any(d.valeur == "none" and d.nom == "filter" for d in decls):
            tete = t[n.debut:n.ouvre]
            tetes[n] = re.sub(r"(?<=[(,])(?:img|picture),", "", tete, count=2)

    vider(noeuds, suppr)
    for i, n in enumerate(noeuds):
        if n.sorte == "note" and n not in suppr:
            suivants = []
            for m in noeuds[i + 1:]:
                if m.sorte == "note" and t.startswith("/*@@", m.debut):
                    break
                suivants.append(m)
            if all(m in suppr for m in suivants):
                suppr.add(n)

    if inconnus:
        sys.exit("jetons de Magique sans valeur dans etude/etude.css : " + ", ".join(inconnus))

    modifs = []
    for n in tout(noeuds):
        if n in suppr:
            modifs.append((*etendue(t, n), ""))
            continue
        if n in rempl:
            modifs.append((n.debut, n.fin, rempl[n]))
        if n in tetes:
            modifs.append((n.debut, n.ouvre, tetes[n]))
    modifs.sort(key=lambda m: (m[0], -m[1]))
    morceaux, pos = [entete], debut
    for a, b, r in modifs:
        if a < pos:
            continue
        morceaux += [t[pos:a], r]
        pos = b
    morceaux.append(t[pos:])
    sortie = "".join(morceaux)
    sortie = re.sub(r"\n{3,}", "\n\n", sortie).rstrip() + "\n\n" + ajouts + "\n"
    CIBLE.write_text(sortie)
    if "--retires" in sys.argv:
        for n in tout(noeuds):
            if n in suppr and n.sorte == "bloc" and not n.tete.startswith("@") and n.section not in SECTIONS_ETOILES:
                print(f"retirée [{n.section}] {n.tete[:110]}")
    return sortie


def racine_jetons(n, jetons, suppr, rempl, inconnus):
    vus, dernier = set(), None
    for d in n.decls():
        vus.add(d.nom)
        if d.nom in SANS_JETON:
            suppr.add(d)
        elif d.nom in jetons:
            rempl[d] = d.avec(jetons[d.nom])
            dernier = d
        else:
            inconnus.append(d.nom)
    nouveaux = [k for k in jetons if k not in vus]
    if nouveaux and dernier is not None:
        retrait = "\n  "
        rempl[dernier] += ";" + retrait + (";" + retrait).join(f"{k}: {jetons[k]}" for k in nouveaux)


def regle(n, suppr, rempl):
    sel = n.tete
    decls = n.decls()
    if any(ETOILE.search(d.valeur) or d.nom == "--sm-et" for d in decls):
        suppr.add(n)
        return
    etat = ETAT.search(sel)
    police = [d for d in decls if d.nom.lower() in ("font-family", "font") and POLICE.search(d.valeur)]
    etroite = any("etroite" in d.valeur for d in police)
    etiquette = any("--sm-etiquette-fond" in d.valeur for d in decls)
    bouge = []
    for d in decls:
        nom, v = d.nom.lower(), d.valeur
        if nom in MOUVEMENT and (etat or nom == "rotate" and v not in ("none", "0", "0deg")):
            bouge.append(d)
        elif nom.startswith("transition") and "--sm-snap" in v:
            suppr.add(d)
        elif nom.startswith("animation") and (re.search(r"\bsm-[a-z]", v) or nom == "animation-play-state"):
            suppr.add(d)
        elif police and (d in police or nom in AVEC_POLICE):
            suppr.add(d)
        elif etiquette and nom == "border-radius":
            rempl[d] = d.avec("999px")
        elif etiquette and nom == "padding" and v in ("1px 8px 1px 6px", "0 7px 0 5px"):
            rempl[d] = d.avec("1px 7px")
        else:
            nv = couleurs(sel, nom, v, decls, etroite)
            if nom == "box-shadow":
                sr = sans_relief(nv)
                if sr != nv and etat:
                    bouge.append(d)
                    continue
                nv = sr
            if nv != v:
                rempl[d] = d.avec(nv)
    suppr.update(bouge)
    if bouge and ":hover" in sel and not PSEUDO.search(sel) and not any(d.nom.startswith("border") for d in decls):
        premier = bouge[0]
        suppr.discard(premier)
        rempl[premier] = "border-color: var(--sm-accent)" + (" !important" if any(d.important for d in decls) else "")


def couleurs(sel, nom, v, decls, etroite):
    if "var(--sm-rouge)" in v or re.search(r"#ff3b3b\b", v, re.I):
        if nom != "caret-color" and not GARDE_ROUGE.search(sel + " " + nom):
            v = re.sub(r"var\(--sm-rouge\)|#ff3b3b\b", "var(--sm-accent)", v, flags=re.I)
    if etroite and nom == "color":
        v = re.sub(r"var\(--sm-(?:violet-vif|bleu-vif|lien)\)", "var(--sm-pale)", v)
    if ("border" in nom or nom == "box-shadow" or nom.startswith("outline")) and VIOLET.search(v):
        v = VIOLET.sub("var(--sm-bouton-bord)", v)
    elif VIOLET.search(v) and not nom.startswith("--"):
        v = re.sub(r"#610089\b", "var(--sm-violet)", v, flags=re.I)
    if nom == "filter" and re.search(r"invert\((?:1|100%)\)", v) and "brightness(.785)" not in v \
            and not re.search(r"img|video|picture|canvas|iframe|background-image", sel):
        v += " brightness(.785)"
    if nom in ("color", "-webkit-text-fill-color", "fill", "caret-color") or nom.endswith(("-color-text", "-fg", "fgColor-rest")):
        fond_violet = any(d.nom.lower().startswith("background") and VIOLET.search(d.valeur) for d in decls)
        if BLANC.search(v) and not fond_violet:
            v = BLANC.sub("var(--sm-texte)", v)
    return v


def vider(noeuds, suppr):
    for n in noeuds:
        if n.sorte == "bloc":
            vider(n.enfants, suppr)
            if all(e in suppr for e in n.enfants):
                suppr.add(n)


def releve(texte):
    lignes = [0] + [m.end() for m in re.finditer("\n", texte)]
    noeuds = lire(texte, texte.index("==/UserStyle== */") + 17, len(texte))
    definis = set(re.findall(r"(--sm-[\w-]+)\s*:", texte))
    compte = {}

    def note(quoi, d):
        compte.setdefault(quoi, []).append(bisect(lignes, d.debut))

    for d in tout(noeuds):
        if d.sorte != "decl":
            continue
        nom, v = d.nom.lower(), d.valeur
        sel = d.parent.tete if d.parent is not None else ""
        if nom in MOUVEMENT and v not in ("none", "0", "0deg"):
            note(f"{nom} (gardé : placement)", d)
        if nom.startswith("animation") and v != "none":
            note("animation", d)
        if "clip-path" == nom and v != "none":
            note("clip-path", d)
        if nom == "box-shadow" and any(en_relief(o) for o in decouper(v)):
            note("ombre en relief", d)
        if "var(--sm-rouge)" in v and nom != "caret-color":
            note("rouge gardé (erreur, danger, YouTube)", d)
        if BLANC.search(v) and nom == "color":
            note("texte blanc (sur violet)", d)
        if POLICE.search(v) or re.search(r"Gloock|Archivo", v):
            note("Gloock ou Archivo", d)
        for j in re.findall(r"var\((--sm-[\w-]+)", v):
            if j not in definis:
                note(f"jeton absent {j}", d)
        if d.parent is None or d.parent.tete.startswith("@-moz"):
            note("déclaration hors règle", d)
    for quoi, ou in sorted(compte.items()):
        print(f"{len(ou):4}  {quoi} : lignes {', '.join(map(str, ou[:12]))}{' …' if len(ou) > 12 else ''}")
    print(f"{len(texte) // 1024} Ko, {texte.count('@-moz-document')} blocs @-moz-document")


if __name__ == "__main__":
    texte = CIBLE.read_text() if "--releve" in sys.argv else fabriquer()
    releve(texte)
