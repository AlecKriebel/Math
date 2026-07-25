#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
output_file=$(mktemp "${TMPDIR:-/tmp}/line22-finite-outer-pari.XXXXXX")
trap 'rm -f "$output_file"' EXIT HUP INT TERM

if ! gp -q -s 134217728 \
    "$script_dir/verify_line_22_finite_outer_critical_pari.gp" \
    >"$output_file" 2>&1; then
    cat "$output_file"
    exit 1
fi

cat "$output_file"

if grep -q '\*\*\*' "$output_file"; then
    echo "FAIL: PARI/GP emitted a parser or runtime diagnostic" >&2
    exit 1
fi

expected='PASS: independent PARI/GP finite-outer-critical line-(2,2) identities'
if ! tail -n 1 "$output_file" | grep -Fqx "$expected"; then
    echo "FAIL: PARI/GP success sentinel missing" >&2
    exit 1
fi
