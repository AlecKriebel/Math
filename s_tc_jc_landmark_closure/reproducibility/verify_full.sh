#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
source "$HERE/bootstrap.sh"
cd "$STC_JC_PROJECT"

bash reproducibility/verify_quick.sh
"$STC_JC_PYTHON" reviews/root_probe/verify_active_structural.py
bash reviews/global_bridge/verify_all.sh --with-upstream-replay
bash reviews/n3_universe_generator/verify.sh
bash reviews/bounded_directed_relation_cleanroom/verify_n3.sh
bash reviews/theta2_signature_gate/verify.sh
bash reviews/base_gate_adversarial_referee_n3/verify_all.sh
bash reviews/base_gate_adversarial_referee/verify_all.sh
bash reviews/direct_anchor_probe_closure/verify.sh
PYTHON_BIN="$STC_JC_PYTHON" bash reviews/compact_probe_clean_clone_gate/verify_full.sh

echo "VERIFIED: full Outcome-P release gates"
