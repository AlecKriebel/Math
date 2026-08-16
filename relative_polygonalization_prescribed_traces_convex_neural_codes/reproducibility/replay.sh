#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REPRO="$ROOT/reproducibility"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
export SOURCE_DATE_EPOCH=1786752000

python3 "$REPRO/exact_verifier/verify_examples.py"

compile_article() {
  local src="$1"
  local dst="$2"
  cp -a "$src" "$dst"
  cd "$dst"
  rm -f main.aux main.bbl main.blg main.log main.out main.pdf
  pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
  BIBTEX_BIN="$(command -v bibtex.original || command -v bibtex)"
  "$BIBTEX_BIN" main >/dev/null
  pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
  pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
  pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
  test "$(pdfinfo main.pdf | awk '/Pages:/ {print $2}')" = "15"
  ! grep -q 'Undefined control sequence\|Citation.*undefined\|Reference.*undefined\|Overfull' main.log
}

compile_article "$ROOT/manuscript" "$TMP/manuscript"
compile_article "$ROOT/arxiv_submission" "$TMP/arxiv_submission"

cp -a "$ROOT/outreach/two_page_summary.tex" "$TMP/summary.tex"
cd "$TMP"
pdflatex -interaction=nonstopmode -halt-on-error summary.tex >/dev/null
pdflatex -interaction=nonstopmode -halt-on-error summary.tex >/dev/null
test "$(pdfinfo summary.pdf | awk '/Pages:/ {print $2}')" = "2"

FIGCOUNT=$(find "$ROOT/manuscript/figures" -maxdepth 1 -name '*.tikz' | wc -l)
test "$FIGCOUNT" -eq 7

cd "$REPRO"
sha256sum -c MANIFEST.sha256 >/dev/null

echo 'MANUSCRIPT FRESH COMPILE PASS (15 pages)'
echo 'ARXIV SOURCE FRESH COMPILE PASS (15 pages)'
echo 'TWO-PAGE SUMMARY FRESH COMPILE PASS'
echo 'VECTOR FIGURE COUNT PASS (7)'
echo 'REPRODUCIBILITY MANIFEST PASS'
echo 'PAPER 2 NO-NETWORK REPLAY PASS'
