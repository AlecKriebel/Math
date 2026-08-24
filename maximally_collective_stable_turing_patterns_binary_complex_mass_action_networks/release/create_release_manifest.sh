#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
MANIFEST=release/sha256_manifest.txt

if [[ "${1:-}" == "--check" ]]; then
  sha256sum -c "$MANIFEST" >/dev/null
  grep -Fq '  ./RESEARCH_LOG.md' "$MANIFEST"
  printf 'RELEASE_MANIFEST_PASS entries=%s\n' "$(wc -l < "$MANIFEST")"
  exit 0
fi

temporary_manifest="$(mktemp "$ROOT/release/.sha256_manifest.XXXXXX")"
trap 'rm -f "$temporary_manifest"' EXIT
find . -type f \
  ! -name '.DS_Store' \
  ! -path './release/replay.log' \
  ! -path './release/sha256_manifest.txt' \
  ! -path './release/.sha256_manifest.*' \
  ! -path '*/.pytest_cache/*' \
  ! -path '*/__pycache__/*' \
  ! -name '*.pyc' \
  \( ! -name '*.log' -o -path './release/build_logs/*.log' -o -path './release/public_full_replay.log' \) \
  ! -name '*.aux' ! -name '*.bcf' ! -name '*.blg' ! -name '*.fls' \
  ! -name '*.fdb_latexmk' ! -name '*.run.xml' ! -name '*.out' \
  ! -name '*.toc' ! -name '*.xdv' \
  -print0 | sort -z | xargs -0 sha256sum > "$temporary_manifest"
grep -Fq '  ./RESEARCH_LOG.md' "$temporary_manifest"
mv "$temporary_manifest" "$MANIFEST"
trap - EXIT
sha256sum -c "$MANIFEST" >/dev/null
printf 'RELEASE_MANIFEST_CREATED entries=%s\n' "$(wc -l < "$MANIFEST")"
