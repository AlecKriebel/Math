#!/bin/sh
set -eu

paper_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(CDPATH= cd -- "$paper_dir/../../.." && pwd)
default_output="$paper_dir/output/release/complete_graph_extremality_db_source_and_certificates.tar.gz"
output=${1:-"$default_output"}

case "$output" in
  /*) ;;
  *) output="$PWD/$output" ;;
esac

mkdir -p "$(dirname -- "$output")"
if [ -f "$paper_dir/submission/verify_submission_materials.py" ]; then
  python3 "$paper_dir/submission/verify_submission_materials.py"
fi
python3 "$paper_dir/bundle_manifest.py" \
  --repo-root "$repo_root" \
  --output "$output"
