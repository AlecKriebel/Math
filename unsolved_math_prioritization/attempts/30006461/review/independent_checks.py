"""Exact bounded controls, not arithmetic-profile computations.
Run with Python 3, standard library only.
"""
from fractions import Fraction as Q
from collections import Counter
from pathlib import Path
import hashlib,json
checks=Counter()
def ck(k,v):
    assert v,k
    checks[k]+=1
amps=[Q(i,8) for i in [-7,-4,-1,1,4,7]]
# Direct cyclic convolution by summing physical-space probabilities.
# Order-two and order-three characters have disjoint nonzero frequencies.
for N in range(6,49,6):
    for b in amps:
        mu=[(1+b*((-1)**j))/N for j in range(N)]
        for c in amps:
            nu=[(1+c*(Q(1) if j%3==0 else Q(-1,2)))/N for j in range(N)]
            ck('positive_mass_one',min(mu)>0 and min(nu)>0 and sum(mu)==sum(nu)==1)
            ck('nonuniform_inputs',len(set(mu))>1 and len(set(nu))>1)
            conv=[sum(mu[j]*nu[(k-j)%N] for j in range(N)) for k in range(N)]
            ck('direct_Haar_convolution',conv==[Q(1,N)]*N)
# Every q, including q=1 and odd/composite q, has the quadrature bound.
for q in range(1,81):
    for shift in [Q(i,17) for i in range(17)]:
        avg=sum(min(t,1-t) for t in [((Q(j,q)-shift)%1) for j in range(q)])/q
        ck('translated_Lipschitz_quadrature',abs(avg-Q(1,4))<=Q(1,2*q))
# A positive cosine kernel and two positive cosine densities model (10).
# Their convolution is 1+(a*b*c/4)cos(2*pi*x).
for a in amps:
    for b in amps:
        for c in amps:
            d=abs(a*b*c)/4
            ratio=(1+d)/(1-d)
            ck('ratio_certificate_exact_mode',ratio>=1+d>1)
            for e in [Q(0),Q(1,100)]:
                for ep in [Q(0),Q(1,100)]:
                    lower=abs(b)/2-e
                    lowerp=abs(c)/2-ep
                    cert=1+abs(a)*lower*lowerp
                    ck('ratio_certificate_with_error',lower>0 and lowerp>0 and ratio>=cert>1)
# Quantifier control: distinct nonzero coefficients alone are insufficient.
for r in range(1,31):
    for s in range(1,31):
        support={-r,r}&{-s,s}
        ck('common_mode_quantifier',bool(support)==(r==s))
p=Path(__file__).resolve().parent
source=p/'OBSTRUCTION.md'
sha=hashlib.sha256(source.read_bytes()).hexdigest()
assert sha=='1fcff39750423d8e4b31d84bb4816f76378fb70f0c855beb2f9fd5008d0a2332'
receipt={'status':'PASS','exact_assertions':sum(checks.values()),'checks':dict(sorted(checks.items())),
'artifact_sha256':sha,'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
'limitations':'Direct cyclic-group countermodels, rational Lipschitz quadrature and cosine-model certificates only; no actual arithmetic measures, gamma numerical evaluation or nonconstancy certificate.'}
(p/'independent_results.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
