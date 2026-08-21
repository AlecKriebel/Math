#!/bin/sh
set -eu

probe_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
keller_python=${KELLER_PROBE_PYTHON:-/Users/alec/Documents/Math/.venv/bin/python}
component_output=$(mktemp)
intersection_output=$(mktemp)
trap 'rm -f "$component_output" "$intersection_output"' EXIT HUP INT TERM

cd "$probe_dir"
"$keller_python" verify_l07_representative_components.py | tee "$component_output"
grep -Fx "L07_REPRESENTATIVE_COMPONENTS_ALL_PASS" "$component_output" >/dev/null

"$keller_python" reduce_power_intersection_e4.py | tee "$intersection_output"
grep -Fx "POWER_INTERSECTION_COMPLETE_PASS_DETL_ZERO" "$intersection_output" >/dev/null

echo "DELTA_GE3_SURVIVOR_PROBE_STRICT_PASS"
