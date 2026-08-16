#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
source "$HERE/bootstrap.sh"
cd "$STC_JC_PROJECT"

"$STC_JC_PYTHON" reproducibility/verify_active_release.py
"$STC_JC_PYTHON" reproducibility/verify_fixed_graph_scope.py
"$STC_JC_PYTHON" reviews/v1_1_proof_hardening/verify_endpoint_and_analytic_regressions.py
"$STC_JC_PYTHON" reviews/v1_1_proof_hardening/verify_noncut_compression.py
bash reviews/final_standard_convention/verify_all.sh
bash reviews/triangle_redirection_cleanroom/verify_all.sh
bash reviews/global_bridge/verify_all.sh
"$STC_JC_PYTHON" reviews/n3_universe_generator/verify_manifest.py
"$STC_JC_PYTHON" reviews/theta2_signature_gate/verify_manifest.py
(cd reviews/direct_anchor_probe_closure && shasum -a 256 -c MANIFEST.sha256)
PYTHON_BIN="$STC_JC_PYTHON" bash reviews/compact_probe_clean_clone_gate/verify_quick.sh
"$STC_JC_PYTHON" s_tc_jc_sharp_boundary/reproducibility/verify_release.py
"$STC_JC_PYTHON" omega_audit/independent/verify_omega_release.py
"$STC_JC_PYTHON" omega_audit/independent/verify_omega_rank_readability.py

echo "VERIFIED: quick Outcome-A bioRxiv release gates"
