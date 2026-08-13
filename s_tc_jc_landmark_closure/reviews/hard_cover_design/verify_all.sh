#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
python3 structural_audit.py
python3 make_manifest.py --check
