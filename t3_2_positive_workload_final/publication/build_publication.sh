#!/bin/sh
set -eu

project_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
publication_dir="$project_dir/publication"
fragment_dir="$publication_dir/supplement"
output_dir="$project_dir/output/pdf"

mkdir -p "$fragment_dir" "$output_dir"

"$publication_dir/verify_supplement.py"
"$publication_dir/generate_supplement.sh"

tectonic -X compile \
  --keep-logs \
  --outdir "$output_dir" \
  "$publication_dir/main.tex"

tectonic -X compile \
  --keep-logs \
  --outdir "$output_dir" \
  "$publication_dir/technical-supplement.tex"
