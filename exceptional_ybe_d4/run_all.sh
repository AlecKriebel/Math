#!/usr/bin/env bash
set -euo pipefail

YBE_SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
YBE_PYTHON="${YBE_PYTHON:-${YBE_SYMPY_PYTHON:-python3}}"

cd "$YBE_SCRIPT_DIR"

if ! "$YBE_PYTHON" -c 'import sys; raise SystemExit(0 if sys.flags.optimize == 0 else 1)'; then
  echo "Optimized Python is not permitted for scientific verification." >&2
  exit 2
fi

if ! "$YBE_PYTHON" -c 'import sympy, mpmath; raise SystemExit(0 if (sympy.__version__, mpmath.__version__) == ("1.14.0", "1.3.0") else 1)' >/dev/null 2>&1; then
  echo "This package requires SymPy 1.14.0 and mpmath 1.3.0." >&2
  echo "Install requirements.txt into the selected YBE_PYTHON environment." >&2
  exit 2
fi

"$YBE_PYTHON" - <<'PY'
import platform
import sys
import mpmath
import sympy

print(
    "verification environment: "
    f"Python {platform.python_version()}; "
    f"SymPy {sympy.__version__}; "
    f"mpmath {mpmath.__version__}; "
    f"optimization={sys.flags.optimize}"
)
PY

echo
echo "== dependency-free exact matrix verifier =="
"$YBE_PYTHON" verify_exact.py

echo
echo "== abstract tensor-word verifier =="
"$YBE_PYTHON" verify_tensor_words.py

echo
echo "== hardened SymPy verifier =="
"$YBE_PYTHON" verify_supplied.py

echo
echo "== concurrent-work exact equivalence verifier =="
"$YBE_PYTHON" verify_concurrent_equivalence.py

echo
echo "== global braid-and-link exact verifier =="
"$YBE_PYTHON" verify_braid_link.py

echo
echo "All five verification routes passed."
