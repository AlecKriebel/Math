#!/usr/bin/env python3
"""Exact elementary checks supporting the authored local proof.

This does not evaluate the LSSW cocycle, compute a global K2 presentation,
or independently certify the supplied Hilbert class polynomial.
"""
import json
from pathlib import Path
import sympy as s

x, b2, b4, b6, b8 = s.symbols('x b2 b4 b6 b8')
psi2sq = 4*x**3+b2*x**2+2*b4*x+b6
psi3 = 3*x**4+b2*x**3+3*b4*x**2+3*b6*x+b8
q4 = 2*x**6+b2*x**5+5*b4*x**4+10*b6*x**3+10*b8*x**2+(b2*b8-b4*b6)*x+b4*b8-b6**2
psi5 = s.Poly(s.expand(psi2sq**2*q4-psi3**3), x,b2,b4,b6,b8)
weights = (2,2,4,6,8)
assert all(sum(a*w for a,w in zip(m,weights)) == 24 for m,_ in psi5.terms())
assert s.Poly(psi5.as_expr(),x).degree() == 12
assert s.Poly(psi5.as_expr(),x).LC() == 5

# F8 = F2[j]/(j^3+j+1). Polynomial-basis integers 0..7.
def add(a,b): return a^b
def mul(a,b):
    z=0
    while b:
        if b&1: z ^= a
        b >>= 1
        a <<= 1
        if a&8: a ^= 0b1011
    return z

def power(a,n):
    if n<0:
        assert a
        return power(power(a,6),-n)
    z=1
    while n:
        if n&1: z=mul(z,a)
        a=mul(a,a)
        n >>= 1
    return z

j=2
assert add(add(power(j,3),j),1)==0
assert power(j,7)==1 and j!=1
assert len({power(j,n) for n in range(7)})==7
H=[1,3491750,-5151296875,12771880859375]
assert [a%2 for a in H]==[1,0,1,1]
assert all((a**3+a+1)%2 for a in (0,1))

# Upstairs exponent: Delta^48/a1^576 = j^-48 exactly,
# since Delta=a1^12/j. No finite-field assumption on a1 needed.
assert 48*12-576==0
assert power(j,-48)==j
base_residue=power(j,4)
assert power(base_residue,2)==j
assert [a for a in range(1,8) if power(a,2)==j]==[base_residue]
assert pow(576,-1,7)==4
normalized_residue=power(base_residue,pow(576,-1,7))
assert normalized_residue==power(j,2)
assert (624*pow(576,-1,7))%7==4
assert power(base_residue,(624*pow(576,-1,7))%7)==power(j,2)

# Ray-unit and coordinate checks at q²; w maps to 2 modulo 4.
assert (2**2-2+6)%4==0
units=[a for a in range(4) if s.gcd(a,4)==1]
assert units==[1,3]
def eps(a):
    assert a%4
    return int(a%2==0)

def residue(c,d,normal=False):
    assert c%4 and d%4 and (c%2 or d%2)
    return power(j,(2 if normal else 4)*(eps(d)-eps(c)))

pairs=[]
for c in range(1,4):
    for d in range(1,4):
        if c%2 or d%2:
            pairs.append({'c':c,'d':d,'raw':residue(c,d),'normalized':residue(c,d,True)})
            if (c+d)%4 and (c%2 or (c+d)%2) and ((c+d)%2 or d%2):
                assert residue(c,d)==mul(residue(c,c+d),residue(c+d,d))
                assert residue(c,d,True)==mul(residue(c,c+d,True),residue(c+d,d,True))

# All eligible determinant-one matrices modulo four satisfy the same
# endpoint difference pattern. This is a finite graph check only.
mats=[]
for a in range(4):
 for b in range(4):
  for c in range(1,4):
   for d in range(1,4):
    if (a*d-b*c)%4==1:
      assert c%2 or d%2
      mats.append((a,b,c,d))

result={
 'status':'all exact elementary checks passed',
 'scope':'specified local theta symbols; no LSSW cocycle evaluation',
 'psi5':{'degree_in_x':12,'leading_coefficient':5,'weierstrass_weight':24},
 'hilbert_polynomial_input':H,
 'hilbert_polynomial_mod_2':[1,0,1,1],
 'field_modulus_binary':'0b1011',
 'j_powers_polynomial_basis':[power(j,n) for n in range(7)],
 'residue_exponents_mod_7':{'upstairs':1,'base':4,'normalized':2,'candidate_correctly_smoothed':2},
 'admissible_coordinate_pairs':pairs,
 'eligible_SL2_Z4_matrices':len(mats),
 'warnings':['Hilbert class polynomial identification is sourced, not certified by this script.',
             'The script checks algebra in the written proof, not global CM descent or cocycle comparison.']
}
out=Path(__file__).with_name('EXACT_CHECK_RESULTS.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
