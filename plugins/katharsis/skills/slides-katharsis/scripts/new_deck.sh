#!/usr/bin/env bash
# Prépare un dossier de présentation à la charte Katharsis.
#   new_deck.sh <dossier> [nom.html]
# Copie theme.css, logo, fontes, le gabarit et les scripts de build / contrôle.
# N'écrase jamais un fichier existant.
set -euo pipefail
SKILL="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
[ $# -ge 1 ] || { echo "usage : $0 <dossier> [nom.html]" >&2; exit 2; }
D="$1"; NAME="${2:-presentation.html}"
mkdir -p "$D/assets/fonts"
cp -n "$SKILL/assets/theme.css" "$D/" || true
cp -n "$SKILL/assets/logo-katharsis.svg" "$D/assets/" || true
cp -n "$SKILL"/assets/fonts/*.woff2 "$D/assets/fonts/" || true
[ -e "$D/$NAME" ] || cp "$SKILL/assets/template.html" "$D/$NAME"
for f in build.sh preview.sh check_layout.py; do cp -n "$SKILL/scripts/$f" "$D/" || true; done
chmod +x "$D"/build.sh "$D"/preview.sh
echo "Prêt : $D/$NAME"
