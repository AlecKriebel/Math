from fractions import Fraction as F
from itertools import product,combinations
from pathlib import Path
import hashlib,json
checks=0
def ck(t):
 global checks
 assert t;checks+=1
b=(-1,1,1,1,-1)
for mask in product((0,1),repeat=5):
 s=sum(bi*mi for bi,mi in zip(b,mask));v=sum(b[i]*b[j]*(mask[i]!=mask[j]) for i in range(5) for j in range(i+1,5));ck(v==s*(1-s));ck(v<=0)
D=((0,1,1,1,1),(1,0,2,2,1),(1,2,0,2,1),(1,2,2,0,1),(1,1,1,1,0))
for n in range(3,31):
 us=[(0,0,0),(0,0,1),(0,1,0),(1,0,0),(1,1,1)]
 us=[u+(0,)*(n-2) for u in us]
 ps=[tuple(F(2**v,sum(2**w for w in u)) for v in u) for u in us]
 for p in ps:ck(sum(p)==1);ck(min(p)>0);ck(len(p)==n+1)
 for i,j in combinations(range(5),2):
  ds=[a-c for a,c in zip(us[i],us[j])];ck(max(ds)-min(ds)==D[i][j])
  rs=[q/p for p,q in zip(ps[i],ps[j])];m=min(rs);M=max(rs)
  A=-1/(M-1);B=1/(1-m);ck(A<0<1<B)
  cr=B*(1-A)/((B-1)*(-A));ck(cr==M/m);ck(cr==2**D[i][j])
 ck(sum(b[i]*b[j]*D[i][j] for i,j in combinations(range(5),2))==1)
for u in product(range(-8,9),repeat=3):ck(2*(max(u)-min(u))==sum(abs(u[i]-u[j]) for i,j in combinations(range(3),2)))
# Rational planar segment level p_i=k p_j: its intersection is between
# endpoints exactly when the level lies between their endpoint ratios.
P=[(F(i,10),F(j,10),F(10-i-j,10)) for i in range(1,9) for j in range(1,10-i)]
levels=[F(i,4) for i in range(1,25)]
for p,q in combinations(P,2):
 for i,j in combinations(range(3),2):
  for k in levels:
   f0=p[i]-k*p[j];f1=q[i]-k*q[j]
   if f0==0 or f1==0:continue
   crossing=f0*f1<0
   ck(crossing==(min(p[i]/p[j],q[i]/q[j])<k<max(p[i]/p[j],q[i]/q[j])))
   if f0!=f1:ck(crossing==(0<f0/(f0-f1)<1))
r={'artifact_sha256':hashlib.sha256(Path('PARTIAL_RESULT.md').read_bytes()).hexdigest(),'exact_assertions':checks,'simplex_dimensions_checked':[3,30],'cut_patterns':32,'scope':'Finite exact algebra and incidence checks; coarea and all-dimensional proofs are in the note.'}
Path('verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
