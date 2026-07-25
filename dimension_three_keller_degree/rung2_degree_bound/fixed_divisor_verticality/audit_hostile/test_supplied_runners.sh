#!/bin/sh
set -eu

audit_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
package_dir=$(CDPATH= cd -- "$audit_dir/.." && pwd)
fake_path="$audit_dir/fakebin:$PATH"

/usr/bin/python3 "$package_dir/verify_fixed_divisor_verticality_sympy.py" \
    >/dev/null
"$package_dir/verify_fixed_divisor_verticality_pari_strict.sh" >/dev/null

if /usr/bin/python3 -O \
    "$package_dir/verify_fixed_divisor_verticality_sympy.py" \
    >/dev/null 2>&1; then
    printf '%s\n' "FAIL: optimized Python bypassed the assertion guard" >&2
    exit 1
fi

for mode in failure diagnostic trailing nonzero; do
    if PATH="$fake_path" FAKE_GP_MODE="$mode" \
        "$package_dir/verify_fixed_divisor_verticality_pari_strict.sh" \
        >/dev/null 2>&1; then
        printf '%s\n' "FAIL: wrapper accepted fake GP mode $mode" >&2
        exit 1
    fi
done

printf '%s\n' "PASS: supplied verifiers and fail-closed runner behavior"
