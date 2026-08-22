#!/bin/sh
set -eu

paper_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(CDPATH= cd -- "$paper_dir/../../.." && pwd)
project_root=$(CDPATH= cd -- "$paper_dir/../.." && pwd)
default_output="$paper_dir/output/release/simultaneous_amplifier_beyond_three_halves_source_and_certificates.tar.gz"
output=${1:-"$default_output"}

if [ -n "${PYTHON:-}" ]; then
  python=$PYTHON
elif [ -x "$project_root/.venv-paper2/bin/python" ]; then
  python="$project_root/.venv-paper2/bin/python"
elif [ -n "${BOOTSTRAP_PYTHON:-}" ]; then
  python=$BOOTSTRAP_PYTHON
else
  python=python3
fi

"$python" -c '
import sys
if sys.version_info[:3] != (3, 14, 6):
    raise SystemExit(f"Python 3.14.6 is required; found {sys.version}")
'
export PYTHONDONTWRITEBYTECODE=1

case "$output" in
  /*) ;;
  *) output="$PWD/$output" ;;
esac

mkdir -p "$(dirname -- "$output")"
PYTHON="$python" "$paper_dir/replay.sh"
"$paper_dir/build.sh" >/dev/null
"$python" "$paper_dir/bundle_manifest.py" \
  --repo-root "$repo_root" \
  --output "$output"
