#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-$ROOT/.venv/bin/python}"
if [[ ! -x "$PYTHON_BIN" ]]; then
  PYTHON_BIN="python3"
fi
WORK="$(mktemp -d "${TMPDIR:-/tmp}/k3p-cut-topology.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT

cd "$ROOT"
"$PYTHON_BIN" cut_recovery/strong_crossbridge/topology_regeneration/generate_cut_topology.py \
  --output "$WORK/fresh_cut_topology.json"
"$PYTHON_BIN" cut_recovery/strong_crossbridge/topology_regeneration/verify_cut_topology_regeneration.py \
  --candidate "$WORK/fresh_cut_topology.json" \
  --report "$WORK/CUT_TOPOLOGY_REGENERATION_REPORT.json"
"$PYTHON_BIN" cut_recovery/strong_crossbridge/topology_regeneration/test_cut_topology_regeneration_mutations.py
echo CUT_TOPOLOGY_GRAPH_REGENERATION_SUITE_PASS
