#!/usr/bin/env python3
"""Exact controls for the scoped different/ramification theorem. Requires SymPy."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from collections import Counter
import hashlib,json
import sympy as S
C=Counter()
def ck(k,b):
 assert bool(b),k
 C[k]+=1
def v2(a):
 a=abs(int(a));assert a
 return (a&-a).bit_length()-1
x=S.Symbol('x');polys=[S.Poly(x,x)];rows=[]
for n in range(1,8):
 P=polys[-1]**2+S.Poly(1,x);polys.append(P)
 eps=n%2;Q=S.Poly(P.as_expr().subs(x,x+eps),x)
 ck('mod2_iterate',all(int(c)%2==int(i==2**n or (i==0 and eps)) for i,c in enumerate(reversed(P.all_coeffs()))))
 ck('Eisenstein_monic',Q.LC()==1)
 ck('Eisenstein_nonleading',all(int(c)%2==0 for c in Q.all_coeffs()[1:]))
 ck('Eisenstein_constant',int(Q.TC())%4==2)
 rhs=S.Poly(2**n,x)
 for j in range(n):rhs*=polys[j]
 ck('chain_rule_polynomial',P.diff()==rhs)
 d=2**n*(F(n)+sum((F(1,4**j) for j in range(1,n//2+1)),F(0)))
 ck('different_integer',d.denominator==1)
 if n<=6:
  disc=P.discriminant();ck('polynomial_discriminant_valuation',v2(disc)==d)
  ck('translation_discriminant',Q.discriminant()==disc)
 rows.append({'n':n,'degree':2**n,'different_exponent':int(d),'normalized_different':str(d/F(2**n)),'upper_break_lower_bound_without_positive_remainder':str(d/F(2**n)-1)})
# Exact recurrence congruences without growing the full critical orbit.
a=0
for n in range(1,129):
 a=(a*a+1)%16
 ck('critical_orbit_mod4',a%4==(1 if n%2 else 2))
 delta=F(n)+(1-F(1,4**(n//2)))/3
 direct=F(n)+sum((F(1,4**j) for j in range(1,n//2+1)),F(0))
 ck('geometric_sum',delta==direct)
 ck('upper_break_growth',delta-1>=n-1)
 ck('integral_different_formula',(2**n*delta).denominator==1)
# Hilbert/Herbrand identity for abstract finite order profiles. These are
# normalization controls; no assertion that each profile is realizable by a field.
for k in range(1,5):
 e=2**k
 for exponents in product(range(1,k+1),repeat=4):
  if list(exponents)!=sorted(exponents,reverse=True):continue
  orders=[e]+[2**i for i in exponents]
  different=(e-1)+sum(g-1 for g in orders)
  upper_widths=[F(g,e) for g in orders]
  b=sum(upper_widths,F(0))
  integral=sum((width*(1-F(1,g)) for width,g in zip(upper_widths,orders)),F(0))
  ck('Hilbert_Herbrand_normalization',F(different,e)==1-F(1,e)+integral)
  ck('largest_break_bound',b>=F(different,e)-1+F(1,e))
# First four exact values separately guard against parity/indexing mistakes.
ck('first_values',[row['different_exponent'] for row in rows[:4]]==[2,9,26,69])
root=Path(__file__).resolve().parent
r={'status':'PASS','exact_assertions':sum(C.values()),'checks':dict(C),'finite_levels':rows,'artifact_sha256':hashlib.sha256((root/'PARTIAL_RESULT.md').read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'sympy_version':S.__version__,'scope':'Finite Eisenstein, derivative and discriminant controls, exact geometric sums, and abstract ramification-normalization tests. No splitting-field group enumeration or numerical inference of an infinite tower.'}
(root/'verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
