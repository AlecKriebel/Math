#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
PROJECT="$(cd "$HERE/../.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"

cd "$PROJECT"
export PYTHONHASHSEED=0
"$PYTHON_BIN" reviews/theta2_signature_gate/verify_gate.py
"$PYTHON_BIN" reviews/theta2_signature_gate/canonicalize_relations.py
"$PYTHON_BIN" reviews/theta2_signature_gate/verify_manifest.py

