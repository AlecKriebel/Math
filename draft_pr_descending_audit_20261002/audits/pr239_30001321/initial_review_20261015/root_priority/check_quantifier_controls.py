"""Exact finite illustrations of the accompanying logical counterexample.
These random measures are not asserted to be quenched laws of iid RWRE.
"""
from fractions import Fraction as F
from math import comb,isqrt
import json
rows=[]
for n in [16,64,256,1024,4096]:
    m=isqrt(isqrt(n));r=F(1,n*n)
    alpha={2*j-n:F(comb(n,j),2**n) for j in range(n+1)}
    h=sum((p for x,p in alpha.items() if x>=0),F(0))
    nu={x:p/h if x>=0 else F(0) for x,p in alpha.items()}
    good_mu={x:(p-r*nu[x])/(1-r) for x,p in alpha.items()}
    assert all(p>=0 for p in good_mu.values()) and sum(good_mu.values())==1
    assert all(r*nu[x]+(1-r)*good_mu[x]==p for x,p in alpha.items())
    def coarse(mu):
        d={}
        for x,p in mu.items():d[x//m]=d.get(x//m,F(0))+p
        return d
    a,b,g=coarse(alpha),coarse(nu),coarse(good_mu)
    bad=sum(abs(b.get(k,F(0))-a.get(k,F(0))) for k in a.keys()|b.keys())
    good=sum(abs(g.get(k,F(0))-a.get(k,F(0))) for k in a.keys()|g.keys())
    assert bad==2*(1-h) and good==r*bad/(1-r)
    assert bad>F(1,2) and good<F(1,2)
    assert r*n**3==n
    assert m**4<=n<(m+1)**4
    rows.append({'N':n,'M':m,'bad_event_probability':str(r),'bad_coarse_L1':str(bad),
                 'good_coarse_L1':str(good),'N_cubed_times_failure_probability':n})
print(json.dumps({'status':'PASS','cases':rows,'scope':'Finite exact checks of an abstract quantifier counterexample; not an iid RWRE counterexample or priority verdict.'},indent=2,sort_keys=True))
