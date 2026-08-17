#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Canonical Version 1.2 build environment. Ambient values are deliberately
# ignored so the committed PDFs do not depend on the caller's shell.
# shellcheck disable=SC1091
source ../REPRODUCIBILITY.env
export SOURCE_DATE_EPOCH
readonly EXPECTED_TECTONIC_VERSION="Tectonic $TECTONIC_VERSION"

if ! command -v tectonic >/dev/null 2>&1; then
  echo "build error: canonical PDFs require Tectonic 0.16.9" >&2
  exit 2
fi
if [[ "$(tectonic --version)" != "$EXPECTED_TECTONIC_VERSION" ]]; then
  echo "build error: expected $EXPECTED_TECTONIC_VERSION, found $(tectonic --version)" >&2
  exit 2
fi

inputs=(
  main_arxiv.tex
  main_biorxiv.tex
  main_jap.tex
  paper_content.tex
  references.bib
  supplementary_note.tex
)
for input in "${inputs[@]}"; do
  if [[ ! -r "$input" ]]; then
    echo "build error: required input is missing or unreadable: $input" >&2
    exit 2
  fi
done

build_tmp="$(mktemp -d "${TMPDIR:-/tmp}/bimolecular-tex.XXXXXX")"
trap 'rm -rf -- "$build_tmp"' EXIT

build_pdf() {
  local input="$1"
  local output="$2"
  local label="$3"
  local outdir="$build_tmp/$label"
  mkdir -p "$outdir"

  # The checked-in inputs begin with two pdfTeX metadata controls. Define
  # compatible count registers before loading them under Tectonic.
  printf '%s\n' \
    '\newcount\pdfinfoomitdate' \
    '\newcount\pdfsuppressptexinfo' \
    "\\input{$input}" \
    | tectonic \
        --color never \
        --bundle "$TECTONIC_BUNDLE_URL" \
        -Z deterministic-mode \
        --outdir "$outdir" \
        -
  cp "$outdir/texput.pdf" "$output"
}

echo "Building canonical PDFs with $EXPECTED_TECTONIC_VERSION"
echo "Tectonic bundle digest: $TECTONIC_BUNDLE_CONTENT_DIGEST"
build_pdf main_arxiv.tex main_arxiv.pdf main_arxiv
build_pdf main_biorxiv.tex main_biorxiv.pdf main_biorxiv
build_pdf main_jap.tex main_jap.pdf main_jap
build_pdf supplementary_note.tex supplementary_note.pdf supplementary_note
