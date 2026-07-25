#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
RUNG_DIR=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)

cd "$RUNG_DIR"

/usr/bin/python3 taxonomy_freeze/verify_bridge_q2_e3_a1_b1_d1_n1_v1.py

/usr/bin/python3 verify_fixed_cubic_line_sympy.py
./verify_fixed_cubic_line_pari_strict.sh

/usr/bin/python3 -u verify_binary_fixed_cubic_complete.py
gp -q verify_binary_fixed_cubic_complete_pari.gp
/usr/bin/python3 -u audit_binary_fixed_cubic_hostile/audit_orbits_lower_exact.py
/usr/bin/python3 -u audit_binary_fixed_cubic_hostile/audit_exceptional_branches_exact.py
./audit_binary_fixed_cubic_hostile/test_fail_closed.sh

printf '%s\n' \
  'PASS: full fixed-cubic-line bridge candidate and legacy exact replay'
