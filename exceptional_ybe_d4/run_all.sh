#!/usr/bin/env bash
set -euo pipefail

YBE_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
YBE_SYMPY_PYTHON="${YBE_SYMPY_PYTHON:-python3}"

cd "$YBE_SCRIPT_DIR"

echo "== dependency-free exact matrix verifier =="
python3 verify_exact.py

echo
echo "== abstract tensor-word verifier =="
python3 verify_tensor_words.py

echo
echo "== preserved SymPy verifier =="
if ! "$YBE_SYMPY_PYTHON" -c "import sympy" >/dev/null 2>&1; then
  echo "SymPy is unavailable to $YBE_SYMPY_PYTHON." >&2
  echo "Install requirements.txt or set YBE_SYMPY_PYTHON to a compatible interpreter." >&2
  exit 2
fi
"$YBE_SYMPY_PYTHON" verify_supplied.py

echo
echo "All three verification routes passed."
