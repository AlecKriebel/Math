from itertools import product
from pathlib import Path
import json
import sympy as sy
from collections import Counter
m=3
r=tuple(3*((y-x)%3)+(-x)%3 for x in range(3) for y in range(3));s=tuple(3*((-y)%3)+(-x)%3 for x in range(3) for y in range(3));R=tuple(3*((-x-y)%3)+x for x in range(3) for y in range(3));t=tuple(3*y+x for x in range(3) for y in range(3))
# op index0 classical,1 virtual, pairslot0or1; compose rightmost first.
rels=[([(0,0),(0,1),(0,0)],[(0,1),(0,0),(0,1)]), ([(1,0),(1,1),(1,0)],[(1,1),(1,0),(1,1)]), ([(1,0),(1,0)],[]), ([(1,0),(0,1),(1,0)],[(1,1),(0,0),(1,1)]), ([(1,0),(0,1),(0,0)],[(0,1),(0,0),(1,1)])]
def follow(ops,w,x):
 x=list(x);v=[0]*18
 for k,i in reversed(w):
  pair=3*x[i]+x[i+1];v[9*k+pair]+=1;x[i],x[i+1]=divmod(ops[k][pair],3)
 return x,v

def matrix(ops,normalized=False):
 rows=[]
 for x in product(range(3),repeat=3):
  for L,H in rels:
   a,b=follow(ops,L,x);c,d=follow(ops,H,x);assert a==c;rows.append([u-v for u,v in zip(b,d)])
 if normalized:
  for k,p in enumerate(ops):
   for i,j in enumerate(p):
    if i==j:v=[0]*18;v[9*k+i]=1;rows.append(v)
 return rows

def modnull(rows,p):
 A=[[x%p for x in r] for r in rows];piv=[];rank=0
 for c in range(18):
  j=next((j for j in range(rank,len(A)) if A[j][c]),None)
  if j is None:continue
  A[rank],A[j]=A[j],A[rank];inv=pow(A[rank][c],-1,p);A[rank]=[inv*x%p for x in A[rank]]
  for j in range(len(A)):
   if j!=rank:
    z=A[j][c];A[j]=[(x-z*y)%p for x,y in zip(A[j],A[rank])]
  piv.append(c);rank+=1
 free=[x for x in range(18) if x not in piv];basis=[]
 for c in free:
  v=[0]*18;v[c]=1
  for j,pc in enumerate(piv):v[pc]=-A[j][c]%p
  basis.append(v)
 return basis

def invariant(v,p):return all((v[9*k+3*x+y]-v[9*k+3*((-x)%3)+(-y)%3])%p==0 for k in [0,1] for x,y in product(range(3),repeat=2))
if __name__=='__main__':
 out=[]
 for norm in [False,True]:
  for name,ops in [('general_s',(r,s)),('derived_flip',(R,t))]:
   rows=matrix(ops,norm);rec={'normalized':norm,'pair':name,'rational_dimension':18-sy.Matrix(rows).rank(),'finite':[]}
   for p in [2,3,5,7]:
    basis=modnull(rows,p);rec['finite'].append({'prime':p,'dimension':len(basis),'all_negation_invariant':all(invariant(v,p) for v in basis),'basis':basis})
   out.append(rec)
 print(json.dumps([{k:v if k!='finite' else [{a:b for a,b in z.items() if a!='basis'} for z in v] for k,v in x.items()} for x in out],indent=2));Path(__file__).with_name('weights_explore.json').write_text(json.dumps(out,indent=2)+'\n')
