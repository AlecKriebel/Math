#!/usr/bin/env bash
set -euo pipefail

PACKAGE_ROOT="$(cd "$(dirname "$0")/.." && pwd -P)"
REPO_ROOT="$(git -C "$PACKAGE_ROOT" rev-parse --show-toplevel)"
PACKAGE_REL="${PACKAGE_ROOT#"$REPO_ROOT"/}"
ARCHIVE_REL="${PACKAGE_REL}.zip"
PYTHON_BIN="${BIMOL_PYTHON:-python3}"

cd "$PACKAGE_ROOT"

echo "VERSION 1.2.1 RELEASE REPLAY"
echo "Commit: $(git -C "$REPO_ROOT" rev-parse HEAD)"
if tag="$(git -C "$REPO_ROOT" describe --tags --exact-match 2>/dev/null)"; then
  echo "Exact tag: $tag"
else
  echo "Exact tag: none"
fi
echo "Python: $($PYTHON_BIN --version 2>&1)"
echo "Tectonic: $(tectonic --version 2>&1)"
echo "Platform: $(uname -srm)"

BIMOL_PYTHON="$PYTHON_BIN" code/reproduce.sh
"$PYTHON_BIN" -m unittest supplement/test_release_tools.py -v
"$PYTHON_BIN" supplement/verify_manifest.py
cmp supplement/MANIFEST.sha256 validation/MANIFEST.sha256
cmp code/verification_report.json supplement/verification_report.json
cmp code/verification_report.json validation/VERIFICATION_REPORT.json
manuscript/build.sh
"$PYTHON_BIN" supplement/build_release_archive.py --check

"$PYTHON_BIN" - \
  code/verification_report.json \
  supplement/MANIFEST.sha256 \
  manuscript/main_arxiv.pdf \
  manuscript/main_biorxiv.pdf \
  manuscript/main_jap.pdf \
  manuscript/supplementary_note.pdf \
  "../$ARCHIVE_REL" <<'PY'
from hashlib import sha256
from pathlib import Path
import sys

for raw in sys.argv[1:]:
    path = Path(raw)
    print(f"{sha256(path.read_bytes()).hexdigest()}  {path}")
PY

git -C "$REPO_ROOT" diff --exit-code -- "$PACKAGE_REL" "$ARCHIVE_REL"
status="$(git -C "$REPO_ROOT" status --porcelain=v1 --untracked-files=all -- "$PACKAGE_REL" "$ARCHIVE_REL")"
if [[ -n "$status" ]]; then
  echo "release replay left a nonclean package/archive status:" >&2
  echo "$status" >&2
  exit 1
fi
echo "PASS: complete Version 1.2.1 release replay"
