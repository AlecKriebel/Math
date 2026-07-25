#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
temporary_dir=$(mktemp -d "${TMPDIR:-/tmp}/vertical-yz2-chart.XXXXXX")
trap 'rm -rf "$temporary_dir"' EXIT HUP INT TERM

/usr/bin/python3 \
  "$script_dir/verify_vertical_triple_yz2_gamma0_ell0_sympy.py" \
  >"$temporary_dir/sympy.out" 2>&1
cat "$temporary_dir/sympy.out"
sympy_expected='VERTICAL_TRIPLE_YZ2_GAMMA0_ELL0_SYMPY_PASS_4FD8A2'
if ! tail -n 1 "$temporary_dir/sympy.out" | grep -Fqx "$sympy_expected"; then
  echo "FAIL: SymPy success sentinel missing" >&2
  exit 1
fi

gp -q \
  "$script_dir/verify_vertical_triple_yz2_gamma0_ell0_pari.gp" \
  >"$temporary_dir/pari.out" 2>&1
cat "$temporary_dir/pari.out"
if grep -Eq '^  \\*\\*\\*|FAIL:' "$temporary_dir/pari.out"; then
  echo "FAIL: PARI/GP reported an error" >&2
  exit 1
fi
pari_expected='VERTICAL_TRIPLE_YZ2_GAMMA0_ELL0_PARI_PASS_7B16E9'
if ! tail -n 1 "$temporary_dir/pari.out" | grep -Fqx "$pari_expected"; then
  echo "FAIL: PARI/GP success sentinel missing" >&2
  exit 1
fi

echo "PASS: independent exact certificates for the vertical yz2 chart"
