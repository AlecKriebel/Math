#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
PUB="$ROOT/reproducibility/publication"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

python3 "$ROOT/reproducibility/verify_integrity.py"
# Fresh independent replays of every dependency introduced by the all-level-2
# strengthening.
python3 "$PUB/src/verify_multitriangle_exclusion.py"
g++ -O3 -std=c++17 "$PUB/review/review_multitriangle_exclusion.cpp" -o "$TMP/review_multitriangle_exclusion"
"$TMP/review_multitriangle_exclusion"
# The unchanged statistical, atlas, seven-port, root, cut, and sharpness base
# is byte-attested against its preserved successful clean full-adversarial
# replay.  Use verify_regenerate_all.sh for a complete from-scratch rerun of
# those unchanged high-cost algebra streams.
python3 "$ROOT/reproducibility/verify_base_release_attestation.py"
python3 "$PUB/review/review_publication_release.py"
bash "$ROOT/reproducibility/build_paper.sh"
python3 "$ROOT/reproducibility/build_component_archives.py"
python3 "$PUB/review/review_submission_package.py"
python3 "$ROOT/reproducibility/verify_integrity.py"
echo 'AUTHOR-READY FULL INDEPENDENT VERIFICATION PASSED'
