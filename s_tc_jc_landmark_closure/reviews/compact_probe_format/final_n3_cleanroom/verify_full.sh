#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
PROJECT="$(cd "$HERE/../../.." && pwd)"
PYTHON="$PROJECT/../.venv/bin/python"
CERT="$PROJECT/primary/certificates"

cd "$PROJECT"
export PYTHONHASHSEED=0

# Resource-safety invariant: the four expensive shard replays are deliberately
# serial.  Do not parallelize this loop on the 16 GB M1 audit host.
for shard in s0 s1 s2 s3; do
  "$PYTHON" "$HERE/audit_final_n3.py" --shard "$shard"
done

"$PYTHON" "$HERE/reproduce_first_mismatch.py"
"$PYTHON" "$HERE/mutation_tests.py"

"$PYTHON" "$PROJECT/primary/merge_compact_probe_shards.py" \
  --summary "$CERT/compact_probe_schema3_n3_compact_s0_summary.json" \
  --summary "$CERT/compact_probe_schema3_n3_compact_s1_summary.json" \
  --summary "$CERT/compact_probe_schema3_n3_compact_s2_summary.json" \
  --summary "$CERT/compact_probe_schema3_n3_compact_s3_summary.json" \
  --primary-replay "$CERT/compact_probe_schema3_n3_compact_s0_replay.json" \
  --primary-replay "$CERT/compact_probe_schema3_n3_compact_s1_replay.json" \
  --primary-replay "$CERT/compact_probe_schema3_n3_compact_s2_replay.json" \
  --primary-replay "$CERT/compact_probe_schema3_n3_compact_s3_replay.json" \
  --independent-replay "$HERE/certificates/independent_s0.json" \
  --independent-replay "$HERE/certificates/independent_s1.json" \
  --independent-replay "$HERE/certificates/independent_s2.json" \
  --independent-replay "$HERE/certificates/independent_s3.json" \
  --output "$HERE/certificates/hardened_merge_manifest.json"

"$PYTHON" "$HERE/merger_mutations.py"
"$PYTHON" "$HERE/adversarial_release_review.py"
"$PYTHON" "$HERE/finalize_certificate.py"
"$PYTHON" "$HERE/build_manifest.py"
