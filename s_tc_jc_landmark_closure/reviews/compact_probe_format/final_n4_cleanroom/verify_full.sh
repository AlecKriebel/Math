#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../../.."
PYTHON="${PYTHON:-../.venv/bin/python}"
REVIEW="reviews/compact_probe_format/final_n4_cleanroom"
CERT="$REVIEW/certificates"
PRIMARY_CERT="primary/certificates"

for shard in s0 s1 s2 s3; do
  "$PYTHON" "$REVIEW/audit_final_n4.py" --shard "$shard"
done

"$PYTHON" "$REVIEW/mutation_tests.py"

merge_args=()
for shard in s0 s1 s2 s3; do
  merge_args+=(--summary "$PRIMARY_CERT/compact_probe_theta2_compact_n4_${shard}_summary.json")
done
for shard in s0 s1 s2 s3; do
  merge_args+=(--primary-replay "$PRIMARY_CERT/compact_probe_theta2_compact_n4_${shard}_replay.json")
done
for shard in s0 s1 s2 s3; do
  merge_args+=(--independent-replay "$CERT/independent_${shard}.json")
done
"$PYTHON" primary/merge_compact_probe_shards.py "${merge_args[@]}" \
  --output "$CERT/hardened_merge_manifest.json"

"$PYTHON" "$REVIEW/merger_mutations.py"
"$PYTHON" "$REVIEW/finalize_certificate.py"
