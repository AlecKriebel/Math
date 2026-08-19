#!/usr/bin/env bash
set -euo pipefail

review_dir="$(cd "$(dirname "$0")" && pwd)"
repo_dir="$(cd "$review_dir/../.." && pwd)"
cd "$repo_dir"

/usr/bin/python3 reviews/final_hard_cover_cleanroom/audit_candidate_stream.py \
  --relations primary/certificates/hard_cover_n4_schema3_theta2_full.jsonl.gz \
  --graphs primary/certificates/hard_cover_graphs_n4_schema3_theta2_full.jsonl.gz \
  --roots primary/certificates/hard_cover_root_cases_n4_schema3_theta2_full.jsonl.gz \
  --polynomials primary/certificates/hard_cover_polynomials_n4_schema3_theta2_full.jsonl.gz \
  --summary primary/certificates/hard_cover_schema3_theta2_full_summary.json \
  --expected-summary-sha256 dde4040865d055427e85c83e7dfe18bebce1f6bfb737a54032be9e3f3827b824 \
  --invariant-metadata primary/certificates/invariant_multihomogeneity.json \
  --family-tag n4_minimum \
  --output reviews/final_hard_cover_cleanroom/certificates/schema3_n4_theta2_full_audit.json \
  --terminal-records-output reviews/final_hard_cover_cleanroom/certificates/schema3_n4_theta2_terminal_records.jsonl.gz

/usr/bin/python3 reviews/final_hard_cover_cleanroom/mutation_schema3_stream.py
/usr/bin/python3 reviews/final_hard_cover_cleanroom/verify_schema3_n4_certificates.py
