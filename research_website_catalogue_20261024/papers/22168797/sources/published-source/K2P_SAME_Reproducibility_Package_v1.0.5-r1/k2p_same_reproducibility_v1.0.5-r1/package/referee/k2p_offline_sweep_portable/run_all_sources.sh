#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
OUT="${1:-$ROOT/run}"
PYTHON_BIN="${PYTHON_BIN:-python3}"
K2P_WORKERS="${K2P_WORKERS:-1}"
K2P_MANIFEST_EVERY="${K2P_MANIFEST_EVERY:-25}"
K2P_LANE_STAGGER_SECONDS="${K2P_LANE_STAGGER_SECONDS:-15}"

"$PYTHON_BIN" - <<'PY'
if not __debug__:
    raise SystemExit("K2P_PORTABLE_OPTIMIZED_MODE_FORBIDDEN")
PY

export PYTHONHASHSEED="${PYTHONHASHSEED:-0}"
export PYTHONDONTWRITEBYTECODE="${PYTHONDONTWRITEBYTECODE:-1}"
export OMP_NUM_THREADS="${OMP_NUM_THREADS:-1}"
export OPENBLAS_NUM_THREADS="${OPENBLAS_NUM_THREADS:-1}"
export MKL_NUM_THREADS="${MKL_NUM_THREADS:-1}"
export VECLIB_MAXIMUM_THREADS="${VECLIB_MAXIMUM_THREADS:-1}"
export NUMEXPR_NUM_THREADS="${NUMEXPR_NUM_THREADS:-1}"

read -r COMPILER CANONICALIZER < <("$PYTHON_BIN" - "$ROOT" <<'PY'
import json, pathlib, sys
lock=json.loads((pathlib.Path(sys.argv[1])/'INPUT_LOCK.json').read_text())
print(lock['compiler_sha256'],lock['canonicalizer_sha256'])
PY
)

mkdir -p "$OUT/logs"

run_lane() {
  local lane="$1"
  shift
  "$PYTHON_BIN" "$ROOT/resumable_four_port_driver.py" \
    --package-root "$ROOT" \
    --output-root "$OUT" \
    --manifest-every "$K2P_MANIFEST_EVERY" \
    --expected-compiler-sha256 "$COMPILER" \
    --expected-canonicalizer-sha256 "$CANONICALIZER" \
    "$@" 2>&1 | tee -a "$OUT/logs/${lane}.log"
}

case "$K2P_WORKERS" in
  1)
    run_lane lane_all \
      --source-index 0 --source-index 1 --source-index 2 \
      --source-index 3 --source-index 4 --source-index 5
    ;;
  2)
    run_lane lane_a --source-index 1 --source-index 2 &
    lane_a_pid=$!
    sleep "$K2P_LANE_STAGGER_SECONDS"
    run_lane lane_b \
      --source-index 0 --source-index 3 --source-index 4 --source-index 5 &
    lane_b_pid=$!
    status=0
    wait "$lane_a_pid" || status=$?
    wait "$lane_b_pid" || status=$?
    if [[ "$status" -ne 0 ]]; then
      exit "$status"
    fi
    ;;
  *)
    echo "K2P_WORKERS must be 1 or 2; independent drivers use about 1.3 GiB before classification." >&2
    exit 2
    ;;
esac

"$PYTHON_BIN" "$ROOT/merge_manifests.py" --package-root "$ROOT" --run-root "$OUT"
