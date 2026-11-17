"""Passive writer custody: complete source/old reviews, exact approval/CSS inputs only."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,os,stat,sys
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
A=P/'verification/binary-gram-locus-editorial-sol-20261117'
S=P/'papers/23318851/sources'
I=P/'papers/23318851/reviews/adversarial-sol'
C=P/'papers/23318851/reviews/adversarial-continuation-20261117'
CSS=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research/research.css')
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
def filepin(p):
    b=p.read_bytes();return {'path':str(p),'mode':oct(stat.S_IMODE(p.lstat().st_mode)),'bytes':len(b),'SHA256':sha(b)}
assert sha((S/'SOURCE_FINAL.json').read_bytes())=='c61fb0473f0954877ab5af49e7b6139732eb4afab7cfab3377864a91dd98b317'
assert sha((S/'SOURCE_MANIFEST.json').read_bytes())=='ed5c217040b7a0d72df7de7ef1d5cbce9bc516ab32c1f20ed6466ef153a6bac8'
assert sha((I/'INITIAL_MANIFEST.json').read_bytes())=='dbb198866601fd68216f11628a508407e5a98d90c8228204f2e3d72ae39c20e6'
assert sha((I/'INITIAL_SEAL.json').read_bytes())=='9e314a96b491a96f18ad3cdaa1cdcc9c1c3c125e69a16bbb3a60fae5e8cf4d86'
assert sha((C/'FINAL_MANIFEST.json').read_bytes())=='d7a25669b161de9b9a4edbf255b9d4ba7e9039c9bdadab25b4196c1c475549ee'
assert sha((C/'FINAL_SEAL.json').read_bytes())=='26b2ed0e66948b646f75f0af0f8639442521666d5559c2b9198c2faf88d8a575'
approval=P/'verification/root-clearance-23318851-20261117.json'
review=P/'papers/23318851/reviews/root-continuation-20261117/ROOT_REVIEW.md'
assert sha(approval.read_bytes())=='ef479bc20bdcd8d789736abd17b9999184fee354b3a15d41bc53a6c872b807d9'
assert sha(review.read_bytes())=='d6d6efca566214ccb39080bd7160c3437ede74c026150bc74e149d6878867d5f'
data={'UTC':datetime.now(timezone.utc).isoformat(),'source':snap(S),'INITIAL':snap(I),'continuation':snap(C),
      'specific_inputs':[filepin(approval),filepin(review),filepin(CSS)]}
for name,nfiles,ndirs in [('source',95,16),('INITIAL',18,1),('continuation',98,10)]:
    assert sum(r['kind']=='file' for r in data[name])==nfiles
    assert sum(r['kind']=='directory' for r in data[name])==ndirs+1
baseline=json.loads((C/'CUSTODY_BEFORE.json').read_text())
assert data['source']==baseline['source'] and data['INITIAL']==baseline['INITIAL']
target=sys.argv[1];assert target in ['CUSTODY_BEFORE.json','CUSTODY_AFTER.json']
assert not (A/target).exists()
if target=='CUSTODY_AFTER.json':
    before=json.loads((A/'CUSTODY_BEFORE.json').read_text())
    assert all(data[k]==before[k] for k in ['source','INITIAL','continuation','specific_inputs'])
(A/target).write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({'UTC':data['UTC'],'target':target,'source95_16_INITIAL18_1_continuation98_10':True,
    'complete_exact_if_after':target=='CUSTODY_AFTER.json','website_scope':'CSS file only; no whole website guard'}))
