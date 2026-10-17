#!/usr/bin/env python3
"""Exact local convention checks, not computations of arithmetic K2 values."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path


def mat(a,b,c,d): return (F(a),F(b),F(c),F(d))
def mul(x,y):
    a,b,c,d=x; e,f,g,h=y
    return mat(a*e+b*g,a*f+b*h,c*e+d*g,c*f+d*h)
def inv(x):
    a,b,c,d=x; t=a*d-b*c
    if not t: raise ValueError('singular matrix')
    return mat(d/t,-b/t,-c/t,a/t)
def conj(x,y): return mul(mul(x,y),inv(x))
def eq(x,y,msg):
    if x!=y: raise RuntimeError(msg+': '+str((x,y)))
def up(b): return mat(1,b,0,1)
def low(c): return mat(1,0,c,1)
def diag(a,d=1): return mat(a,0,0,d)
def normalize(g,source_scale,target_scale):
    return mul(mul(diag(source_scale),g),inv(diag(target_scale)))
def in_strict(g,N):
    a,b,c,d=g
    return all(x.denominator==1 for x in g) and a*d-b*c==1 and c%N==0 and (d-1)%N==0

counts={'class_permutations':0,'inverse_coset_equations':0,'semilinear_conjugations':0,'higher_depth_intertwinings':0,'principal_scalar_comparisons':0}
# In a cyclic class group, first-coordinate forward and inverse correspondences
# have opposite shifts. Z^-1 has the sum of two inverse shifts.
for h in range(2,10):
    for qclass,r in product(range(1,h),range(h)):
        forward=(r-qclass)%h; inverse=(r+qclass)%h
        central_inverse=(r+2*qclass)%h
        if (inverse+qclass)%h != central_inverse: raise RuntimeError('bad D U component')
        if (central_inverse-qclass)%h != inverse: raise RuntimeError('bad Z^-1 T component')
        if (inverse-2*qclass)%h != forward: raise RuntimeError('bad opposite component')
        counts['class_permutations']+=1

for q,A,ar,as_,at in product((2,3,5,7),(1,2,3,5),(F(1),F(2,3)),(F(1),F(4,5)),(F(1),F(7,11))):
    N=A*q
    beta=diag(q*ar/as_); g=inv(beta)
    beta_s=diag(q*as_/at)
    eq(normalize(beta,as_,ar),diag(q),'beta lattice normalization')
    eq(normalize(g,ar,as_),diag(F(1,q)),'inverse lattice normalization')
    for b,c,e in product((-1,0,2),(-1,1),(0,1)):
        gamma0=mul(mul(up(b),low(N*c)),up(e))
        gamma=normalize(gamma0,1/ar,1/ar)
        Dgamma=conj(beta,gamma)
        if not in_strict(normalize(Dgamma,as_,as_),A): raise RuntimeError('D not low level')
        a,bb,cc,d=gamma0
        seen=[]
        for t in range(q):
            s=int(((cc/N+d*t)*pow(int(a),-1,q))%q)
            seen.append(s)
            kt=low(A*as_*t); ks=low(A*as_*s)
            tau=mul(mul(inv(ks),Dgamma),kt)
            if not in_strict(normalize(tau,as_,as_),N): raise RuntimeError('tau not high level')
            eq(mul(gamma,mul(g,kt)),mul(mul(g,ks),tau),'inverse right coset')
            counts['inverse_coset_equations']+=1
            if A%q==0:
                # Conjugating a low-unipotent target factor by beta_s divides
                # its lower coordinate by eta_s, hence gives the lower-level factor.
                eq(conj(beta_s,kt),low(F(A,q)*at*t),'higher-depth coset parameter')
                counts['higher_depth_intertwinings']+=1
        if sorted(seen)!=list(range(q)): raise RuntimeError('coset map is not a permutation')
        # Semilinear input: gamma^- = Phi^- gamma (Phi^-)^-1.
        # Target factorwise identification A^- has diagonal entries iota^-1, phi_1^-.
        iota=F(3,2); phir=(q*ar/as_)/iota; phi1=F(5,3)
        Phi_minus=diag(phir,phi1); A_minus=diag(1/iota,phi1)
        gamma_minus=conj(Phi_minus,gamma)
        transported=mul(mul(inv(A_minus),gamma_minus),A_minus)
        eq(transported,Dgamma,'semilinear conjugation')
        counts['semilinear_conjugations']+=1
        # Global principal scalar does not alter the conjugation.
        alpha=diag(1,q)
        eq(mul(mul(inv(alpha),gamma0),alpha),conj(diag(q),gamma0),'principal alpha versus inverse beta')
        counts['principal_scalar_comparisons']+=1

result={
    'status':'PASS',
    'scope':'Exact local rational matrix and determinant-class bookkeeping only; no CM K2 values, global ideal principalization, ray-field degree, or arithmetic descent is computed.',
    'counts':counts,
    'free_module_identity':'Using F U=Q D, D U=T^vee D-Z^-1 F, g T^vee=(1+Q sigma^-1)g, and g Z^-1=sigma^-1 g gives (sigma g D-g F)U=sigma g D-g F by literal cancellation.',
}
print(json.dumps(result,indent=2))
Path(__file__).with_name('INVERSE_COMPONENT_CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
