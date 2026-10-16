#!/usr/bin/env python3
"""Independent exact finite controls; not a proof of a universal topological claim.
Standard library, deterministic, no network, no mutation apart from stdout.
"""
from itertools import combinations
from collections import Counter
import json, random

def subsets(x, proper=False):
 x=sorted(x)
 return {frozenset(y) for k in range(len(x)+(not proper)) for y in combinations(x,k)}
def closure(facets):
 return set().union(*(subsets(f) for f in facets))
def rank2(cols):
 b={}
 for c in cols:
  while c:
   j=c.bit_length()-1
   if j not in b:b[j]=c;break
   c^=b[j]
 return len(b)
def boundary(x):return [x-{a} for a in sorted(x)]
def betti01(k):
 vs=sorted((f for f in k if len(f)==1),key=lambda s:tuple(sorted(s)))
 es=sorted((f for f in k if len(f)==2),key=lambda s:tuple(sorted(s)))
 ts=[f for f in k if len(f)==3]
 vi={f:i for i,f in enumerate(vs)};ei={f:i for i,f in enumerate(es)}
 r1=rank2([sum(1<<vi[f] for f in boundary(e)) for e in es])
 r2=rank2([sum(1<<ei[f] for f in boundary(t)) for t in ts])
 return [len(vs)-r1-1,len(es)-r1-r2]
def solve(columns,target):
 b={}
 for j,c in enumerate(columns):
  w=1<<j
  while c:
   i=c.bit_length()-1
   if i not in b:b[i]=(c,w);break
   c^=b[i][0];w^=b[i][1]
 out=0
 while target:
  i=target.bit_length()-1
  assert i in b,'No chain filling'
  target^=b[i][0];out^=b[i][1]
 return [j for j in range(len(columns)) if (out>>j)&1]
def fill(k,z,degree,avoid):
 pool=sorted((f for f in k if len(f)==degree+1 and not f&avoid),key=lambda s:tuple(sorted(s)))
 lower=sorted({e for f in pool for e in boundary(f)}|z,key=lambda s:tuple(sorted(s)))
 ix={e:i for i,e in enumerate(lower)}
 cols=[sum(1<<ix[e] for e in boundary(f)) for f in pool]
 target=sum(1<<ix[e] for e in z)
 return {pool[j] for j in solve(cols,target)}
def moves(facets,k,next_vertex):
 out=[]
 for a in sorted((x for x in k if x),key=lambda s:(len(s),tuple(sorted(s)))):
  fs={f for f in facets if a<=f}
  if len(a)==5:
   b=frozenset({next_vertex})
  else:
   b=frozenset().union(*(f-a for f in fs))
   if len(a)+len(b)!=6 or b in k:continue
   if {f-a for f in fs}!={b-{v} for v in b}:continue
  if len(a)+len(b)==6:
   nf=(facets-fs)|{b|(a-{v}) for v in a}
   out.append((a,b,nf))
 return out

def missing(k):
 vs=sorted(set().union(*k))
 return {frozenset(t) for t in combinations(vs,3) if frozenset(t) not in k and all(frozenset(e) in k for e in combinations(t,2))}

def witness(k,newk,a,b,v):
 U=a|b;M=b|{v};V=U|{v};cv={}
 for w in sorted(U):
  e=frozenset({v,w})
  cv[frozenset({w})]={e} if e in k else fill(k,{frozenset({v}),frozenset({w})},1,U-{w})
 for e in sorted((f for f in k if len(f)==2 and f<=U),key=lambda s:tuple(sorted(s))):
  t=e|{v}
  if t in k:cv[e]={t}
  else:
   z={e}
   for w in e:z^=cv[frozenset({w})]
   cv[e]=fill(k,z,2,U-e)
 def B(s):
  if v not in s or s==M:return {s}
  return cv[s-{v}]
 triangles=[frozenset(s) for s in combinations(sorted(V),3)]
 omega=set()
 for i,s in enumerate(triangles):
  for t in triangles[i+1:]:
   if s&t:continue
   for x in B(s):
    for y in B(t):
     assert not x&y
     assert x in newk or x==M
     assert y in newk or y==M
     cell=tuple(sorted((tuple(sorted(x)),tuple(sorted(y)))))
     if cell in omega:omega.remove(cell)
     else:omega.add(cell)
 bd=set()
 for s,t in omega:
  for x,y in [(s,t),(t,s)]:
   for e in combinations(x,2):
    c=(e,y)
    if c in bd:bd.remove(c)
    else:bd.add(c)
 assert not bd
 paired={frozenset(t if frozenset(s)==M else s) for s,t in omega if frozenset(s)==M or frozenset(t)==M}
 assert paired==set(boundary(a))
 crossings=0
 for s,t in omega:
  u=sorted(s+t)
  crossings+=tuple(u[::2]) in (s,t)
 assert crossings%2==1
 return {'cells':len(omega),'moment_curve_pairing_mod2':crossings%2}

def main():
 rng=random.Random(49830000689)
 facets={frozenset(s) for s in combinations(range(6),5)}
 counts=Counter();common=0;new2=0;new1=0;complements=0;records=[];nextv=6
 for step in range(100):
  k=closure(facets);opts=moves(facets,k,nextv)
  # Favor all five move types and bounded vertex counts without losing determinism.
  n=len(set().union(*k));weights=[]
  for a,b,nf in opts:
   p=len(a)-1
   w=1/(1+counts[p])
   if p==4:w*=2 if n<8 else .04
   if p==0:w*=3 if n>9 else .1
   weights.append(w)
  a,b,nf=rng.choices(opts,weights=weights,k=1)[0]
  p=len(a)-1;q=len(b)-1;nk=closure(nf);counts[p]+=1
  if q==0:nextv+=1
  oldT={f for f in k if f<=a|b and len(f)<=3}
  newT={f for f in nk if f<=a|b and len(f)<=3}
  support=frozenset().union(*oldT)
  assert set().union(*k)-support
  # Check the cone and induced-complement homology hypotheses, including endpoint moves.
  for rho in oldT&newT:
   W=support-rho
   kw={f for f in k if f<=W}
   assert any(all(f|{v} in kw for f in kw) for v in W)
   complement={f for f in k if not f&W and len(f)<=3}
   assert betti01(complement)==[0,0]
   complements+=1
  om=missing(k);nm=missing(nk)
  for M in om&nm:
   common+=1
   assert not M<=support
   assert not a<=M
   assert all(not a<=e for e in boundary(M))
  for M in nm-om:
   if M in k:
    assert p==q==2 and M==a and b in om
    assert {f for f in nk if len(f)<=3}|{M}=={f for f in k if len(f)<=3}|{b}
    new2+=1
   else:
    assert p==3 and q==1 and b<=M and len(M-(a|b))==1
    v=next(iter(M-(a|b)))
    rec=witness(k,nk,a,b,v);records.append(rec);new1+=1
  facets=nf
 assert all(counts[p] for p in range(5)),counts
 assert new1 and new2 and common
 print(json.dumps({'seed':49830000689,'transitions':100,'moves_by_p':dict(sorted(counts.items())),
  'complement_checks':complements,'persistent_missing_triangle_checks':common,
  'new_missing_p2_q2_checks':new2,'new_missing_p3_q1_witnesses':new1,
  'witness_details':records,'scope':'Independent finite combinatorial and mod-2 chain controls only; no exotic sphere recognition or universal topology claim.'},indent=2,sort_keys=True))
if __name__=='__main__':main()
