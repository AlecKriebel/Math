#!/usr/bin/env python3
"""Exact standard-library checks supporting the all-degree proof."""
from pathlib import Path
from datetime import datetime,timezone
import json,random,hashlib
M=((10,3),(3,1));C=((1,-3),(-3,10));B=((0,-3),(-3,9));I=((1,0),(0,1));e1=(1,0);e2=(0,1)
def mm(a,b):return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)) for i in range(2))
def mv(a,v):return tuple(sum(a[i][j]*v[j] for j in range(2)) for i in range(2))
def mp(a,n):
 out=I
 while n:
  if n&1:out=mm(out,a)
  a=mm(a,a);n//=2
 return out
def det(v,w):return v[0]*w[1]-v[1]*w[0]
def dm(a):return det((a[0][0],a[1][0]),(a[0][1],a[1][1]))
def sub(v,w):return tuple(x-y for x,y in zip(v,w))
def ell(v):return det(v,mv(B,e2))
def f(n):return ell(sub(mv(mp(C,n),e1),e1))
def heis(x,y,mod):
 v,z=x;w,s=y
 return (tuple((v[i]+w[i])%mod for i in range(2)),(z+s+det(v,w)*pow(2,-1,mod))%mod)
def act(a,x,mod):
 v,z=x;return (tuple(k%mod for k in mv(a,v)),z%mod)
def run():
 assert mm(M,C)==I and dm(M)==dm(C)==1 and dm(B)==-9
 assert [f(n) for n in range(4)]==[0,-9,-18,-108]
 vals=[ell(mv(mp(C,n),e1)) for n in range(70)]
 assert all(vals[n+2]==11*vals[n+1]-vals[n] for n in range(68))
 assert all(vals[n+1]<vals[n] for n in range(2,69))
 ds=[]
 for d in range(1,51):
  v=mv(mp(B,d),e1);assert det(v,mv(C,v))==(-9)**d*(-3)
  lhs=[f(n) for n in range(d+2)]
  for _ in range(d):lhs=[lhs[i+1]-lhs[i] for i in range(len(lhs)-1)]
  rhs=[ell(mv(mp(C,n),v)) for n in range(2)]
  assert lhs==rhs and any(rhs);ds.append(d)
 rng=random.Random(1222026);samples=0
 for r in range(1,8):
  mod=3**r;a=mp(M,mod)
  assert all((a[i][j]-I[i][j])%(3**(r+1))==0 for i in range(2) for j in range(2))
  for _ in range(100):
   x=((rng.randrange(mod),rng.randrange(mod)),rng.randrange(mod));y=((rng.randrange(mod),rng.randrange(mod)),rng.randrange(mod))
   assert act(M,heis(x,y,mod),mod)==heis(act(M,x,mod),act(M,y,mod),mod);samples+=1
 return {'utc':datetime.now(timezone.utc).isoformat(),'result':'PASS_EXACT_CENTRAL_NONPOLYNOMIAL_CONTROLS','matrices':{'M':M,'C':C,'B':B},'finite_difference_degrees_checked':ds,'finite_quotient_levels':7,'heisenberg_automorphism_samples':samples,'first_f_values':[str(f(n)) for n in range(8)],'proof_sha256':hashlib.sha256(Path(__file__).with_name('CENTRAL_NONPOLYNOMIAL.md').read_bytes()).hexdigest(),'scope':'Supporting finite checks; all-degree failure follows from the written determinant argument. Not a21.122 counterexample or complete solution.'}
if __name__=='__main__':
 out=run();Path(__file__).with_name('central_countermodel_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
