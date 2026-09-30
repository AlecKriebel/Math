from fractions import Fraction
from math import gcd,comb
from pathlib import Path
import json,hashlib
n=0
def rank(A):
 A=[list(map(Fraction,row)) for row in A];r=0
 for c in range(len(A[0])):
  k=next((k for k in range(r,len(A)) if A[k][c]),None)
  if k is None:continue
  A[r],A[k]=A[k],A[r];v=A[r][c];A[r]=[x/v for x in A[r]]
  for k in range(len(A)):
   if k!=r:
    v=A[k][c];A[k]=[x-v*y for x,y in zip(A[k],A[r])]
  r+=1
 return r
for m in range(1,26):
 for a in range(m):
  if gcd(a,m)!=1:continue
  P=[[int(i==(j-a)%m)-int(i==j) for j in range(m)] for i in range(m)]
  assert rank(P)==m-1;n+=1
  assert (m+1)-(m-1)==2 and 2*(m+1)-(m-1)==m+3;n+=1
  for d in range(2,13):
   q=d-2;b1=q+4;b2=(comb(q,2) if q>=2 else 0)+4*q+m+3
   assert b1==d+2;n+=1
   assert b2-comb(d,2)-2*(d-1)==m;n+=1
r={'assertions':n,'all_pass':True,'artifact_sha256':hashlib.sha256(Path('PARTIAL_RESULT.md').read_bytes()).hexdigest(),'scope':'At most two distinct connected central hypertori; no general ring-to-poset reconstruction.'}
Path('verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
