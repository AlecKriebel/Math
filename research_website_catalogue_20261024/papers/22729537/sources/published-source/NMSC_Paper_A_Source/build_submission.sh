#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
TECTONIC="${NMSC_TECTONIC:-tectonic}"
export SOURCE_DATE_EPOCH=1787875200

(
  cd "$ROOT/manuscript"
  "$TECTONIC" --only-cached --keep-logs main.tex
)
(
  cd "$ROOT/supplement"
  "$TECTONIC" --only-cached --keep-logs technical_supplement.tex
)
(
  cd "$ROOT/navigation"
  "$TECTONIC" --only-cached --keep-logs technical_summary.tex
  "$TECTONIC" --only-cached --keep-logs theorem_graph.tex
)

printf 'SUBMISSION_SOURCE_BUILD_PASS\n'
