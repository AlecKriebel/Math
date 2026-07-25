#!/bin/sh
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
rung2=$(CDPATH= cd -- "$here/.." && pwd)
python_bin=${PYTHON_BIN:-/usr/bin/python3}
work_tmp=$(mktemp -d "${TMPDIR:-/tmp}/fixed-linear-all-strict.XXXXXX")
trap 'rm -rf "$work_tmp"' EXIT HUP INT TERM
suite_number=0

run_suite() {
    suite_number=$((suite_number + 1))
    suite_label=$1
    shift
    suite_log="$work_tmp/suite-$suite_number.log"
    if ! "$@" >"$suite_log" 2>&1; then
        printf '%s\n' "FAIL: $suite_label" >&2
        sed -n '1,240p' "$suite_log" >&2
        exit 1
    fi
    printf '%s\n' "PASS suite $suite_number: $suite_label"
    sed -n '1,240p' "$suite_log"
}

run_exact() {
    suite_label=$1
    expected_output=$2
    shift 2
    suite_number=$((suite_number + 1))
    suite_log="$work_tmp/suite-$suite_number.log"
    if ! "$@" >"$suite_log" 2>&1; then
        printf '%s\n' "FAIL: $suite_label" >&2
        cat "$suite_log" >&2
        exit 1
    fi
    actual_output=$(cat "$suite_log")
    if [ "$actual_output" != "$expected_output" ]; then
        printf '%s\n' "FAIL: $suite_label emitted an unexpected sentinel" >&2
        cat "$suite_log" >&2
        exit 1
    fi
    printf '%s\n' "PASS suite $suite_number: $suite_label"
    printf '%s\n' "$actual_output"
}

# Horizontal theorem: supplied exact reconstructions and an independent
# finite-field hostile reconstruction.
run_exact \
    "horizontal SymPy reconstruction" \
    "horizontal fixed-linear cubic-pencil SymPy checks passed" \
    "$python_bin" "$here/verify_horizontal_fixed_linear_cubic_pencil_sympy.py"
run_suite \
    "horizontal PARI/GP strict reconstruction" \
    "$here/verify_horizontal_fixed_linear_cubic_pencil_pari_strict.sh"
run_suite \
    "horizontal dependency-free hostile reconstruction" \
    "$here/audit_hostile/audit_finite_field_strict.sh"

# Vertical multiplicity and companion normalization.
run_exact \
    "vertical top SymPy reconstruction" \
    "vertical fixed-linear cubic-pencil SymPy checks passed" \
    "$python_bin" "$here/vertical_locus/verify_vertical_locus_sympy.py"
run_suite \
    "vertical top PARI/GP strict reconstruction" \
    "$here/vertical_locus/verify_vertical_locus_pari_strict.sh"
run_suite \
    "vertical top hostile reconstruction and fault injection" \
    "$here/vertical_locus/audit_vertical_hostile/verify_strict_and_faults.sh"

# Nonvertical companion.
run_suite \
    "nonvertical nontriple supplied strict suite" \
    "$here/vertical_locus/verify_nonvertical_nontriple_e4_strict.sh"
run_suite \
    "nonvertical triple-root supplied strict suite" \
    "$here/vertical_locus/verify_nonvertical_triple_root_strict.sh"
run_suite \
    "complete nonvertical independent hostile reconstruction" \
    "$here/vertical_locus/audit_nonvertical_companion/verify_strict.sh"

# Vertical companion, nonzero companion parameter.
run_suite \
    "zero-ell nontriple supplied strict suite" \
    "$here/vertical_locus/verify_vertical_ell_zero_nontriple_strict.sh"
run_suite \
    "zero-ell nontriple hostile reconstruction" \
    "$here/vertical_locus/audit_vertical_ell_zero_nontriple/verify_strict.sh"
run_suite \
    "nonzero-ell nontriple supplied strict suite" \
    "$here/vertical_locus/verify_vertical_nonzero_ell_nontriple_strict.sh"
run_suite \
    "nonzero-ell nontriple hostile reconstruction" \
    "$here/vertical_locus/audit_vertical_nonzero_ell_nontriple/verify_strict.sh"
run_suite \
    "triple-root gamma-nonzero supplied strict suite" \
    "$here/vertical_locus/verify_vertical_triple_gamma_nonzero_strict.sh"
run_suite \
    "triple-root gamma-nonzero hostile reconstruction" \
    "$here/vertical_locus/audit_vertical_triple_gamma_nonzero/verify_strict.sh"
run_suite \
    "triple-root gamma-zero reduction supplied strict suite" \
    "$here/vertical_locus/verify_vertical_triple_gamma0_reduction_strict.sh"
run_suite \
    "triple-root gamma-zero reduction hostile reconstruction" \
    "$here/vertical_locus/audit_vertical_triple_gamma0_reduction/verify_strict.sh"
run_suite \
    "triple-root gamma=ell=0 supplied strict suite" \
    "$here/vertical_locus/verify_vertical_triple_gamma0_ell0_strict.sh"
run_suite \
    "triple-root gamma=ell=0 hostile reconstruction" \
    "$here/vertical_locus/audit_vertical_triple_gamma0_ell0/verify_strict.sh"

# Vertical companion, zero companion parameter.
run_suite \
    "zero-parameter W0=0 supplied strict suite" \
    "$here/vertical_locus/verify_vertical_a0_w0zero_strict.sh"
run_suite \
    "zero-parameter W0=0 hostile reconstruction" \
    "$here/vertical_locus/audit_vertical_a0_w0_zero/verify_strict.sh"
run_suite \
    "zero-parameter W0!=0 dual exact suite" \
    "$here/vertical_locus/a0_w0_nonzero_attack/verify_strict.sh"
run_suite \
    "zero-parameter W0!=0 independent hostile reconstruction" \
    "$here/vertical_locus/audit_a0_w0_nonzero/verify_strict.sh"

# Complete internal route ledger.
run_suite \
    "complete vertical coverage audit and mutations" \
    "$here/vertical_locus/audit_complete_vertical_coverage/verify_strict.sh"

# Standalone quadratic-component regression. The literature theorem remains
# a cited black box and is not claimed to be computer-proved here.
run_exact \
    "quadratic-component exact regression" \
    "PASS: exact quadratic-coordinate, degree, and fibre identities verified" \
    "$python_bin" \
    "$rung2/audit_quadratic_component_exit/verify_quadratic_component_exit_exact.py"

# The final wrapper pins the frozen inputs, checks 45 pivots, 48 route atoms,
# all 15 terminals, semantic truncations, deliberate route mutations, the
# W0!=0 hostile suite, and the quadratic-component regression. It must be
# last, and its final sentinel is required exactly.
bridge_runner="$rung2/taxonomy_freeze/audit_bridge_q2_e1_a3_b1_d1_n1_v1/verify_strict.sh"
suite_number=$((suite_number + 1))
bridge_log="$work_tmp/suite-$suite_number.log"
if ! "$bridge_runner" >"$bridge_log" 2>&1; then
    printf '%s\n' "FAIL: final frozen bridge strict wrapper" >&2
    cat "$bridge_log" >&2
    exit 1
fi
cat "$bridge_log"
if ! tail -n 1 "$bridge_log" |
    grep -Fqx "BRIDGE_Q2_E1_A3_B1_D1_N1_STRICT_PASS_72C8E1"
then
    printf '%s\n' "FAIL: final frozen bridge sentinel missing" >&2
    exit 1
fi
printf '%s\n' "PASS suite $suite_number: final frozen bridge strict wrapper"

printf '%s\n' "FIXED_LINEAR_CUBIC_PENCIL_ALL_STRICT_PASS_5E7C2A"
