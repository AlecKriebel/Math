"""Direct full n+2-dimensional coordinate ambient norm, including null slots."""
import sympy as s
from itertools import product
from functools import lru_cache
from pathlib import Path
import json
Q=s.Rational
t,r,rho=s.symbols('t r rho',positive=True)

def check(p):
 n=len(p)+1; N=n+2; ids=range(N); inf=N-1
 g=s.zeros(N); g[0,0]=2*rho;g[0,inf]=g[inf,0]=t
 g[1,1]=t*t
 for i,pi in enumerate(p,2):g[i,i]=t*t*r**(2*pi)
 inv=g.inv(); invrows={i:[(j,inv[i,j]) for j in ids if inv[i,j]] for i in ids}
 def d(f,a):return s.diff(f,{0:t,1:r,inf:rho}[a]) if a in (0,1,inf) else s.S.Zero
 @lru_cache(None)
 def G(u,a,b):return s.expand(sum(v*(d(g[e,b],a)+d(g[e,a],b)-d(g[a,b],e)) for e,v in invrows[u])/2)
 @lru_cache(None)
 def R(a,b,c,dd):
  return s.expand(-sum(g[dd,e]*(d(G(e,b,c),a)-d(G(e,a,c),b)+sum(G(e,a,u)*G(u,b,c)-G(e,b,u)*G(u,a,c) for u in ids)) for e in ids if g[dd,e]))
 subs={t:1,r:1,rho:0}
 tensor={};groups={}
 for m in ids:
  for q in product(ids,repeat=4):
   v=d(R(*q),m)
   for j in range(4):
    for u in ids:
     gamma=G(u,m,q[j])
     if gamma:
      other=list(q);other[j]=u
      v-=gamma*R(*other)
   v=s.expand(v).subs(subs)
   if v:
    inds=q+(m,);tensor[inds]=v
    key=f'{inds.count(0)} zero, {inds.count(inf)} infinity'
    groups[key]=groups.get(key,0)+1
 swap=lambda i:inf if i==0 else 0 if i==inf else i
 norm=sum(v*tensor.get(tuple(map(swap,inds)),0) for inds,v in tensor.items())
 tangential=sum(v*v for inds,v in tensor.items() if 0 not in inds and inf not in inds)
 assert norm==tangential
 out={'p':list(map(str,p)),'ambient_dimension':N,'ambient_D':str(norm),'tangential_D':str(tangential),'nonzero_derivative_component_groups':groups,'null_slot_cross_contribution':'0'}
 print(json.dumps(out),flush=True)
 return out
ps=[(Q(-1,3),Q(2,3),Q(2,3),0,0),(Q(-1,2),Q(1,2),Q(1,2),Q(1,2),0),(Q(-3,5),Q(2,5),Q(2,5),Q(2,5),Q(2,5))]
res=[check(p) for p in ps]
assert [x['ambient_D'] for x in res]==['1280/81','27','21504/625']
Path(__file__).with_suffix('.result.json').write_text(json.dumps({'checks':res,'passed':True},indent=2)+'\n')
