#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PYTHON=${PYTHON:-"$ROOT/../../../.venv/bin/python"}

"$PYTHON" "$ROOT/verify_separated_pair_first_event.py"
"$PYTHON" "$ROOT/verify_star_reservoir_diode.py"
