#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1

review_dir="$(cd "$(dirname "$0")" && pwd)"
landmark_dir="$(cd "$review_dir/../.." && pwd)"
cd "$landmark_dir"

python3 reviews/arbitrary_subdivision_promotion_referee/audit_promotion.py \
  --output reviews/arbitrary_subdivision_promotion_referee/certificates/promotion_audit_certificate.json \
  >/tmp/stc_jc_arbitrary_subdivision_promotion_audit.json

python3 reviews/arbitrary_subdivision_promotion_referee/mutation_tests.py \
  --output reviews/arbitrary_subdivision_promotion_referee/certificates/mutation_certificate.json \
  >/tmp/stc_jc_arbitrary_subdivision_promotion_mutations.json

python3 reviews/arbitrary_subdivision_promotion_referee/build_manifest.py

python3 - <<'PY'
import json
from pathlib import Path

root = Path("reviews/arbitrary_subdivision_promotion_referee")
audit = json.loads((root / "certificates/promotion_audit_certificate.json").read_text())
mutations = json.loads((root / "certificates/mutation_certificate.json").read_text())
assert audit["status"] == "VERIFIED_AFTER_CORRECTION"
assert audit["aggregate"]["exact_attained_probe_tensor_port_bound"] == 10
assert audit["aggregate"]["probe_relations"] == 269730
assert mutations["status"] == "VERIFIED"
assert mutations["mutations_attempted"] == mutations["mutations_rejected"] == 16
print("VERIFIED_AFTER_CORRECTION: arbitrary-subdivision promotion; exact bound 10; 16/16 mutations rejected")
PY
