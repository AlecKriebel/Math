#!/bin/sh
set -eu

paper_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(CDPATH= cd -- "$paper_dir/../../.." && pwd)
default_output="$paper_dir/output/release/simultaneous_amplifier_beyond_three_halves_source_and_certificates.tar.gz"
output=${1:-"$default_output"}

case "$output" in
  /*) ;;
  *) output="$PWD/$output" ;;
esac

mkdir -p "$(dirname -- "$output")"
"$paper_dir/replay.sh"
"$paper_dir/build.sh" >/dev/null
python3 "$paper_dir/bundle_manifest.py" \
  --repo-root "$repo_root" \
  --output "$output"
