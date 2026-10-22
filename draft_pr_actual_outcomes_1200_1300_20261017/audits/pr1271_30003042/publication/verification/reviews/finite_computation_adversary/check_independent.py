#!/usr/bin/env python3
"""Adversarial root-monomial coefficient check; standard library only.
No import/read of candidate code, results, or printed Schubert coefficients.
Uses type-A coefficient extraction after a direct symplectic zero locus.
"""
from collections import defaultdict
from itertools import combinations, permutations, product
from fractions import Fraction
from math import prod
import json

K=5
BASE=32
UNIT=tuple(BASE**i for i in range(K))
ONE={0:1}
X=[{u:1} for u in UNIT]
BOUNDS=(15,13,11,9,7)

def ensure(ok, msg):
    if not ok: raise ArithmeticError(msg)

def add(*terms):
    out=defaultdict(int)
    for p in terms:
        for m,c in p.items(): out[m]+=c
    return {m:c for m,c in out.items() if c}

def scale(p,c): return {m:a*c for m,a in p.items() if a*c}

def mul(p,q,bound=None):
    out=defaultdict(int)
    for m,a in p.items():
        for n,b in q.items():
            r=m+n
            if bound is not None and any((r//UNIT[i])%BASE>bound[i] for i in range(K)): continue
            out[r]+=a*b
    return {m:c for m,c in out.items() if c}

def power(p,n):
    r=ONE
    for _ in range(n):r=mul(r,p)
    return r

def compositions(n,k):
    if k==1:
        yield (n,)
    else:
        for a in range(n+1):
            for rest in compositions(n-a,k-1):yield (a,)+rest

def elem(k): return {sum(UNIT[i] for i in s):1 for s in combinations(range(K),k)}

def complete(k,squared=False):
    return {sum((2 if squared else 1)*a*u for a,u in zip(v,UNIT)):1 for v in compositions(k,K)}

def normalized_root_polynomial():
    # c(Q)=prod_i(1-x_i^2)^(-1), Q symplectic rank six.
    u=elem(1); h1,h2,h3,h4=[complete(j,True) for j in range(1,5)]
    A=add(power(u,8),scale(mul(h1,power(u,6)),4),
          mul(add(scale(power(h1,2),6),scale(h2,-8)),power(u,4)),
          mul(add(scale(power(h1,3),4),scale(mul(h1,h2),-16),scale(h3,64)),power(u,2)),
          power(add(power(h1,2),scale(h2,-4)),2))
    n=add(A,scale(h4,-64))
    ensure(all(c%128==0 for c in n.values()),'free root polynomial normalization')
    b={m:c//128 for m,c in n.items()}
    e1,e2,e3,e4,e5=[elem(i) for i in range(1,6)]
    certificate=add(mul(add(mul(e1,e3),mul(power(e1,2),e2)),complete(4)),
                    mul(e3,complete(5)),mul(e2,complete(6)),mul(e1,complete(7)),complete(8))
    ensure(all(c%2==0 for c in add(b,scale(certificate,-1)).values()),'independent root-monomial mod2 certificate')
    # Frobenius is checked in the free ring, before any geometric relation.
    ordinary_h=[complete(j) for j in range(4,9)]
    for j,H in enumerate(ordinary_h,4):
        ensure(all(c%2==0 for c in add(power(H,2),scale(complete(j,True),-1)).values()),'Frobenius h identity')
    return b

def v2(n):
    ensure(n!=0,'nonzero valuation')
    return (abs(n)&-abs(n)).bit_length()-1

def coefficient_witness(b):
    # Rectangle/complement duality: coefficient s_(11,10,9,8,7) in b^3 e2^9 e3.
    # Multiplying by Vandermonde extracts that coefficient. No Pieri operation.
    p=ONE
    for _ in range(9):p=mul(p,elem(2),BOUNDS)
    p=mul(p,elem(3),BOUNDS)
    sizes=[len(p)]
    for _ in range(3):
        p=mul(p,b,BOUNDS); sizes.append(len(p))
    value=0; contributions=[]
    for perm in permutations(range(K)):
        exponents=tuple(BOUNDS[i]-(K-1-perm[i]) for i in range(K))
        if any(t<0 for t in exponents):continue
        c=p.get(sum(t*u for t,u in zip(exponents,UNIT)),0)
        inversions=sum(perm[i]>perm[j] for i in range(K) for j in range(i+1,K))
        signed=c*(-1)**inversions
        contributions.append(signed);value+=signed
    return value,sizes,contributions

def evalues(x):
    return [sum(prod(s) for s in combinations(x,j)) for j in range(len(x)+1)]

def root_localize(weights,k,polynomial,mutation=None):
    n=len(weights); roots=[]
    # Positive C_n roots outside A_(k-1) x C_(n-k).
    for i in range(k):
        roots.append((i,i,1)) # 2 epsilon_i
        for j in range(i+1,k):roots.append((i,j,1))
        for j in range(k,n):roots.extend([(i,j,1),(i,j,-1)])
    total=Fraction(); points=0
    for indices in combinations(range(n),k):
        unused=[j for j in range(n) if j not in indices]
        for signs in product((1,-1),repeat=k):
            t=[weights[i]*s for i,s in zip(indices,signs)]+[weights[i] for i in unused]
            terms=[t[i]+s*t[j] for i,j,s in roots]
            if mutation=='omit_long':terms=[a for a,(i,j,s) in zip(terms,roots) if i!=j]
            if mutation=='reverse':terms=[-a for a in terms]
            total+=Fraction(polynomial(t[:k],t[k:]),prod(terms)); points+=1
    return total,points,len(roots)

def main():
    b=normalized_root_polynomial()
    witness,sizes,contributions=coefficient_witness(b)
    def original(xs,ys):
        orbit=prod(sum(xs)+sum(t*s for t,s in zip(ys,signs)) for signs in product((1,-1),repeat=3))
        es=evalues(xs)
        return orbit**3*es[2]**9*es[3]
    # New irregular weights, with signs and order unlike the candidate.
    fixed,points,dim=root_localize([103,-13,47,5,79,-31,17,61],5,original)
    ensure(fixed.denominator==1 and fixed==witness*128**3,'independent root and coefficient witnesses agree')
    controls={}
    for n in range(1,5):
        value,_,_=root_localize(list(range(1,n+1)),1,lambda x,y:x[0]**(2*n-1))
        ensure(value==1,'projective space orientation/control')
        controls['IG(1,%d)'%(2*n)]=str(value)
    for n,expected in [(2,2),(3,16)]:
        d=n*(n+1)//2
        value,_,_=root_localize(list(range(1,n+1)),n,lambda x,y:sum(x)**d)
        ensure(value==expected,'Lagrangian Plucker-degree control')
        controls['LG(%d,%d)'%(n,2*n)]=str(value)
    mutated,_,_=root_localize([1,2],2,lambda x,y:sum(x)**3,mutation='omit_long')
    ensure(mutated!=2,'omitted long roots detected')
    reversed_value,_,_=root_localize([1,2],2,lambda x,y:sum(x)**3,mutation='reverse')
    ensure(reversed_value==-2,'orientation reversal detected')
    # Standard P4 has dimension 42 and 1120 points; P5 dimension45 and1792.
    dims={str(k):k*(16-k)-k*(k-1)//2 for k in (4,5)}
    ensure(dims=={'4':42,'5':45},'parabolic off-by-one changes dimension')
    out={'method':'root-monomial coefficient extraction and independently generated C8 quotient roots',
         'independent_of_candidate_imports_and_expected_numeric_inputs':True,
         'b_root_monomial_count':len(b),'bounded_monomial_state_sizes':sizes,
         'vandermonde_contributions':contributions,
         'pairing_b_cubed':witness,'pairing_a_cubed':witness*128**3,
         'v2_pairing_a_cubed':v2(witness*128**3),'normalization_and_mod2_certificate':'passed in root-monomial polynomial ring',
         'irregular_signed_weight_localization':{'weights':[103,-13,47,5,79,-31,17,61],'value':str(fixed),'points':points,'tangent_root_count':dim},
         'small_geometry_controls':controls,
         'mutation_controls':{'omitted_long_roots_quadric_degree':str(mutated),'reversed_orientation_quadric_degree':str(reversed_value)},
         'standard_P4_and_P5_dimensions':dims}
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':main()
