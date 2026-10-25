#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
for f in k2p_displayed_tree_clarification combined-paper-clarified technical-summary-clarified; do
  if command -v latexmk >/dev/null 2>&1; then
    latexmk -pdf -interaction=nonstopmode -halt-on-error "$f.tex"
  elif command -v tectonic >/dev/null 2>&1; then
    tectonic --keep-logs "$f.tex"
  else
    echo "A TeX engine (latexmk or tectonic) is required." >&2
    exit 1
  fi
done
