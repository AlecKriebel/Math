#!/bin/sh
set -eu

paper_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$paper_dir"

if command -v tectonic >/dev/null 2>&1; then
    exec tectonic main.tex --keep-logs
fi

if command -v latexmk >/dev/null 2>&1; then
    exec latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
fi

printf '%s\n' "Install Tectonic or latexmk to build paper/main.pdf." >&2
exit 1
