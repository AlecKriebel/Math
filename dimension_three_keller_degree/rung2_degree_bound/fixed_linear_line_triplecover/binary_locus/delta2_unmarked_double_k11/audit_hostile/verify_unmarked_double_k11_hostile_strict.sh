#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python_bin=${PYTHON_BIN:-/usr/bin/python3}
verifier="$script_dir/verify_unmarked_double_k11_independent.py"
expected='ALL INDEPENDENT UNMARKED-DOUBLE {1,1} AUDIT CHECKS PASSED'

output=$("$python_bin" -u "$verifier")
printf '%s\n' "$output"
if ! printf '%s\n' "$output" | grep -Fqx "$expected"; then
    echo "FAIL independent verifier did not reach its terminal certificate" >&2
    exit 1
fi

optimized_output=$("$python_bin" -O -u "$verifier")
if ! printf '%s\n' "$optimized_output" | grep -Fqx "$expected"; then
    echo "FAIL optimized run changed the independent certificate" >&2
    exit 1
fi

for mutation in q2_jet gcd_J contact_R3 contact_E1; do
    if AUDIT_MUTATION="$mutation" "$python_bin" -u "$verifier" \
        >/dev/null 2>&1; then
        echo "FAIL mutation $mutation escaped detection" >&2
        exit 1
    fi
    echo "PASS rejected mutation $mutation"
done

echo "ALL HOSTILE STRICT AND MUTATION CHECKS PASSED"
