#!/usr/bin/env python3
"""Exact consistency checks for the independently authored Turn 1 proofs."""
import json
from pathlib import Path
import sympy as sp

checks=[]
t=sp.Symbol('t')

# Companion characteristic-polynomial indexing.
for k in range(1,8):
    c=sp.symbols(f'c1:{k}')
    for sign in [-1,1]:
        M=sp.zeros(k)
        for i in range(k-1): M[i,i+1]=1
        M[k-1,0]=sign
        for j in range(1,k): M[k-1,j]=-sign*c[j-1]
        expected=t**k-sign+sign*sum(c[j-1]*t**j for j in range(1,k))
        assert sp.expand(M.charpoly(t).as_expr()-expected)==0
checks.append({'name':'companion_polynomial_indexing','orders':list(range(1,8)),'passed':True})

# Exact two-cycle monodromy formula, with palindromic coefficients.
for k in [3,5,7,9]:
    m=(k-1)//2
    a=list(sp.symbols(f'a1:{m+1}'))
    coeff=a+a[::-1]
    u,v=sp.symbols('u v', nonzero=True)
    E=sum(coeff[2*r-1]*t**r for r in range(1,m+1))
    O=sum(coeff[2*r]*t**r for r in range(m))
    H=t**(m+1)*O-E
    C=E**2-t*O**2
    def D(u,v):
        M=sp.zeros(k)
        for i in range(k-1): M[i,i+1]=1
        M[k-1,0]=-v/u
        for j in range(1,k): M[k-1,j]=coeff[j-1]/u
        return M
    expected=t**k-1-((u+v)*H+C)/(u*v)
    actual=(D(v,u)*D(u,v)).charpoly(t).as_expr()
    assert sp.cancel(actual-expected)==0
checks.append({'name':'two_cycle_monodromy_identity','orders':[3,5,7,9],'passed':True})

# Exact periodic identities and least global period for the five base maps.
base=[]
for name,k,p,formula in [
    ('identity',1,1,lambda z:z[0]),
    ('reciprocal',1,2,lambda z:1/z[0]),
    ('six_period',2,6,lambda z:z[1]/z[0]),
    ('five_period',2,5,lambda z:(1+z[1])/z[0]),
    ('eight_period',3,8,lambda z:(1+z[1]+z[2])/z[0]),
]:
    xs=sp.symbols(f'x0:{k}', positive=True)
    state=list(xs); identities=[]
    for n in range(1,p+1):
        state=state[1:]+[sp.cancel(formula(state))]
        same=all(sp.cancel(state[j]-xs[j])==0 for j in range(k))
        if same: identities.append(n)
    assert identities==[p],(name,identities)
    base.append({'name':name,'order':k,'least_global_period':p})
checks.append({'name':'base_map_periods','results':base,'passed':True})

# Check sparse-support exponent matching used in the odd-order proof.
for k in range(3,40,2):
    matches=[]
    for e in range(2,k,2):
        r=e//2
        if {e:1,k-e:-1}=={k-r:1,r:-1}:
            matches.append(e)
    expected=[2*k//3] if k%3==0 else []
    assert matches==expected,(k,matches,expected)
checks.append({'name':'odd_sparse_exponent_consistency','orders':list(range(3,40,2)),'passed':True})

result={'sympy_version':sp.__version__,'all_passed':True,'checks':checks,
        'scope':'Exact finite consistency tests, not a classification proof or numerical evidence of periodicity.'}
output=Path(__file__).with_name('turn01_verification.json')
output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
