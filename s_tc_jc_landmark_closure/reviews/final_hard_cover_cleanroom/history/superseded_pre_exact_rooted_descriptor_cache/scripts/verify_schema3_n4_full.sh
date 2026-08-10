#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-/opt/homebrew/bin/python3}"
SYMPY_SITE="${SYMPY_SITE:-/Users/alec/Library/Python/3.9/lib/python/site-packages}"
export PYTHONPATH="$HERE:$SYMPY_SITE${PYTHONPATH:+:$PYTHONPATH}"
cd "$ROOT"

"$PYTHON_BIN" "$HERE/audit_candidate_stream.py" \
  --relations primary/certificates/hard_cover_n4_schema3_theta2_full.jsonl.gz \
  --graphs primary/certificates/hard_cover_graphs_n4_schema3_theta2_full.jsonl.gz \
  --roots primary/certificates/hard_cover_root_cases_n4_schema3_theta2_full.jsonl.gz \
  --family-tag n4_minimum \
  --output "$HERE/certificates/schema3_n4_theta2_full_audit.json" \
  --terminal-records-output "$HERE/certificates/schema3_n4_theta2_terminal_records.jsonl.gz"
"$PYTHON_BIN" "$HERE/mutation_schema3_stream.py"
"$PYTHON_BIN" "$HERE/audit_probe_extension_structure.py"
"$PYTHON_BIN" "$HERE/audit_probe_extension_algebra.py"
"$PYTHON_BIN" "$HERE/mutation_probe_extension.py"
"$PYTHON_BIN" "$HERE/verify_schema3_n4_certificates.py"
