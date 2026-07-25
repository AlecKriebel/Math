#!/bin/sh
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

if /usr/bin/python3 -O "$script_dir/audit_reconstruct_mod101.py" \
    >/dev/null 2>&1; then
  echo "FAIL: optimized Python was accepted"
  exit 1
fi

fake_dir=$(mktemp -d)
trap 'rm -f "$fake_dir/gp"; rmdir "$fake_dir"' EXIT HUP INT TERM

make_fake_gp() {
  diagnostic=$1
  {
    printf '%s\n' '#!/bin/sh'
    printf '%s\n' "printf '%s\\n' '$diagnostic'"
    printf '%s\n' \
      "printf '%s\\n' 'PASS: hostile exact PARI normal-form and kernel reconstruction'"
    printf '%s\n' 'exit 0'
  } >"$fake_dir/gp"
  chmod +x "$fake_dir/gp"
}

make_fake_gp 'FAIL forged algebraic check'
if PATH="$fake_dir:$PATH" "$script_dir/audit_exact_pari_strict.sh" \
    >/dev/null 2>&1; then
  echo "FAIL: forged algebraic failure was accepted"
  exit 1
fi

make_fake_gp '*** forged PARI diagnostic'
if PATH="$fake_dir:$PATH" "$script_dir/audit_exact_pari_strict.sh" \
    >/dev/null 2>&1; then
  echo "FAIL: forged PARI diagnostic was accepted"
  exit 1
fi

echo "hostile audit guard tests passed"
