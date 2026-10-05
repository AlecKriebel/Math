#!/usr/bin/env python3
"""Independent primary-source verification of HT Theorem 5.1 at A4,r=10,p=5.
The existence of the modular category remains a cited construction input.
No submitted proof/calculator is imported or executed.
"""
from pathlib import Path
from itertools import permutations, product
from fractions import Fraction
import json, sys, platform
import sympy as sp

z=sp.Symbol('z'); phi=sp.Poly(sp.cyclotomic_poly(50,z),z,domain=sp.QQ)
def red(a): return sp.rem(sp.Poly(a,z,domain=sp.QQ),phi).as_expr()
def mul(a,b):return red(a*b)
def powz(n):return red(z**(n%50))
def conj(a):return red(sum(c*powz(-i[0]) for i,c in sp.Poly(a,z).terms()))
def divide(a,b):return mul(a,sp.invert(sp.Poly(b,z,domain=sp.QQ),phi).as_expr())
def sign(w):return (-1)**sum(w[i]>w[j] for i in range(5) for j in range(i+1,5))
rho=(2,1,0,-1,-2)
s2=sp.Rational(1,50000)
for j in range(1,5):
 factor=red(2-powz(5*j)-powz(-5*j))
 for unused in range(5-j):s2=mul(s2,factor)
# sqrt(5)=1+2(ζ5+ζ5^-1), ζ5=ζ50^10.
sqrt5=red(1+2*(powz(10)+powz(-10)))
assert mul(sqrt5,sqrt5)==5
records=[]
for q in (1,2,3,4):
 good=[]; G=sp.Integer(0); nontrivial=0
 for w in permutations(range(5)):
  wr=tuple(rho[w[i]] for i in range(5))
  alpha=tuple(q*rho[i]-wr[i] for i in range(5))
  counts=[0]*5
  # ν = Σ_(i=0..3) ni(e_i-e_4), ni∈{0,...,4}.
  for ns in product(range(5),repeat=4):
   exponent=sum(ns[i]*(alpha[i]-alpha[4]) for i in range(4))%5
   counts[exponent]+=1
  qualifies=all((alpha[i]-alpha[4])%5==0 for i in range(4))
  # Explicit exact character cancellation in Q(ζ5): either 625 or 125Φ5.
  assert counts==([625,0,0,0,0] if qualifies else [125]*5)
  if not qualifies:nontrivial+=1;continue
  dot=sum(rho[i]*wr[i] for i in range(5))
  sg=sign(w);G=red(G+sg*powz(-dot))
  good.append({'permutation':w,'rho_dot_w_rho':dot,'sign':sg,'coordinate_residue':alpha[0]%5,'character_counts':counts})
 assert len(good)==5 and nontrivial==115
 G2=mul(G,conj(G)); ht2=red(G2/sp.Integer(80)); normalized=divide(ht2,s2)
 A,B=(3475,1550) if q in (1,4) else (4025,1800)
 target=red(A+B*sqrt5)
 assert normalized==target
 records.append({'q':q,'qualifying_permutations':good,'G_cyclotomic':str(G),'G_abs_squared':str(G2),'HT_abs_squared':str(ht2),'S3_normalized_abs_squared':str(normalized),'radical':[A,B],'matches_claim_exactly':True,'approx_normalized':A+B*5**0.5})
result={'method':'HT Theorem 5.1 direct root-lattice character sums, rational polynomial arithmetic modulo Φ50; no submitted code','python':sys.version,'platform':platform.platform(),'sympy':sp.__version__,'phi50':str(phi.as_expr()),'rho':rho,'S00_squared':str(s2),'D_squared':str(divide(1,s2)),'sqrt5_cyclotomic':str(sqrt5),'results':records,'difference_q2_minus_q1':{'radical':[550,250],'positive_proof':'550 + 250*sqrt(5) > 0'},'construction_input':'Hansen–Takata Sections 4/5 modular category V_r^g; not independently re-proved here'}
Path('computation/independent_ht_gauss.result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
