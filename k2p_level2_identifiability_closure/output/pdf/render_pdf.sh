#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
project_root=$(CDPATH= cd -- "$script_dir/../.." && pwd)
pandoc_bin=${PANDOC:-$(command -v pandoc)}
tectonic_bin=${TECTONIC:-$(command -v tectonic)}
source_date_epoch=${SOURCE_DATE_EPOCH:-1787270400}

SOURCE_DATE_EPOCH=$source_date_epoch "$pandoc_bin" \
  "$project_root/work/global_theorem_closure/promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md" \
  --from=markdown+tex_math_dollars+tex_math_single_backslash+pipe_tables+raw_tex \
  --standalone \
  --toc \
  --toc-depth=2 \
  --lua-filter="$script_dir/pdf_filter.lua" \
  --include-in-header="$script_dir/pdf_header.tex" \
  --pdf-engine="$tectonic_bin" \
  --metadata title='Generic Identifiability and Directed Containment for Strongly Tree-Child Level-2 Networks under K2P' \
  --metadata subtitle='Principal positive domain theorem and reproducibility manifest' \
  --metadata date='August 21, 2026' \
  -V geometry:margin=0.9in \
  -V fontsize=10pt \
  -V colorlinks=true \
  -V linkcolor=blue \
  -V urlcolor=blue \
  -V documentclass=article \
  -o "$script_dir/K2P_SAME_Principal_Domain_Theorem.pdf"

