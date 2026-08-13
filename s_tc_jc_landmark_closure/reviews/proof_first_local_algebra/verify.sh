#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../.."
python3 reviews/proof_first_local_algebra/verify_completed.py
