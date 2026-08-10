#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-/opt/homebrew/bin/python3}"
SYMPY_SITE="${SYMPY_SITE:-/Users/alec/Library/Python/3.9/lib/python/site-packages}"
export PYTHONPATH="$HERE:$SYMPY_SITE${PYTHONPATH:+:$PYTHONPATH}"
cd "$ROOT"

"$PYTHON_BIN" "$HERE/verify_schema3_n4_certificates.py"
"$PYTHON_BIN" "$HERE/mutation_schema3_stream.py"
"$PYTHON_BIN" "$HERE/mutation_probe_extension.py"
