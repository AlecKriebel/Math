#!/bin/sh
set -eu

paper_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
tmp_dir="$paper_dir/tmp/pdfs"
out_dir="$paper_dir/output/pdf"
render_dir="$paper_dir/output/rendered"

mkdir -p "$tmp_dir" "$out_dir" "$render_dir"
export SOURCE_DATE_EPOCH=1786147200
export FORCE_SOURCE_DATE=1
export TZ=UTC

tectonic --keep-logs --keep-intermediates \
  --outdir "$tmp_dir" "$paper_dir/main.tex"
install -m 0644 "$tmp_dir/main.pdf" \
  "$out_dir/simultaneous_amplification_beyond_three_halves.pdf"
pdfinfo "$out_dir/simultaneous_amplification_beyond_three_halves.pdf"
find "$render_dir" -type f -name 'page-*.png' -delete
pdftoppm -png -r 150 \
  "$out_dir/simultaneous_amplification_beyond_three_halves.pdf" \
  "$render_dir/page" >/dev/null 2>&1
