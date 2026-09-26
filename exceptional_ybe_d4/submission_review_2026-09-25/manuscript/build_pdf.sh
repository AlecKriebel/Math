#!/usr/bin/env bash
set -euo pipefail
YBE_SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
YBE_OUTPUT_DIR="${YBE_OUTPUT_DIR:-$YBE_SOURCE_DIR/../output/pdf}"
mkdir -p "$YBE_OUTPUT_DIR"
# Fixed epoch for the submission revision, not a new archival DOI release.
export SOURCE_DATE_EPOCH=1790398800
tectonic -X compile "$YBE_SOURCE_DIR/main.tex" \
  --bundle https://relay.fullyjustified.net/default_bundle_v33.tar \
  --keep-logs --keep-intermediates --outdir "$YBE_OUTPUT_DIR"
cp "$YBE_OUTPUT_DIR/main.pdf" "$YBE_OUTPUT_DIR/01_Manuscript.pdf"
