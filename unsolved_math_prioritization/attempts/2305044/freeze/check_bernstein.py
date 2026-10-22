#!/usr/bin/env python3
"""Reproduce the failed global Bernstein certificate attempt.
Optional dependency: SymPy 1.14. This is not a proof of failure of Brannan's
inequality: negative Bernstein coefficients only defeat this certificate.
"""
import json
from math import comb
import sympy as S

a,t,u,v=S.symbols('a t u v')
records=[]
for n in (3,5,7):
    c=[S.prod(a-j for j in range(k))/S.factorial(k) for k in range(n+1)]
    D=S.expand(sum(c)**2-sum(x*x for x in c)-2*sum(
        c[j]*c[k]*S.chebyshevt(k-j,t)
        for j in range(n+1) for k in range(j+1,n+1)))
    Q=S.cancel(D/(a*(1-t)))
    assert S.expand(a*(1-t)*Q-D)==0
    p=S.Poly(Q.subs({a:1-u,t:1-2*v}),u,v)
    du,dv=p.degree(u),p.degree(v)
    coeff={(i,j):sum(q*S.Rational(comb(i,k)*comb(j,l),comb(du,k)*comb(dv,l))
               for (k,l),q in p.terms() if k<=i and l<=j)
           for i in range(du+1) for j in range(dv+1)}
    lo=min(coeff.values())
    assert lo<0
    records.append({'degree':n,'bernstein_bidegree':[du,dv],
                    'minimum_coefficient':str(lo),
                    'minimum_locations':[list(k) for k,x in coeff.items() if x==lo],
                    'global_nonnegative_coefficient_certificate':False})
print(json.dumps({'sympy_version':S.__version__,'status':'CONTROL_PASS',
                  'interpretation':'Certificate route fails; no counterexample to the inequality is implied.',
                  'records':records},indent=2,sort_keys=True))
