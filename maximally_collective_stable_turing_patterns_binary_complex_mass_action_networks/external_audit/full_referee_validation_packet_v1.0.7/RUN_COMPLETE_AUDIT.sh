#!/usr/bin/env bash
set -euo pipefail

PACKET_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$PACKET_ROOT"

required_commands=(python bash cp cmp mktemp pdflatex biber pdffonts sha256sum awk grep find sort xargs tail)
for command_name in "${required_commands[@]}"; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    printf 'missing required command: %s\n' "$command_name" >&2
    exit 2
  fi
done

export PYTHONOPTIMIZE=0
python - <<'PY'
import sys
if sys.flags.optimize:
    raise SystemExit("Assertions are disabled; do not use python -O")
PY

echo '[1/7] pristine outer and inner integrity'
sha256sum -c SHA256SUMS.txt
(
  cd repository
  sha256sum -c sha256_manifest.txt >/dev/null
)
cmp paper/main.pdf repository/manuscript/main.pdf
cmp paper/supplement.pdf repository/manuscript/supplement.pdf

echo '[2/7] disposable working trees'
WORK_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/exact-diffusion-referee.XXXXXX")"
cp -a repository "$WORK_ROOT/repository"
cp -a minimal_verifier "$WORK_ROOT/minimal_verifier"
printf 'WORK_ROOT=%s\n' "$WORK_ROOT"

echo '[3/7] minimal exact replay'
bash "$WORK_ROOT/minimal_verifier/replay.sh"

echo '[4/7] complete portable replay'
bash "$WORK_ROOT/repository/replay.sh"

echo '[5/7] every supplied verifier entrypoint'
python RUN_ALL_VERIFIERS.py "$WORK_ROOT/repository"

echo '[6/7] supplemental source and stale-claim audits'
(
  cd "$WORK_ROOT/repository"
  python computation/audit_manuscript.py
  python computation/audit_stale_claims.py
  python computation/audit_numerical_provenance.py
  python computation/audit_pdfs.py --profile public
  python -m pytest -q computation/tests
  sha256sum -c sha256_manifest.txt >/dev/null
)

echo '[7/7] completion'
printf 'Regenerated working copy retained at %s\n' "$WORK_ROOT"
echo REFEREE_PACKET_COMPLETE_AUDIT_PASS
