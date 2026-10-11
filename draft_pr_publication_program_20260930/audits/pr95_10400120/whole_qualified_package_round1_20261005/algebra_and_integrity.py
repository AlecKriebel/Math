from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import hashlib,json,datetime
A=Path(__file__).resolve().parent;B=A.parent;Q=B/'qualified_publication_package_v1';P=Q/'publicfiles'
def guard(c,m):
 if not c:raise RuntimeError(m)
def mul(x,y):return (x[0]*y[0]+5*x[1]*y[1],x[0]*y[1]+x[1]*y[0])
def scale(x,n):return (n*x[0],n*x[1])
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def realpair(v):
 guard(all(x==0 for i,x in enumerate(v) if i not in [0,20,30]),'unexpected polynomial support')
 guard(v[20]==-v[30],'not coefficient of real cyclotomic pair')
 # zeta100^20-zeta100^30=2cos72deg=(sqrt5-1)/2.
 return (F(v[0])-F(v[20],2),F(v[20],2))
r=json.loads((A/'fresh_reproduction/verify_positive_normal/verification.json').read_text());AA=realpair(r['AA']);BB=realpair(r['BB']);DD=realpair(r['DD'])
guard(DD==(225,-100),'DD positive branch')
guard(AA==scale(mul(DD,(3475,1550)),50000),'one-word normalized value')
guard(BB==scale(mul(DD,(4025,1800)),50000**2),'two-word normalized value')
guard(realpair(r['difference'])==add(scale(AA,50000),scale(BB,-1)),'cross difference')
labels=[(a,b,c,d) for a in range(6) for b in range(6) for c in range(6) for d in range(6) if a+b+c+d<=5];charges=Counter((a+2*b+3*c+4*d)%5 for a,b,c,d in labels);guard(charges=={0:26,1:25,2:25,3:25,4:25},'full center charges')
checks=[]
for line in (P/'SHA256SUMS.txt').read_text().splitlines():
 h,n=line.split(None,1);n=n.strip().lstrip('*');p=P/n;checks.append({'kind':'outer_digest','file':n,'ok':hashlib.sha256(p.read_bytes()).hexdigest()==h})
f=json.loads((Q/'private_notes/FROZEN_CANDIDATE_MANIFEST.json').read_text())
for row in f['public_files']+[f['deposit_manifest']]:
 p=Q/row['file'];checks.append({'kind':'frozen_manifest','file':row['file'],'ok':p.stat().st_size==row['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256']})
d=json.loads((Q/'PREPARATION_MANIFEST.json').read_text())
for row in d['files']:
 # preparation manifest uses file key and candidate-relative paths
 p=Q/row['file'];checks.append({'kind':'preparation_manifest','file':row['file'],'ok':p.stat().st_size==row['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256']})
guard(all(c['ok'] for c in checks),'candidate integrity mismatch')
print(json.dumps({'status':'PASS','actual_algorithmic_checks':len(checks),'normalization_pairs':{'AA':list(map(str,AA)),'BB':list(map(str,BB)),'DD':list(map(str,DD))},'all_center_charge_counts':dict(charges),'limits':'finite algorithmic counts, no quality or theorem counts'},indent=2))
(A/'CANDIDATE_INTEGRITY.json').write_text(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'checks':checks,'all_pass':True},indent=2)+'\n')
