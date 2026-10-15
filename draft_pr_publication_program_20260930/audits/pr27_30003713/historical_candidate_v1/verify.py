#!/usr/bin/env python3
"""Small exact free-Lie adjoint checks. No all-degree solution is certified."""
from functools import lru_cache
from itertools import product
from pathlib import Path
from math import comb
import json
import sympy as s

def lyndon(w):return bool(w) and all(w<w[k:]+w[:k] for k in range(1,len(w)))
def mul(a,b):
 out={}
 for u,x in a.items():
  for v,y in b.items():out[u+v]=out.get(u+v,0)+x*y
 return {w:x for w,x in out.items() if x}
def bracket(a,b):
 out=mul(a,b)
 for w,x in mul(b,a).items():out[w]=out.get(w,0)-x
 return {w:x for w,x in out.items() if x}
@lru_cache(None)
def expansion(w):
 if len(w)==1:return {w:1}
 k=next(k for k in range(1,len(w)) if lyndon(w[k:]))
 assert lyndon(w[:k])
 return bracket(expansion(w[:k]),expansion(w[k:]))
def words(m,d):return [w for w in product(range(m),repeat=d) if lyndon(w)]
def witt(m,d):return sum(int(s.mobius(a))*m**(d//a) for a in s.divisors(d))//d
results=[]
for m,maxd in [(2,6),(3,5)]:
 for d in range(2,maxd+1):
  prev=words(m,d-1);basis=words(m,d)
  assert len(prev)==witt(m,d-1) and len(basis)==witt(m,d)
  columns=[bracket({(v,):1},expansion(w)) for v in range(m) for w in prev]
  rowwords=sorted(set().union(*(set(x) for x in columns)))
  M=s.Matrix([[c.get(w,0) for c in columns] for w in rowwords]);rank=M.rank()
  assert rank==len(basis)
  kernel=len(columns)-rank
  if d==2:assert kernel==comb(m+1,2)
  if d==3:assert kernel==comb(m,3)
  if d==4:assert kernel==m*m*(m*m-1)//12
  results.append({'dim_V':m,'degree_V':d,'domain':len(columns),'rank':rank,'kernel':kernel})
# Dimension-one V: the current Lie algebra is abelian; check splitting (1).
for e in range(0,8):
 for n in range(0,e+3):
  choose=lambda a,b:comb(a,b) if 0<=b<=a else 0
  assert choose(e,n)+choose(e,n-1)==choose(e+1,n)
out={'scope':'Known adjoint layer and abelian boundary case only; not the full requested decomposition','adjoint_models':results,'abelian_boundary_models':sum(e+3 for e in range(8)),'all_passed':True,'sympy_version':s.__version__}
Path(__file__).with_name('verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
