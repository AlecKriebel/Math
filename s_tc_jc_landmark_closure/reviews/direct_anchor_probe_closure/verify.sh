#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
PROJECT="$(cd "$HERE/../.." && pwd)"
cd "$PROJECT"

python3 -m py_compile \
  reviews/direct_anchor_probe_closure/exact_engine.py \
  reviews/direct_anchor_probe_closure/verify_direct_anchor_probes.py \
  reviews/direct_anchor_probe_closure/mutation_tests.py

PYTHONPATH=reviews/direct_anchor_probe_closure \
  python3 reviews/direct_anchor_probe_closure/verify_direct_anchor_probes.py
PYTHONPATH=reviews/direct_anchor_probe_closure \
  python3 reviews/direct_anchor_probe_closure/mutation_tests.py

(cd reviews/direct_anchor_probe_closure && shasum -a 256 -c MANIFEST.sha256)
