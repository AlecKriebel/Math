#!/bin/sh
set -eu

audit_directory=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
package_directory=$(CDPATH= cd -- "$audit_directory/.." && pwd)
runner="$package_directory/verify_line22_marked_critical_infinity_pari_strict.sh"
fake_path="$audit_directory/fakebin:$PATH"

chmod +x "$audit_directory/fakebin/gp"

run_mode() {
    mode=$1
    expected=$2
    set +e
    PATH="$fake_path" FAKE_GP_MODE="$mode" "$runner" >/dev/null 2>&1
    actual=$?
    set -e
    if [ "$actual" -ne "$expected" ]; then
        echo "FAIL: mode=$mode expected=$expected actual=$actual" >&2
        exit 1
    fi
}

run_mode success 0
run_mode diagnostic 1
run_mode extra 1
run_mode wrong 1
run_mode nonzero 7

echo "PASS: strict GP runner rejects diagnostics, extra/wrong output, and nonzero status"
