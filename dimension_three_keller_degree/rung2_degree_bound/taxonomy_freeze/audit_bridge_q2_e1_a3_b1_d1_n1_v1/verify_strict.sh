#!/bin/sh
set -eu

audit_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
rung_dir=$(CDPATH= cd -- "$audit_dir/../.." && pwd)
python_bin=/usr/bin/python3
audit_tmp=$(mktemp -d "${TMPDIR:-/tmp}/fixed-linear-bridge-strict.XXXXXX")
trap 'rm -rf "$audit_tmp"' EXIT HUP INT TERM

expected_audit='FROZEN_PIVOTS=45
POTENTIAL_ROUTED=30
FORCED_EMPTY=15
ROUTE_ATOMS=48
INTRINSIC_TERMINALS=15
AUDITED_TERMINALS=15
QUADRATIC_PROVENANCE=STANDALONE_HOSTILE_PASS
STALE_STATUS_MARKERS=0
CANDIDATE_STATUS=UNCONDITIONAL
BRIDGE_Q2_E1_A3_B1_D1_N1_INDEPENDENT_PASS_F4A93C'

audit_output=$("$python_bin" "$audit_dir/verify_bridge_independent.py")
if [ "$audit_output" != "$expected_audit" ]; then
    printf '%s\n' "FAIL: independent checker output mismatch" >&2
    printf '%s\n' "$audit_output" >&2
    exit 1
fi

if "$python_bin" -O "$audit_dir/verify_bridge_independent.py" \
    >"$audit_tmp/optimized.out" 2>&1; then
    printf '%s\n' "FAIL: optimized Python was accepted" >&2
    exit 1
fi

for audit_mutation in \
    drop_normalization_chart \
    drop_pivot \
    overlap_pivot \
    drop_atom \
    overlap_terminal \
    drop_terminal \
    unaudit_a0 \
    unaudit_quadratic
do
    if BRIDGE_AUDIT_MUTATION=$audit_mutation \
        "$python_bin" "$audit_dir/verify_bridge_independent.py" \
        >"$audit_tmp/mutation-$audit_mutation.out" 2>&1
    then
        printf '%s\n' "FAIL: mutation survived: $audit_mutation" >&2
        exit 1
    fi
done

expected_probe='CANDIDATE_CHECKER_SEMANTIC_MUTATION=REJECTED
INDEPENDENT_CHECKER_SEMANTIC_MUTATION=REJECTED
CANDIDATE_CHECKER_PINNED_INPUT_MUTATION=REJECTED'
probe_output=$(
    "$python_bin" "$audit_dir/verify_bridge_independent.py" \
        --probe-original-checker
)
if [ "$probe_output" != "$expected_probe" ]; then
    printf '%s\n' "FAIL: supplied-checker probe output mismatch" >&2
    printf '%s\n' "$probe_output" >&2
    exit 1
fi

candidate_checker="$rung_dir/taxonomy_freeze/verify_bridge_q2_e1_a3_b1_d1_n1_v1.py"
expected_candidate='PASS: fixed-linear cubic-pencil bridge candidate; 30 routed potential + 15 forced-empty pivots; 15 intrinsic terminals; 0 conditional hostile audits'
candidate_output=$("$python_bin" "$candidate_checker")
if [ "$candidate_output" != "$expected_candidate" ]; then
    printf '%s\n' "FAIL: supplied candidate checker output mismatch" >&2
    printf '%s\n' "$candidate_output" >&2
    exit 1
fi
if "$python_bin" -O "$candidate_checker" \
    >"$audit_tmp/candidate-optimized.out" 2>&1; then
    printf '%s\n' "FAIL: supplied checker accepted optimized Python" >&2
    exit 1
fi

a0_runner="$rung_dir/fixed_linear_cubic_pencil/vertical_locus/audit_a0_w0_nonzero/verify_strict.sh"
a0_output=$("$a0_runner")
case "$a0_output" in
    *A0_W0_NONZERO_INDEPENDENT_STRICT_PASS_94A60D*) ;;
    *)
        printf '%s\n' "FAIL: final a=0,W0!=0 hostile replay failed" >&2
        exit 1
        ;;
esac

quadratic_checker="$rung_dir/audit_quadratic_component_exit/verify_quadratic_component_exit_exact.py"
expected_quadratic='PASS: exact quadratic-coordinate, degree, and fibre identities verified'
quadratic_output=$("$python_bin" "$quadratic_checker")
if [ "$quadratic_output" != "$expected_quadratic" ]; then
    printf '%s\n' "FAIL: quadratic-component hostile replay failed" >&2
    exit 1
fi
quadratic_optimized=$("$python_bin" -O "$quadratic_checker")
if [ "$quadratic_optimized" != "$expected_quadratic" ]; then
    printf '%s\n' "FAIL: quadratic checker changed under optimized Python" >&2
    exit 1
fi

printf '%s\n' "$audit_output"
printf '%s\n' "$probe_output"
printf '%s\n' "BRIDGE_Q2_E1_A3_B1_D1_N1_STRICT_PASS_72C8E1"
