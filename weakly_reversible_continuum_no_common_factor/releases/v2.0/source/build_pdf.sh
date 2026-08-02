#!/bin/sh
set -eu

draft_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
output_dir="$draft_dir/output/pdf"
temporary_dir="$draft_dir/tmp/pdfs"

mkdir -p "$output_dir" "$temporary_dir"

pandoc "$draft_dir/MANUSCRIPT_V2.md" \
    --from=markdown+tex_math_single_backslash \
    --standalone \
    --pdf-engine=tectonic \
    --lua-filter="$draft_dir/strip-title.lua" \
    --metadata-file="$draft_dir/pdf-metadata.yaml" \
    --include-in-header="$draft_dir/pdf-header.tex" \
    --output="$output_dir/manuscript-v2.0.0.pdf"
