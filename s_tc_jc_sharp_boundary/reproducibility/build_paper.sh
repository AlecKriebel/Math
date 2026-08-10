#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source_file="$repo_dir/source/paper/main.tex"
output_dir="$repo_dir/submission"
output_file="$output_dir/Weakly_Tree_Child_Level2_JC_Ambiguity.pdf"

if [[ -n "${TECTONIC_BIN:-}" ]]; then
  tectonic_bin="$TECTONIC_BIN"
elif command -v tectonic >/dev/null 2>&1; then
  tectonic_bin="$(command -v tectonic)"
elif [[ -x /opt/homebrew/bin/tectonic ]]; then
  tectonic_bin=/opt/homebrew/bin/tectonic
else
  echo "ERROR: Tectonic is required (set TECTONIC_BIN or install tectonic)." >&2
  exit 2
fi

build_dir="$(mktemp -d "${TMPDIR:-/tmp}/stc-jc-paper.XXXXXX")"
cleanup() {
  rm -rf -- "$build_dir"
}
trap cleanup EXIT

mkdir -p "$output_dir"
export SOURCE_DATE_EPOCH=1786258800
"$tectonic_bin" -X compile "$source_file" --outdir "$build_dir" --keep-logs

if [[ ! -s "$build_dir/main.pdf" ]]; then
  echo "ERROR: manuscript build did not produce a nonempty PDF." >&2
  exit 3
fi

install -m 0644 "$build_dir/main.pdf" "$output_file"
printf 'BUILT %s\n' "$output_file"
shasum -a 256 "$output_file"
