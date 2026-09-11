#!/usr/bin/env bash
# The Python runner maintains fresh receipts and never installs Lean itself.
set -euo pipefail
cd "$(dirname "$0")/.."
exec python3 scripts/run_lean.py "$@"
