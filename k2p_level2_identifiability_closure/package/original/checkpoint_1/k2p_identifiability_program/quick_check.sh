#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$ROOT/logs"
python3 "$ROOT/code/verify_k2p_domain.py" | tee "$ROOT/logs/quick_domain.txt"
python3 "$ROOT/code/verify_k2p_bridge_fibre.py" | tee "$ROOT/logs/quick_bridge.txt"
python3 "$ROOT/code/run_cleanroom_tests.py" | tee "$ROOT/logs/quick_cleanroom.txt"
python3 "$ROOT/code/run_mutation_tests.py" | tee "$ROOT/logs/quick_mutations.txt"
echo 'quick check PASS'
