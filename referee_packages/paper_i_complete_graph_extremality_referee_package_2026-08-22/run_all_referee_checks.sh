#!/bin/sh
set -eu

package_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
bootstrap_python=${BOOTSTRAP_PYTHON:-python3}
tmp_base=${TMPDIR:-/tmp}
tmp_base=${tmp_base%/}

"$bootstrap_python" "$package_dir/verify_referee_package.py"

for command_name in make tectonic pdfinfo pdftoppm; do
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

BOOTSTRAP_PYTHON="$bootstrap_python" \
  "$paper_dir/submission/bootstrap_replay.sh"

"$paper_dir/build.sh"
cmp \
  "$package_dir/complete_graph_extremality_db.pdf" \
  "$paper_dir/output/pdf/complete_graph_extremality_db.pdf"

"$bootstrap_python" - "$paper_dir/output/pdf/complete_graph_extremality_db.pdf" <<'PY'
from pathlib import Path
import hashlib
import sys

pdf = Path(sys.argv[1])
print(f"REBUILT_PDF_SHA256: {hashlib.sha256(pdf.read_bytes()).hexdigest()}")
PY

echo "PASS: manifests, pinned replay, deterministic PDF rebuild, and PDF identity"
