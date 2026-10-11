from character_tools import parts,character,centralizer
from fractions import Fraction as F
from collections import Counter
import json
C=Counter()
def ck(x,key):assert x,key;C[key]+=1
for n in range(1,12):
 ps=parts(n);p=len(ps)
 for size in range(n+1):
  for nu in parts(size):
   if any(x<3 for x in nu):continue
   R=n-size;s=R//2;q=s+1;mus=[nu+(2,)*r+(1,)*(R-2*r) for r in range(q)]
   zs=[centralizer(mu) for mu in mus];tab=[[character(lam,mu) for mu in mus] for lam in ps]
   diag=[sum((F(row[r]**2,zs[r]) for r in range(q)),F(0)) for row in tab]
   ck(sum(diag)==q,'projection_trace');ck(all(0<=x<=1 for x in diag),'projection_diagonal_bounds')
   v=sum(x*x for x in diag);z=sum(x==0 for x in diag)
   ck(F(z,p)<=1-F(q*q,p*v),'zero_fiber_fourth_moment_bound')
   ck(F(q*q,p)<=v<=q,'fourth_moment_range')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'scope':'Finite projection identities only; no bulk fourth-moment estimate.'},indent=2))
