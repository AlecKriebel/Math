#!/bin/sh
set -eu

PACKAGE_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_DIR=$(CDPATH= cd -- "$PACKAGE_DIR/.." && pwd)
PYTHON_BIN=${PYTHON_BIN:-python3}
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/cyclic-bell-reproduce.XXXXXX")
trap 'rm -rf "$BUILD_DIR"' EXIT HUP INT TERM

export PYTHONDONTWRITEBYTECODE=1
export SOURCE_DATE_EPOCH=1786190400

for command_name in "$PYTHON_BIN" tectonic pdfinfo shasum xmllint; do
  command -v "$command_name" >/dev/null 2>&1 || {
    echo "FAIL: required command not found: $command_name" >&2
    exit 1
  }
done

echo "[1/10] Unified scalar, polar, strategy, permutation, SOS, and setting checks"
"$PYTHON_BIN" "$PACKAGE_DIR/verification/verify_merged.py"

echo "[2/10] Independent exact d=4 first-family certificate"
"$PYTHON_BIN" "$REPO_DIR/cyclic_randomness_counterexample/verify_exact.py"

echo "[3/10] Independent exact d=4 second-family certificate"
"$PYTHON_BIN" "$REPO_DIR/minimum_bell_randomness/verify_second_family_d4_exact.py"

echo "[4/10] Retained setting-complexity regressions"
"$PYTHON_BIN" "$REPO_DIR/minimum_bell_randomness/verify_binary_2x2.py"
"$PYTHON_BIN" "$REPO_DIR/minimum_bell_randomness/satwap_ideal_audit.py"
"$PYTHON_BIN" "$PACKAGE_DIR/verification/verify_mub_obstruction.py"
"$PYTHON_BIN" "$REPO_DIR/minimum_bell_randomness/test_cases.py"

echo "[5/10] Historical source-package integrity"
(cd "$REPO_DIR/cyclic_bell_tsirelson_bound" && shasum -a 256 -c SHA256SUMS)
(cd "$REPO_DIR/cyclic_randomness_counterexample" && shasum -a 256 -c MANIFEST.sha256)
(cd "$REPO_DIR/minimum_bell_randomness" && shasum -a 256 -c MANIFEST.sha256)

echo "[6/10] Canonical manuscript build"
mkdir -p "$BUILD_DIR/manuscript"
tectonic -X compile "$PACKAGE_DIR/main.tex" --outdir "$BUILD_DIR/manuscript" --keep-logs
test -s "$BUILD_DIR/manuscript/main.pdf"
if grep -Eiq '(undefined references|undefined citations|overfull|underfull|LaTeX Error|Emergency stop)' "$BUILD_DIR/manuscript/main.log"; then
  echo "FAIL: canonical manuscript log contains a layout/reference error" >&2
  grep -Ei '(undefined references|undefined citations|overfull|underfull|LaTeX Error|Emergency stop)' "$BUILD_DIR/manuscript/main.log" >&2
  exit 1
fi
pdfinfo "$BUILD_DIR/manuscript/main.pdf" | grep -F 'Exact Quantum Values and Permutation-Blind Maximizers' >/dev/null
pdfinfo "$BUILD_DIR/manuscript/main.pdf" | grep -F 'Author:          Alec Kriebel' >/dev/null

echo "[7/10] Two-page reviewer-summary build"
mkdir -p "$BUILD_DIR/summary"
tectonic -X compile "$PACKAGE_DIR/review_packet/two_page_summary.tex" --outdir "$BUILD_DIR/summary" --keep-logs
test -s "$BUILD_DIR/summary/two_page_summary.pdf"
if grep -Eiq '(undefined references|undefined citations|overfull|underfull|LaTeX Error|Emergency stop)' "$BUILD_DIR/summary/two_page_summary.log"; then
  echo "FAIL: reviewer-summary log contains a layout/reference error" >&2
  exit 1
fi
pdfinfo "$BUILD_DIR/summary/two_page_summary.pdf" | grep -F 'Pages:           2' >/dev/null

echo "[8/10] PDF metadata and deployed asset checks"
pdfinfo "$PACKAGE_DIR/output/pdf/cyclic_bell_exact_values_and_randomness.pdf" | grep -F 'Author:          Alec Kriebel' >/dev/null
pdfinfo "$PACKAGE_DIR/review_packet/two_page_summary.pdf" | grep -F 'Pages:           2' >/dev/null
test -s "$REPO_DIR/docs/papers/cyclic-bell-exact-values-and-randomness/paper.pdf"
test -s "$REPO_DIR/docs/papers/cyclic-bell-exact-values-and-randomness/two-page-summary.pdf"

echo "[9/10] Website metadata, redirects, sitemap, and local links"
"$PYTHON_BIN" "$PACKAGE_DIR/verification/verify_site.py"
xmllint --noout "$REPO_DIR/docs/sitemap.xml"

echo "[10/10] Canonical package integrity manifest"
(cd "$PACKAGE_DIR" && shasum -a 256 -c manifest.sha256)

echo "PASS: complete cyclic-Bell reproduction, build, integrity, and website validation"
