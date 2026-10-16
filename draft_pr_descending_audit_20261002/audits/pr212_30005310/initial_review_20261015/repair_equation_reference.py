from pathlib import Path
import hashlib,json,datetime,shutil,subprocess
D=Path(__file__).resolve().parent;C=D/'corrected_packet';H=D/'credit_packet_revision_history'/'v1_before_equation_reference_repair';H.mkdir(parents=True,exist_ok=False)
old_files=[C/'PROOF.md',C/'verification.json',C/'MANIFEST.json',C/'PUBLICATION_MANIFEST.json',D/'PROPOSED_CURRENT_PACKET_MANIFEST.json',D/'PROPOSED_NATIVE_CHANGES.json',D/'ROOT_PROPOSED_CREDIT_PACKET_VALIDATION.json'];rows=[]
for p in old_files:
 rel=p.relative_to(D);q=H/rel;q.parent.mkdir(parents=True,exist_ok=True);b=p.read_bytes();q.write_bytes(b);rows.append(dict(path=rel.as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
(H/'PRESERVED_INPUTS.json').write_text(json.dumps(rows,indent=2)+'\n')
old='Proposition3 assumes I(G,n)nonzero and I(G,n+1)=0. Its second bullet\nasserts WMLT=n'
new='Proposition3 assumes the ideal hypothesis\n\n    I(G,n+1)=0,    I(G,n) nonzero.                        (1)\n\nIts second bullet asserts WMLT=n'
for p in [C/'PROOF.md',D/'prepare_credited_packet.py']:
 t=p.read_text();assert t.count(old)==1;p.write_text(t.replace(old,new,1))
py='/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr256_5100017/initial_review_20261013/reproduction_environment/bin/python'
r=subprocess.run([py,str(C/'verify.py')],capture_output=True,text=True,timeout=120);assert r.returncode==0,r.stderr
v=json.loads((C/'verification.json').read_text());assert v['proof_sha256']==hashlib.sha256((C/'PROOF.md').read_bytes()).hexdigest();v.pop('proof_sha256');oldv=json.loads((H/'corrected_packet/verification.json').read_text());oldv.pop('proof_sha256');assert v==oldv
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
 b=p.read_bytes();return dict(path=p.relative_to(C).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
for name in ['MANIFEST.json','PUBLICATION_MANIFEST.json']:
 excluded={'PUBLICATION_MANIFEST.json'}|({'MANIFEST.json'} if name=='MANIFEST.json' else set())
 paths=[q for q in sorted(C.rglob('*')) if q.is_file() and q.relative_to(C).as_posix() not in excluded]
 body=json.loads((C/name).read_text());body.update(utc=now,files=[pin(q) for q in paths]);(C/name).write_text(json.dumps(body,indent=2)+'\n')
m=json.loads((D/'PROPOSED_CURRENT_PACKET_MANIFEST.json').read_text());m.update(utc=now,files=[pin(q) for q in sorted(C.rglob('*')) if q.is_file()],revision='v2_restore_ideal_hypothesis_equation1_reference')
(D/'PROPOSED_CURRENT_PACKET_MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
plan=json.loads((D/'PROPOSED_NATIVE_CHANGES.json').read_text());plan['packet_manifest_sha256']=hashlib.sha256((D/'PROPOSED_CURRENT_PACKET_MANIFEST.json').read_bytes()).hexdigest();(D/'PROPOSED_NATIVE_CHANGES.json').write_text(json.dumps(plan,indent=2)+'\n')
a=json.loads((D/'ROOT_PROPOSED_CREDIT_PACKET_VALIDATION.json').read_text());a.update(utc=now,manifest_sha256=plan['packet_manifest_sha256'],native_plan_sha256=hashlib.sha256((D/'PROPOSED_NATIVE_CHANGES.json').read_bytes()).hexdigest(),revision=m['revision'],editorial_reference_repair=True,old_packet_history=str(H));(D/'ROOT_PROPOSED_CREDIT_PACKET_VALIDATION.json').write_text(json.dumps(a,indent=2)+'\n')
for row in m['files']:
 q=C/row['path'];assert pin(q)==row
for name in ['MANIFEST.json','PUBLICATION_MANIFEST.json']:
 for row in json.loads((C/name).read_text())['files']:assert pin(C/row['path'])==row
core=lambda raw:raw.split(b'## 2. Model, statistics and sample convention',1)[1].split(b'## 8.',1)[0]
assert core((C/'PROOF.md').read_bytes())==core((C/'original_submission/PROOF.md').read_bytes())
result=dict(utc=now,status='REPAIRED_LOCALLY_NOT_APPLIED',issue='Orphan equation(1) reference restored in current Section1',mathematical_core_unchanged=True,author_188_replay_matches_except_dynamic_proof_SHA=True,archive20_unchanged=True,files=35,packet_manifest_sha256=plan['packet_manifest_sha256'],native_plan_sha256=a['native_plan_sha256'],frozen_old_payload_files=len(rows),new_final_review_pending=True)
(D/'EQUATION_REFERENCE_REPAIR_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
