#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
"$ROOT/quick_check.sh"
python3 "$ROOT/code/extract_sources.py" | tee "$ROOT/logs/full_extract_sources.txt"
python3 "$ROOT/code/build_dependency_crosswalk.py" | tee "$ROOT/logs/full_crosswalk.txt"
python3 "$ROOT/code/discover_collision_graphs.py" | tee "$ROOT/logs/full_graph_discovery.txt"
python3 "$ROOT/code/extract_membership_evidence.py" | tee "$ROOT/logs/full_membership_evidence.txt"
python3 "$ROOT/code/scan_collision_certificates.py" | tee "$ROOT/logs/full_certificate_scan.txt"
python3 "$ROOT/code/replay_supplied_k2p.py" | tee "$ROOT/logs/full_supplied_replay.txt" || true
python3 "$ROOT/code/build_checkpoint.py" | tee "$ROOT/logs/full_build_checkpoint.txt"
python3 "$ROOT/code/make_manifest.py" | tee "$ROOT/logs/full_manifest.txt"
echo 'full check complete; inspect supplied replay statuses separately'
