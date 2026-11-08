#!/usr/bin/env bash
# Style « Stylus magique » pour le lecteur PDF.js (copie non empaquetée de l'extension « PDF Viewer »).
# Ajoute magique-pdfjs.css juste après viewer.css, avec une mise à jour automatique (timer systemd).
# Remplace l'ancien thème de stylus-oled (oled-pdfjs.css) s'il est installé.
# Usage : curl -fsSL https://raw.githubusercontent.com/glime32/stylus-magique/main/pdfjs/install.sh | bash
set -euo pipefail

URL="https://raw.githubusercontent.com/glime32/stylus-magique/main/pdfjs/magique-pdfjs.css"

trouver() {
  if [ -n "${PDFJS_DIR:-}" ]; then echo "$PDFJS_DIR"; return; fi
  for d in "$HOME/pdfjs-custom" "$HOME/extensions/pdfjs" "$HOME/extensions/pdfjs-custom"; do
    if [ -f "$d/content/web/viewer.html" ]; then echo "$d"; return; fi
  done
  # sinon : une copie non empaquetée (jamais celle du Web Store, rangée dans .../Extensions/)
  local f
  f=$(find "$HOME" -maxdepth 5 -path "$HOME/.cache" -prune -o -path '*/content/web/viewer.html' -print 2>/dev/null \
      | grep -v '/Extensions/' | head -n1 || true)
  if [ -n "$f" ]; then echo "${f%/content/web/viewer.html}"; fi
}

DIR=$(trouver)
if [ -z "$DIR" ] || [ ! -f "$DIR/content/web/viewer.html" ]; then
  echo "Lecteur PDF.js introuvable."
  echo "Relance avec son dossier : curl -fsSL ... | PDFJS_DIR=/chemin/du/dossier bash"
  exit 1
fi
WEB="$DIR/content/web"
UNIT="$HOME/.config/systemd/user"

# L'ancien thème (stylus-oled) : on coupe sa mise à jour et on retire son fichier
if systemctl --user list-unit-files oled-pdfjs-maj.timer >/dev/null 2>&1; then
  systemctl --user disable --now oled-pdfjs-maj.timer 2>/dev/null || true
fi
rm -f "$UNIT/oled-pdfjs-maj.timer" "$UNIT/oled-pdfjs-maj.service" "$HOME/.local/bin/oled-pdfjs-maj" "$WEB/oled-pdfjs.css"
sed -i '/href="oled-pdfjs.css"/d' "$WEB/viewer.html"

# Script local de mise à jour : il télécharge seulement le CSS, aucun code distant n'est exécuté
mkdir -p "$HOME/.local/bin"
MAJ="$HOME/.local/bin/magique-pdfjs-maj"
cat > "$MAJ" <<EOF
#!/usr/bin/env bash
# Met à jour le style Stylus magique du lecteur PDF.js ($WEB)
set -eu
WEB="$WEB"
curl -fsSL --retry 2 "$URL" -o "\$WEB/magique-pdfjs.css.tmp"
mv -f "\$WEB/magique-pdfjs.css.tmp" "\$WEB/magique-pdfjs.css"
if ! grep -q 'magique-pdfjs.css' "\$WEB/viewer.html"; then
  sed -i '0,/href="viewer.css"[^>]*>/s//&\n    <link rel="stylesheet" href="magique-pdfjs.css" \/>/' "\$WEB/viewer.html"
fi
if ! grep -q 'magique-pdfjs.css' "\$WEB/viewer.html"; then
  sed -i '0,/<\/head>/s//  <link rel="stylesheet" href="magique-pdfjs.css" \/>\n<\/head>/' "\$WEB/viewer.html"
fi
EOF
chmod +x "$MAJ"
"$MAJ"

# Timer systemd utilisateur : au démarrage de la session, puis toutes les heures
mkdir -p "$UNIT"
cat > "$UNIT/magique-pdfjs-maj.service" <<EOF
[Unit]
Description=Mise à jour du style Stylus magique du lecteur PDF.js
Wants=network-online.target
After=network-online.target

[Service]
Type=oneshot
ExecStart=$MAJ
EOF

cat > "$UNIT/magique-pdfjs-maj.timer" <<EOF
[Unit]
Description=Mise à jour auto du style Stylus magique du lecteur PDF.js

[Timer]
OnStartupSec=45s
OnUnitActiveSec=1h
Persistent=true

[Install]
WantedBy=timers.target
EOF

systemctl --user daemon-reload
systemctl --user enable --now magique-pdfjs-maj.timer

echo
echo "OK : style appliqué dans $WEB"
echo "Mise à jour auto : active (toutes les heures)."
echo "Recharge tes onglets PDF. Si rien ne change : helium://extensions, bouton recharger de PDF Viewer."
