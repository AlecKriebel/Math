#!/usr/bin/env python3
"""Independent exact rational post-check of modular signed-permutation candidates."""
from fractions import Fraction as F
from pathlib import Path
import json
PAIRS=((3,2),(20,14),(119,84))
def matrix(ss):
 n=len(ss[0]);a=[[0]*(3*n) for _ in range(3*n)]
 for k,((p,q),s) in enumerate(zip(PAIRS,ss)):
  for c,x in enumerate(s):
   sg=1 if x>0 else -1;r=abs(x)-1
   a[k*n+r][c]+=p*sg;a[k*n+c][n+c]-=q
   a[k*n+r][2*n+c]+=sg;a[k*n+c][2*n+c]-=1
 return a

def kernel(a):
 a=[[F(x) for x in r] for r in a];n=len(a[0]);r=0;piv=[]
 for c in range(n):
  k=next((i for i in range(r,len(a)) if a[i][c]),None)
  if k is None:continue
  a[k],a[r]=a[r],a[k];v=a[r][c];a[r]=[x/v for x in a[r]]
  for i in range(len(a)):
   if i!=r and a[i][c]:
    v=a[i][c];a[i]=[x-v*y for x,y in zip(a[i],a[r])]
  piv.append(c);r+=1
 for c in set(range(n))-set(piv):
  v=[F(0)]*n;v[c]=F(1)
  for i,j in enumerate(piv):v[j]=-a[i][c]
  yield v

def run():
 out=[]
 for file in sorted(Path(__file__).parent.glob('signed_candidates_*.jsonl')):
  count=0;positive=[]
  for line in file.read_text().splitlines():
   row=json.loads(line);ss=row['matrices'];n=len(ss[0]);count+=1
   for v in kernel(matrix(ss)):
    if any(v[:n]):
     assert any(v[n:2*n]);assert all(sum(F(x)*y for x,y in zip(r,v))==0 for r in matrix(ss))
     positive.append({'matrices':ss,'kernel_vector':[str(x) for x in v]})
  out.append({'file':file.name,'modular_candidates':count,'rational_horizontal_witnesses':positive})
 return {'scope':'Exact verification of modular survivors only; modular non-survivors are excluded by maximal-rank certificates. No arbitrary-dimension conclusion.', 'results':out}
if __name__=='__main__':
 out=run();Path(__file__).with_name('signed_exact_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
