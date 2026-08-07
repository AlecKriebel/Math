#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
export SOURCE_DATE_EPOCH="${SOURCE_DATE_EPOCH:-1785974400}"
BIBTEX="$(command -v bibtex || command -v bibtex.original)"
for base in main_arxiv main_jap; do
  pdflatex -interaction=nonstopmode -halt-on-error "$base.tex"
  "$BIBTEX" "$base"
  pdflatex -interaction=nonstopmode -halt-on-error "$base.tex"
  pdflatex -interaction=nonstopmode -halt-on-error "$base.tex"
done
