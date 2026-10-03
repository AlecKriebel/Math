#!/usr/bin/env python3
"""Read-only author replay; full stdout/stderr stay in private audit storage."""
from pathlib import Path
import hashlib,json,os,subprocess,sys,time
HERE=Path(__file__).absolute().parent.parent
SOURCE=HERE.parent/'snapshot/unsolved_math_prioritization/attempts/7800012'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
before={str(p.relative_to(SOURCE)):sha(p) for p in SOURCE.rglob('*') if p.is_file()}
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
records=[]
for name in [*(f'verify_turn{n}.py' for n in range(1,6)),'hessian_certificate.py','REPLAY_ALL.py']:
    start=time.monotonic()
    p=subprocess.run([sys.executable,'-B',str(SOURCE/name)],cwd=SOURCE,env=env,capture_output=True)
    output=HERE/'private'/f'{name}.stdout'
    error=HERE/'private'/f'{name}.stderr'
    output.write_bytes(p.stdout);error.write_bytes(p.stderr)
    record={'program':name,'exit_code':p.returncode,'elapsed_seconds':round(time.monotonic()-start,6),'stdout_bytes':len(p.stdout),'stdout_sha256':sha(output),'stderr_bytes':len(p.stderr),'stderr_sha256':sha(error)}
    if name.startswith('verify_turn') and p.returncode==0:
        record['exact_author_output_match']=p.stdout==(SOURCE/f'TURN_{name[11]}_CHECKS.json').read_bytes()
        record['summary']=json.loads(p.stdout)
    elif name=='REPLAY_ALL.py' and p.returncode==0: record['summary']=json.loads(p.stdout)
    elif name=='hessian_certificate.py' and p.returncode==0:
        record['exact_author_certificate_match']=json.loads(p.stdout)==json.loads((SOURCE/'TURN_4_CERTIFICATE.json').read_bytes())
    records.append(record)
after={str(p.relative_to(SOURCE)):sha(p) for p in SOURCE.rglob('*') if p.is_file()}
receipt={'status':'PASS' if all(r['exit_code']==0 and r.get('exact_author_output_match',True) and r.get('exact_author_certificate_match',True) for r in records) and before==after else 'FAIL','candidate_unchanged':before==after,'candidate_file_count':len(before),'python':sys.executable,'primary_source_replay':'NOT RUN (independent online source-first read, not frozen local source hashes)','programs':records}
(HERE/'receipts/author_replay.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps(receipt,indent=2,sort_keys=True))
