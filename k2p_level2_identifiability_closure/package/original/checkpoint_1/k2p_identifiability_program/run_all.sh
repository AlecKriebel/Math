#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
python3 "$ROOT/code/build_checkpoint.py" | tee "$ROOT/logs/build_checkpoint.txt"
python3 "$ROOT/code/make_manifest.py" | tee "$ROOT/logs/make_manifest.txt"
echo 'checkpoint replay complete'
