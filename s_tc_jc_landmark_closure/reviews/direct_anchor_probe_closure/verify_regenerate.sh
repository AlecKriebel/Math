#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
PROJECT="$(cd "$HERE/../.." && pwd)"
PYTHON="${PYTHON:-python3}"
cd "$PROJECT"

"$PYTHON" -c 'import sympy' >/dev/null
PYTHONPATH=reviews/direct_anchor_probe_closure \
  "$PYTHON" reviews/direct_anchor_probe_closure/compile_direct_anchor_probes.py
PYTHONPATH=reviews/direct_anchor_probe_closure \
  "$PYTHON" reviews/direct_anchor_probe_closure/verify_direct_anchor_probes.py
PYTHONPATH=reviews/direct_anchor_probe_closure \
  "$PYTHON" reviews/direct_anchor_probe_closure/mutation_tests.py

(cd reviews/direct_anchor_probe_closure && shasum -a 256 -c MANIFEST.sha256)
