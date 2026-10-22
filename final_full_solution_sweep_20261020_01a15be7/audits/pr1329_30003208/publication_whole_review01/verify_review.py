"""Read-only closure and parent-input verification; no service calls or edits."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;S=P.parent/'publication_preparation_01'
def need(x,m):
 if not x:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
m=json.loads((P/'MANIFEST.json').read_bytes());actual={str(f.relative_to(P)) for f in P.rglob('*') if f.is_file() and f!=P/'MANIFEST.json'}
need(actual==set(m['files']),'review closure')
for n,v in m['files'].items():
 f=P/n;need(not f.is_symlink(),'symlink');b=f.read_bytes();need(len(b)==v['bytes'] and sha(b)==v['sha256'],'review hash '+n)
size=sum(f.stat().st_size for f in P.rglob('*') if f.is_file());need(size<=8*1024*1024,'cap')
sb=(S/'MANIFEST.json').read_bytes();need(sha(sb)==m['reviewed_preparation_manifest_sha256'],'parent manifest changed')
sm=json.loads(sb);af={str(f.relative_to(S)) for f in S.rglob('*') if f.is_file() and f!=S/'MANIFEST.json'};need(af==set(sm['files']),'parent closure changed')
for n,v in sm['files'].items():
 b=(S/n).read_bytes();need(len(b)==v['bytes'] and sha(b)==v['sha256'],'parent hash changed '+n)
d=json.loads((P/'DECISION.json').read_bytes());need(d['scientific_whole_package_decision']=='PASS' and d['remaining_substantive_objections']==[],'decision')
need(d['publication_ready']is False and d['provider_write_calls']==0 and d['git_mutation_calls']==0,'no action/readiness')
print(json.dumps({'status':'PASS','review_members':len(m['files']),'review_total_bytes_with_manifest':size,'review_manifest_sha256':sha((P/'MANIFEST.json').read_bytes()),'parent_members_verified_unchanged':len(sm['files']),'publication_ready':False,'next_fresh_review_required':True},sort_keys=True,indent=2))
