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
  universal_simultaneous_amplification/phase4_landmark_closure/threshold/dilute_pair_leaf_hybrid/verify_leading_algebra.py
PYTHONDONTWRITEBYTECODE=1 "$PYTHON" \
  universal_simultaneous_amplification/phase4_landmark_closure/threshold/endpoint_construction_v2/verify_hybrid_lumping.py
PYTHONDONTWRITEBYTECODE=1 "$PYTHON" \
  universal_simultaneous_amplification/phase4_landmark_closure/threshold/endpoint_construction_v2/verify_hybrid_coefficients.py
