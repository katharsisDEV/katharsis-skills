#!/usr/bin/env bash
# Rend chaque page d'un PDF en PNG pour la relecture visuelle.
#   preview.sh <deck.pdf> [dossier] [dpi]   → <dossier>/p-01.png, p-02.png…
# Le contrôle automatique ne voit ni les collisions dans les SVG, ni les
# déséquilibres de page : il faut regarder les images.
set -euo pipefail
[ $# -ge 1 ] || { echo "usage : $0 <deck.pdf> [dossier] [dpi]" >&2; exit 2; }
DIR="${2:-$(dirname "$1")/_preview}"; DPI="${3:-80}"
mkdir -p "$DIR"; rm -f "$DIR"/p-*.png
if command -v pdftoppm >/dev/null; then
  pdftoppm -r "$DPI" -png "$1" "$DIR/p"
else
  echo "pdftoppm absent : brew install poppler" >&2; exit 1
fi
ls "$DIR"/p-*.png
