#!/bin/sh
set -eu

certificate_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python_bin=${KELLER_DN1CC_PYTHON:-/Users/alec/Documents/Math/.venv/bin/python}
hostile_output=$(mktemp "${TMPDIR:-/tmp}/d4-dn1cc-hostile.XXXXXX")
pari_output=$(mktemp "${TMPDIR:-/tmp}/d4-dn1cc-pari.XXXXXX")
mutated_script=$(mktemp "${TMPDIR:-/tmp}/d4-dn1cc-mutant.XXXXXX")
mutated_output=$(mktemp "${TMPDIR:-/tmp}/d4-dn1cc-mutant-out.XXXXXX")
trap 'rm -f "$hostile_output" "$pari_output" "$mutated_script" "$mutated_output"' EXIT HUP INT TERM

test -x "$python_bin"
cd "$certificate_dir"
"$python_bin" verify_full_contact_sympy.py

if ! gp -q verify_full_contact_pari.gp >"$pari_output" 2>&1; then
    cat "$pari_output"
    exit 1
fi
if grep -q '\*\*\*' "$pari_output"; then
    cat "$pari_output"
    exit 1
fi
grep -Fx 'D4_DN1CC_PARI_INDEPENDENT_PASS_ONE_LINE' "$pari_output"

if ! sh verify_hostile.sh >"$hostile_output" 2>&1; then
    cat "$hostile_output"
    exit 1
fi
cat "$hostile_output"
grep -Fx 'D4_DN1CC_HOSTILE_AUDIT_STRICT_PASS' "$hostile_output" >/dev/null

# Required-failure mutation: corrupt the nonzero-contact E4 obstruction.
sed 's/sp.Rational(16, 135)/sp.Rational(17, 135)/g' \
    verify_full_contact_sympy.py >"$mutated_script"
if cmp -s verify_full_contact_sympy.py "$mutated_script"; then
    echo 'FAIL: DN1CC E4 mutation did not alter the script' >&2
    exit 1
fi
if "$python_bin" "$mutated_script" >"$mutated_output" 2>&1; then
    cat "$mutated_output"
    echo 'FAIL: corrupted DN1CC E4 obstruction was accepted' >&2
    exit 1
fi
grep -F 'AssertionError' "$mutated_output" >/dev/null

printf '%s\n' 'D4_DN1CC_FAIL_CLOSED_STRICT_PASS'
