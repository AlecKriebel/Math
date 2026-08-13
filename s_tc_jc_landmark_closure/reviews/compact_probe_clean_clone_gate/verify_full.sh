#!/bin/sh
set -eu
PYTHON_BIN=${PYTHON_BIN:-python3}
"$PYTHON_BIN" reviews/compact_probe_clean_clone_gate/semantic_gate.py \
  --family all \
  --output reviews/compact_probe_clean_clone_gate/certificates/compact_only_semantic_replay.json
"$PYTHON_BIN" reviews/compact_probe_clean_clone_gate/mutation_tests.py
"$PYTHON_BIN" reviews/compact_probe_clean_clone_gate/verify_tracked_inputs.py
"$PYTHON_BIN" reviews/compact_probe_clean_clone_gate/build_manifest.py
"$PYTHON_BIN" reviews/compact_probe_clean_clone_gate/verify_quick.py
