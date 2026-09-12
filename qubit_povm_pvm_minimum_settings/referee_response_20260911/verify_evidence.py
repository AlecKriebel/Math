#!/usr/bin/env python3
"""Verify this response's recorded checks and unchanged certified proof inputs.

Does not rerun Lean or rewrite any production receipt. Commands for rerunning
Lean, artifact arithmetic and PDF builds are in RESPONSE.md.
"""
from pathlib import Path
import hashlib,json,re
ROOT=Path(__file__).resolve().parent
PROGRAM=ROOT.parent
LEAN=PROGRAM/'bell_lean'
RUN=LEAN/'reports/runs/20260911T022153Z-2ea5f99b'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
r=json.loads((RUN/'kernel_report.json').read_text())
assert r['status']=='passed' and r['last_stage']=='complete'
assert all(sha(LEAN/k)==v for k,v in r['source_snapshot'].items())
assert all(sha(LEAN/c['log'])==c['log_sha256'] for c in r['commands'])
for name in ('counterexample_lean','matrix_contract_lean'):
 s=(ROOT/'evidence'/f'{name}.log').read_text()
 assert not re.search(r'\berror:|sorryAx|PANIC',s)
 assert 'depends on axioms:' in s
 for axes in re.findall(r'depends on axioms: \[([^]]*)\]',s):
  assert set(map(str.strip,axes.split(','))) <= {'propext','Classical.choice','Quot.sound'}
assert 'All exact reproducibility checks passed' in (ROOT/'evidence/exact_verification.log').read_text()
assert 'Built warning-free main.pdf and review.pdf.' in (ROOT/'evidence/paper_build.log').read_text()
assert 'Writing' in (ROOT/'evidence/arxiv_build.log').read_text()
assert 'warning:' not in (ROOT/'evidence/arxiv_build.log').read_text().lower()
tex=(PROGRAM/'paper/main.tex').read_text()
assert 'These inequalities alone do not imply signature' in tex
paths=['paper/main.tex','paper/appendices.tex','paper/main.pdf','paper/review.pdf','submission/arxiv_source.tar.gz',
 'referee_2026-09-11/computations/StrictDomainCounterexample.lean','referee_2026-09-11/contracts/MatrixModelContract.lean']
report={'status':'passed','original_certified_run':r['run_id'],
 'production_snapshot_files_unchanged':len(r['source_snapshot']),
 'original_command_logs_rehashed':len(r['commands']),
 'fresh_full_675_theorem_audit_performed_in_this_response':False,
 'reason':'Production proof, verifier, and contract inputs are unchanged; retained complete receipt rehashed. Counterexample and independent matrix-model contract rechecked separately.',
 'current_artifact_sha256':{n:sha(PROGRAM/n) for n in paths},
 'response_log_sha256':{p.name:sha(p) for p in sorted((ROOT/'evidence').glob('*.log'))}}
(ROOT/'evidence/verification.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS: unchanged certified inputs, retained full receipt, new Lean checks, exact arithmetic, and PDF build evidence.')
