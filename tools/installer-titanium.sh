#!/bin/sh
# Ouvre Stylus magique, Stylus étude et Stylus téléphone dans Titanium (A54) par adb :
# Stylus montre sa page d'installation dans un onglet par style, il reste à toucher « Installer » dans chacun.
# Sans argument : les trois ; sinon les styles nommés (ex. stylus-etude stylus-telephone).
set -e
VERROU="$HOME/.local/state/telephone-pris"
if [ -s "$VERROU" ] && [ "$(cat "$VERROU")" != "${CLAUDE_FRAME_COLOR:-moi}" ]; then
  echo "Téléphone pris par : $(cat "$VERROU")"; exit 1
fi
echo "${CLAUDE_FRAME_COLOR:-moi}" > "$VERROU"
trap 'rm -f "$VERROU"' EXIT
if adb devices | grep -q 'device usb:' || adb devices -l | grep -q ' usb:'; then
  cible=$(adb devices -l | awk '/ usb:/{print $1; exit}')
else
  cible=$(adb-a54 | tail -1 | grep -o '[0-9]\{1,3\}\(\.[0-9]\{1,3\}\)\{3\}:[0-9]\{2,5\}' || true)
fi
[ -n "$cible" ] || { echo "A54 injoignable : câble, ou même Wi-Fi que le PC (pas eduroam)"; exit 1; }
[ $# -gt 0 ] || set -- stylus-magique stylus-etude stylus-telephone
for s in "$@"; do
  adb -s "$cible" shell am start -a android.intent.action.VIEW -p io.github.jqssun.helium \
    -d "https://raw.githubusercontent.com/glime32/stylus-magique/main/$s.user.css" >/dev/null
  echo "$s ouvert dans Titanium"
  sleep 2
done
echo "Un onglet par style : touche « Installer » dans chacun."
