#!/usr/bin/env python3
"""Exact finite algebra controls. Requires SymPy; no network or file writes.
These do not formally verify Jensen, contraction, asymptotics, or Rouché.
"""
import json
import sympy as s

z, w, r, theta = s.symbols('z w r theta')
a, b, C, q, H, J, Hp, Jp = s.symbols('a b C q H J Hp Jp')
u=s.Function('u')(z)
F=s.Function('F')(z)
checks=[]
def eq(label, expression):
    assert s.simplify(expression)==0, label
    checks.append(label)

W=(1+z)/(1-z)
eq('Cayley inverse', s.simplify((W-1)/(W+1))-z)
eq('Cayley derivative',s.diff(W,z)-(W+1)**2/2)
eq('reciprocal derivative',s.diff(1/u,z)-1+(s.diff(u,z)+u**2)/u**2)
eq('quotient derivative',s.diff(F/s.diff(F,z),z)-1+F*s.diff(F,z,2)/s.diff(F,z)**2)
eq('integrating factor equation',(Hp*(C+J)+H*Jp-q*H*(C+J)-1).subs({Hp:q*H,Jp:1/H}))
eq('exponential derivative chain',s.diff(s.exp(a*W+b),z)-(a/2)*(W+1)**2*s.exp(a*W+b))
eq('Q kernel primitive',s.diff(s.log(1-2*r*s.cos(theta)+r*r),theta)-2*r*s.sin(theta)/(1-2*r*s.cos(theta)+r*r))
for m in range(1,17):
    um=s.Rational(m,2)*z**m
    fm=s.Rational(2,m)/z**m
    R=s.diff(um,z)+um**2
    fact=s.Rational(m*m,4)*z**(m-1)*(2+z**(m+1))
    eq(f'pole_{m}: Riccati factorization',R-fact)
    eq(f'pole_{m}: derivative',s.diff(fm,z)+2*z**(-m-1))
    eq(f'pole_{m}: q residue and analytic part',(s.diff(fm,z)-1)/fm-(-m/z-s.Rational(m,2)*z**m))
    # The first nonzero coefficient determines the exact local order m-1.
    assert s.Poly(R,z).coeff_monomial(z**(m-1))==s.Rational(m*m,2)
    assert all(s.Poly(R,z).coeff_monomial(z**j)==0 for j in range(m-1))
    checks.append(f'pole_{m}: forced multiplicity {m-1}')
# Local integrating-factor cancellation: H=t^(-m), J=t^(m+1)/(m+1).
for m in range(1,17):
    Hm=z**(-m)
    Jm=z**(m+1)/s.Integer(m+1)
    eq(f'primitive_{m}: derivative',s.diff(Jm,z)-1/Hm)
    eq(f'primitive_{m}: cancellation gives simple zero',Hm*Jm-z/s.Integer(m+1))
    eq(f'primitive_{m}: linear differential equation',s.diff(Hm*(C+Jm),z)+m/z*Hm*(C+Jm)-1)
print(json.dumps({'status':'pass','exact_checks':len(checks),'checks':checks,
 'scope':'finite symbolic identities only; analytic arguments are in the proof notes'},indent=2,sort_keys=True))
