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

paper_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo_root=$(CDPATH= cd -- "$paper_dir/../../.." && pwd)
bootstrap_python=${BOOTSTRAP_PYTHON:-python3}
default_output="$paper_dir/output/release/complete_graph_extremality_db_source_and_certificates.tar.gz"
output=${1:-"$default_output"}

case "$output" in
  /*) ;;
  *) output="$PWD/$output" ;;
esac

mkdir -p "$(dirname -- "$output")"
BOOTSTRAP_PYTHON="$bootstrap_python" "$paper_dir/submission/bootstrap_replay.sh"
"$paper_dir/build.sh"
if [ -f "$paper_dir/submission/verify_submission_materials.py" ]; then
  "$bootstrap_python" -I "$paper_dir/submission/verify_submission_materials.py"
fi
"$bootstrap_python" -I "$paper_dir/bundle_manifest.py" \
  --repo-root "$repo_root" \
  --output "$output"
"$bootstrap_python" -I - "$output" <<'PY'
from __future__ import annotations

import hashlib
from pathlib import Path
import sys

archive = Path(sys.argv[1]).resolve()
sidecar = archive.with_name(f"{archive.name}.sha256")
digest = hashlib.sha256(archive.read_bytes()).hexdigest()
sidecar.write_text(f"{digest}  {archive.name}\n", encoding="ascii")
print(f"CHECKSUM: {sidecar}")
PY
