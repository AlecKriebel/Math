"""Read-only verification of this closed review and its entire exact-current inputs."""
from pathlib import Path
import argparse,hashlib,json
p=argparse.ArgumentParser();p.add_argument('--review');p.add_argument('--audit');a=p.parse_args()
H=Path(a.review).resolve() if a.review else Path(__file__).resolve().parent;A=Path(a.audit).resolve() if a.audit else H.parent;C=A/'reviewed_candidate'
sha=lambda b:hashlib.sha256(b).hexdigest();load=lambda p:json.loads(p.read_bytes())
m=load(H/'MANIFEST.json');members=m['files'];assert len(members)==m['files_count'] and len({r['path'] for r in members})==len(members)
actual={str(p.relative_to(H)) for p in H.rglob('*') if p.is_file() and str(p.relative_to(H))!='MANIFEST.json' and not {'tmp','__pycache__'}.intersection(p.relative_to(H).parts)}
assert actual=={r['path'] for r in members},(actual-{r['path'] for r in members},{r['path'] for r in members}-actual)
parsed=0
for base,rows in [(H,members),(C,load(C/'MANIFEST.json')['files']),(A,load(C/'CURRENT_PROOF_DEPENDENCIES.json')['files'])]:
 for r in rows:
  p=base/r['path'];b=p.read_bytes();assert len(b)==r['bytes'] and sha(b)==r['sha256'],str(p)
  if p.suffix=='.json':json.loads(b);parsed+=1
  if p.suffix=='.jsonl':
   for z in b.splitlines():
    if z.strip():json.loads(z);parsed+=1
assert sha((C/'MANIFEST.json').read_bytes())=='65e7ac9d28b8504346d68c771256c2f4642c374d07bbce06bdaecfe85b8f644a'
v=load(H/'VERDICT.json');assert v['status']=='PASS_SCOPED_CURRENT_UNSOLVED_PARTIAL' and not v['literal_problem_solved'] and v['attempts']=='1/5' and v['new_substantive_attempts']==0
l=load(H/'literal_seal.json');assert l['seal_sha256']==sha((H/'LITERAL_TARGET_SEAL.md').read_bytes())
s=load(H/'proof_seal.json');assert s['sha256']==sha((H/'revisions/UNIVERSAL_PROOF_INITIAL_SEAL.md').read_bytes())
q=load(H/'PROOF_SEAL_QUALIFICATION.json');assert q['initial_sha256']==s['sha256'] and q['current_sha256']==sha((H/'UNIVERSAL_PROOF.md').read_bytes())
r=load(H/'REPLAY_RESULTS.json');assert r['status']=='PASS' and r['unchanged'] and r['outer_runs']==9 and r['explicit_original_runs']==r['explicit_current_runs']==3 and len(r['runs'])==15
for e in r['runs']:
 assert e['exit']==0 and e['stdout_sha256']==sha((H/'receipts'/(e['name']+'.stdout')).read_bytes()) and e['stderr_sha256']==sha((H/'receipts'/(e['name']+'.stderr')).read_bytes())
 if 'actual_result_sha256' in e:assert e['actual_result_sha256']==sha((H/'receipts'/(e['name']+'.result.json')).read_bytes()) and (e['byte_exact'] or e['full_json_equal_except_utc_and_private_path'])
z=load(H/'AUDIT_RESULTS.json');assert z['status']=='PASS' and z['before_bindings']==z['after_bindings'] and z['new_scientific_diagnostics']==33 and len(z['actual_new_scientific_mutants'])==6 and len(z['actual_false_prose_runs'])==4
for e in z['runs']:
 assert e['stdout']==(H/(e['name']+'.stdout')).read_text() and e['stderr']==(H/(e['name']+'.stderr')).read_text()
print(json.dumps({'closed_review_verified':True,'review_members':len(members),'current_members':42,'dependency_members':115,'json_parse_executions':parsed,'manifest_sha256':sha((H/'MANIFEST.json').read_bytes()),'status':v['status']}))
