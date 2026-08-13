#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
PAPER="$ROOT/source/paper"
DOCS="$ROOT/docs"
OUT="$ROOT/submission"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
export SOURCE_DATE_EPOCH=1785974400 FORCE_SOURCE_DATE=1 TZ=UTC
mkdir -p "$OUT"

build_tex() {
  local source=$1 expected_pages=$2 output=$3
  local work="$TMP/$(basename "$source" .tex)"
  mkdir -p "$work"
  cp "$source" "$work/input.tex"
  (cd "$work" && latexmk -pdf -interaction=nonstopmode -halt-on-error input.tex >build.log 2>&1) || {
    cat "$work/build.log" >&2; exit 1;
  }
  if grep -Eq 'LaTeX Warning: (There were undefined references|Citation .* undefined)|Overfull \\hbox|Overfull \\vbox' "$work/input.log"; then
    echo "$(basename "$source") contains an unresolved reference/citation or overfull box" >&2
    grep -E 'LaTeX Warning: (There were undefined references|Citation .* undefined)|Overfull \\hbox|Overfull \\vbox' "$work/input.log" >&2 || true
    exit 1
  fi
  pdfinfo "$work/input.pdf" | grep -q "^Pages:[[:space:]]*$expected_pages$"
  pdffonts "$work/input.pdf" | awk 'NR>2 {if ($5!="yes") bad=1} END {exit bad}'
  cp "$work/input.pdf" "$OUT/$output"
}

cd "$PAPER"
latexmk -C >/dev/null 2>&1 || true
if ! latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex >"$TMP/paper.log" 2>&1; then
  cat "$TMP/paper.log" >&2
  exit 1
fi
if grep -Eq 'LaTeX Warning: (There were undefined references|Citation .* undefined)|Overfull \\hbox|Overfull \\vbox' main.log; then
  echo 'paper log contains an unresolved reference/citation or overfull box' >&2
  grep -E 'LaTeX Warning: (There were undefined references|Citation .* undefined)|Overfull \\hbox|Overfull \\vbox' main.log >&2 || true
  exit 1
fi
pdfinfo main.pdf | grep -q '^Pages:[[:space:]]*48$'
pdffonts main.pdf | awk 'NR>2 {if ($5!="yes") bad=1} END {exit bad}'
cp main.pdf "$OUT/Generic_Identifiability_STC_Level2_JC.pdf"

build_tex "$DOCS/COVER_LETTER.tex" 1 Cover_Letter.pdf
build_tex "$DOCS/COVER_LETTER_JMB.tex" 1 Cover_Letter_JMB.pdf
build_tex "$DOCS/COVER_LETTER_BMB.tex" 1 Cover_Letter_BMB.pdf
build_tex "$DOCS/REFEREE_GUIDE.tex" 2 Referee_Guide.pdf

# Keep the source tree submission-clean; all auxiliary products are reproducible.
rm -f main.aux main.bcf main.blg main.fdb_latexmk main.fls main.log main.out main.run.xml main.bbl
printf '%s\n' 'PAPER AND EDITORIAL PDF BUILD PASSED (48 manuscript pages; all fonts embedded)'
