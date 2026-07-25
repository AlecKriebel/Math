#!/bin/sh
set -eu

audit_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
row_dir=$(CDPATH= cd -- "$audit_dir/.." && pwd)
python_cert="$row_dir/verify_binary_fixed_cubic_complete.py"
gp_cert="$row_dir/verify_binary_fixed_cubic_complete_pari.gp"
scratch=$(mktemp -d "${TMPDIR:-/tmp}/binary-fixed-cubic-audit.XXXXXX")
trap 'rm -rf "$scratch"' EXIT HUP INT TERM

if /usr/bin/python3 -O "$python_cert" >"$scratch/python-optimized.log" 2>&1; then
    echo "FAIL: promoted Python verifier accepts optimized execution"
    exit 1
fi
echo "PASS: promoted Python verifier rejects optimized execution"

sed 's/D.det() - 4/D.det() - 5/' \
    "$python_cert" >"$scratch/forged.py"
if /usr/bin/python3 "$scratch/forged.py" >"$scratch/python-forged.log" 2>&1; then
    echo "FAIL: promoted Python verifier accepted a forged top identity"
    exit 1
fi
echo "PASS: promoted Python verifier rejects a forged top identity"

sed 's/matdet(D)-4/matdet(D)-5/' \
    "$gp_cert" >"$scratch/forged.gp"
if gp -q "$scratch/forged.gp" >"$scratch/gp-forged.log" 2>&1; then
    echo "FAIL: promoted GP verifier accepted a forged top identity"
    exit 1
fi
echo "PASS: promoted GP verifier rejects a forged top identity"

echo "ALL FAIL-CLOSED TESTS PASSED"
