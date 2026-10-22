#!/usr/bin/env python3
"""Non-rigorous high-precision sanity checks; PROOFS.md carries the proof.
Optional dependency: mpmath 1.3.0. These calculations do not certify quadrature
error or continuous parameter ranges.
"""
import json
import mpmath as m
m.mp.dps=60
worst=m.mpf(0)
cases=0
for a in [m.mpf(1)/100,m.mpf(1)/7,m.mpf(1)/2,m.mpf(99)/100]:
    for j in [1,3,5,11,53]:
        B=m.fprod(1-a/r for r in range(1,j+1))
        sp=sum(m.binomial(a,k) for k in range(j+1))
        for fraction in [m.mpf(2)/3,m.mpf(3)/4,m.mpf(9)/10,m.mpf(999)/1000]:
            theta=m.pi*fraction
            x=m.exp(1j*theta)
            p=sum(m.binomial(a,k)*x**k for k in range(j+1))
            rem=m.quad(lambda t:(1-t)**j*(1+t*x)**(a-j-1),[0,m.mpf('.5'),m.mpf('.9'),1])
            err=abs(p-(1+x)**a-a*B*x**(j+1)*rem)
            assert err<m.mpf('1e-45')
            assert abs(p)<sp and abs(p)<2**a
            cases+=1
            worst=max(worst,err)
print(json.dumps({'status':'SANITY_PASS','rigorous_interval_certificate':False,
                  'mpmath_version':m.__version__,'decimal_precision':m.mp.dps,
                  'cases':cases,'maximum_observed_identity_residual':m.nstr(worst,20)},
                 indent=2,sort_keys=True))
