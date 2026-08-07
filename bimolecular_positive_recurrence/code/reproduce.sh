#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
python -m pip install -e . --disable-pip-version-check >/dev/null
python -m unittest discover -s tests -v
python -m bimolecular_pr.verification --root "$ROOT" --output .verification_run_1.json
python -m bimolecular_pr.verification --root "$ROOT" --output .verification_run_2.json
cmp .verification_run_1.json .verification_run_2.json
cp .verification_run_1.json verification_report.json
sha256sum verification_report.json
rm -f .verification_run_1.json .verification_run_2.json
