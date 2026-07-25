#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
temporary_dir=$(mktemp -d "${TMPDIR:-/tmp}/vertical-triple-zero.XXXXXX")
trap 'rm -rf "$temporary_dir"' EXIT HUP INT TERM

if ! /usr/bin/python3 \
  "$script_dir/verify_vertical_triple_gamma0_ell0_sympy.py" \
  >"$temporary_dir/sympy.out" 2>&1; then
  cat "$temporary_dir/sympy.out"
  exit 1
fi
cat "$temporary_dir/sympy.out"
sympy_expected='VERTICAL_TRIPLE_GAMMA0_ELL0_SYMPY_PASS_83A4E1'
if ! tail -n 1 "$temporary_dir/sympy.out" | grep -Fqx "$sympy_expected"; then
  echo "FAIL: SymPy success sentinel missing" >&2
  exit 1
fi

if ! gp -q \
  "$script_dir/verify_vertical_triple_gamma0_ell0_pari.gp" \
  >"$temporary_dir/pari.out" 2>&1; then
  cat "$temporary_dir/pari.out"
  exit 1
fi
cat "$temporary_dir/pari.out"
if grep -Eq '^  \*\*\*|FAIL:' "$temporary_dir/pari.out"; then
  echo "FAIL: PARI/GP reported an error" >&2
  exit 1
fi
pari_expected='VERTICAL_TRIPLE_GAMMA0_ELL0_PARI_PASS_6D291C'
if ! tail -n 1 "$temporary_dir/pari.out" | grep -Fqx "$pari_expected"; then
  echo "FAIL: PARI/GP success sentinel missing" >&2
  exit 1
fi

echo "PASS: all triple-root zero-gamma zero-ell charts"
