#!/bin/sh
set -eu
PYTHON_BIN=${PYTHON_BIN:-python3}
"$PYTHON_BIN" reviews/compact_probe_clean_clone_gate/verify_tracked_inputs.py
"$PYTHON_BIN" reviews/compact_probe_clean_clone_gate/verify_quick.py
