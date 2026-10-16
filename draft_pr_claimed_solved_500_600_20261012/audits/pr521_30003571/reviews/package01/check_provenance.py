#!/usr/bin/env python3
import hashlib,json,subprocess,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent
BASE=OUT.parents[1]
ROOT=OUT/'scratch/fresh_extraction/positivity-loss-30003571'
REPO=Path('/Users/alec/Documents/Math')
HEAD='91385a9ba0d445a2fae4629cd60b70026584e24b'
def meta(p):b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
checks=[]
# No remote operation: authenticate exact archived content against the locally available Git object.
for p in sorted((ROOT/'original').rglob('*')):
    if p.is_file():
        rel=str(p.relative_to(ROOT/'original'))
        q=subprocess.run(['git','show',HEAD+':unsolved_math_prioritization/attempts/30003571/'+rel],cwd=REPO,capture_output=True,check=True)
        assert q.stdout==p.read_bytes(), rel
        checks.append('original exact Git blob: '+rel)
for rel in ['original/PUBLICATION_MANIFEST.json','original/public/FROZEN_MANIFEST.json','original/audit/AUDIT_MANIFEST.json','reviews/geometry01/MANIFEST.json']:
    f=ROOT/rel;m=json.loads(f.read_text())
    for name,info in m['files'].items():assert meta(f.parent/name)==info,(rel,name)
    checks.append('historical manifest verified: '+rel)
snapshot=json.loads((BASE/'ORIGINAL_SNAPSHOT.json').read_text())
for info in snapshot['files']:
    rel=info['path'].split('attempts/30003571/')[1]
    got=meta(ROOT/'original'/rel)
    assert got['sha256']==info['sha256'] and got['bytes']==info['bytes']
checks.append('all 14 original snapshot records match')
for rel in ['positivity_loss.tex','README.md','CORRECTIONS.md']:
    assert (ROOT/'paper'/rel).read_bytes()==(BASE/'publication'/rel).read_bytes()
for rel in ['requirements.txt','run_all.py']:
    assert (ROOT/rel).read_bytes()==(BASE/'publication'/rel).read_bytes()
checks.append('all 5 current package paper/wrapper inputs match publication source')
# Exercise rejection gates in review-only extraction, then restore the original inventory.
for label,args,extra in [('optimization',[sys.executable,'-O','run_all.py'],False),('extra_rebuilt_pdf',[sys.executable,'run_all.py'],True)]:
    if extra:(ROOT/'paper'/'positivity_loss.pdf').write_bytes(b'%PDF-synthetic-review-probe\n')
    p=subprocess.run(args,cwd=ROOT,capture_output=True,text=True)
    if extra:(ROOT/'paper'/'positivity_loss.pdf').unlink()
    assert p.returncode!=0
    (OUT/'scratch'/f'{label}.stderr.txt').write_text(p.stderr)
    checks.append('rejection gate: '+label)
manifest=json.loads((ROOT/'MANIFEST.json').read_text())
for rel,info in manifest['files'].items():assert meta(ROOT/rel)==info
# Local deposit metadata checks; this does not contact or validate a live Zenodo draft.
z=json.loads((BASE/'publication/zenodo-deposit.json').read_text())
c=json.loads((BASE/'publication/zenodo_check.json').read_text())
assert z['metadata']['title']==c['title']
assert z['metadata']['publication_type']=='preprint' and z['metadata']['version']=='1.0'
assert z['metadata']['publication_date']=='2026-10-12'
assert z['metadata']['creators']==[{'name':'Kriebel, Alec','affiliation':'Independent researcher','orcid':'0009-0001-9320-500X'}]
assert z['metadata']['license']=='cc-by-4.0' and z['metadata']['access_right']=='open'
assert [f['path'] for f in z['files']]==[f['name'] for f in c['files']]
for f in c['files']:
    m=meta(BASE/'publication'/f['name']);assert m['bytes']==f['size'] and m['sha256']==f['sha256']
checks.append('Zenodo local exact metadata and file-check consistency')
result={'status':'PASS','checks':checks,'count':len(checks),'metadata':z,'limits':'No live Zenodo draft inspected or mutated; local manifest only. Git provenance authenticated without network.'}
(OUT/'PROVENANCE_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'count':len(checks),'checks':checks},indent=2))
