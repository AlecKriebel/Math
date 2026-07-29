#!/usr/bin/env bash
set -euo pipefail

YBE_FRONTIER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
YBE_FRONTIER_TECTONIC="${YBE_FRONTIER_TECTONIC:-tectonic}"
YBE_FRONTIER_SOURCE_DATE_EPOCH="${YBE_FRONTIER_SOURCE_DATE_EPOCH:-1785351600}"
YBE_FRONTIER_BUILD_DIR="$YBE_FRONTIER_DIR/tmp/tex-build"
YBE_FRONTIER_OUTPUT_DIR="$YBE_FRONTIER_DIR/output/pdf"

mkdir -p "$YBE_FRONTIER_BUILD_DIR" "$YBE_FRONTIER_OUTPUT_DIR"
export SOURCE_DATE_EPOCH="$YBE_FRONTIER_SOURCE_DATE_EPOCH"

"$YBE_FRONTIER_TECTONIC" -X compile \
  "$YBE_FRONTIER_DIR/manuscript/main.tex" \
  --outdir "$YBE_FRONTIER_BUILD_DIR" \
  --keep-logs \
  --keep-intermediates

cp "$YBE_FRONTIER_BUILD_DIR/main.pdf" \
  "$YBE_FRONTIER_OUTPUT_DIR/exceptional_ybe_constraints.pdf"

echo "Built $YBE_FRONTIER_OUTPUT_DIR/exceptional_ybe_constraints.pdf"
