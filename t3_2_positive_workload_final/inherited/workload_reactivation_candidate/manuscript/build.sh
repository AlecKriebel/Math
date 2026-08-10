#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
export SOURCE_DATE_EPOCH=1786233600
rm -f main.aux main.log main.out main.pdf
pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
if grep -E 'Undefined|Citation.*undefined|Reference.*undefined|Overfull \\hbox' main.log; then
  echo 'LaTeX diagnostic failure' >&2
  exit 1
fi
pdfinfo main.pdf | grep '^Pages:'
sha256sum main.pdf
