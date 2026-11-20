#!/bin/sh
# Ouvre Stylus magique, Stylus étude et Stylus téléphone dans Titanium (A54) par adb :
# Stylus montre sa page d'installation, il reste à toucher « Installer » sur chacune.
set -e
VERROU="$HOME/.local/state/telephone-pris"
if [ -s "$VERROU" ] && [ "$(cat "$VERROU")" != "${CLAUDE_FRAME_COLOR:-moi}" ]; then
  echo "Téléphone pris par : $(cat "$VERROU")"; exit 1
fi
echo "${CLAUDE_FRAME_COLOR:-moi}" > "$VERROU"
trap 'rm -f "$VERROU"' EXIT
cible=$(adb-a54 | tail -1 | grep -o '[0-9.]*:[0-9]*' || true)
if [ -z "$cible" ]; then
  adb devices | grep -q 'device$' || { echo "A54 injoignable (même Wi-Fi que le PC, ou câble)"; exit 1; }
  cible=$(adb devices | awk '/device$/{print $1; exit}')
fi
for s in stylus-magique stylus-etude stylus-telephone; do
  adb -s "$cible" shell am start -a android.intent.action.VIEW -p io.github.jqssun.helium \
    -d "https://raw.githubusercontent.com/glime32/stylus-magique/main/$s.user.css" >/dev/null
  printf '%s ouvert dans Titanium : touche « Installer », puis Entrée ici. ' "$s"
  read _
done
