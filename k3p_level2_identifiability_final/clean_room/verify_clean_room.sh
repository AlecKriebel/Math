#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PROJECT_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
PYTHON_BIN=${K3P_CLEANROOM_PYTHON:-"$PROJECT_DIR/.venv/bin/python"}

export PYTHONDONTWRITEBYTECODE=1

cd "$PROJECT_DIR"

/usr/bin/time -p "$PYTHON_BIN" clean_room/replay_historical_failure.py
/usr/bin/time -p "$PYTHON_BIN" clean_room/verify_h21_transport_and_fourteen_orbits.py
/usr/bin/time -p "$PYTHON_BIN" clean_room/test_h21_transport_regression.py
/usr/bin/time -p "$PYTHON_BIN" clean_room/test_clean_room_mutations.py

OPTIMIZED_OUTPUT=$(mktemp -t k3p-cleanroom-optimized.XXXXXX)
trap 'rm -f "$OPTIMIZED_OUTPUT"' EXIT HUP INT TERM
if "$PYTHON_BIN" -O clean_room/verify_h21_transport_and_fourteen_orbits.py \
        >"$OPTIMIZED_OUTPUT" 2>&1; then
    echo "FAIL optimized Python unexpectedly accepted the certification verifier" >&2
    exit 1
fi
if ! /usr/bin/grep -q "certification verifier refuses optimized Python" \
        "$OPTIMIZED_OUTPUT"; then
    echo "FAIL optimized Python was rejected for an unexpected reason" >&2
    /bin/cat "$OPTIMIZED_OUTPUT" >&2
    exit 1
fi

echo "CLEAN_ROOM_FULL_GATE_PASS"
