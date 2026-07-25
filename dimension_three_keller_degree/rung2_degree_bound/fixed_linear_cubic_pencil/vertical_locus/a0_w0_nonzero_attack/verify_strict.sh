#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SYSTEM_PYTHON=${SYSTEM_PYTHON:-/usr/bin/python3}
PLAIN_PYTHON=${PLAIN_PYTHON:-python3}

"$SYSTEM_PYTHON" "$HERE/verify_a0_w0_nonzero_sympy.py"
"$PLAIN_PYTHON" "$HERE/verify_a0_w0_nonzero_sparse.py"

TMP_AUDIT=$(mktemp -d "${TMPDIR:-/tmp}/a0-w0-nonzero.XXXXXX")
trap 'rm -rf "$TMP_AUDIT"' EXIT HUP INT TERM

for mutation in wrong_U drop_chi flip_bracket
do
    log="$TMP_AUDIT/sympy-$mutation.log"
    if A0_W0_MUTATION="$mutation" \
        "$SYSTEM_PYTHON" "$HERE/verify_a0_w0_nonzero_sympy.py" >"$log" 2>&1
    then
        echo "FAIL: SymPy mutation $mutation escaped" >&2
        exit 1
    fi
    grep -q "FAIL:" "$log"
done

for mutation in wrong_U flip_bracket
do
    log="$TMP_AUDIT/sparse-$mutation.log"
    if A0_W0_SPARSE_MUTATION="$mutation" \
        "$PLAIN_PYTHON" "$HERE/verify_a0_w0_nonzero_sparse.py" >"$log" 2>&1
    then
        echo "FAIL: sparse mutation $mutation escaped" >&2
        exit 1
    fi
    grep -q "FAIL:" "$log"
done

if "$SYSTEM_PYTHON" -O "$HERE/verify_a0_w0_nonzero_sympy.py" \
    >"$TMP_AUDIT/sympy-optimized.log" 2>&1
then
    echo "FAIL: optimized SymPy verifier escaped" >&2
    exit 1
fi
grep -q "FAIL:" "$TMP_AUDIT/sympy-optimized.log"

if "$PLAIN_PYTHON" -O "$HERE/verify_a0_w0_nonzero_sparse.py" \
    >"$TMP_AUDIT/sparse-optimized.log" 2>&1
then
    echo "FAIL: optimized sparse verifier escaped" >&2
    exit 1
fi
grep -q "FAIL:" "$TMP_AUDIT/sparse-optimized.log"

echo "PASS: A0_W0_NONZERO_STRICT_31F80B"
