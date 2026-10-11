#!/usr/bin/env python3
"""Independent bounded checks of the known local Hilbert--Burch theorem's application."""
from pathlib import Path
from itertools import product
from collections import Counter
from fractions import Fraction as F
import hashlib,json
import sympy as s
counts=Counter()
def check(v,label):
 assert v,label
 counts[label]+=1
def compositions(n,k):
 if k==1:yield(n,);return
 for a in range(n+1):
  for q in compositions(n-a,k-1):yield(a,)+q
staircases=0
# Generate exponent differences, rather than sorted staircase heights.
for t in range(1,6):
 for total in range(1,8):
  for tail in compositions(total-1,t):
   d=(tail[0]+1,)+tail[1:];m=[0]
   for q in d:m.append(m[-1]+q)
   staircases+=1;M=1+t+sum(m)
   for i in range(1,t+2):
    for j in range(1,t+1):
     cap=d[min(i,j)-1];u=m[j]-m[i-1]+i-j
     positive=[];allowed=[]
     for e in range(cap):
      wx=i-j;wy=m[j]-m[i-1]-e
      weight=-(M-1)*wx-M*wy
      check(weight==M*(e-u)+i-j,'bidegree_weight_identity')
      check(weight!=0,'no_zero_weight')
      if weight>0:positive.append(e)
      if (e>u if i<=j else e>=u):allowed.append(e)
     check(positive==allowed,'matrix_space_equality')
   # Count surviving monomials directly by divisibility against every generator.
   gens=[(t-j,m[j]) for j in range(t+1)]
   standard=[(a,b) for a in range(t) for b in range(m[-1]) if not any(a>=c and b>=e for c,e in gens)]
   check(len(standard)==sum(m),'direct_staircase_colength')
# Finite-order comparison by sorting monomials in two unrelated ways.
for D in range(1,25):
 mon=[(a,b) for a in range(D+1) for b in range(D+1-a)]
 bylocal=sorted(mon,key=lambda ab:(sum(ab),-ab[0]))
 for M in (D+2,2*D+7):
  byweight=sorted(mon,key=lambda ab:-(-(M-1)*ab[0]-M*ab[1]))
  check(bylocal==byweight,'negative_degree_lex_sorted_order')
# Inverse coefficients by a triangular recurrence, not a geometric-series sum.
for u in (F(-3),F(-1),F(1,2),F(1),F(2)):
 for W in product(range(-2,3),repeat=3):
  f=[u]+list(map(F,W));g=[1/u]
  for n in range(1,13):g.append(-sum(f[j]*g[n-j] for j in range(1,min(n,3)+1))/u)
  check(all(sum(f[j]*g[n-j] for j in range(min(n,3)+1))==(1 if n==0 else 0) for n in range(13)),'formal_inverse_recurrence')
# Independently compute the explicit support-removal example from the primary source.
x,y,a,b=s.symbols('x y a b')
M=s.Matrix([[y,0,a,0],[-x,1,0,0],[0,-x,1,0],[0,0,-x,y*y],[0,0,0,b*y-x]])
f=[s.expand(M[[j for j in range(5) if j!=i],:].det()) for i in range(5)]
check(s.expand(s.resultant(f[0],f[-1],x)-y**12*(1+a*b*b*y))==0,'symbolic_resultant_factor')
for av,bv in product((-2,-1,1,2),repeat=2):
 I=[p.subs({a:av,b:bv}) for p in f]
 distant={x:-s.Rational(1,av*bv),y:-s.Rational(1,av*bv*bv)}
 check(all(p.subs(distant)==0 for p in I),'distant_component_present')
 for cut,want in ((False,7),(True,6)):
  G=s.groebner(I+([y**12] if cut else[]),x,y,order='lex')
  leading=[p.LM(order=G.order).exponents for p in G.polys]
  basis=[(r,q) for r in range(16) for q in range(16) if not any(r>=u and q>=v for u,v in leading)]
  check(len(basis)==want,'polynomial_vs_punctual_colength')
  check(max(r for r,q in basis)<15 and max(q for r,q in basis)<15,'standard_monomial_bound')
 # A polynomial Bezout identity proves completion equality in this example.
 z=av*bv*bv*y;geom=sum((-z)**j for j in range(12))
 check(s.expand((1+z)*geom-(1-z**12))==0,'unit_factor_Bezout_identity')
base=Path(__file__).resolve().parent
r={'status':'PASS','assertions':sum(counts.values()),'categories':dict(counts),'staircases':staircases,'artifact_sha256':hashlib.sha256((base/'author_replay/KNOWN_RESULT.md').read_bytes()).hexdigest(),'limits':'Bounded convention and completion controls; Oszer\'s published isomorphism remains a credited theorem, not independently reproved.'}
(base/'independent_results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
