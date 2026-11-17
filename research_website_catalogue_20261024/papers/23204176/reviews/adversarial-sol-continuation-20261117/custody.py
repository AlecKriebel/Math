"""Passive complete custody reader; no project imports or execution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, stat, sys
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
A=P/'papers/23204176/reviews/adversarial-sol-continuation-20261117'
S=P/'papers/23204176/sources';I=P/'papers/23204176/reviews/adversarial-sol'
def sha(b):return hashlib.sha256(b).hexdigest()
def snap(root):
    rows=[]
    for p in [root,*sorted(root.rglob('*'))]:
        st=p.lstat();n='.' if p==root else str(p.relative_to(root));r={'path':n,'mode':oct(stat.S_IMODE(st.st_mode)),'hidden':any(x.startswith('.') for x in p.relative_to(root).parts)}
        if stat.S_ISDIR(st.st_mode):r.update(kind='directory',empty=not any(p.iterdir()))
        elif stat.S_ISREG(st.st_mode):
            b=p.read_bytes();r.update(kind='file',bytes=len(b),SHA256=sha(b))
        else:r.update(kind='other',target=os.readlink(p) if p.is_symlink() else None)
        rows.append(r)
    return rows
data={'UTC':datetime.now(timezone.utc).isoformat(),'source':snap(S),'old_INITIAL':snap(I)}
assert sum(r['kind']=='file' for r in data['source'])==43
assert sum(r['kind']=='directory' for r in data['source'])==8
assert sum(r['kind']=='file' for r in data['old_INITIAL'])==20
assert sum(r['kind']=='directory' for r in data['old_INITIAL'])==2
assert sha((I/'INITIAL_MANIFEST.json').read_bytes())=='54154aca5b5fbcd8c6199c9182b95cccf52a4db1e1865753f7929c74b65d72ce'
assert sha((I/'INITIAL_SEAL.json').read_bytes())=='c2d4d655fa7e04df3a03975ea168feb63c9fb3979b3f1c7404b019af4176ac2c'
assert sha((S/'zenodo-files/paper.pdf').read_bytes())=='483a6edff90202ef4d31560049a32ce946dcd1c6a999ab5b1f25b66a8f326612'
target=sys.argv[1];assert target in ['CUSTODY_BEFORE.json','CUSTODY_AFTER.json']
if target=='CUSTODY_AFTER.json':
    before=json.loads((A/'CUSTODY_BEFORE.json').read_text());assert all(data[k]==before[k] for k in ['source','old_INITIAL'])
(A/target).write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({'UTC':data['UTC'],'target':target,'source_files':43,'source_child_directories':7,'old_INITIAL_files':20,'old_INITIAL_child_directories':1,'exact_match_if_after':target=='CUSTODY_AFTER.json'}))
