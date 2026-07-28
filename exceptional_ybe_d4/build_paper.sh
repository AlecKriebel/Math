#!/usr/bin/env bash
set -euo pipefail

YBE_PAPER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
YBE_TECTONIC="${YBE_TECTONIC:-tectonic}"
YBE_SOURCE_DATE_EPOCH="${YBE_SOURCE_DATE_EPOCH:-1785207600}"
YBE_BUILD_DIR="$YBE_PAPER_DIR/tmp/tex-build"
YBE_OUTPUT_DIR="$YBE_PAPER_DIR/output/pdf"

mkdir -p "$YBE_BUILD_DIR" "$YBE_OUTPUT_DIR"
export SOURCE_DATE_EPOCH="$YBE_SOURCE_DATE_EPOCH"

"$YBE_TECTONIC" -X compile "$YBE_PAPER_DIR/main.tex" \
  --outdir "$YBE_BUILD_DIR" \
  --keep-logs \
  --keep-intermediates

cp "$YBE_BUILD_DIR/main.pdf" \
  "$YBE_OUTPUT_DIR/exceptional_ybe_d4.pdf"

echo "Built $YBE_OUTPUT_DIR/exceptional_ybe_d4.pdf"
