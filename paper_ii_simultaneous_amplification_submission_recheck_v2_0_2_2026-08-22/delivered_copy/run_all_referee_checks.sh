#!/bin/sh
set -eu

package_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
bootstrap_python=${BOOTSTRAP_PYTHON:-python3}
tmp_base=${TMPDIR:-/tmp}
export PYTHONDONTWRITEBYTECODE=1

case "$tmp_base" in
  /) tmp_base=/tmp ;;
  /*/) tmp_base=${tmp_base%/} ;;
  /*) ;;
  *) echo "TMPDIR must be an absolute path: $tmp_base" >&2; exit 2 ;;
esac

"$bootstrap_python" -c '
import sys
if sys.flags.optimize != 0:
    raise SystemExit(
        "ERROR: optimized Python is unsupported because verification checks must remain active"
    )
if sys.version_info[:3] != (3, 14, 6):
    raise SystemExit(f"ERROR: Python 3.14.6 is required; found {sys.version}")
'

"$bootstrap_python" "$package_dir/verify_referee_package.py"

for command_name in tectonic pdfinfo pdftoppm; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    echo "Missing required document tool: $command_name" >&2
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

work_dir=$(mktemp -d "$tmp_base/paper2-referee.XXXXXX")
cleanup() {
  case "$work_dir" in
    "$tmp_base"/paper2-referee.*) rm -rf -- "$work_dir" ;;
    *) echo "Refusing to remove unexpected work directory: $work_dir" >&2 ;;
  esac
}
trap cleanup EXIT HUP INT TERM

cp -R "$package_dir/source_and_certificates/." "$work_dir/"
paper_dir="$work_dir/universal_simultaneous_amplification/phase4_landmark_closure/paper_hybrid_threshold"

PIP_NO_INDEX=1 BOOTSTRAP_PYTHON="$bootstrap_python" \
  "$paper_dir/bootstrap_replay.sh"
rebuilt_archive="$work_dir/rebuilt-source-and-certificates.tar.gz"
PYTHON="$work_dir/universal_simultaneous_amplification/.venv-paper2/bin/python" \
  "$paper_dir/release_bundle.sh" "$rebuilt_archive"
cmp \
  "$package_dir/simultaneous_amplifier_beyond_three_halves_source_and_certificates.tar.gz" \
  "$rebuilt_archive"
cmp \
  "$package_dir/simultaneous_amplification_beyond_three_halves.pdf" \
  "$paper_dir/output/pdf/simultaneous_amplification_beyond_three_halves.pdf"

"$bootstrap_python" - \
  "$rebuilt_archive" \
  "$paper_dir/output/pdf/simultaneous_amplification_beyond_three_halves.pdf" <<'PY'
from pathlib import Path
import hashlib
import sys

archive = Path(sys.argv[1])
pdf = Path(sys.argv[2])
print(f"REBUILT_SOURCE_ARCHIVE_SHA256: {hashlib.sha256(archive.read_bytes()).hexdigest()}")
print(f"REBUILT_PDF_SHA256: {hashlib.sha256(pdf.read_bytes()).hexdigest()}")
PY

echo "PASS: manifests, pinned replay, deterministic archive/PDF rebuilds, and identities"
