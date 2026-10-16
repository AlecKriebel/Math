#!/usr/bin/env python3
"""Exact controls for spectral-projection identities and explicit eigenfunctions.
Requires SymPy. These checks do not replace the infinite-dimensional proof.
"""
import sympy as s
from fractions import Fraction as Q
from collections import Counter
from itertools import product
from pathlib import Path
import hashlib,json,math
counts=Counter()
def ck(k,v):
    if not bool(v):
        raise AssertionError(k)
    counts[k]+=1
def zero(M):return all(s.simplify(z)==0 for z in M)
S=s.Matrix([[1,1,0,2,0],[0,1,1,0,1],[0,0,1,1,0],[0,0,0,1,1],[0,0,0,0,1]])
D=s.diag(s.I,-1,s.Rational(1,2),s.Rational(1,2),0)
D[2,3]=s.Rational(1,4)
A=S*D*S.inv()
P=S*s.diag(1,1,0,0,0)*S.inv()
ck('projection_idempotent',zero(P*P-P))
ck('projection_commutes',zero(A*P-P*A))
ck('adapted_projection_norm',max(sum(abs(z) for z in row) for row in (S.inv()*P*S).tolist())==1)
ck('adapted_contraction_norm',max(sum(abs(z) for z in row) for row in D.tolist())==1)
for n in range(1,25):
    N=s.Matrix([[s.Rational(1,2),s.Rational(1,4)],[0,s.Rational(1,2)]])
    expected=s.Rational(1,2)**n*s.Matrix([[1,s.Rational(n,2)],[0,1]])
    ck('stable_Jordan_power_formula',zero(N**n-expected))
    ck('stable_Jordan_row_bound',sum(abs(z) for z in (N**n).tolist()[0])==s.Rational(1,2)**n*(1+s.Rational(n,2)))
    if n%4==0:
        R=S.inv()*(A**n-P)*S
        ck('peripheral_power_subsequence',zero(R-s.diag(s.zeros(2),N**n,s.zeros(1))))
# Nonnormal nilpotent/peripheral mixture, with nilpotent index three.
D0=s.zeros(5);D0[0,0]=s.I;D0[1,2]=1;D0[2,3]=1
A0=S*D0*S.inv()
P0=S*s.diag(1,0,0,0,0)*S.inv()
ck('nilpotent_projection_commutes',zero(A0*P0-P0*A0))
ck('nilpotent_remainder',zero(A0**3*(s.eye(5)-P0)))
ck('finite_spectral_polynomial',zero(A0**7-A0**3))
# Exact complex phase eigenfunction controls on radial orbit samples.
mus=[s.Rational(1,2),-s.Rational(1,2),s.I/2,-s.I/3,(1+s.I)/3]
for mu in mus:
    ck('strict_interior_multiplier',s.simplify(mu*s.conjugate(mu))<1 and mu!=0)
    for j in range(16):
        ck('radial_orbit_eigenidentity',s.simplify(mu**(j+1)-mu*mu**j)==0)
# Kernel functions f0(t)=(t-r)_+ on [0,1].
for r in [Q(1,4),Q(1,3),Q(1,2),Q(2,3),Q(3,4)]:
    for j in range(41):
        t=Q(j,40)
        ck('zero_eigenfunction',max(Q(0),r*t-r)==0)
    ck('zero_eigenfunction_nonzero',max(Q(0),1-r)>0)
# The general positive-radius complex-power identity is symbolic.
r,t=s.symbols('r t',positive=True)
z=s.symbols('z')
lhs=s.exp(z*s.expand_log(s.log(r*t)))
rhs=s.exp(z*s.log(r))*s.exp(z*s.log(t))
ck('complex_power_scaling_identity',s.simplify(lhs-rhs)==0)
# Finite peripheral groups, represented exactly by angles mod 1.
for denominators in [(1,),(2,),(4,),(3,4),(4,6),(5,7),(2,3,5)]:
    generators=[Q(1,d) for d in denominators]
    q=math.lcm(*denominators)
    group={Q(0)};pending=[Q(0)]
    while pending:
        x=pending.pop()
        for y in generators+[-a for a in generators]:
            v=(x+y)%1
            if v not in group:group.add(v);pending.append(v)
    ck('finite_peripheral_group',group=={Q(j,q) for j in range(q)})
    for g in generators:ck('finite_peripheral_order',q*g==int(q*g))
# Monomials on a two-dimensional reversible ball: eigenvalues i^(p-q)*(-1)^(r-s).
u,v,ub,vb=s.symbols('u v ub vb')
for p,q,r0,s0 in product(range(3),repeat=4):
    f=u**p*ub**q*v**r0*vb**s0
    evolved=f.subs({u:s.I*u,ub:-s.I*ub,v:-v,vb:-vb},simultaneous=True)
    multiplier=s.I**(p-q)*s.Integer(-1)**(r0-s0)
    ck('monomial_eigenfunction',s.simplify(evolved-multiplier*f)==0)
# Cesaro annihilation for unequal fourth-root frequencies.
roots=[s.Integer(1),s.I,s.Integer(-1),-s.I]
for lam,gam in product(roots,repeat=2):
    avg=s.simplify(sum((gam/lam)**j for j in range(4))/4)
    ck('Cesaro_frequency_projection',avg==int(lam==gam))
p=Path(__file__)
receipt={'status':'PASS','exact_assertions':sum(counts.values()),'checks':dict(sorted(counts.items())),
'artifact_sha256':hashlib.sha256(p.with_name('CLASSIFICATION.md').read_bytes()).hexdigest(),
'checker_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'sympy_version':s.__version__,
'limitations':'Finite exact algebraic controls, not a finite-dimensional approximation to the full Koopman spectrum. Compactness, continuity, recurrence, Stone-Weierstrass density and spectral closure are justified in the written proof.'}
print(json.dumps(receipt,indent=2,sort_keys=True))
