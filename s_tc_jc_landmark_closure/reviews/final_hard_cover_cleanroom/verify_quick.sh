#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE/../.."

PYTHONPATH="$HERE" python3 "$HERE/mutation_tests.py"
PYTHONPATH="$HERE" python3 "$HERE/verify_universes.py"
PYTHONPATH="$HERE" python3 "$HERE/verify_pq_extension.py"
PYTHONPATH="$HERE" python3 "$HERE/audit_primary_stream.py"

