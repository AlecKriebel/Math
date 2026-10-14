"""Independent orbit-marginal checks for a finite-support restricted obstruction."""
from math import gcd, prod
from itertools import product
import json

def determinants(a):
    # Fraction-free elimination, with explicit pivot checks rather than assertions.
    a=[list(r) for r in a];n=len(a);den=1;sgn=1
    for k in range(n-1):
        if not a[k][k]:
            row=next((i for i in range(k+1,n) if a[i][k]),None)
            if row is None:return 0
            a[k],a[row]=a[row],a[k];sgn=-sgn
        p=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                v=a[i][j]*p-a[i][k]*a[k][j]
                if v%den:raise RuntimeError('nonintegral Bareiss division')
                a[i][j]=v//den
            a[i][k]=0
        den=p
    return sgn*a[-1][-1]

cases=[]
for m in [2,3,4,5,7,8,9,12,16,18,25,27,30,49]:
    ds=[d for d in range(1,m+1) if m%d==0]
    M=[]
    for a in ds:
        x=a%m
        M.append([sum(gcd(gcd(x,y),m)==d for y in range(m)) for d in ds])
    det=determinants(M);expected=prod(m//d for d in ds)
    if det!=expected:raise RuntimeError(('determinant',m,M,det,expected))
    cases.append({'modulus':m,'content_divisors':ds,'matrix':M,'determinant':det,'expected_determinant':expected,'passed':True})
# The same local-ring formula applies to non-cyclic additive residue rings.
local=[]
for Q in [2,3,4,5,8,9,25]:
    for e in range(1,5):
        M=[[0 if a<r else Q**(e-r) if a==r else Q**(e-r)-Q**(e-r-1) for r in range(e+1)] for a in range(e+1)]
        det=determinants(M)
        if det!=Q**(e*(e+1)//2):raise RuntimeError(('local determinant',Q,e))
        local.append({'residue_size':Q,'length':e,'determinant':det,'passed':True})
print(json.dumps({'integer_quotient_enumeration':cases,'local_formula_checks':local,'all_passed':True},indent=2))
