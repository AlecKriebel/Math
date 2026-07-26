#!/bin/sh
set -eu

PYTHON=/Users/alec/Documents/Math/.venv/bin/python
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
OUTPUT=$("$PYTHON" "$HERE/verify_full_e6_elimination.py")

printf '%s\n' "$OUTPUT"
printf '%s\n' "$OUTPUT" | grep -Fqx \
  "D4_DN2C_E7_KERNEL_PASS_RANKS_2_3_4 FREE_BINARY_11_CONTACT_6"
printf '%s\n' "$OUTPUT" | grep -Fqx \
  "D4_DN2C_CONTACT_RADICAL_PASS_TWO_PLANES_OVER_Q_SQRT_MINUS_2"
printf '%s\n' "$OUTPUT" | grep -Fqx \
  "D4_DN2C_FULL_E6_ATLAS_PASS PLANE_RANK7_INTERSECTION_RANK6_ORIGIN_RANK5 ALL_18_LOWER"
printf '%s\n' "D4_DN2C_FULL_REBUILD_STRICT_PASS"
