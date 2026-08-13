#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
source "$HERE/bootstrap.sh"
cd "$STC_JC_PROJECT"

bash reproducibility/verify_quick.sh
"$STC_JC_PYTHON" reviews/root_probe/verify_all.py
bash reviews/global_bridge/verify_all.sh --with-upstream-replay
bash reviews/bounded_directed_relation_cleanroom/verify_n3.sh
bash reviews/theta2_signature_gate/verify.sh
bash reviews/base_gate_adversarial_referee_n3/verify_all.sh
bash reviews/base_gate_adversarial_referee/verify_all.sh
bash reviews/arbitrary_subdivision_promotion_referee/verify_all.sh
bash reviews/compact_probe_format/final_n3_cleanroom/verify_full.sh
bash reviews/compact_probe_format/final_n4_cleanroom/verify_full.sh

echo "VERIFIED: full Outcome-P release gates"
