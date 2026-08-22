#!/bin/sh
set -eu

case ${PYTHONOPTIMIZE-} in
  ""|0) ;;
  *)
    echo "Refusing inherited PYTHONOPTIMIZE=${PYTHONOPTIMIZE}" >&2
    exit 2
    ;;
esac
unset PYTHONOPTIMIZE PYTHONPATH PYTHONHOME PYTHONSTARTUP PYTHONINSPECT \
  PYTHONWARNINGS PYTHONPYCACHEPREFIX PYTHONCASEOK PYTHONPLATLIBDIR \
  PYTHONUSERBASE PYTHONEXECUTABLE MAKEFLAGS MFLAGS GNUMAKEFLAGS MAKEOVERRIDES
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
"$bootstrap_python" -I "$package_dir/verify_referee_package.py"

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

work_dir=$(mktemp -d "$tmp_base/paper1-referee.XXXXXX")
cleanup() {
  case "$work_dir" in
    "$tmp_base"/paper1-referee.*) rm -rf -- "$work_dir" ;;
    *) echo "Refusing to remove unexpected work directory: $work_dir" >&2 ;;
  esac
}
trap cleanup EXIT HUP INT TERM

cp -R "$package_dir/source_and_certificates/." "$work_dir/"
paper_dir="$work_dir/universal_simultaneous_amplification/phase5_exact_threshold/paper_db_extremality"

negative_log="$work_dir/intentional-negative-control.log"
if BOOTSTRAP_PYTHON="$bootstrap_python" \
  "$paper_dir/submission/bootstrap_replay.sh" --negative-control \
  >"$negative_log" 2>&1; then
  echo "Intentional false check incorrectly returned success" >&2
  exit 2
fi
if ! grep -F "INTENTIONAL_NEGATIVE_CONTROL" "$negative_log" >/dev/null; then
  echo "Intentional false check did not reach the explicit failure" >&2
  cat "$negative_log" >&2
  exit 2
fi
echo "PASS: intentional false check propagates a nonzero top-level status"

optimized_check_log="$work_dir/optimized-explicit-check-negative-control.log"
if "$bootstrap_python" -O -I \
  "$paper_dir/submission/verify_execution_safety.py" --intentional-failure \
  >"$optimized_check_log" 2>&1; then
  echo "Explicit false check disappeared under python -O" >&2
  exit 2
fi
if ! grep -F "INTENTIONAL_NEGATIVE_CONTROL" "$optimized_check_log" >/dev/null; then
  echo "Optimized explicit false check did not reach the intended failure" >&2
  cat "$optimized_check_log" >&2
  exit 2
fi
echo "PASS: explicit false check remains active under python -O"

optimized_log="$work_dir/optimized-environment-negative-control.log"
if PYTHONOPTIMIZE=1 BOOTSTRAP_PYTHON="$bootstrap_python" \
  "$paper_dir/submission/bootstrap_replay.sh" --negative-control \
  >"$optimized_log" 2>&1; then
  echo "Optimized environment incorrectly returned success" >&2
  exit 2
fi
if ! grep -F "Refusing inherited PYTHONOPTIMIZE=1" "$optimized_log" >/dev/null; then
  echo "Optimized environment was not rejected explicitly" >&2
  cat "$optimized_log" >&2
  exit 2
fi
echo "PASS: inherited optimized mode is rejected before replay"

false_interpreter_log="$work_dir/false-interpreter-negative-control.log"
if PYTHON=/usr/bin/true "$paper_dir/replay.sh" \
  >"$false_interpreter_log" 2>&1; then
  echo "Non-Python command incorrectly passed direct replay" >&2
  exit 2
fi
if ! grep -F "did not execute the Paper I safety preflight" \
  "$false_interpreter_log" >/dev/null; then
  echo "False interpreter was not rejected by the authenticated preflight" >&2
  cat "$false_interpreter_log" >&2
  exit 2
fi
echo "PASS: direct replay rejects a false interpreter command"

BOOTSTRAP_PYTHON="$bootstrap_python" \
  "$paper_dir/submission/bootstrap_replay.sh"

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

echo "PASS: manifests, fail-closed hashed replay, deterministic PDF rebuild, and PDF identity"
