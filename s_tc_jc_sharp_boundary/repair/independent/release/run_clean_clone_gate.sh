#!/usr/bin/env bash
# Run release diagnostics in an isolated clone. This script never edits the
# caller's manuscript, submission PDFs, or reproducibility artifacts.

set -u

KEEP=0
if [[ "${1:-}" == "--keep" ]]; then
  KEEP=1
elif [[ $# -ne 0 ]]; then
  echo "usage: $0 [--keep]" >&2
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd -P)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd -P)"
REPOSITORY_ROOT="$(git -C "$PROJECT_ROOT" rev-parse --show-toplevel)"
COMMIT="$(git -C "$REPOSITORY_ROOT" rev-parse HEAD)"
PROJECT_RELATIVE="$(python3 - "$REPOSITORY_ROOT" "$PROJECT_ROOT" <<'PY'
import os
import sys
print(os.path.relpath(sys.argv[2], sys.argv[1]))
PY
)"

TEMP_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/stc-jc-release-gate.XXXXXX")"
CLONE_ROOT="$TEMP_ROOT/repository"
CLONE_PROJECT="$CLONE_ROOT/$PROJECT_RELATIVE"

cleanup() {
  if [[ "$KEEP" -eq 1 ]]; then
    echo "kept isolated clone: $TEMP_ROOT"
    return
  fi
  python3 - "$TEMP_ROOT" <<'PY'
from pathlib import Path
import shutil
import sys

path = Path(sys.argv[1]).resolve()
if not path.name.startswith("stc-jc-release-gate."):
    raise SystemExit(f"refusing to remove unexpected temporary path: {path}")
if path.exists():
    shutil.rmtree(path)
PY
}
trap cleanup EXIT

FAILURES=0

run_gate() {
  local label="$1"
  shift
  echo
  echo "===== $label ====="
  "$@"
  local status=$?
  if [[ "$status" -ne 0 ]]; then
    echo "GATE FAILED ($status): $label" >&2
    FAILURES=$((FAILURES + 1))
  else
    echo "GATE PASSED: $label"
  fi
}

echo "source repository: $REPOSITORY_ROOT"
echo "project: $PROJECT_RELATIVE"
echo "commit: $COMMIT"
echo "isolated clone: $CLONE_ROOT"

# The parent mathematics repository is large.  A shared object database plus
# cone-mode sparse checkout gives the semantics of a fresh committed checkout
# without duplicating unrelated projects or gigabytes of Git objects.
git clone --quiet --shared --no-checkout "$REPOSITORY_ROOT" "$CLONE_ROOT" || exit 1
git -C "$CLONE_ROOT" sparse-checkout init --cone || exit 1
git -C "$CLONE_ROOT" sparse-checkout set "$PROJECT_RELATIVE" || exit 1
git -C "$CLONE_ROOT" checkout --quiet --detach "$COMMIT" || exit 1

run_gate "G0 clean detached checkout" bash -c 'test -z "$(git -C "$1" status --porcelain)"' _ "$CLONE_ROOT"
run_gate "G1-G3 independent layout/status/toolchain audit" \
  python3 "$SCRIPT_DIR/audit_release_layout.py" --root "$CLONE_PROJECT"
run_gate "historical manifest verifier" \
  python3 "$CLONE_PROJECT/reproducibility/verify_integrity.py"

REQUIRED=(python3 g++ latexmk biber pdfinfo pdffonts pdftoppm)
MISSING=()
for tool in "${REQUIRED[@]}"; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    MISSING+=("$tool")
  fi
done

if [[ "${#MISSING[@]}" -ne 0 ]]; then
  echo
  echo "GATE FAILED: build/replay toolchain missing: ${MISSING[*]}" >&2
  FAILURES=$((FAILURES + 1))
else
  run_gate "historical paper build" bash "$CLONE_PROJECT/reproducibility/build_paper.sh"
  run_gate "historical quick verifier" bash "$CLONE_PROJECT/reproducibility/verify_quick.sh"
  run_gate "historical full verifier" bash "$CLONE_PROJECT/reproducibility/verify_full.sh"
fi

run_gate "G10 source tree unchanged by release commands" \
  bash -c 'test -z "$(git -C "$1" status --porcelain)"' _ "$CLONE_ROOT"

echo
if [[ "$FAILURES" -eq 0 ]]; then
  echo "CLEAN-CLONE RELEASE GATE: PASS"
  exit 0
fi
echo "CLEAN-CLONE RELEASE GATE: BLOCKED ($FAILURES failed gate(s))" >&2
exit 1
