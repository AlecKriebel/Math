#!/usr/bin/env python3
"""Check independently expanded matrix semantics against the fresh Bell build."""
from pathlib import Path
import datetime, hashlib, json, re, subprocess
HERE = Path(__file__).resolve().parent
WORK = HERE / 'work/bell_lean'
source = HERE / 'contracts/MatrixModelContract.lean'
log = HERE / 'evidence/matrix_contract.log'
build = json.loads((WORK/'reports/kernel_report.json').read_text())
if build.get('status') != 'passed':
    raise SystemExit('A successful complete fresh project build is required first.')
argv = ['lake', 'env', 'lean', str(source)]
with log.open('w') as stream:
    proc = subprocess.run(argv, cwd=WORK, stdout=stream, stderr=subprocess.STDOUT)
text = log.read_text()
match = re.search(r"'RefereeMatrixModel.explicit_complex_matrix_convex_equality' depends on axioms:\s*\[([^]]*)\]", text)
axioms = [a.strip() for a in match.group(1).split(',')] if match else None
passed = proc.returncode == 0 and axioms is not None and set(axioms) <= {'propext','Classical.choice','Quot.sound'} and not re.search(r'error:|sorryAx|declaration uses .sorry', text)
receipt = {'status': 'passed' if passed else 'failed', 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'command': argv, 'cwd': str(WORK), 'exit_code': proc.returncode, 'axioms': axioms, 'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(), 'log_sha256': hashlib.sha256(log.read_bytes()).hexdigest(), 'fresh_build_run_id': build['run_id'], 'independent_definitions':'Explicit complex matrices, PSD, trace one, POVM normalization, PVM orthogonality and idempotence, tensor entries, ordinary convexHull.'}
(HERE/'evidence/matrix_contract.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
raise SystemExit(0 if passed else 1)
