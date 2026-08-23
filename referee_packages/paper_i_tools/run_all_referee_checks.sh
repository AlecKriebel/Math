#!/bin/sh
set -eu

if [ "${PYTHON+x}" = x ]; then
  echo "Refusing inherited PYTHON; use BOOTSTRAP_PYTHON for the trusted host interpreter" >&2
  exit 2
fi
case ${PYTHONOPTIMIZE-} in
  ""|0) ;;
  *)
    echo "Refusing inherited PYTHONOPTIMIZE=${PYTHONOPTIMIZE}" >&2
    exit 2
    ;;
esac
unset PYTHONOPTIMIZE PYTHONPATH PYTHONHOME PYTHONSTARTUP PYTHONINSPECT \
  PYTHONWARNINGS PYTHONPYCACHEPREFIX PYTHONCASEOK PYTHONPLATLIBDIR \
  PYTHONUSERBASE PYTHONEXECUTABLE PYTHON MAKEFLAGS MFLAGS GNUMAKEFLAGS \
  MAKEOVERRIDES
export PYTHONNOUSERSITE=1
export PYTHONDONTWRITEBYTECODE=1

package_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
bootstrap_python=${BOOTSTRAP_PYTHON:-python3}
tmp_base=${TMPDIR:-/tmp}
tmp_base=${tmp_base%/}

"$bootstrap_python" -I - <<'PY'
import sys
if sys.version_info[:3] != (3, 14, 6):
    raise SystemExit(f"Python 3.14.6 is required; found {sys.version.split()[0]}")
if sys.flags.optimize != 0:
    raise SystemExit("optimized Python is forbidden for certificate replay")
PY

for command_name in tectonic pdfinfo pdftoppm; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    echo "Missing required build tool: $command_name" >&2
    exit 2
  fi
done

if [ "$(tectonic --version)" != "Tectonic 0.16.9" ]; then
  echo "Tectonic 0.16.9 is required" >&2
  tectonic --version >&2
  exit 2
fi
if [ "$(pdfinfo -v 2>&1 | sed -n '1p')" != "pdfinfo version 26.08.0" ]; then
  echo "pdfinfo 26.08.0 is required" >&2
  pdfinfo -v >&2
  exit 2
fi
if [ "$(pdftoppm -v 2>&1 | sed -n '1p')" != "pdftoppm version 26.08.0" ]; then
  echo "pdftoppm 26.08.0 is required" >&2
  pdftoppm -v >&2
  exit 2
fi

run_root=$(mktemp -d "$tmp_base/paper1-certified.XXXXXX")
case "$run_root" in
  "$tmp_base"/paper1-certified.*) ;;
  *)
    echo "Unexpected certified-run directory: $run_root" >&2
    exit 2
    ;;
esac
chmod 700 "$run_root"
cleanup() {
  case "$run_root" in
    "$tmp_base"/paper1-certified.*) rm -rf -- "$run_root" ;;
    *) echo "Refusing to remove unexpected run directory: $run_root" >&2 ;;
  esac
}
trap cleanup EXIT HUP INT TERM

logs="$run_root/logs"
source_dir="$run_root/source"
mkdir -m 700 "$logs" "$source_dir"
"$bootstrap_python" -I "$package_dir/verify_referee_package.py" \
  --extract-to "$source_dir"
paper_dir="$source_dir/universal_simultaneous_amplification/phase5_exact_threshold/paper_db_extremality"

negative_log="$logs/intentional-negative-control.log"
if BOOTSTRAP_PYTHON="$bootstrap_python" \
  "$paper_dir/submission/bootstrap_replay.sh" --negative-control \
  >"$negative_log" 2>&1; then
  echo "Intentional false check incorrectly returned success" >&2
  exit 2
fi
if ! grep -F "INTENTIONAL_NEGATIVE_CONTROL" "$negative_log" >/dev/null; then
  echo "Intentional false check did not reach the explicit failure" >&2
  sed -n '1,200p' "$negative_log" >&2
  exit 2
fi
echo "PASS: intentional false check propagates a nonzero top-level status"

optimized_check_log="$logs/optimized-explicit-check-negative-control.log"
if "$bootstrap_python" -O -I \
  "$paper_dir/submission/verify_execution_safety.py" --intentional-failure \
  >"$optimized_check_log" 2>&1; then
  echo "Explicit false check disappeared under python -O" >&2
  exit 2
fi
if ! grep -F "INTENTIONAL_NEGATIVE_CONTROL" \
  "$optimized_check_log" >/dev/null; then
  echo "Optimized explicit false check did not reach the intended failure" >&2
  sed -n '1,200p' "$optimized_check_log" >&2
  exit 2
fi
echo "PASS: explicit false check remains active under python -O"

optimized_log="$logs/optimized-environment-negative-control.log"
if PYTHONOPTIMIZE=1 BOOTSTRAP_PYTHON="$bootstrap_python" \
  "$paper_dir/submission/bootstrap_replay.sh" --negative-control \
  >"$optimized_log" 2>&1; then
  echo "Optimized environment incorrectly returned success" >&2
  exit 2
fi
if ! grep -F "Refusing inherited PYTHONOPTIMIZE=1" \
  "$optimized_log" >/dev/null; then
  echo "Optimized environment was not rejected explicitly" >&2
  sed -n '1,200p' "$optimized_log" >&2
  exit 2
fi
echo "PASS: inherited optimized mode is rejected before replay"

token_log="$logs/public-token-interpreter-negative-control.log"
if PYTHON="$paper_dir/submission/fake_python_public_token.sh" \
  "$paper_dir/replay.sh" >"$token_log" 2>&1; then
  echo "Token-printing non-Python command incorrectly passed internal replay" >&2
  exit 2
fi
if ! grep -F "PYTHON overrides are forbidden" "$token_log" >/dev/null; then
  echo "Token-printing interpreter was not rejected at the shell boundary" >&2
  sed -n '1,200p' "$token_log" >&2
  exit 2
fi
if grep -F "PAPER1_EXECUTION_SAFETY_OK" "$token_log" >/dev/null; then
  echo "Token-printing fake interpreter was invoked before rejection" >&2
  exit 2
fi
echo "PASS: public-token fake interpreter is rejected before invocation"

tree_negative_control() {
  mode=$1
  expected_message=$2
  negative_tree="$run_root/negative-$mode"
  negative_log="$logs/tree-$mode-negative-control.log"
  mkdir -m 700 "$negative_tree"
  "$bootstrap_python" -I "$package_dir/verify_referee_package.py" \
    --extract-to "$negative_tree" >/dev/null
  "$bootstrap_python" -I \
    "$negative_tree/universal_simultaneous_amplification/phase5_exact_threshold/paper_db_extremality/submission/create_tree_negative_control.py" \
    "$mode" "$negative_tree" >/dev/null
  negative_paper="$negative_tree/universal_simultaneous_amplification/phase5_exact_threshold/paper_db_extremality"
  if BOOTSTRAP_PYTHON="$bootstrap_python" \
    "$negative_paper/submission/bootstrap_replay.sh" \
    --certified-package-stage >"$negative_log" 2>&1; then
    echo "Contaminated $mode tree incorrectly passed certified bootstrap" >&2
    exit 2
  fi
  if ! grep -F "$expected_message" "$negative_log" >/dev/null; then
    echo "Contaminated $mode tree failed for the wrong reason" >&2
    sed -n '1,200p' "$negative_log" >&2
    exit 2
  fi
  if find "$negative_tree" -name PYCACHE_EXECUTED -print -quit | grep . >/dev/null; then
    echo "Hostile bytecode executed before the $mode tree was rejected" >&2
    exit 2
  fi
  echo "PASS: certified tree audit rejects $mode contamination before import"
}

tree_negative_control bytecode "forbidden bytecode/cache directory"
tree_negative_control extra-file "bundle tree node-set mismatch"
tree_negative_control extra-dir "bundle tree node-set mismatch"
tree_negative_control symlink "bundle tree contains a symlink"
tree_negative_control fifo "bundle tree contains a special node"

BOOTSTRAP_PYTHON="$bootstrap_python" \
  "$paper_dir/submission/bootstrap_replay.sh" --certified-package-stage

"$paper_dir/build.sh"
cmp \
  "$package_dir/complete_graph_extremality_db.pdf" \
  "$paper_dir/output/pdf/complete_graph_extremality_db.pdf"

"$bootstrap_python" -I - "$paper_dir/output/pdf/complete_graph_extremality_db.pdf" <<'PY'
from pathlib import Path
import hashlib
import sys

pdf = Path(sys.argv[1])
print(f"REBUILT_PDF_SHA256: {hashlib.sha256(pdf.read_bytes()).hexdigest()}")
PY

"$bootstrap_python" -I "$package_dir/verify_referee_package.py" >/dev/null
echo "PASS: sole certified package replay verified the exact tree, rejected hostile controls, ran the hash-locked certificates, and reproduced the PDF"
