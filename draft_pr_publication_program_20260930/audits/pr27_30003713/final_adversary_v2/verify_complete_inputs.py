"""Read-only closure gate for the exact corrected candidate and all94 support."""
from pathlib import Path
import hashlib,json,subprocess,datetime
P=Path(__file__).resolve().parent;A=P.parent;R=P.parents[3]
sha=lambda b:hashlib.sha256(b).hexdigest()
expected='1e7f1bca0d4e210f6113d9f9b47c15f03308cadfa5b0bedcb02e36a8ad4a3d27'
C=A/'reviewed_candidate';m=json.loads((C/'MANIFEST.json').read_text());assert sha((C/'MANIFEST.json').read_bytes())==expected
assert len(m['files'])==23
receipts=[]
def check_rows(root,rows):
 for x in rows:
  b=(root/x['path']).read_bytes();assert sha(b)==x['sha256'] and len(b)==x['bytes'],x['path'];receipts.append({'path':str((root/x['path']).relative_to(R)),'sha256':sha(b),'bytes':len(b)})
check_rows(C,m['files']);assert {x['path'] for x in m['files']}=={p.relative_to(C).as_posix() for p in C.rglob('*') if p.is_file() and p.name!='MANIFEST.json'}
d=json.loads((C/'CURRENT_PROOF_DEPENDENCIES.json').read_text());assert len(d['supporting_first_party_files'])==94;check_rows(R,d['supporting_first_party_files'])
counts={}
for family,manifest in [('character_family','artifact_manifest.json'),('homological_family','FIRST_PARTY_SHA256_MANIFEST.json'),('primary_scope_family','FIRST_PARTY_SHA256_MANIFEST.json'),('final_adversary','FIRST_PARTY_SHA256_MANIFEST.json')]:
 F=A/family;data=json.loads((F/manifest).read_text());rows=[{'path':k,**v} for k,v in data['artifacts'].items()] if 'artifacts' in data else data['files'];check_rows(F,rows)
 excluded={'tmp','tmp_sources','tmp_replay','__pycache__'}
 assert {x['path'] for x in rows}=={p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_file() and p.name!=manifest and not set(p.relative_to(F).parts)&excluded},family
 counts[family]=len(rows)
H=A/'historical_candidate_v1';hm=json.loads((H/'MANIFEST.json').read_text());assert len(hm['files'])==22;assert sha((H/'MANIFEST.json').read_bytes())=='2bb662fe662ac51380e57ecb03a8b404591ba7761d7e57cd6f6dab7520ec2a69';check_rows(H,hm['files'])
f=json.loads((A/'snapshot_manifest.json').read_text());assert f['head']=='84d7f6103b087e431d7afb751501380ebd7ffd42';assert len(f['files'])==13
for x in f['files']:
 b=subprocess.check_output(['git','show',f['head']+':unsolved_math_prioritization/attempts/30003713/'+x['path']],cwd=R);assert b==(A/'source_snapshot'/x['path']).read_bytes();assert sha(b)==x['sha256'];assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['git_blob_sha1']
assert subprocess.check_output(['git','diff','--name-only',f['actual_merge_base'],f['head']],cwd=R).decode().splitlines()==f['changed_paths'];assert len(f['changed_paths'])==14
assert subprocess.check_output(['git','branch','--show-current'],cwd=R).decode().strip()=='main'
for old,new in [('PARTIAL.md','ORIGINAL_PARTIAL.md'),('README.md','ORIGINAL_README.md'),('readiness.json','ORIGINAL_readiness.json')]:assert (A/'source_snapshot'/old).read_bytes()==(C/new).read_bytes()
for x in f['files']:
 if x['path'] not in {'PARTIAL.md','README.md','readiness.json'}:assert (A/'source_snapshot'/x['path']).read_bytes()==(C/x['path']).read_bytes()
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','candidate_manifest_sha256':expected,'candidate_files':23,'support_files':94,'closed_family_counts':counts,'original_git_files':13,'original_changed_paths':14,'historical_candidate_files':22,'all_binding_receipts':receipts,'main_branch':True,'original_archives_and_unchanged_files_exact':True}
(P/'INTEGRITY_RECEIPT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='all_binding_receipts'},indent=2))
