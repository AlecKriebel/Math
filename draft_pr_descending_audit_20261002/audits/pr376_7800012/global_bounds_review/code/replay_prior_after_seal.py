#!/usr/bin/env python3
"""Optional prior-check reconciliation, only after independent verdict seal."""
from pathlib import Path
import hashlib,json,os,subprocess
HERE=Path(__file__).absolute().parent.parent
SOURCE=HERE.parent/'snapshot/unsolved_math_prioritization/attempts/7800012'
PYTHON='/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python'
assert (HERE/'receipts/verdict_seal.sha256').exists()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
before={str(p.relative_to(SOURCE)):sha(p) for p in SOURCE.rglob('*') if p.is_file()}
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
records=[]
for name in ['final_review/independent_check.py','verify_review.py']:
    p=subprocess.run([PYTHON,'-B',str(SOURCE/name)],cwd=SOURCE,env=env,capture_output=True)
    out=HERE/'private'/f'{Path(name).name}.post_seal.stdout'
    err=HERE/'private'/f'{Path(name).name}.post_seal.stderr'
    out.write_bytes(p.stdout);err.write_bytes(p.stderr)
    record={'program':name,'exit_code':p.returncode,'stdout_bytes':len(p.stdout),'stdout_sha256':sha(out),'stderr_bytes':len(p.stderr),'stderr_sha256':sha(err)}
    if name.endswith('independent_check.py') and p.returncode==0:
        record['exact_prior_output_match']=p.stdout==(SOURCE/'final_review/INDEPENDENT_CHECKS.json').read_bytes()
        record['summary']=json.loads(p.stdout)
    records.append(record)
after={str(p.relative_to(SOURCE)):sha(p) for p in SOURCE.rglob('*') if p.is_file()}
receipt={'status':'PASS' if all(r['exit_code']==0 and r.get('exact_prior_output_match',True) for r in records) and before==after else 'FAIL','candidate_unchanged':before==after,'python_literal_path':PYTHON,'independence_boundary':'Prior report/checker read and executed only after independent baseline and verdict seals.','programs':records}
(HERE/'receipts/post_seal_prior_replay.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps(receipt,indent=2,sort_keys=True))
