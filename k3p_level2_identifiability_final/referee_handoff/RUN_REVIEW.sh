#!/bin/sh
set -eu
umask 022

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
PYTHON_BIN="$SCRIPT_DIR/.venv/bin/python"
MODE=${1:-verify}
shift || true

if [ "${K3P_REFEREE_EXTERNAL_SANDBOX:-}" != YES ]; then
  echo "Refusing to execute package code without an external sandbox attestation." >&2
  echo "After supplying an offline, credential-free OS/VM/container boundary, set:" >&2
  echo "  K3P_REFEREE_EXTERNAL_SANDBOX=YES" >&2
  exit 2
fi

CONFIRM_REGENERATION=${K3P_REFEREE_CONFIRM_REGENERATION:-}

if [ -n "${K3P_REFEREE_TRUSTED_PYTHON:-}" ]; then
  TRUSTED_PYTHON=$K3P_REFEREE_TRUSTED_PYTHON
elif [ -x /usr/bin/python3 ]; then
  TRUSTED_PYTHON=/usr/bin/python3
else
  TRUSTED_PYTHON=python3
fi

env -i \
  PATH=/usr/bin:/bin:/usr/sbin:/sbin \
  HOME=/ TMPDIR=/tmp \
  PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 PYTHONNOUSERSITE=1 \
  LC_ALL=C LANG=C TZ=UTC SOURCE_DATE_EPOCH=0 \
  "$TRUSTED_PYTHON" "$SCRIPT_DIR/referee_tools/verify_package_integrity.py" \
    --package-root "$SCRIPT_DIR"

env -i \
  PATH=/usr/bin:/bin:/usr/sbin:/sbin \
  HOME=/ TMPDIR=/tmp \
  PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 PYTHONNOUSERSITE=1 \
  LC_ALL=C LANG=C TZ=UTC SOURCE_DATE_EPOCH=0 \
  K3P_REFEREE_EXTERNAL_SANDBOX=YES \
  "$TRUSTED_PYTHON" "$SCRIPT_DIR/referee_tools/run_active_verifiers.py" \
    --package-root "$SCRIPT_DIR" --prepare-runtime-only

RUNTIME_ROOT="$SCRIPT_DIR/review_runs/runner_control"
RUNTIME_HOME="$RUNTIME_ROOT/home"
RUNTIME_TMP="$RUNTIME_ROOT/tmp"

if [ ! -x "$PYTHON_BIN" ]; then
  echo "Missing $PYTHON_BIN" >&2
  echo "Run: python3 -m venv .venv" >&2
  echo "Then: .venv/bin/python -m pip install -r proof_package/reproducibility/requirements.txt" >&2
  exit 2
fi

exec env -i \
  PATH=/usr/bin:/bin:/usr/sbin:/sbin \
  HOME="$RUNTIME_HOME" TMPDIR="$RUNTIME_TMP" \
  PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 PYTHONNOUSERSITE=1 \
  LC_ALL=C LANG=C TZ=UTC SOURCE_DATE_EPOCH=0 \
  K3P_REFEREE_EXTERNAL_SANDBOX=YES \
  K3P_REFEREE_CONFIRM_REGENERATION="$CONFIRM_REGENERATION" \
  "$PYTHON_BIN" "$SCRIPT_DIR/referee_tools/run_active_verifiers.py" \
    --package-root "$SCRIPT_DIR" --python "$PYTHON_BIN" --mode "$MODE" "$@"
