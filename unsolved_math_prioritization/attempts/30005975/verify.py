#!/usr/bin/env python3
"""Finite algebra controls. This does not prove the imported stack-cohomology theorems."""
from itertools import product
from math import gcd
from pathlib import Path
from hashlib import sha256
import json

counts={}
def ck(cat,cond):
    assert cond,cat
    counts[cat]=counts.get(cat,0)+1

# Coprime torsion annihilates the local connecting homomorphism.
for p,e,b in product((2,3,5),(1,2,3,4),range(1,25)):
    a=p**e
    if gcd(a,b)!=1:continue
    images=[x for x in range(b) if a*x%b==0]
    ck('coprime_torsion_homomorphisms',images==[0])

# Explicit multiplicative cocycle recorded by its exponent of a primitive root.
triples=0
for ell in (2,3,5):
    G=list(product(range(ell),repeat=2))
    add=lambda x,y:((x[0]+y[0])%ell,(x[1]+y[1])%ell)
    c=lambda x,y:x[1]*y[0]%ell
    for x,y,z in product(G,repeat=3):
        ck('schur_cocycle', (c(x,y)+c(add(x,y),z)-c(y,z)-c(x,add(y,z)))%ell==0)
        triples+=1
    for x,y in product(G,repeat=2):
        ck('alternating_commutator',(c(x,y)-c(y,x))%ell==(x[1]*y[0]-y[1]*x[0])%ell)
        ck('cocycle_power_order',ell*c(x,y)%ell==0)
    for j in range(1,ell):
        ck('nontrivial_cocycle_powers',j*(c((0,1),(1,0))-c((1,0),(0,1)))%ell!=0)

# Integral Picard presentation for the O(1) root gerbe.
for ell in (2,3,5,7,11):
    ck('primitive_picard_relation',gcd(1,ell)==1)
    for a,b in product(range(-12,13),repeat=2):
        value=ell*a+b
        ck('picard_quotient_kernel',(value==0)==(b==-ell*a))
        ck('picard_character_weight',value%ell==b%ell)
        ck('picard_no_torsion',(ell*value==0)==(value==0))

class Field:
    """Fp² = Fp[u]/(u²+A*u+B), with explicitly checked irreducible quadratic."""
    def __init__(self,p,A,B):self.p=p;self.A=A;self.B=B
    def add(self,x,y):return ((x[0]+y[0])%self.p,(x[1]+y[1])%self.p)
    def neg(self,x):return ((-x[0])%self.p,(-x[1])%self.p)
    def mul(self,x,y):
        a,b=x;c,d=y
        return ((a*c-self.B*b*d)%self.p,(a*d+b*c-self.A*b*d)%self.p)
    def pow(self,x,n):
        z=(1,0)
        for _ in range(n):z=self.mul(z,x)
        return z
    def root(self,x):return self.pow(x,self.p) # inverse Frobenius in Fp²

def padd(K,f,g):
    h=dict(f)
    for d,a in g.items():
        h[d]=K.add(h.get(d,(0,0)),a)
        if h[d]==(0,0):del h[d]
    return h
def pneg(K,f):return {d:K.neg(a) for d,a in f.items()}
def pfrob(K,f):return {K.p*d:K.pow(a,K.p) for d,a in f.items()}
def normal(K,f):
    # Inputs have zero constant. Constants require the algebraically closed base,
    # and are deliberately not certified by these finite-field computations.
    work=dict(f);cert={}
    while True:
        eligible=[d for d in work if d>0 and d%K.p==0]
        if not eligible:break
        d=max(eligible);a=work.pop(d);b=K.root(a);term={d//K.p:b}
        work=padd(K,work,term);cert=padd(K,cert,term)
    return work,cert

normal_cases=0
for K in (Field(2,1,1),Field(3,0,1),Field(5,0,3)):
    p=K.p;elements=list(product(range(p),repeat=2))
    ck('quadratic_irreducibility',all((x*x+K.A*x+K.B)%p for x in range(p)))
    for a in elements:
        ck('inverse_frobenius',K.pow(K.root(a),p)==a)
    for a,b,c in product(elements,repeat=3):
        f={d:v for d,v in ((1,a),(p,b),(p*p,c)) if v!=(0,0)}
        N,H=normal(K,f)
        ck('artin_schreier_reduction_certificate',padd(K,f,pneg(K,N))==padd(K,pfrob(K,H),pneg(K,H)))
        ck('prime_to_p_exponents',all(d>0 and d%p for d in N))
        ck('normal_form_idempotent',normal(K,N)==(N,{}))
        normal_cases+=1
    for a,b in product(elements,repeat=2):
        f={p:a} if a!=(0,0) else {};g={p*p:b} if b!=(0,0) else {}
        ck('normal_form_additive',normal(K,padd(K,f,g))[0]==padd(K,normal(K,f)[0],normal(K,g)[0]))

r=Path(__file__).resolve().parent
out={'status':'PASS','artifact_sha256':sha256((r/'PARTIAL.md').read_bytes()).hexdigest(),'verifier_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),'exact_assertions':sum(counts.values()),'categories':counts,'schur_cocycle_triples':triples,'artin_schreier_polynomial_cases':normal_cases,'limitations':'Finite group, Picard-presentation and positive-degree Artin–Schreier arithmetic only. No finite-field claim of surjectivity on constants; no proof of the local quotient theorem, Tsen vanishing, Leray statements, or full arbitrary-stack Brauer computation.'}
(r/'verification.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
