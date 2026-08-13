#!/usr/bin/env bash
set -euo pipefail

# The active proof has a finite, theorem-derived support universe.  This
# command regenerates every load-bearing normalized relation/sign/probe record
# from its committed primitive graph inputs.  It deliberately does not launch
# any broader topology census.

HERE="$(cd "$(dirname "$0")" && pwd)"
source "$HERE/bootstrap.sh"
cd "$STC_JC_PROJECT"

bash reviews/n3_universe_generator/verify.sh
bash reviews/bounded_directed_relation_cleanroom/verify_n3.sh
bash reviews/theta2_signature_gate/verify.sh
bash reviews/base_gate_adversarial_referee_n3/verify_all.sh
bash reviews/base_gate_adversarial_referee/verify_all.sh
bash reviews/direct_anchor_probe_closure/verify_regenerate.sh
bash reviews/compact_probe_format/final_n3_cleanroom/verify_full.sh
bash reviews/compact_probe_format/final_n4_cleanroom/verify_full.sh
bash reviews/global_bridge/verify_all.sh --with-upstream-replay
bash reviews/triangle_redirection_cleanroom/verify_all.sh
"$STC_JC_PYTHON" ../s_tc_jc_sharp_boundary/reproducibility/verify_release.py
"$STC_JC_PYTHON" reproducibility/verify_active_release.py

echo "VERIFIED: all theorem-forced bounded records regenerated"
