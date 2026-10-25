#!/usr/bin/env bash
set -euo pipefail

PACKAGE_ROOT="$(cd "$(dirname "$0")/.." && pwd -P)"
REPO_ROOT="$(git -C "$PACKAGE_ROOT" rev-parse --show-toplevel)"
PACKAGE_REL="${PACKAGE_ROOT#"$REPO_ROOT"/}"
ARCHIVE_REL="${PACKAGE_REL}.zip"
PYTHON_BIN="${BIMOL_PYTHON:-python3}"
EXPECTED_TAG="bimolecular-positive-recurrence-v1.2.4"

HEAD_COMMIT="$(git -C "$REPO_ROOT" rev-parse HEAD)"
if ! tag="$(git -C "$REPO_ROOT" describe --tags --exact-match HEAD 2>/dev/null)"; then
  echo "ERROR: release replay requires exact tag $EXPECTED_TAG; HEAD $HEAD_COMMIT is untagged." >&2
  exit 1
fi
if [[ "$tag" != "$EXPECTED_TAG" ]]; then
  echo "ERROR: expected exact tag $EXPECTED_TAG, found $tag." >&2
  exit 1
fi
if ! git -C "$REPO_ROOT" rev-parse --verify \
  "refs/tags/${EXPECTED_TAG}^{tag}" >/dev/null 2>&1; then
  echo "ERROR: $EXPECTED_TAG must be an annotated tag." >&2
  exit 1
fi
TAG_COMMIT="$(git -C "$REPO_ROOT" rev-parse --verify "${EXPECTED_TAG}^{commit}")"
if [[ "$TAG_COMMIT" != "$HEAD_COMMIT" ]]; then
  echo "ERROR: $EXPECTED_TAG does not identify checked-out commit $HEAD_COMMIT." >&2
  exit 1
fi

cd "$PACKAGE_ROOT"

echo "VERSION 1.2.4 RELEASE REPLAY"
echo "Commit: $HEAD_COMMIT"
echo "Exact annotated tag: $tag"
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
echo "PASS: complete Version 1.2.4 release replay"
