#!/bin/sh
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/../../../.." && pwd)
cd "$root"
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  universal_simultaneous_amplification/phase4_landmark_closure/threshold/dilute_pair_leaf_hybrid/verify_leading_algebra.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  universal_simultaneous_amplification/phase4_landmark_closure/threshold/endpoint_construction_v2/verify_hybrid_lumping.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  universal_simultaneous_amplification/phase4_landmark_closure/threshold/endpoint_construction_v2/verify_hybrid_coefficients.py
