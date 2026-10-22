#!/usr/bin/env python3
"""Exact supplementary controls. These finite checks are not the analytic proofs."""
from fractions import Fraction as F
import json

checks = 0
negative_controls = []

def check(condition):
    global checks
    if not condition:
        raise RuntimeError('Exact control failed')
    checks += 1

def reject(name, false_statement):
    check(not false_statement)
    negative_controls.append(name)

def h(t):
    return (t*t-1)/(t*t+1)

def W(n, j, r):
    return r**n*(1+r*r*h(j*r))

def A(n,j,r):
    return 1+F(n+2,n)*r*r*h(j*r)+F(4,n)*j*j*r**4/(1+j*j*r*r)**2

# Exact rational instances of the independently proved identities.
for n in range(2,13):
    for j in range(2,20):
        r=F(1,2*j)
        check(W(n,j,r)<r**n)
        check(W(n,j,r)>0)
        check(A(n,j,r)>=F(1,2))
        for r in (F(1,2), F(1,3), F(1,2*j),F(1,j)):
            y=j*j*r*r
            diff=(F(-2*(n+2),n)*y/(1+y)+F(4,n)*y*y/(1+y)**2)/(j*j)
            check(A(n,j,r)-(1+F(n+2,n)*r*r)==diff)
            check(r**n*(1+r*r)-W(n,j,r)==2*r**(n+2)/(1+j*j*r*r))
            check(0<=r**n*(1+r*r)-W(n,j,r)<=2*r**n/(j*j))
            # Derivative using the product/quotient rules, kept separate from A.
            derivative=n*r**(n-1)+(n+2)*r**(n+1)*h(j*r)+r**(n+2)*4*j*j*r/(1+j*j*r*r)**2
            check(derivative==n*r**(n-1)*A(n,j,r))
            check(derivative>0)
        if j>=4:
            check(W(n,j,F(2,j))>F(2,j)**n)
        # Central scalar values via the radial Taylor coefficient.
        bminus=F(-(n+2),n*(n-1))
        bplus=-bminus
        check(-6*n*(n-1)*bminus==6*(n+2))
        check(-6*n*(n-1)*bplus==-6*(n+2))
    # Conformal coefficient: coordinate density minus radius reparametrization.
    coefficient=F(n*n,n+2)-F(n,3)
    check(coefficient==F(2*n*(n-1),3*(n+2)))
    check(-6*(n+2)*coefficient==-4*n*(n-1))

# Seam integrals after factoring a_+ - a_-.
check(F(2,3)-F(1,2)*F(2,3)==F(1,3))
# Normalized two-sphere scalar curvature is 2/R^2.
for lam in range(1,21):
    r2=F(2,lam)
    check(2/r2==lam)
    reject('omit factor 2 in model radius '+str(lam),2/F(1,lam)==lam)

reject('retain central comparison outside its witness',W(3,10,F(1,5))<F(1,5)**3)
reject('claim central positive curvature is preserved',-6*(3+2)>=0)
reject('replace second-order little-o by big-O',-4*3*(3-1)==0)
reject('reverse upward-seam sign',F(1,3)<=0)
reject('infer e=o(R^2) from e tending to zero',F(1,100)/(F(1,100)**2)<1)

result={
  'outcome':'PASS',
  'exact_assertions':checks,
  'negative_controls_rejected':len(negative_controls),
  'negative_controls':negative_controls,
  'limitations':'Finite rational controls supplement, and do not replace, the universal written arguments. No general conjecture verification is claimed.'
}
print(json.dumps(result,indent=2,sort_keys=True))
