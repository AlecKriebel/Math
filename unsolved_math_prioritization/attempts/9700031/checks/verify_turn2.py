"""Exact scalar controls for the geometric criterion; not a proof of SIRSN geometry."""
from fractions import Fraction as F
import json
count=0
for alpha_n in range(1,21):
    alpha=F(alpha_n,20)
    for beta_n in range(41,81):
        beta=F(beta_n,20)
        exponent=1-beta+2*alpha
        assert (exponent>-1)==(beta<2+2*alpha);count+=1
        # The dyadic shell mass is proportional to 2^{-j(2-beta+2alpha)}.
        assert (2-beta+2*alpha>0)==(exponent+1>0);count+=1
for s_n in range(1,61):
    s=F(s_n,3)
    if s<1:continue
    a=1/(s+1)
    assert 2-2*a==1+a*(s-1)==2*s/(s+1);count+=1
    assert 2+2*s/(s+1)==4-2/(s+1);count+=1
# Logarithmic endpoint after u=log(e/t): integral u^{-2a}du.
for a_n in range(-20,41):
    a=F(a_n,20)
    assert (2*a>1)==(a>F(1,2));count+=1
# Endpoint admissibility: t/log(e/t)^a < t for t<1 when a>0.
for u in range(2,102):
    for a in (1,2,3):
        assert F(1,u**a)<1;count+=1
print(json.dumps({'status':'PASS_EXACT_SCALAR_CONTROLS','exact_assertions':count,'scope':'Power/logarithmic integrability, moment-exponent preservation and endpoint caveat; no geometric or universal SIRSN certification.'},indent=2))
