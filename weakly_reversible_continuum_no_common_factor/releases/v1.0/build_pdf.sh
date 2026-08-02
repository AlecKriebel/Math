#!/bin/sh
set -eu

release_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
output_dir="$release_dir/output/pdf"
temporary_dir="$release_dir/tmp/pdfs"

mkdir -p "$output_dir" "$temporary_dir"
pandoc "$release_dir/source/MANUSCRIPT.md" \
    --from=markdown+tex_math_single_backslash \
    --standalone \
    --pdf-engine=tectonic \
    --lua-filter="$release_dir/strip-title.lua" \
    --metadata-file="$release_dir/pdf-metadata.yaml" \
    --include-in-header="$release_dir/pdf-header.tex" \
    --output="$output_dir/manuscript-v1.0.0.pdf"
