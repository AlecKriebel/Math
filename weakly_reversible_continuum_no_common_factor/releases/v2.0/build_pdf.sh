#!/bin/sh
set -eu

release_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
source_dir="$release_dir/source"
output_dir="$release_dir/output/pdf"
temporary_dir="$release_dir/tmp/pdfs"

mkdir -p "$output_dir" "$temporary_dir"

pandoc "$source_dir/MANUSCRIPT_V2.md" \
    --from=markdown+tex_math_dollars+raw_tex \
    --standalone \
    --pdf-engine=xelatex \
    --lua-filter="$source_dir/strip-title.lua" \
    --metadata-file="$source_dir/pdf-metadata.yaml" \
    --include-in-header="$source_dir/pdf-header.tex" \
    --output="$output_dir/manuscript-v2.0.0.pdf"

pdfinfo "$output_dir/manuscript-v2.0.0.pdf"
pdftoppm -png "$output_dir/manuscript-v2.0.0.pdf" \
    "$temporary_dir/manuscript-v2.0.0"
