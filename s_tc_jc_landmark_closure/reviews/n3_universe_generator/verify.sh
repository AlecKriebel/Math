#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
PROJECT="$(cd "$HERE/../.." && pwd)"
PYTHON="${STC_JC_PYTHON:-python3}"

cd "$PROJECT"
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  "$PYTHON" reviews/n3_universe_generator/generate_universe.py
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  "$PYTHON" reviews/n3_universe_generator/verify_manifest.py

echo "VERIFIED: independently generated complete n3 decorated relation universe"
