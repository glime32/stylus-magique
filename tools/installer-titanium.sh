#!/bin/sh
# Dépose sur l'A54 une sauvegarde Stylus avec Stylus téléphone (allumé), Magique et Étude (éteints).
# Titanium bloque la page d'installation de Stylus ouverte depuis un lien : il faut importer la sauvegarde
# dans le gestionnaire de Stylus. Ensuite, les mises à jour arrivent par Stylus (icône ⟳ du gestionnaire).
set -e
ICI=$(dirname "$0")/..
VERROU="$HOME/.local/state/telephone-pris"
if [ -s "$VERROU" ] && [ "$(cat "$VERROU")" != "${CLAUDE_FRAME_COLOR:-moi}" ]; then
  echo "Téléphone pris par : $(cat "$VERROU")"; exit 1
fi
echo "${CLAUDE_FRAME_COLOR:-moi}" > "$VERROU"
trap 'rm -f "$VERROU"' EXIT
if adb devices -l | grep -q ' usb:'; then
  cible=$(adb devices -l | awk '/ usb:/{print $1; exit}')
else
  cible=$(adb-a54 | tail -1 | grep -o '[0-9]\{1,3\}\(\.[0-9]\{1,3\}\)\{3\}:[0-9]\{2,5\}' || true)
fi
[ -n "$cible" ] || { echo "A54 injoignable : câble, ou même Wi-Fi que le PC (pas eduroam)"; exit 1; }
json=$(mktemp --suffix=.json)
python3 - "$ICI" "$json" <<'PY'
import json, re, sys, time
from pathlib import Path
ici, sortie = Path(sys.argv[1]), sys.argv[2]
styles = []
for nom, allume in (("stylus-telephone", True), ("stylus-magique", False), ("stylus-etude", False)):
    src = (ici / f"{nom}.user.css").read_text()
    m = dict(re.findall(r"^@(\w+)\s+(.+?)\s*$", src[:src.index("==/UserStyle==")], re.M))
    ucd = {k: m[k] for k in ("name", "namespace", "version", "description", "author", "license", "homepageURL", "updateURL") if k in m}
    ucd["preprocessor"] = "default"
    styles.append({"name": m["name"], "enabled": allume, "sourceCode": src, "usercssData": ucd, "updateUrl": m["updateURL"],
                   "url": m["homepageURL"], "installDate": int(time.time() * 1000), "sections": [{"code": ""}]})
Path(sortie).write_text(json.dumps(styles, ensure_ascii=False))
PY
adb -s "$cible" push "$json" /sdcard/Download/stylus-a54.json >/dev/null
rm -f "$json"
echo "Sauvegarde déposée dans Téléchargements : Stylus (icône S) → grille (gestionnaire) → Importer → stylus-a54.json → Fermer."
echo "Ne pas toucher « Supprimer » dans la fenêtre de résultat : il viserait les styles absents de la sauvegarde."
