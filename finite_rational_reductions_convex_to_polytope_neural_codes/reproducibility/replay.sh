#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export SOURCE_DATE_EPOCH=1786752000
export FORCE_SOURCE_DATE=1
export TZ=UTC
BIBTEX=/usr/bin/bibtex.original
if [[ ! -x "$BIBTEX" ]]; then BIBTEX=bibtex; fi

cd "$ROOT"
sha256sum -c reproducibility/MANIFEST.sha256
python3 reproducibility/exact_verifier/verify_all.py

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

copy_manuscript() {
  mkdir -p "$TMP/manuscript/figures" "$TMP/manuscript/appendices"
  cp manuscript/*.tex manuscript/references.bib "$TMP/manuscript/"
  cp manuscript/figures/*.tex "$TMP/manuscript/figures/"
  cp manuscript/appendices/*.tex "$TMP/manuscript/appendices/"
}
copy_manuscript
(
  cd "$TMP/manuscript"
  pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
  "$BIBTEX" main >/dev/null
  pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
  pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
  pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
)
cmp "$TMP/manuscript/main.pdf" manuscript/main.pdf
echo "MANUSCRIPT REPRODUCIBLE PDF BUILD PASS"

mkdir -p "$TMP/appendix"
cp reproducibility/technical_appendix.tex reproducibility/technical_appendix_body.tex "$TMP/appendix/"
(
  cd "$TMP/appendix"
  pdflatex -interaction=nonstopmode -halt-on-error technical_appendix.tex >/dev/null
  pdflatex -interaction=nonstopmode -halt-on-error technical_appendix.tex >/dev/null
)
cmp "$TMP/appendix/technical_appendix.pdf" reproducibility/technical_appendix.pdf
echo "TECHNICAL APPENDIX REPRODUCIBLE PDF BUILD PASS"

mkdir -p "$TMP/summary"
cp outreach/two_page_summary.tex "$TMP/summary/"
(
  cd "$TMP/summary"
  pdflatex -interaction=nonstopmode -halt-on-error two_page_summary.tex >/dev/null
  pdflatex -interaction=nonstopmode -halt-on-error two_page_summary.tex >/dev/null
)
cmp "$TMP/summary/two_page_summary.pdf" outreach/two_page_summary.pdf
echo "TWO-PAGE SUMMARY REPRODUCIBLE PDF BUILD PASS"

mkdir -p "$TMP/arxiv"
cp -a arxiv_submission/. "$TMP/arxiv/"
(
  cd "$TMP/arxiv"
  pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
  "$BIBTEX" main >/dev/null
  pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
  pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
  pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
)
cmp "$TMP/arxiv/main.pdf" manuscript/main.pdf
echo "ARXIV CLEAN SOURCE COMPILE PASS"

echo "PAPER 1 COMPLETE NO-NETWORK REPLAY PASS"
