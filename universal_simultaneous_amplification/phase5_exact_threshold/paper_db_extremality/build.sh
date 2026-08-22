#!/bin/sh
set -eu

paper_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
tmp_dir="$paper_dir/tmp/pdfs"
out_dir="$paper_dir/output/pdf"
render_dir="$paper_dir/output/rendered"
bundle_url="https://relay.fullyjustified.net/default_bundle_v33.tar"
bundle_digest="6ffe055852f8faf66c0acbe1a7fb27f87b869a90bad1204f3bf4d9683f597c7c"

if [ "$(tectonic --version)" != "Tectonic 0.16.9" ]; then
  echo "Tectonic 0.16.9 is required" >&2
  exit 2
fi
if [ "$(pdfinfo -v 2>&1 | sed -n '1p')" != "pdfinfo version 26.08.0" ]; then
  echo "pdfinfo 26.08.0 is required" >&2
  exit 2
fi
if [ "$(pdftoppm -v 2>&1 | sed -n '1p')" != "pdftoppm version 26.08.0" ]; then
  echo "pdftoppm 26.08.0 is required" >&2
  exit 2
fi

mkdir -p "$tmp_dir" "$out_dir" "$render_dir"
export SOURCE_DATE_EPOCH=1787270400
export FORCE_SOURCE_DATE=1
export TZ=UTC

tectonic --keep-logs --keep-intermediates \
  --bundle "$bundle_url" \
  --outdir "$tmp_dir" "$paper_dir/main.tex"

tectonic_cache=$(tectonic -X show user-cache-dir)
bundle_record="$tectonic_cache/hashes/https,58,,47,,47,relay.fullyjustified.net,47,default_bundle_v33.tar"
if [ ! -f "$bundle_record" ]; then
  echo "Cannot locate Tectonic's v33 bundle-content record" >&2
  exit 2
fi
actual_bundle_digest=$(tr -d '\r\n' < "$bundle_record")
if [ "$actual_bundle_digest" != "$bundle_digest" ]; then
  echo "Tectonic v33 bundle digest mismatch" >&2
  echo "expected: $bundle_digest" >&2
  echo "actual:   $actual_bundle_digest" >&2
  exit 2
fi
echo "PASS: pinned Tectonic v33 bundle digest $bundle_digest"

install -m 0644 "$tmp_dir/main.pdf" \
  "$out_dir/complete_graph_extremality_db.pdf"
pdfinfo "$out_dir/complete_graph_extremality_db.pdf"
find "$render_dir" -type f -name 'page-*.png' -delete
pdftoppm -png -r 150 \
  "$out_dir/complete_graph_extremality_db.pdf" \
  "$render_dir/page" >/dev/null 2>&1
