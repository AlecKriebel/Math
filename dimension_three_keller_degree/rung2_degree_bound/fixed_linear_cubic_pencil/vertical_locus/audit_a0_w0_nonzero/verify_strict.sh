#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PYTHON_BIN=${PYTHON_BIN:-/opt/homebrew/bin/python3}
CHECKER="$HERE/verify_a0_w0_nonzero_independent.py"

"$PYTHON_BIN" "$CHECKER"

TMP_AUDIT=$(mktemp -d "${TMPDIR:-/tmp}/a0-w0-independent.XXXXXX")
trap 'rm -rf "$TMP_AUDIT"' EXIT HUP INT TERM

for mutation in wrong_U flip_factor erase_chi skip_unit_scope
do
    log="$TMP_AUDIT/$mutation.log"
    if A0_W0_INDEPENDENT_MUTATION=$mutation \
        "$PYTHON_BIN" "$CHECKER" >"$log" 2>&1
    then
        echo "FAIL: mutation $mutation escaped the independent guard" >&2
        exit 1
    fi
    if ! grep -q "FAIL \\[" "$log"
    then
        echo "FAIL: mutation $mutation did not fail through a named guard" >&2
        sed -n '1,80p' "$log" >&2
        exit 1
    fi
    echo "PASS fail-closed mutation: $mutation"
done

if "$PYTHON_BIN" -O "$CHECKER" >"$TMP_AUDIT/optimized.log" 2>&1
then
    echo "FAIL: optimized Python escaped the independent guard" >&2
    exit 1
fi
grep -q "FAIL:" "$TMP_AUDIT/optimized.log"
echo "PASS fail-closed optimized-Python guard"

echo "A0_W0_NONZERO_INDEPENDENT_STRICT_PASS_94A60D"
