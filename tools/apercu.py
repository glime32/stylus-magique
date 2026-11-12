#!/usr/bin/env python3
"""Capture des pages avec Stylus magique et Stylus étude côte à côte, sans l'extension.

    ~/.venvs/pw/bin/python tools/apercu.py DOSSIER URL [URL…] [--bas N] [--largeur L]

Pour chaque adresse : DOSSIER/<nom>.jpg, Magique à gauche, Étude à droite.
"""

import argparse
import base64
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from etude import CIBLE, MAGIQUE, lire  # noqa: E402

HELIUM = "/opt/helium-browser-bin/helium"
FONCTION = re.compile(r'(domain|url-prefix|url|regexp)\(\s*"((?:[^"\\]|\\.)*)"\s*\)')


def applique(tete, url):
    hote = urlsplit(url).hostname or ""
    for f, arg in FONCTION.findall(tete):
        arg = re.sub(r"\\(.)", r"\1", arg)
        if (f == "domain" and (hote == arg or hote.endswith("." + arg))
                or f == "url-prefix" and url.startswith(arg)
                or f == "url" and url == arg
                or f == "regexp" and re.fullmatch(arg, url)):
            return True
    return False


def css_pour(style, url):
    t = Path(style).read_text()
    debut = t.index("==/UserStyle== */") + 17
    morceaux = []
    for n in lire(t, debut, len(t)):
        if n.sorte != "bloc":
            continue
        if not n.tete.startswith("@-moz-document"):
            morceaux.append(t[n.debut:n.fin])
        elif applique(n.tete, url):
            morceaux.append(t[n.ouvre + 1:n.fin - 1])
    return "\n".join(morceaux)


MESURE = """() => {
  const p = [...document.querySelectorAll("main p, article p, [role=main] p, p")].filter(e => e.offsetWidth)
    .sort((a, b) => b.textContent.length - a.textContent.length)[0];
  if (!p) return "pas de paragraphe";
  const s = document.createElement("span");
  s.textContent = "Les fonctions continues sur un segment sont intégrables au sens de Riemann. ";
  p.appendChild(s);
  const car = s.getBoundingClientRect().width / s.textContent.length;
  s.remove();
  const cs = getComputedStyle(p);
  const larg = p.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
  return `${Math.round(larg / car)} caractères par ligne, ${cs.fontSize}, interligne ${(parseFloat(cs.lineHeight) / parseFloat(cs.fontSize) || 0).toFixed(2)}`;
}"""


def nom(url):
    p = urlsplit(url)
    return re.sub(r"[^\w.-]+", "-", (p.hostname or "") + p.path).strip("-")[:60]


def main():
    a = argparse.ArgumentParser()
    a.add_argument("dossier")
    a.add_argument("urls", nargs="+")
    a.add_argument("--bas", type=int, default=0, help="défilement vers le bas, en pixels")
    a.add_argument("--largeur", type=int, default=1440)
    a.add_argument("--mesure", action="store_true", help="caractères par ligne du plus long paragraphe, avec Étude")
    args = a.parse_args()
    from playwright.sync_api import sync_playwright

    sortie = Path(args.dossier)
    sortie.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        navigateur = p.chromium.launch(executable_path=HELIUM, headless=True)
        contexte = navigateur.new_context(viewport={"width": args.largeur, "height": 900}, color_scheme="dark", locale="fr-FR")
        contexte.add_cookies([{"name": "SOCS", "value": "CAI", "domain": ".youtube.com", "path": "/"}]
                             + [{"name": f"{w}wikimwclientpreferences", "value": "skin-theme-clientpref-os",
                                 "domain": f"{w}.wikipedia.org", "path": "/"} for w in ("fr", "en")])
        page = contexte.new_page()
        for url in args.urls:
            images = []
            for style in (MAGIQUE, CIBLE):
                page.goto(url, wait_until="domcontentloaded", timeout=20000)
                page.add_style_tag(content=css_pour(style, page.url))
                page.wait_for_timeout(2500)
                if args.bas:
                    page.mouse.wheel(0, args.bas)
                    page.wait_for_timeout(700)
                if args.mesure and style == CIBLE:
                    print(url, page.evaluate(MESURE))
                images.append(base64.b64encode(page.screenshot(type="jpeg", quality=80)).decode())
            planche = "".join(f'<img src="data:image/jpeg;base64,{i}">' for i in images)
            page.goto("about:blank")
            page.set_content(f'<body style="margin:0;display:flex;gap:6px;background:#444">{planche}'
                             '<style>img{width:calc(50% - 3px)}</style></body>')
            page.set_viewport_size({"width": args.largeur, "height": 450})
            fichier = sortie / f"{nom(url)}.jpg"
            page.screenshot(path=str(fichier), type="jpeg", quality=75, full_page=True)
            page.set_viewport_size({"width": args.largeur, "height": 900})
            print(fichier)
        navigateur.close()


if __name__ == "__main__":
    main()
