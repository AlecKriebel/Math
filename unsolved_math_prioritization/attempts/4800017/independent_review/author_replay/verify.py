from fractions import Fraction as F
from itertools import product
from pathlib import Path
from hashlib import sha256
import json
checks=0
def ck(v):
 global checks
 assert v
 checks+=1
def rank(A):
 A=[[F(v) for v in r] for r in A];rr=0
 for j in range(len(A[0])):
  k=next((i for i in range(rr,len(A)) if A[i][j]),None)
  if k is None:continue
  A[rr],A[k]=A[k],A[rr];v=A[rr][j];A[rr]=[a/v for a in A[rr]]
  for i in range(len(A)):
   if i!=rr:
    v=A[i][j];A[i]=[a-v*b for a,b in zip(A[i],A[rr])]
  rr+=1
 return rr
families=[[(0,1,0,0),(0,0,1,0)],[(0,0,0,1),(0,1,0,1)],[(0,1,0,0),(0,0,1,0),(0,1,1,1)]]
def pval(p,n):return sum(c*n**i for i,c in enumerate(p))
for ps in families:
 ck(all(p[0]==0 for p in ps));ck(rank(ps)==len(ps));ck(rank([[-x for x in p] for p in ps])==len(ps))
 for q in range(1,40):
  for k in range(1,7):
   for p in ps:ck(pval(p,q*k)%q==0)
# Shift transformations commute even when a shift is the identity/nonergodic.
cases=0
for q in range(1,9):
 X=set(range(q))
 for mask in range(1<<q):
  A={i for i in X if mask>>i&1};mu=F(len(A),q)
  for ps in families:
   shifts=tuple((j*2+1)%q for j in range(len(ps)))
   for n in range(1,q+2):
    source=set(A);converted=set(A)
    for t,p in zip(shifts,ps):
     source&={(a+t*pval(p,n))%q for a in A}
     converted&={(a+(-t)*(-pval(p,n)))%q for a in A}
    ck(source==converted);cases+=1
   recur=set(A)
   for t,p in zip(shifts,ps):recur&={(a+t*pval(p,q))%q for a in A}
   ck(recur==A);ck(F(len(recur),q)>=mu**(len(ps)+1))
   # Finite coding factor: cylinder membership under inverse shift powers.
   for x in X:
    for t in shifts:
     for k in range(-2,3):ck(((x-t*k)%q in A)==(x in {(a+t*k)%q for a in A}))
r={'artifact_sha256':sha256(Path('KNOWN_RESULT.md').read_bytes()).hexdigest(),'assertions':checks,'finite_sign_cases':cases,'scope':'Elementary convention controls only; the general recurrence and bounded-gap theorem is imported with explicit primary attribution.'}
Path('verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
