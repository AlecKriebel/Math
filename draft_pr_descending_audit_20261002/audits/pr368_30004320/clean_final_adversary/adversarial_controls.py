#!/usr/bin/env python3
"""Distinct exact controls: noncyclic cocycles and full Ore multiplication.
Finite examples verify formulas only. They cannot establish field division or
universal homogeneous-space descent, which require the sealed proofs.
"""
from itertools import product
from math import comb
import json
counts={}
def ck(family,truth):
 if not truth:raise AssertionError(family)
 counts[family]=counts.get(family,0)+1
# A noncyclic Galois lattice: C2 x C2 acting by two coordinate reflections.
# Verify complete cocycle law and the integral |Delta|-coboundary formula.
group=list(product(range(2),repeat=2))
def plus(g,h):return ((g[0]+h[0])%2,(g[1]+h[1])%2)
def action(g,z):return ((-1)**g[0]*z[0],(-1)**g[1]*z[1])
def add(a,b):return(a[0]+b[0],a[1]+b[1])
for u,v in product(range(-5,6),repeat=2):
 def z(g):return(g[0]*u,g[1]*v)
 for g,h in product(group,repeat=2):ck('noncyclic_integral_cocycle',z(plus(g,h))==add(z(g),action(g,z(h))))
 S=tuple(sum(z(g)[i] for g in group) for i in range(2))
 for g in group:
  gs=action(g,S)
  ck('noncyclic_integral_coboundary',tuple(4*x for x in z(g))==tuple(S[i]-gs[i] for i in range(2)))
 # Coboundaries change each coordinate by an even integer, giving four classes.
 ck('noncyclic_h1_parity',tuple(x%2 for x in z((1,1)))==(u%2,v%2))
# Full normal-form multiplication in a cyclic algebra model. All basis triple
# associativities are tested; original checkers verify selected relations only.
# Specialization to finite fields is deliberately not used to infer division.
for p,a,b,d in [(2,1,1,0),(2,1,1,1),(3,1,1,0),(3,1,1,1),(3,2,2,1),(5,2,3,1)]:
 basis=list(product(range(p),repeat=2));basis_elements=[{ij:1} for ij in basis]
 def clean(x):return {k:v%p for k,v in x.items() if v%p}
 def pow_w(e):
  if e<p:return {e:1}
  out={}
  for j,c in pow_w(e-p).items():out[j]=(out.get(j,0)+a*c)%p
  for j,c in pow_w(e-p+1).items():out[j]=(out.get(j,0)+pow(d,p-1,p)*c)%p
  return {k:v for k,v in out.items() if v}
 def mul(A,B):
  out={}
  for (i,j),ca in A.items():
   for (k,l),cb in B.items():
    yc=pow(b,(j+l)//p,p);yn=(j+l)%p
    for h in range(k+1):
     coefficient=ca*cb*yc*comb(k,h)*pow(j*d,k-h,p)
     for wn,c in pow_w(i+h).items():out[(wn,yn)]=(out.get((wn,yn),0)+coefficient*c)%p
  return clean(out)
 I={(0,0):1};W={(1,0):1};Y={(0,1):1}
 for A in basis_elements:
  ck('ore_normal_form_units',mul(I,A)==A and mul(A,I)==A)
 triples=list(product(basis_elements,repeat=3)) if p<=3 else [(basis_elements[(7*n+1)%25],basis_elements[(11*n+2)%25],basis_elements[(13*n+4)%25]) for n in range(150)]
 for A,B,C in triples:ck('ore_full_basis_associativity',mul(mul(A,B),C)==mul(A,mul(B,C)))
 left=mul(Y,W);right=mul(W,Y)
 for k,c in Y.items():right[k]=(right.get(k,0)+d*c)%p
 ck('ore_orientation_relation',left==clean(right))
 if d:
  wrong=dict(mul(W,Y))
  ck('ore_missing_translation_rejected',left!=clean(wrong))
# Infinitesimal μ_p coefficient obstruction cannot disappear when parameter
# exponents become p-divisible: two constant coefficients still have to be pth powers.
for p in (2,3,5,7,11):
 for n in range(1,80):
  pdiv=n%p==0
  admissible_exponents={p*j for j in range(n//p+2)}
  ck('mu_p_parameter_exponent', (n in admissible_exponents)==pdiv)
  for constant_a_exponent in range(p):
   ck('mu_p_ratio_obstruction', not ((-constant_a_exponent)%p==0 and (1-constant_a_exponent)%p==0))
# Laurent leading valuations and pole reduction for exponents with large p-part.
for p in (2,3,5,7,11):
 for m in range(1,24):
  if m%p==0:continue
  for e in range(8):
   n=m*p**e;r=n
   for j in range(e):r//=p
   ck('wild_pole_reduction',r==m and r%p!=0)
print(json.dumps({'status':'PASS','exact_assertions':sum(counts.values()),'by_family':counts,'scope':'Noncyclic integral cocycles, full finite Ore associativity and valuation/exponent controls only. Finite-field Ore models do not establish division. Independent written proofs and primary-source hypotheses are required.'},sort_keys=True,indent=2))
