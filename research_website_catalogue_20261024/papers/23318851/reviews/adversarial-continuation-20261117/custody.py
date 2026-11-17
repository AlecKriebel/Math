"""Passive complete source and frozen INITIAL custody; no project imports/execution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import stat
import sys
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
S=P/'papers/23318851/sources'
I=P/'papers/23318851/reviews/adversarial-sol'
A=P/'papers/23318851/reviews/adversarial-continuation-20261117'
def sha(b):return hashlib.sha256(b).hexdigest()
def snap(root):
    rows=[]
    for p in [root,*sorted(root.rglob('*'))]:
        st=p.lstat();r={'path':'.' if p==root else str(p.relative_to(root)),
            'mode':oct(stat.S_IMODE(st.st_mode)),'hidden':any(x.startswith('.') for x in p.relative_to(root).parts)}
        if stat.S_ISDIR(st.st_mode):r.update(kind='directory',empty=not any(p.iterdir()))
        elif stat.S_ISREG(st.st_mode):
            b=p.read_bytes();r.update(kind='file',bytes=len(b),SHA256=sha(b))
        else:r.update(kind='other',target=os.readlink(p) if p.is_symlink() else None)
        rows.append(r)
    return rows
assert sha((S/'SOURCE_FINAL.json').read_bytes())=='c61fb0473f0954877ab5af49e7b6139732eb4afab7cfab3377864a91dd98b317'
assert sha((S/'SOURCE_MANIFEST.json').read_bytes())=='ed5c217040b7a0d72df7de7ef1d5cbce9bc516ab32c1f20ed6466ef153a6bac8'
assert sha((I/'INITIAL_MANIFEST.json').read_bytes())=='dbb198866601fd68216f11628a508407e5a98d90c8228204f2e3d72ae39c20e6'
assert sha((I/'INITIAL_SEAL.json').read_bytes())=='9e314a96b491a96f18ad3cdaa1cdcc9c1c3c125e69a16bbb3a60fae5e8cf4d86'
data={'UTC':datetime.now(timezone.utc).isoformat(),'source':snap(S),'INITIAL':snap(I)}
assert sum(r['kind']=='file' for r in data['source'])==95
assert sum(r['kind']=='directory' for r in data['source'])==17
assert sum(r['kind']=='file' for r in data['INITIAL'])==18
assert sum(r['kind']=='directory' for r in data['INITIAL'])==2
baseline=json.loads((I/'CUSTODY_BEFORE.json').read_text())['entries']
converted=[{**{k:v for k,v in r.items() if k not in ['mode_octal','sha256','md5']},
    'mode':r['mode_octal'],**({'SHA256':r['sha256']} if r['kind']=='file' else {})} for r in baseline]
assert converted==data['source']
target=sys.argv[1];assert target in ['CUSTODY_BEFORE.json','CUSTODY_AFTER.json']
assert not (A/target).exists()
if target=='CUSTODY_AFTER.json':
    old=json.loads((A/'CUSTODY_BEFORE.json').read_text())
    assert all(data[k]==old[k] for k in ['source','INITIAL'])
(A/target).write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({'UTC':data['UTC'],'target':target,'source_files':95,'source_child_dirs':16,
    'INITIAL_files':18,'INITIAL_child_dirs':1,'complete_exact_if_after':target=='CUSTODY_AFTER.json'}))
