#!/usr/bin/env bash
# Installation SANS marketplace : lie chaque skill du dépôt dans ~/.claude/skills.
# Utile pour développer (les modifications du dépôt sont prises en compte tout de suite)
# ou sur une machine où l'on ne veut pas passer par /plugin.
#   ./install.sh            installe tous les skills
#   ./install.sh --remove   retire les liens créés
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
mkdir -p "$DEST"
for s in "$REPO"/plugins/*/skills/*/; do
  name="$(basename "$s")"; target="$DEST/$name"
  if [ "${1:-}" = "--remove" ]; then
    [ -L "$target" ] && rm "$target" && echo "retiré  $name"
    continue
  fi
  if [ -e "$target" ] && [ ! -L "$target" ]; then
    echo "!! $target existe déjà (copie locale) — le renommer ou le supprimer, puis relancer"; continue
  fi
  ln -sfn "${s%/}" "$target" && echo "lié     $name → $target"
done
