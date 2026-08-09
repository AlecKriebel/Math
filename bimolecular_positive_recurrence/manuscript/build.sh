#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
export SOURCE_DATE_EPOCH="${SOURCE_DATE_EPOCH:-1786276800}"

bases=(main_arxiv main_jap)
required=(paper_content.tex references.bib)
for base in "${bases[@]}"; do
  required+=("$base.tex")
done
for input in "${required[@]}"; do
  if [[ ! -r "$input" ]]; then
    echo "build error: required input is missing or unreadable: $input" >&2
    exit 2
  fi
done

engine="${TEX_ENGINE:-auto}"
if [[ "$engine" == auto ]]; then
  if command -v tectonic >/dev/null 2>&1; then
    engine=tectonic
  elif command -v pdflatex >/dev/null 2>&1; then
    engine=pdflatex
  else
    echo "build error: install Tectonic 0.16.9 (reference toolchain) or pdflatex plus BibTeX" >&2
    exit 2
  fi
fi

case "$engine" in
  tectonic)
    if ! command -v tectonic >/dev/null 2>&1; then
      echo "build error: TEX_ENGINE=tectonic but tectonic is not on PATH" >&2
      exit 2
    fi
    echo "Building with $(tectonic --version)"
    build_tmp="$(mktemp -d "${TMPDIR:-/tmp}/bimolecular-tex.XXXXXX")"
    trap 'rm -rf -- "$build_tmp"' EXIT
    for base in "${bases[@]}"; do
      outdir="$build_tmp/$base"
      mkdir -p "$outdir"
      # The checked-in wrappers begin with two pdfTeX metadata controls.
      # Define compatible count registers before loading them under Tectonic.
      printf '%s\n' \
        '\newcount\pdfinfoomitdate' \
        '\newcount\pdfsuppressptexinfo' \
        "\\input{$base.tex}" \
        | tectonic --color never --outdir "$outdir" -
      cp "$outdir/texput.pdf" "$base.pdf"
    done
    ;;
  pdflatex)
    if ! command -v pdflatex >/dev/null 2>&1; then
      echo "build error: TEX_ENGINE=pdflatex but pdflatex is not on PATH" >&2
      exit 2
    fi
    if command -v bibtex >/dev/null 2>&1; then
      bibtex_bin="$(command -v bibtex)"
    elif command -v bibtex.original >/dev/null 2>&1; then
      bibtex_bin="$(command -v bibtex.original)"
    else
      echo "build error: the pdflatex build also requires bibtex" >&2
      exit 2
    fi
    echo "Building with $(pdflatex --version | head -n 1)"
    for base in "${bases[@]}"; do
      pdflatex -interaction=nonstopmode -halt-on-error "$base.tex"
      "$bibtex_bin" "$base"
      pdflatex -interaction=nonstopmode -halt-on-error "$base.tex"
      pdflatex -interaction=nonstopmode -halt-on-error "$base.tex"
    done
    ;;
  *)
    echo "build error: TEX_ENGINE must be auto, tectonic, or pdflatex" >&2
    exit 2
    ;;
esac
