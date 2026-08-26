#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PYTHON_BIN="$SCRIPT_DIR/.venv/bin/python"

if [ -n "${K3P_REFEREE_TRUSTED_PYTHON:-}" ]; then
  TRUSTED_PYTHON=$K3P_REFEREE_TRUSTED_PYTHON
elif [ -x /usr/bin/python3 ]; then
  TRUSTED_PYTHON=/usr/bin/python3
else
  TRUSTED_PYTHON=python3
fi

"$TRUSTED_PYTHON" "$SCRIPT_DIR/referee_tools/verify_package_integrity.py" \
  --package-root "$SCRIPT_DIR"

if [ ! -x "$PYTHON_BIN" ]; then
  echo "Missing $PYTHON_BIN" >&2
  echo "Run: python3 -m venv .venv" >&2
  echo "Then: .venv/bin/python -m pip install -r proof_package/reproducibility/requirements.txt" >&2
  exit 2
fi

MODE=${1:-verify}
shift || true

exec "$PYTHON_BIN" "$SCRIPT_DIR/referee_tools/run_active_verifiers.py" \
  --package-root "$SCRIPT_DIR" --python "$PYTHON_BIN" --mode "$MODE" "$@"
