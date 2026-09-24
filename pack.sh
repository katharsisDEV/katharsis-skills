#!/usr/bin/env bash
# Produit un fichier .zip par skill dans dist/, à téléverser sur claude.ai
# (Paramètres → Capacités → Skills) pour l'utiliser hors de Claude Code.
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
mkdir -p "$REPO/dist"
for s in "$REPO"/plugins/*/skills/*/; do
  name="$(basename "$s")"
  (cd "$(dirname "$s")" && rm -f "$REPO/dist/$name.zip" && zip -qr "$REPO/dist/$name.zip" "$name" -x '*.DS_Store' '*__pycache__*')
  echo "→ dist/$name.zip"
done
