#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PYTHON=${PYTHON:-"$ROOT/../../../.venv/bin/python"}

"$PYTHON" "$ROOT/verify_separated_pair_first_event.py"
"$PYTHON" "$ROOT/verify_star_reservoir_diode.py"
"$PYTHON" "$ROOT/verify_two_channel_entrance.py"
"$PYTHON" "$ROOT/verify_dense_pair_relay.py"
"$PYTHON" "$ROOT/verify_dense_heterogeneous_pair_relay.py"
"$PYTHON" "$ROOT/verify_endpoint_integrated_target.py"
"$PYTHON" "$ROOT/verify_bd_catalyst_ray_target.py"
"$PYTHON" "$ROOT/verify_rank_one_clone_catalyst.py"
"$PYTHON" "$ROOT/verify_regular_adjoint_catalyst_tangent.py"
