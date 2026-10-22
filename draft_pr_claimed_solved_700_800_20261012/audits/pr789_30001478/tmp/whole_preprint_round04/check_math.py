"""Reviewer-owned exact polynomial identities and finite diagnostics; not a proof assistant."""
from itertools import product
import json

def need(ok,msg):
 if not ok:raise ValueError(msg)
def clean(p):return {k:v for k,v in p.items() if v}
def add(*ps):
 r={}
 for p in ps:
  for m,c in p.items():r[m]=r.get(m,0)+c
 return clean(r)
def neg(p):return {m:-c for m,c in p.items()}
def mul(p,q):
 r={}
 for (i,j,w),c in p.items():
  for (h,l,z),d in q.items():
   m=(i+h,j+l,w+z);r[m]=r.get(m,0)+c*d
 return clean(r)
def v(w):return {(0,0,w):1}
def sub(p,images):
 r={}
 for (i,j,w),c in p.items():
  t={(i,j,''):c}
  for x in w:t=mul(t,images[x])
  r=add(r,t)
 return r
def comm(p):
 r={}
 for (i,j,w),c in p.items():
  m=(i,j,''.join(sorted(w)));r[m]=r.get(m,0)+c
 return clean(r)
A={(1,0,''):1};B={(0,1,''):1};X=v('x');Y=v('y')
x={str(i):v(str(i))for i in range(1,5)}
def minus(a,b):return add(a,neg(b))
r=[add(mul(x['1'],minus(mul(A,x['1']),x['3'])),mul(x['3'],minus(x['1'],mul(A,x['3'])))),add(mul(x['1'],minus(mul(A,x['2']),x['4'])),mul(x['3'],minus(x['2'],mul(A,x['4'])))),add(mul(x['2'],minus(mul(A,x['1']),x['3'])),mul(x['4'],minus(x['1'],mul(A,x['3'])))),add(mul(x['2'],minus(mul(A,x['2']),x['4'])),mul(x['4'],minus(x['2'],mul(A,x['4'])))),add(mul(x['1'],minus(mul(B,x['1']),x['2'])),mul(x['4'],minus(x['1'],mul(B,x['2'])))),add(mul(x['1'],minus(mul(B,x['3']),x['4'])),mul(x['4'],minus(x['3'],mul(B,x['4']))))]
Q=add(mul(B,minus(mul(X,X),mul(Y,Y))),neg(mul(X,Y)),mul(Y,X))
def main():
 image={'1':X,'2':Y,'3':X,'4':Y};need([sub(f,image)for f in r]==[{},{},{},{},Q,Q],'six quotient images')
 need(all(not sub(f,{str(i):X for i in range(1,5)})for f in r),'scalar quotient')
 # Positive-pullback twisted degree-two product, followed by commutativization.
 theta={'x':add(X,mul(B,Y)),'y':add(mul(B,X),Y)}
 def twist(p,T):
  out={}
  for (i,j,w),c in p.items():
   need(len(w)==2,'quadratic');out=add(out,mul({(i,j,w[0]):c},T[w[1]]))
  return comm(out)
 need(not twist(Q,theta),'positive-pullback relation')
 need(bool(comm(Q)),'untwisted countercheck')
 need(bool(twist(Q,{'x':minus(X,mul(B,Y)),'y':minus(Y,mul(B,X))})),'inverse-adjugate characteristic-zero countercheck')
 U=v('u');V=v('v');one=v('')
 expected=add(mul(B,mul(U,U)),mul(minus(B,one),mul(U,V)),mul(add(B,one),mul(V,U)))
 need(sub(Q,{'x':add(U,V),'y':V})==expected,'all-characteristics U=X-Y,V=Y')
 mutants=0
 for f in r:
  key=next(iter(f));g=dict(f);g[key]=-g[key]
  need(sub(g,image)!=sub(f,image),'sign perturbation not detected');mutants+=1
 # Finite ranks of ALL placements u Q v, no normal-form assumption.
 def field(p):
  if p==4:
   def times(a,b):
    ans=0
    while b:
     if b&1:ans^=a
     a<<=1
     if a&4:a^=7
     b>>=1
    return ans
   return lambda a,b:a^b,times,lambda a:a,lambda a:times(a,a)
  return lambda a,b:(a+b)%p,lambda a,b:a*b%p,lambda a:-a%p,lambda a:pow(a,p-2,p)
 cases=[]
 for p,beta in [(3,0),(5,0),(5,2),(5,3),(4,0),(4,2),(4,3)]:
  plus,times,negative,inv=field(p)
  for n in range(2,7):
   words=list(product(range(2),repeat=n));cols={w:i for i,w in enumerate(words)};rows=[]
   for pos in range(n-1):
    for pre in product(range(2),repeat=pos):
     for post in product(range(2),repeat=n-pos-2):
      row=[0]*len(words)
      for pair,c in [((0,0),beta),((0,1),negative(1)),((1,0),1),((1,1),negative(beta))]:row[cols[pre+pair+post]]=c
      rows.append(row)
   rank=0
   for col in range(len(words)):
    k=next((i for i in range(rank,len(rows))if rows[i][col]),None)
    if k is None:continue
    rows[rank],rows[k]=rows[k],rows[rank];factor=inv(rows[rank][col]);rows[rank]=[times(factor,c)for c in rows[rank]]
    for i in range(rank+1,len(rows)):
     factor=rows[i][col]
     if factor:rows[i]=[plus(a,negative(times(factor,b)))for a,b in zip(rows[i],rows[rank])]
    rank+=1
   dim=len(words)-rank;need(dim==n+1,'finite rank diagnostic');cases.append({'field':p,'beta':beta,'degree':n,'dimension':dim})
 return {'result':'PASS','exact_symbolic_checks':['six quotient images','scalar quotient','positive pullback','untwisted countercheck','inverse countercheck outside characteristic 2','division-free variable change'],'sign_mutations_rejected':mutants,'finite_cases':cases,'limit':'Finite ranks are diagnostics; universal proof is in MATHEMATICAL_REVIEW.md.'}
if __name__=='__main__':print(json.dumps(main(),indent=2,sort_keys=True))
