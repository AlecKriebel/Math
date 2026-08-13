#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
python3 "$HERE/verify_structural_obstruction.py"

