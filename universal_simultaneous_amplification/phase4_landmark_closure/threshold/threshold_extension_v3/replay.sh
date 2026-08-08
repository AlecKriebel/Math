#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../../../.." && pwd)"

PYTHONDONTWRITEBYTECODE=1 "$ROOT/.venv/bin/python" "$HERE/verify_pair_doublet_no_go.py"
PYTHONDONTWRITEBYTECODE=1 "$ROOT/.venv/bin/python" "$HERE/verify_doublet_event_rates.py"
(cd "$HERE" && shasum -a 256 -c MANIFEST.sha256)
