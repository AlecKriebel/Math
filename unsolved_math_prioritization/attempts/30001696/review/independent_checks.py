#!/usr/bin/env python3
"""Independent exact diagnostics for the bounded-switch ball-product proof.

This finite calculation does not prove the topological theorem. It checks the
zero-sensitive combinatorics, rational spectral flow, and orbit estimates that
are especially susceptible to sign or normalization errors in that theorem.
Run: python independent_checks.py
"""
from itertools import product, combinations
from math import comb
from pathlib import Path
import hashlib
import json
import sympy as sp

counts = {}
def require(value, label):
    assert bool(value), label
    counts[label] = counts.get(label, 0) + 1

def sign(x):
    return int(bool(x > 0)) - int(bool(x < 0))

def changes(v):
    v = [sign(x) for x in v if x != 0]
    return sum(a != b for a, b in zip(v, v[1:]))

def completions(v):
    zeros = [j for j,x in enumerate(v) if x == 0]
    for fills in product((-1,1), repeat=len(zeros)):
        out = list(v)
        for j,x in zip(zeros,fills): out[j] = x
        yield out

def upper_changes(v):
    return max(changes(w) for w in completions(v))

rows=[]
for d in range(2,7):
    N=d-1
    L=sp.zeros(d)
    for j in range(d):
        if j+1<d: L[j,j+1]=N-j
        if j>0: L[j,j-1]=j
    W=sp.diag(*[comb(N,j) for j in range(d)])
    require(W*L == L.T*W, 'weighted_self_adjoint')
    lambdas=[N-2*k for k in range(d)]
    require(sp.expand(L.charpoly().as_expr() - sp.prod(L.charpoly().gen-x for x in lambdas)) == 0, 'characteristic_polynomial')
    projectors=[]
    for k,lam in enumerate(lambdas):
        P=sp.eye(d)
        for h,other in enumerate(lambdas):
            if h != k: P=P*(L-other*sp.eye(d))/(lam-other)
        projectors.append(P)
        require(P*P==P and L*P==lam*P and P.rank()==1, 'spectral_projector')
        # Recover its polynomial degree independently by interpolation of a column.
        column=next(P[:,j] for j in range(d) if P[:,j] != sp.zeros(d,1))
        t=sp.Symbol('t')
        p=sp.interpolate([(j,column[j]) for j in range(d)],t)
        require(sp.degree(p,t)==k, 'eigenvector_polynomial_degree')
    require(sum(projectors,sp.zeros(d))==sp.eye(d), 'projector_resolution')
    for a in (sp.Rational(1,2),sp.Rational(1,3)):
        M=sum((a**k*P for k,P in enumerate(projectors)),sp.zeros(d))
        Minv=sum((a**(-k)*P for k,P in enumerate(projectors)),sp.zeros(d))
        require(M*Minv==sp.eye(d), 'flow_inverse')
        # All minors of D M D^{-1} have the same signs as those of M.
        for k in range(1,d+1):
            subsets=list(combinations(range(d),k))
            for I in subsets:
                for J in subsets:
                    require(M.extract(I,J).det()>0, 'strict_positive_minor')
        for v in product((-1,0,1),repeat=d):
            if not any(v): continue
            v=sp.Matrix(v)
            require(upper_changes(M*v)<=changes(v),'strict_variation_with_zeros')
    for v in product((-1,0,1),repeat=d):
        if not any(v): continue
        values=[changes(w) for w in completions(v)]
        require(min(values)==changes(v),'minimum_completion_variation')
        for i in range(d):
            # Membership in a facet and all local neighboring facets respectively.
            require(any(k<=i for k in values)==(changes(v)<=i),'facet_union_membership')
            require(all(k<=i for k in values)==(upper_changes(v)<=i),'interior_sign_strata')
    # Force multiple zeros, leading/trailing zeros, and general low-degree vectors.
    for r in range(1,d):
        for roots in combinations(range(d),r-1):
            vals=[sp.prod(j-root for root in roots) for j in range(d)]
            require(upper_changes(vals)<=r-1,'polynomial_core_zero_cases')
        for coeffs in product((-1,0,1),repeat=r):
            if not any(coeffs): continue
            vals=[sum(c*j**k for k,c in enumerate(coeffs)) for j in range(d)]
            require(upper_changes(vals)<=r-1,'polynomial_core_samples')
        QF=sum(projectors[r:],sp.zeros(d))
        for coeffs in product((-1,0,1),repeat=d-r):
            if not any(coeffs): continue
            # Each projector is one-dimensional; pick one nonzero column.
            v=sp.zeros(d,1)
            for k,c in enumerate(coeffs,r):
                P=projectors[k]
                col=next(P[:,j] for j in range(d) if P[:,j]!=sp.zeros(d,1))
                v+=c*col
            require(QF*v==v and changes(v)>=r,'repelling_space_samples')
    rows.append({'dimension':d,'full_ternary_patterns':3**d-1})

# Ratio bounds do not depend on the algebraic eigenvectors. Work directly with
# squared orthonormal spectral coefficients, normalizing E and F sums to one.
for d in range(2,9):
    N=d-1
    for r in range(1,d):
        for pattern in range(3):
            weights=[sp.Rational((k+1)**pattern) for k in range(d)]
            e=sum(weights[:r]); f=sum(weights[r:])
            weights=[x/e if k<r else x/f for k,x in enumerate(weights)]
            for a in (sp.Rational(1,8),sp.Rational(1,2),sp.Integer(1),sp.Integer(2),sp.Integer(8)):
                E=sum(weights[k]*a**(2*k) for k in range(r))
                F=sum(weights[k]*a**(2*k) for k in range(r,d))
                ratio=F/E
                diff=sum(k*weights[k]*a**(2*k) for k in range(r,d))/F-sum(k*weights[k]*a**(2*k) for k in range(r))/E
                require(1<=diff<=N,'logarithmic_ratio_derivative')
                require(a**(2*N)<=ratio<=a**2 if a<=1 else a**2<=ratio<=a**(2*N),'uniform_ratio_bounds')
                eps=sp.Rational(1,4)
                require(not ratio<eps**(2*N) or a<eps,'core_cutoff_implication')
# Exact family h and its inverse, including either side of the section a=1.
eps=sp.Rational(1,8)
for beta in (sp.Rational(1,4),sp.Rational(3,4),sp.Integer(1),sp.Integer(3)):
    def h(a): return a if a<=eps else eps+(1-eps)*(a-eps)/(beta-eps)
    def hinv(b): return b if b<=eps else eps+(beta-eps)*(b-eps)/(1-eps)
    samples=[eps/2,eps]+[eps+(beta-eps)*sp.Rational(k,8) for k in range(1,9)]
    require(h(beta)==1 and hinv(1)==beta,'cutoff_endpoints')
    for a in samples:
        require(hinv(h(a))==a,'cutoff_inverse')
        require((h(a)<=eps)==(a<=eps),'cutoff_fixed_neighborhood')
    require(all(h(a)<h(b) for a,b in zip(samples,samples[1:])),'cutoff_strict_monotonicity')

receipt={'status':'PASS','sympy_version':sp.__version__,'arithmetic':'exact integer/rational; no floating-point decisions','diagnostic_scope':'Finite checks only; the review supplies the general mathematical audit.','dimensions':rows,'assertions':sum(counts.values()),'counts':counts,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
