#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
PUB="$ROOT/reproducibility/publication"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

python3 "$ROOT/reproducibility/verify_integrity.py"
python3 "$PUB/src/verify_multitriangle_exclusion.py"
g++ -O3 -std=c++17 "$PUB/review/review_multitriangle_exclusion.cpp" -o "$TMP/review_multitriangle_exclusion"
"$TMP/review_multitriangle_exclusion"
python3 "$ROOT/reproducibility/verify_base_release_attestation.py"
python3 "$PUB/src/regenerate_nonroot_topology_atlases.py"
python3 "$PUB/src/regenerate_nonroot_algebra.py" --k 5
python3 "$PUB/src/regenerate_nonroot_algebra.py" --k 6
for k in 3 4 5 6; do python3 "$PUB/src/regenerate_cycle_algebra.py" --k "$k"; done

g++ -O3 -std=c++17 "$PUB/src/regenerate_directed_pair_universe.cpp" -o "$TMP/regenerate_directed_pair_universe"
for k in 5 6; do
  if [ "$k" = 5 ]; then w=360; else w=840; fi
  "$TMP/regenerate_directed_pair_universe" \
    "$PUB/certificates/theta_k${k}_strong_signatures.bin" \
    "$PUB/certificates/theta_k${k}_weak_signatures.bin" \
    "$w" "$k" "$PUB/certificates/theta_k${k}_directed_pairs.tsv"
done

g++ -O3 -std=c++17 "$PUB/src/regenerate_signature_relation.cpp" -o "$TMP/regenerate_signature_relation"
"$TMP/regenerate_signature_relation" \
  "$PUB/certificates/cycle_k5_strong_signatures.bin" \
  "$PUB/certificates/cycle_k5_weak_signatures.bin" 360 \
  cycle_k5_to_cycle_k5 \
  "$PUB/certificates/cycle_k5_to_cycle_k5_pairs.tsv" 300 300 0 \
  "$PUB/certificates/cycle_k5_to_cycle_k5_summary.json"
"$TMP/regenerate_signature_relation" \
  "$PUB/certificates/cycle_k6_strong_signatures.bin" \
  "$PUB/certificates/cycle_k6_weak_signatures.bin" 840 \
  cycle_k6_to_cycle_k6 \
  "$PUB/certificates/cycle_k6_to_cycle_k6_pairs.tsv" 2160 2160 0 \
  "$PUB/certificates/cycle_k6_to_cycle_k6_summary.json"
"$TMP/regenerate_signature_relation" \
  "$PUB/certificates/theta_k5_strong_signatures.bin" \
  "$PUB/certificates/cycle_k5_weak_signatures.bin" 360 \
  theta_k5_to_cycle_k5 \
  "$PUB/certificates/theta_k5_to_cycle_k5_pairs.tsv" 0 0 0 \
  "$PUB/certificates/theta_k5_to_cycle_k5_summary.json"
"$TMP/regenerate_signature_relation" \
  "$PUB/certificates/theta_k6_strong_signatures.bin" \
  "$PUB/certificates/cycle_k6_weak_signatures.bin" 840 \
  theta_k6_to_cycle_k6 \
  "$PUB/certificates/theta_k6_to_cycle_k6_pairs.tsv" 0 0 0 \
  "$PUB/certificates/theta_k6_to_cycle_k6_summary.json"
"$TMP/regenerate_signature_relation" \
  "$PUB/certificates/cycle_k5_strong_signatures.bin" \
  "$PUB/certificates/theta_k5_weak_signatures.bin" 360 \
  cycle_k5_to_theta_k5 \
  "$PUB/certificates/cycle_k5_to_theta_k5_pairs.tsv" 21780 300 21480 \
  "$PUB/certificates/cycle_k5_to_theta_k5_summary.json"
"$TMP/regenerate_signature_relation" \
  "$PUB/certificates/cycle_k6_strong_signatures.bin" \
  "$PUB/certificates/theta_k6_weak_signatures.bin" 840 \
  cycle_k6_to_theta_k6 \
  "$PUB/certificates/cycle_k6_to_theta_k6_pairs.tsv" 246240 2160 244080 \
  "$PUB/certificates/cycle_k6_to_theta_k6_summary.json"

g++ -O3 -std=c++17 "$PUB/review/review_directed_pair_universe.cpp" -o "$TMP/review_directed_pair_universe"
for k in 5 6; do
  if [ "$k" = 5 ]; then w=360; else w=840; fi
  "$TMP/review_directed_pair_universe" \
    "$PUB/certificates/theta_k${k}_strong_signatures.bin" \
    "$PUB/certificates/theta_k${k}_weak_signatures.bin" \
    "$w" \
    "$PUB/certificates/theta_k${k}_directed_pairs.tsv" \
    "$PUB/certificates/theta_k${k}_directed_pairs_review.tsv"
done

python3 "$PUB/review/review_publication_release.py"
bash "$ROOT/reproducibility/build_paper.sh"
python3 "$ROOT/reproducibility/build_component_archives.py"
python3 "$PUB/review/review_submission_package.py"
python3 "$ROOT/reproducibility/verify_integrity.py"
echo 'AUTHOR-READY FULL INDEPENDENT VERIFICATION PASSED'
