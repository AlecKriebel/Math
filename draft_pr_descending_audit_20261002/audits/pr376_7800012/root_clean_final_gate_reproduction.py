"""Root's read-only private reproduction of the final actual-head gate."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess

A=Path(__file__).resolve().parent
D=A/'clean_final_adversary'
W=A/'tmp/root_clean_final_control'
assert not W.exists(), 'Preserve earlier runs.'
W.mkdir(parents=True)
C=W/'control'; C.mkdir()
def sha(b): return hashlib.sha256(b).hexdigest()
def binding(p,e):
    b=p.read_bytes(); assert len(b)==e['bytes'] and sha(b)==e['sha256'],str(p)
    return b
mf=json.loads((D/'PUBLIC_MANIFEST.json').read_text())
assert len(mf['files'])==139 and mf['audit_completion_percent']==100
before={str(D/'PUBLIC_MANIFEST.json'):sha((D/'PUBLIC_MANIFEST.json').read_bytes())}
for e in mf['files']:
    assert not {'tmp','private','raw_sources'} & set(Path(e['path']).parts)
    p=D/e['path']; b=binding(p,e); before[str(p)]=sha(b)
    q=C/e['path']; q.parent.mkdir(parents=True,exist_ok=True); q.write_bytes(b)
history=json.loads((D/'CHECKPOINT_90_PRESERVATION.json').read_text())
oldmf=D/history['archived_manifest']
assert sha(oldmf.read_bytes())==history['manifest_sha256']
old=json.loads(oldmf.read_text()); assert len(old['files'])==57
for e in old['files']: binding(D/'checkpoint_90'/e['path'],e)
assert len(history['mapping'])==57
for e in history['mapping']: binding(D/e['archived_path'],e)
pending=json.loads((D/'FINAL_METADATA_UPDATE_MAPPING.json').read_text())
assert len(pending['prior_versions'])==5
for e in pending['prior_versions']: binding(D/e['archived_path'],e)
seals=[]
for folder in [D,D/'checkpoint_90']:
    for name in ['BASELINE_SEALED.sha256','MATHEMATICAL_VERDICT_SEALED.sha256']:
        for line in (folder/name).read_text().splitlines():
            h,p=line.split(None,1); assert sha((folder/p.strip()).read_bytes())==h
            seals.append(dict(path=str((folder/p.strip()).relative_to(D)),sha256=h))
# Fetch observations anew: the verifier consumes these private observations,
# never the reviewer's copied captures. All Git checks remain unmodified.
commands=[
 ('finalized_live_pr376',['gh','pr','view','376','--json',','.join(sorted(json.loads((D/'streams/finalized_live_pr376.stdout').read_text())))]),
 ('final_live_pr377',['gh','pr','view','377','--json',','.join(sorted(json.loads((D/'streams/final_live_pr377.stdout').read_text())))]),
 ('final_live_commit',['gh','api','repos/AlecKriebel/Math/git/commits/b19a834793c4b1acef3c6a48fa66299170df8560']),
 ('final_remote_refs',['git','ls-remote','origin','refs/heads/main','refs/heads/dot/math-7800012'])]
observations=[]
for tag,cmd in commands:
    r=subprocess.run(cmd,capture_output=True)
    (A/('root_final_'+tag+'.stdout')).write_bytes(r.stdout)
    (A/('root_final_'+tag+'.stderr')).write_bytes(r.stderr)
    assert r.returncode==0 and not r.stderr,(tag,r.stderr.decode())
    (C/'streams'/(tag+'.stdout')).write_bytes(r.stdout)
    expected=(D/'streams'/(tag+'.stdout')).read_bytes()
    if tag=='final_remote_refs': assert r.stdout==expected
    else: assert json.loads(r.stdout)==json.loads(expected),tag
    observations.append(dict(tag=tag,bytes=len(r.stdout),sha256=sha(r.stdout),fresh_observation_matches=True))
code=(C/'final_integration.py').read_text()
needle='R=pathlib.Path(__file__).parent;A=R.parent;REPO='
assert code.count(needle)==1
code=code.replace(needle,'R=pathlib.Path(__file__).parent;A=pathlib.Path('+repr(str(A))+');REPO=')
(C/'final_integration.py').write_text(code)
r=subprocess.run(['python3','-B',str(C/'final_integration.py')],cwd=C,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
(A/'root_final_integration.stdout').write_bytes(r.stdout)
(A/'root_final_integration.stderr').write_bytes(r.stderr)
assert r.returncode==0 and not r.stderr,r.stderr.decode()
assert r.stdout==(D/'streams/finalized_integration.stdout').read_bytes()
actual=json.loads((C/'FINAL_INTEGRATION_CERTIFICATE.json').read_text())
expected=json.loads((D/'FINAL_INTEGRATION_CERTIFICATE.json').read_text())
actual.pop('at');expected.pop('at');assert actual==expected
assert all(sha(Path(p).read_bytes())==h for p,h in before.items())
math=json.loads((A/'root_clean_mathematical_reproduction_receipt.json').read_text())
assert math['status']=='PASS' and math['public_manifest_sha256']==history['manifest_sha256']
for e in json.loads((A/'repaired_snapshot_manifest.json').read_text())['files']:
    if e['path'].startswith('unsolved_math_prioritization/attempts/7800012/'):
        assert (A/'repaired_snapshot'/e['path']).read_bytes()==(A/'snapshot'/e['path']).read_bytes()
receipt=dict(status='PASS',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),workflow_percent=100,original_resolution_percent=0,public_files=139,public_manifest_sha256=sha((D/'PUBLIC_MANIFEST.json').read_bytes()),checkpoint90_members=57,pending100_versions=5,seals=seals,observations=observations,full_stdout_byte_exact=True,complete_certificate_equal_except_utc=True,all51_git_bindings=True,target50_and_math_reproduced_unchanged=True,nested210=True,queue_only_two_cells=True,reviewer_files_unchanged=True,private_input_redirection_only=True)
(A/'root_clean_final_gate_reproduction_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
