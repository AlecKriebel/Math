#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-/opt/homebrew/bin/python3}"
SYMPY_SITE="${SYMPY_SITE:-/Users/alec/Library/Python/3.9/lib/python/site-packages}"
MODE="${1:---full}"

case "$MODE" in
  --quick|--full) ;;
  *)
    echo "usage: $0 [--quick|--full]" >&2
    exit 2
    ;;
esac

cd "$HERE"
shasum -a 256 -c MANIFEST.sha256

export PYTHONPATH="$HERE:$SYMPY_SITE${PYTHONPATH:+:$PYTHONPATH}"
cd "$ROOT"

if [[ "$MODE" == "--full" ]]; then
  bash "$HERE/verify_schema3_n4_full.sh"
else
  bash "$HERE/verify_schema3_n4_quick.sh"
fi

"$PYTHON_BIN" "$HERE/verify_universes.py"
"$PYTHON_BIN" "$HERE/verify_pq_extension.py"
"$PYTHON_BIN" "$HERE/mutation_tests.py"

cd "$HERE"
shasum -a 256 -c MANIFEST.sha256
echo "VERIFIED: scoped schema-3 n=4 theta-2 hard cover"
echo "UNRESOLVED: merged n=3, unequal-signature directions, primitive-root exhaustiveness, cycle/cross-core directions, and T-edge probe coherence"
