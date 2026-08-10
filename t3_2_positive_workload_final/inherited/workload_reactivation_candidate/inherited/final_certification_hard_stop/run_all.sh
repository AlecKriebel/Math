#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
python -m pytest -q
g++ -O2 -std=c++20 -Wall -Wextra -pedantic src/exhaustive_two_active_atlas.cpp -o /tmp/t3_2_atlas_check
/tmp/t3_2_atlas_check > /tmp/t3_2_atlas_cpp.json
cmp /tmp/t3_2_atlas_cpp.json certificates/atlas_cpp_replay.json
python src/atlas_independent_verifier.py > /tmp/t3_2_atlas_python.json
cmp /tmp/t3_2_atlas_python.json certificates/atlas_python_replay.json
python src/cleanroom_atlas_check.py > /tmp/t3_2_atlas_cleanroom.out
cmp /tmp/t3_2_atlas_cleanroom.out certificates/atlas_cleanroom_replay.out
python src/conditional_activation_counterexample.py
python src/independent_verifier.py > /tmp/t3_2_independent.json
cmp /tmp/t3_2_independent.json certificates/independent_verification.json
sha256sum -c certificates/MANIFEST.sha256
echo 'ALL CERTIFIED PARTIAL CHECKS PASSED; T3-2 IS NOT CERTIFIED'
