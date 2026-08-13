#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
PROJECT="$(cd "$HERE/../.." && pwd)"
PY_EXACT="${PY_EXACT:-/usr/bin/python3}"

cd "$PROJECT"

"$PY_EXACT" "$HERE/audit_quarantined_schema2.py"
"$PY_EXACT" "$HERE/audit_candidate_full.py" \
  --n 4 \
  --tag schema3_theta2_full \
  --source-core-id theta-2 \
  --source-extra-count 0 \
  --summary primary/certificates/hard_cover_schema3_theta2_full_summary.json \
  --output "$HERE/schema3_theta2_full_audit_certificate.json"
"$PY_EXACT" "$HERE/mutation_suite.py" \
  --n 4 \
  --tag schema3_theta2_full \
  --output "$HERE/schema3_theta2_mutation_transcript.json"
"$PY_EXACT" "$HERE/audit_probe_streams.py"
"$PY_EXACT" "$HERE/mutate_probe_streams.py"
"$PY_EXACT" "$HERE/audit_probe_closure.py" \
  --n 4 \
  --tag schema3_theta2_full \
  --output "$HERE/schema3_theta2_probe_closure_certificate.json"
"$PY_EXACT" "$HERE/audit_n4_coverage_gap.py" \
  --output "$HERE/n4_coverage_gap_certificate.json"
"$PY_EXACT" "$HERE/audit_bounded_pair_gap.py" \
  --output "$HERE/bounded_pair_gap_certificate.json"

echo "Independent theta-2 replay complete.  Read REVIEW.md for the distinction between VERIFIED component gates and UNRESOLVED global completeness."
