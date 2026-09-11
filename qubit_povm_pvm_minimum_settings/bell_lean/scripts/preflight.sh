#!/usr/bin/env bash
# Compiler-free checks only. The real proof runner is scripts/check.sh.
set -euo pipefail
cd "$(dirname "$0")/.."
exec python3 scripts/preflight_all.py "$@"
