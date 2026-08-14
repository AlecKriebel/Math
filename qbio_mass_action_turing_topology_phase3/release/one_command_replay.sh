#!/usr/bin/env bash
set -euo pipefail

# Keep exact replay deterministic and avoid BLAS thread oversubscription in
# constrained validation containers.
export PYTHONUNBUFFERED=1
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RELEASE="$ROOT/release"
mkdir -p "$RELEASE"

say() { printf '[phase3] %s\n' "$*"; }

say "verifying frozen inherited archives"
printf '%s  %s\n' \
  'ea8c640f199549710ac1e8de0b896300adfa9be0bdde64753d06b7ada94a5f10' \
  "$ROOT/frozen_inputs/qbio_mass_action_turing_topology_TALG.zip" \
  'dd9be02c8e530b0f603d92029b15cc3fdb2443aa188fa1b41ff8e0d31c60a828' \
  "$ROOT/frozen_inputs/qbio_mass_action_turing_topology.zip" \
  | sha256sum -c -

say "checking Python dependencies and compiling independent sources"
python - <<'PY'
import importlib
for name in ('sympy', 'numpy', 'scipy'):
    module = importlib.import_module(name)
    print(f'{name}={getattr(module, "__version__", "unknown")}')
PY
python -m compileall -q "$ROOT/independent_verifier" "$ROOT/red_team" "$ROOT/strengthening/robust_crossing"

say "running independent unit tests and all falsifier campaigns in parallel"
(
  cd "$ROOT"
  python -m unittest discover -s independent_verifier/tests -v
) >"$RELEASE/independent_all_tests.log" 2>&1 &
pid_tests=$!
(
  cd "$ROOT"
  python red_team/fixed_n_falsifier.py
) >"$RELEASE/fixed_n_falsifier.stdout" 2>&1 &
pid_fixedn=$!
(
  cd "$ROOT"
  python red_team/fixed_j_falsifier.py \
    --random 1000 \
    --seed 20260813 \
    --output release/fixed_j_falsifier_smoke.json
) >"$RELEASE/fixed_j_falsifier_full.stdout" 2>&1 &
pid_fixedj_a=$!
(
  cd "$ROOT"
  python red_team/fixed_j_falsifier.py \
    --skip-exhaustive \
    --random 4000 \
    --seed 20260814 \
    --output release/fixed_j_falsifier_random4000.json
) >"$RELEASE/fixed_j_falsifier_random4000.stdout" 2>&1 &
pid_fixedj_b=$!
(
  cd "$ROOT"
  python red_team/conservation_falsifier.py
) >"$RELEASE/conservation_falsifier.json" 2>&1 &
pid_conservation=$!
(
  cd "$ROOT"
  python red_team/selector_falsifier.py
) >"$RELEASE/selector_falsifier.json" 2>&1 &
pid_selector=$!
(
  cd "$ROOT"
  python red_team/row_realization_falsifier.py
) >"$RELEASE/row_realization_falsifier.json" 2>&1 &
pid_row=$!
(
  cd "$ROOT"
  python red_team/partition_reduction_falsifier.py
) >"$RELEASE/partition_reduction_falsifier.json" 2>&1 &
pid_partition=$!
(
  cd "$ROOT"
  python red_team/mobile_falsifier.py
) >"$RELEASE/mobile_falsifier.stdout" 2>&1 &
pid_mobile=$!

for pid in \
  "$pid_tests" "$pid_fixedn" "$pid_fixedj_a" "$pid_fixedj_b" \
  "$pid_conservation" "$pid_selector" "$pid_row" "$pid_partition" "$pid_mobile"; do
  wait "$pid"
done

cat "$RELEASE/independent_all_tests.log"
grep -q '^OK$' "$RELEASE/independent_all_tests.log"
for file in \
  fixed_n_falsifier.stdout \
  fixed_j_falsifier_full.stdout fixed_j_falsifier_random4000.stdout \
  conservation_falsifier.json selector_falsifier.json \
  row_realization_falsifier.json partition_reduction_falsifier.json \
  mobile_falsifier.stdout; do
  printf '%s\n' "--- $file ---"
  cat "$RELEASE/$file"
done

say "checking all machine-readable falsifier statuses"
python - "$RELEASE" <<'PY'
import json
import sys
from pathlib import Path
release = Path(sys.argv[1])
files = [
    'fixed_j_falsifier_smoke.json',
    'fixed_j_falsifier_random4000.json',
    'conservation_falsifier.json',
    'selector_falsifier.json',
    'row_realization_falsifier.json',
    'partition_reduction_falsifier.json',
    'fixed_n_falsifier.json',
    'mobile_falsifier.json',
]
for name in files:
    data = json.loads((release / name).read_text())
    if data.get('status') != 'PASS':
        raise SystemExit(f'{name}: status={data.get("status")!r}')
    print(f'{name}: PASS')
PY

say "verifying compact external-audit YES and NO examples"
(
  cd "$ROOT"
  python external_audit/minimal_verifier.py external_audit/yes_partition_1_1.json
) >"$ROOT/external_audit/yes_verification.json"
cat "$ROOT/external_audit/yes_verification.json"
(
  cd "$ROOT"
  python external_audit/minimal_verifier.py external_audit/no_partition_1_2.json
) >"$ROOT/external_audit/no_verification.json"
cat "$ROOT/external_audit/no_verification.json"

say "rebuilding all journal and external-audit PDFs in parallel"
(
  cd "$ROOT/manuscript"
  pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
  BIBINPUTS=".:${BIBINPUTS:-}" bibtex8 main >/dev/null
  pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
  pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null
) &
pid_main=$!
(
  cd "$ROOT/manuscript"
  pdflatex -interaction=nonstopmode -halt-on-error supplement.tex >/dev/null
  pdflatex -interaction=nonstopmode -halt-on-error supplement.tex >/dev/null
) &
pid_supplement=$!
(
  cd "$ROOT/external_audit"
  pdflatex -interaction=nonstopmode -halt-on-error theorem_summary.tex >/dev/null
  pdflatex -interaction=nonstopmode -halt-on-error theorem_summary.tex >/dev/null
) &
pid_summary=$!
(
  cd "$ROOT/external_audit"
  pdflatex -interaction=nonstopmode -halt-on-error proof_skeleton.tex >/dev/null
  pdflatex -interaction=nonstopmode -halt-on-error proof_skeleton.tex >/dev/null
) &
pid_skeleton=$!
for pid in "$pid_main" "$pid_supplement" "$pid_summary" "$pid_skeleton"; do
  wait "$pid"
done

say "checking PDF page counts and LaTeX references"
python - "$ROOT" <<'PY'
import re
import subprocess
import sys
from pathlib import Path
root = Path(sys.argv[1])
expected = {
    root / 'manuscript/main.pdf': 10,
    root / 'manuscript/supplement.pdf': 16,
    root / 'external_audit/theorem_summary.pdf': 2,
    root / 'external_audit/proof_skeleton.pdf': 5,
}
for path, pages in expected.items():
    if not path.exists() or path.stat().st_size == 0:
        raise SystemExit(f'missing PDF: {path}')
    out = subprocess.check_output(['pdfinfo', str(path)], text=True)
    match = re.search(r'^Pages:\s+(\d+)$', out, flags=re.MULTILINE)
    actual = int(match.group(1)) if match else None
    if actual != pages:
        raise SystemExit(f'{path}: pages={actual}, expected={pages}')
    print(f'{path.relative_to(root)}: {actual} pages')
for log in [root/'manuscript/main.log', root/'manuscript/supplement.log',
            root/'external_audit/theorem_summary.log', root/'external_audit/proof_skeleton.log']:
    text = log.read_text(errors='replace')
    forbidden = [
        'There were undefined references',
        'Citation `',
        'Reference `',
        '! LaTeX Error',
        'Emergency stop',
    ]
    hits = [x for x in forbidden if x in text]
    if hits:
        raise SystemExit(f'{log}: unresolved LaTeX diagnostics {hits}')
print('LaTeX references: PASS')
PY

say "auditing mandatory Phase III project tree"
python - "$ROOT" <<'PY'
import sys
from pathlib import Path
root = Path(sys.argv[1])
required = [
'STATE.md','CLAIM_LEDGER.md','DEPENDENCY_GRAPH.md',
'independent_proofs/fixed_j_theorem.tex',
'independent_proofs/conservative_reduction.tex',
'independent_proofs/semialgebraic_characterization.tex',
'independent_proofs/selector_encoding.tex',
'independent_proofs/row_segment_realization.tex',
'independent_proofs/open_cube_partition.tex',
'independent_proofs/row_splitting.tex',
'independent_proofs/scaling_elimination.tex',
'independent_proofs/mass_action_hardness.tex',
'independent_proofs/fixed_species_algorithm.tex',
'independent_proofs/certificate_completeness.tex',
'red_team/counterexample_catalog.md',
'red_team/fixed_j_falsifier.py',
'red_team/row_realization_falsifier.py',
'red_team/partition_reduction_falsifier.py',
'red_team/fixed_n_falsifier.py',
'red_team/conservation_falsifier.py',
'red_team/selector_falsifier.py',
'priority_audit/search_protocol.md',
'priority_audit/result_ledger.csv',
'priority_audit/closest_results.md',
'priority_audit/novelty_matrix.md',
'priority_audit/expert_questions.md',
'strengthening/bounded_molecularity/README.md',
'strengthening/strong_hardness/README.md',
'strengthening/existential_real_hardness/README.md',
'strengthening/robust_crossing/README.md',
'strengthening/practical_fixed_n/README.md',
'independent_verifier/README.md',
'independent_verifier/network_parser.py',
'independent_verifier/mass_action_jacobian.py',
'independent_verifier/partition_reduction.py',
'independent_verifier/fixed_n_projection.py',
'independent_verifier/tests/test_core.py',
'independent_verifier/tests/test_certificates.py',
'manuscript/main.tex','manuscript/main.pdf',
'manuscript/supplement.tex','manuscript/supplement.pdf',
'manuscript/references.bib',
'external_audit/theorem_summary.pdf','external_audit/proof_skeleton.pdf',
'external_audit/minimal_verifier.py',
'release/FINAL_REPORT.md','release/reproducibility.md','release/one_command_replay.sh',
]
missing = [p for p in required if not (root/p).is_file()]
if missing:
    raise SystemExit('missing required files:\n' + '\n'.join(missing))
print(f'mandatory files: {len(required)} PASS')
PY

say "writing SHA-256 manifest"
(
  cd "$ROOT"
  find . -type f \
    ! -path './release/sha256_manifest.txt' \
    ! -path './release/replay.log' \
    ! -path '*/__pycache__/*' \
    ! -name '*.pyc' \
    -print0 \
    | sort -z \
    | xargs -0 sha256sum > release/sha256_manifest.txt
)

say "all independent Phase III gates passed"
