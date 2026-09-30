from itertools import product
from pathlib import Path
import hashlib,json
n=0
def clean(p):return {k:v for k,v in p.items() if v}
def add(p,q):
 r=dict(p)
 for k,v in q.items():r[k]=r.get(k,0)+v
 return clean(r)
def mul(p,q):
 r={}
 for (a,z),u in p.items():
  for (b,w),v in q.items():r[(a+b,z+w)]=r.get((a+b,z+w),0)+u*v
 return clean(r)
def deg(p):return max(z for a,z in p)
def sub(p):return {(-2*a,2*z):v for (a,z),v in p.items()}
def mod(p):return {k:v%2 for k,v in p.items() if v%2}
dp={(-1,-1):1,(1,-1):-1};df={(-1,-1):1,(1,-1):1,(0,0):-1}
for cs in product(range(-2,3),repeat=4):
 p=clean(dict(zip([(-1,-1),(0,0),(1,1),(2,3)],cs)))
 if not p:continue
 assert deg(mul(dp,p))==deg(p)-1;n+=1
 assert deg(mul(df,p))==deg(p);n+=1
 assert deg(sub(p))==2*deg(p);n+=1
 for f in [-2,0,3]:
  assert deg(mul({(2*f,0):1},p))==deg(p);n+=1
for d in range(2,14):
 for e in range(1,d):
  F={(0,d):2,(0,e):1};R={(0,2*e):1}
  assert mod(sub(F))==mod(R);n+=1
  assert deg(R)<2*deg(F);n+=1
 F={(0,d):1};R={(0,2*d):1,(0,2*d+2):2}
 assert mod(sub(F))==mod(R);n+=1
 assert deg(R)>2*deg(F);n+=1
# Every odd top coefficient survives any even additive correction.
for c in [-5,-3,-1,1,3,5]:
 for q in range(-100,101):
  assert c+2*q!=0;n+=1
r={'assertions':n,'all_pass':True,'artifact_sha256':hashlib.sha256(Path('PARTIAL_RESULT.md').read_bytes()).hexdigest(),'scope':'Formal integer Laurent polynomial diagnostics, not knot realization or invariant computation.'}
Path('verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
