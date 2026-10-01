#!/usr/bin/env python3
"""Finite exact controls of the known theorem's combinatorial specialization."""
from itertools import product,combinations
import json
checks=0
def ck(v):
 global checks
 assert v
 checks+=1

def lines(t,n):
 result=[]
 for template in product(range(t+1),repeat=n):
  if t not in template:continue
  L=frozenset(tuple(a if b==t else b for b in template) for a in range(t))
  result.append((template,L))
 return result
cases=[]
for t,n in [(2,1),(2,2),(2,3),(3,1),(3,2),(3,3),(4,1),(4,2),(4,3),(4,4)]:
 ls=lines(t,n)
 ck(len(ls)==(t+1)**n-t**n);ck(len({L for _,L in ls})==len(ls))
 for template,L in ls:
  ck(len(L)==t)
  active={i for i,v in enumerate(template) if v==t}
  ck(bool(active))
  for u,v in combinations(L,2):
   ck({i for i in range(n) if u[i]!=v[i]}==active)
   ck(all(u[i]==v[i]==template[i] for i in range(n) if i not in active))
 for (_,L),(_,M) in combinations(ls,2):ck(len(L&M)<=1)
 cases.append({'alphabet':t,'dimension':n,'vertices':t**n,'lines':len(ls)})
# Small Hales-Jewett controls are not proofs of the arbitrary-color theorem.
vs=list(product(range(2),repeat=2));ed=[L for _,L in lines(2,2)]
for cs in product(range(2),repeat=len(vs)):
 color=dict(zip(vs,cs));ck(any(len({color[v] for v in e})==1 for e in ed))
# Why merely preserving a subdivision cannot be used: the old monochromatic
# tetrahedron is replaced by four nonmonochromatic ones with a new vertex.
old=frozenset(range(4));new=[(old-{i})|{4} for i in old];color={i:0 for i in old};color[4]=1
ck(len({color[v] for v in old})==1)
ck(all(len({color[v] for v in e})==2 for e in new))
ck(old not in new)
# A genuine subcomplex inclusion retains every old coloring constraint.
small=[frozenset(range(4)),frozenset([3,4,5,6])]
large=small+[frozenset([0,4,6,7])]
for cs in product(range(2),repeat=8):
 good_big=all(len({cs[v] for v in e})>1 for e in large)
 good_small=all(len({cs[v] for v in e})>1 for e in small)
 ck(not good_big or good_small)
print(json.dumps({'status':'PASS','exact_assertions':checks,'floating_diagnostics':0,'finite_line_controls':cases,'scope':'Checks finite Hales-Jewett incidence, exact four-vertex specialization and preservation of coloring constraints. The published all-color Ramsey and PL topology theorems are mathematical inputs, not computational claims.'},sort_keys=True,indent=2))
