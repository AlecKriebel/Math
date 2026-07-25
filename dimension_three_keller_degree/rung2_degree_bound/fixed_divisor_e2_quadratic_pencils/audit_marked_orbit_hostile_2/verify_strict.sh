#!/bin/sh
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python_bin=${PYTHON_BIN:-/usr/bin/python3}
checker="$here/verify_marked_orbit_hostile_2.py"
tmp_dir=$(mktemp -d "${TMPDIR:-/tmp}/marked-hostile-2.XXXXXX")
trap 'rm -rf "$tmp_dir"' EXIT HUP INT TERM

expected='AUDITED_FREEZE_SHA256=27e5a4f894ef523156abea389f89c2d4481d58d243c756b70386fdea10e9e01f
MARKED_PAIR_TYPES=3
STABLE_STRATA=13
NONZERO_ORBIT_SPACE=3+P1+3
THETA_TAU_CONVERSION=theta=1/(1+tau)
BOUNDARIES=CH:theta1,CT:thetaInfinity,CS:theta0
MIDDLE_RESIDUAL_ACTION=POINTWISE_IDENTITY
MARKED_ORBIT_HOSTILE_2_PASS_C4B821'

output=$("$python_bin" "$checker")
if [ "$output" != "$expected" ]; then
    printf '%s\n' "FAIL: ordinary checker output mismatch" "$output" >&2
    exit 1
fi

optimized=$("$python_bin" -O "$checker")
if [ "$optimized" != "$expected" ]; then
    printf '%s\n' "FAIL: optimized checker output mismatch" "$optimized" >&2
    exit 1
fi

for mutation in drop_stratum wrong_conversion overlap_boundary merge_tau
do
    log="$tmp_dir/$mutation.log"
    if MARKED_HOSTILE_2_MUTATION=$mutation "$python_bin" "$checker" >"$log" 2>&1
    then
        printf '%s\n' "FAIL: mutation survived: $mutation" >&2
        exit 1
    fi
    if ! grep -Fq "FAIL [$mutation]" "$log"; then
        printf '%s\n' "FAIL: mutation did not hit a named guard: $mutation" >&2
        exit 1
    fi
done

printf '%s\n' "$output"
printf '%s\n' "MARKED_ORBIT_HOSTILE_2_STRICT_PASS_91A73E"
