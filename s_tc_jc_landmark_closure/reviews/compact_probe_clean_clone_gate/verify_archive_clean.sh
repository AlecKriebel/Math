#!/bin/sh
set -eu
PYTHON_BIN=${PYTHON_BIN:-python3}
REPO_ROOT=$(git rev-parse --show-toplevel)
TMP_ROOT=$(mktemp -d "${TMPDIR:-/tmp}/compact-probe-archive.XXXXXX")
trap 'rm -rf "$TMP_ROOT"' EXIT HUP INT TERM
git -C "$REPO_ROOT" archive HEAD | tar -x -C "$TMP_ROOT"
cd "$TMP_ROOT/s_tc_jc_landmark_closure"
PYTHON_BIN="$PYTHON_BIN" bash reviews/compact_probe_clean_clone_gate/verify_quick.sh
PYTHON_BIN="$PYTHON_BIN" bash reviews/compact_probe_clean_clone_gate/verify_full.sh
