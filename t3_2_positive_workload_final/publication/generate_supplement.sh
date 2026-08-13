#!/bin/sh
set -eu

project_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
publication_dir="$project_dir/publication"
fragment_dir="$publication_dir/supplement"

mkdir -p "$fragment_dir"

while IFS='|' read -r index source digest title; do
  case "$index" in
    ''|'#'*) continue ;;
  esac
  destination="$fragment_dir/${index}.tex"
  pandoc "$project_dir/$source" \
    --from=markdown+tex_math_dollars+tex_math_single_backslash+tex_math_double_backslash+raw_tex \
    --to=latex \
    --syntax-highlighting=none \
    -o "$destination"
  python3 "$publication_dir/postprocess_supplement.py" "$destination"
done < "$publication_dir/supplement-manifest.txt"
