#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
for f in combined-paper technical-summary; do
  latexmk -pdf -interaction=nonstopmode -halt-on-error "$f.tex"
done
