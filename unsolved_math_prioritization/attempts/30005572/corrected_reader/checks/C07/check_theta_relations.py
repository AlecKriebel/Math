#!/usr/bin/env python3
"""Exact free-exterior-algebra checks; no numerical K-theory inference."""
import itertools, json, math
from collections import defaultdict

def add(x,y): return {k:x.get(k,0)+y.get(k,0) for k in set(x)|set(y) if x.get(k,0)+y.get(k,0)}
def mul(c,x): return {k:c*v for k,v in x.items() if c*v}
def wedge(x,y):
 d=defaultdict(int)
 for a,u in x.items():
  for b,v in y.items():
   if a!=b:d[(min(a,b),max(a,b))]+=u*v*(1 if a<b else -1)
 return {k:v for k,v in d.items() if v}
def total(xs):
 d={}
 for x in xs:d=add(d,x)
 return d

def audit_group(moduli):
 G=list(itertools.product(*(range(n) for n in moduli)))
 zero=tuple(0 for n in moduli)
 plus=lambda x,y:tuple((a+b)%n for a,b,n in zip(x,y,moduli))
 neg=lambda x:tuple(-a%n for a,n in zip(x,moduli))
 minus=lambda x,y:plus(x,neg(y))
 def h(x):
  if x==zero:return {}
  return {min(x,neg(x)):1}
 def psi(a,b):
  c=neg(plus(a,b));return total([wedge(h(a),h(b)),wedge(h(b),h(c)),wedge(h(c),h(a))])
 def pair(x,y):return add(h(plus(x,y)),h(minus(x,y)))
 def phi(x,y,z):
  A,B,C=pair(z,x),pair(y,x),pair(z,y)
  return total([wedge(A,B),wedge(B,C),wedge(C,A)])
 def delta(a,b,c,d):
  P=add(pair(c,a),pair(d,b));Q=add(pair(c,b),pair(d,a));V=add(pair(b,a),pair(d,c))
  return wedge(add(P,mul(-1,Q)),add(V,mul(-1,Q)))
 for a,b,c,d in itertools.product(G,repeat=4):
  expected=total([phi(a,b,c),phi(c,d,a),phi(b,a,d),phi(d,c,b)])
  assert delta(a,b,c,d)==expected
  if len({min(t,neg(t)) for t in [a,b,c,d]})<4:assert not delta(a,b,c,d)
 for y,z in itertools.product(G,repeat=2):assert not total(phi(x,y,z) for x in G)
 for a,b in itertools.product(G,repeat=2):
  c=neg(plus(a,b))
  lhs=total(phi(x,minus(neg(b),x),minus(a,x)) for x in G)
  Rs=total(psi(plus(u,plus(x,x)),v) for u,v in [(c,a),(b,c),(a,b)] for x in G)
  assert lhs==add(mul(len(G),psi(a,b)),Rs)
  for u,v in [(c,a),(b,c),(a,b)]:
   assert total(phi(zero,v,plus(u,plus(x,x))) for x in G)==mul(4,total(psi(plus(u,plus(x,x)),v) for x in G))
 return {'group':moduli,'order':len(G),'identities':'all exact'}

A,B,C={1:1},{2:1},{3:1}
X=total([mul(-1,A),mul(3,B),mul(-2,C)])
Y=total([mul(2,A),B,mul(-3,C)])
Psi=total([wedge(A,B),wedge(B,C),wedge(C,A)])
assert wedge(X,Y)==mul(-7,Psi)
assert 3*(-3)-(-2)*1==-7
out={'groups':[audit_group(m) for m in [(4,),(5,),(7,),(2,2),(2,3)]],
 'cyclic7_cross_ratio_wedge':wedge(X,Y),
 'level4_scalar5':{'theta_divisor_factor':24,'raw_pair_factor':576,'correct_smoothing_factor':624,'three_terms':[576,24,24],'sum':576+24+24},
 'scope':'Free-algebra verification, not K2 nonvanishing or an absolute cocycle computation.'}
# JSON cannot use tuple keys.
out['cyclic7_cross_ratio_wedge']={str(k):v for k,v in out['cyclic7_cross_ratio_wedge'].items()}
print(json.dumps(out,indent=2))
