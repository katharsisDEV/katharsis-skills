#!/usr/bin/env bash
# Rend chaque source HTML en PDF paysage 959 × 540 pt via Chrome headless.
# À copier dans le dossier du projet, à côté des fichiers HTML.
set -euo pipefail
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"

render() {  # render <source.html> <sortie.pdf>
  "$CHROME" \
    --headless=new --disable-gpu \
    --no-pdf-header-footer \
    --allow-file-access-from-files \
    --virtual-time-budget=8000 \
    --print-to-pdf="$DIR/$2" \
    "file://$DIR/$1" 2>/dev/null
  echo "→ $DIR/$2"
}

render presentation.html Dossier_Technique.pdf
# render reserves.html     Points_Ouverts.pdf
