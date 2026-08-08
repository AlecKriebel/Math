#!/bin/sh
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/../../../.." && pwd)
cd "$root"

if [ -z "${PYTHON:-}" ]; then
  if [ -x "$root/.venv/bin/python" ]; then
    PYTHON="$root/.venv/bin/python"
  else
    PYTHON=python3
  fi
fi

PYTHONDONTWRITEBYTECODE=1 "$PYTHON" \
  universal_simultaneous_amplification/phase4_landmark_closure/threshold/endpoint_affine_global_v2/verify_exact_counterexample.py
PYTHONDONTWRITEBYTECODE=1 "$PYTHON" \
  universal_simultaneous_amplification/phase4_landmark_closure/threshold/endpoint_affine_global_v2/verify_independent.py
