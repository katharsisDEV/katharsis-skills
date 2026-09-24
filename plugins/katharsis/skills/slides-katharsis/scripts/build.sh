#!/usr/bin/env bash
# Rend un deck HTML en PDF paysage 959 × 540 pt via Chrome headless.
#   build.sh <deck.html> [sortie.pdf]        (sortie par défaut : même nom en .pdf)
# Aucun serveur, aucun réseau : theme.css et assets/ sont lus depuis le disque.
set -euo pipefail
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
[ $# -ge 1 ] || { echo "usage : $0 <deck.html> [sortie.pdf]" >&2; exit 2; }
SRC="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
OUT="${2:-${SRC%.html}.pdf}"
case "$OUT" in /*) ;; *) OUT="$PWD/$OUT" ;; esac
"$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
  --allow-file-access-from-files --virtual-time-budget=8000 \
  --print-to-pdf="$OUT" "file://$SRC" 2>/dev/null
echo "→ $OUT"
