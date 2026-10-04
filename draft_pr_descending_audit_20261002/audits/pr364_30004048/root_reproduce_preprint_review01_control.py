"""ROOT fresh full reproduction of the new ordinary-graph census.

Write lossless captures outside the sealed review; read and compare all output.
"""
from pathlib import Path
import datetime,hashlib,json,os,subprocess
A=Path(__file__).resolve().parent;B=A/'preprint_review_01'
D=A/'root_replay_private/preprint01_control_reproduction_001'
D.mkdir(parents=True,exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest()
utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
assert sha((B/'FINAL_SEAL.json').read_bytes())=='fb2c374ddcf1d40f8c24949c8d89ee1b57f293c4d1bb4054b646ac9cdcf27677'
before={p.relative_to(B).as_posix():sha(p.read_bytes()) for p in B.rglob('*') if p.is_file()}
cmd=['python3','-B',str(B/'independent_controls.py')]
start=utc();r=subprocess.run(cmd,cwd=B,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'));end=utc()
(D/'stdout').write_bytes(r.stdout);(D/'stderr').write_bytes(r.stderr)
e={'argv':cmd,'cwd':str(B),'started_utc':start,'finished_utc':end,'exit_code':r.returncode,'program_sha256':sha((B/'independent_controls.py').read_bytes()),'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'stderr_bytes':len(r.stderr),'stderr_sha256':sha(r.stderr),'logical_stream_sha256':sha(b'STDOUT\0'+r.stdout+b'STDERR\0'+r.stderr)}
(D/'EXECUTION.json').write_text(json.dumps(e,indent=2)+'\n')
assert r.returncode==0 and r.stderr==b'' and r.stdout==(B/'CONTROLS.json').read_bytes()
assert before=={p.relative_to(B).as_posix():sha(p.read_bytes()) for p in B.rglob('*') if p.is_file()}
obj=json.loads(r.stdout);assert obj['status']=='PASS' and obj['assertions']==188472 and obj['census_pairs']==53919649
receipt={'utc':utc(),'status':'PASS_ROOT_FULL_NEW_CENSUS_REPRODUCTION','entire_stdout_identical':True,'closed_review_namespace_unchanged':True,'execution':e,'control_result':obj,'program_sha256':sha(Path(__file__).read_bytes()),'scope':'Finite ordinary graph falsification census plus repeated-column and ceiling controls, not a universal proof, invariant minimization or novelty certificate.'}
(A/'ROOT_PREPRINT_REVIEW01_CONTROL_REPRODUCTION.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
