from math import comb,gcd,lcm
from fractions import Fraction as F
from collections import Counter
import json

C=Counter()
def check(k,b):
    assert b,k
    C[k]+=1
def vp(n,p):
    r=0
    while n%p==0:n//=p;r+=1
    return r
def ilog(n,p):
    r=0
    while n>=p:n//=p;r+=1
    return r
def primes(n):return [p for p in range(2,n+1) if all(p%d for d in range(2,int(p**.5)+1))]
squarefree=[]
for n in range(81):
    row=[comb(n,k) for k in range(n+1)];L=lcm(*row);M=lcm(*range(1,n+2))
    check('classical_LCM_identity',L*(n+1)==M)
    es={p:ilog(n+1,p)-vp(n+1,p) for p in primes(n+1)}
    for p,e in es.items():
        check('maximum_prime_valuation_formula',e==max(vp(v,p) for v in row))
    if all(e<=1 for e in es.values()):squarefree.append(n)
    for R in range(2,8):
        K=1
        for p,e in es.items():K*=p**(e//R)
        check('divisibility_root_power',L%(K**R)==0)
        for p,e in es.items():
            check('large_prime_omission',e//R==0 or p**R<=n+1)
    # Exact one-pair necessary test on rational odds when the exponent vector is integral.
    for a in range(n):
        for b in range(a+1,n+1):
            r=b-a;delta={p:vp(row[a],p)-vp(row[b],p) for p in es}
            if not any(delta.values()) or any(v%r for v in delta.values()):continue
            q=F(1)
            for p,v in delta.items():q*=F(p)**(v//r)
            check('rational_odds_power_divisibility',L%(q.numerator**r)==0 and L%(q.denominator**r)==0)
check('squarefree_row_classification_control',squarefree==[0,1,2,3,5,7,11,23])
for n in (127,255,511,1023,2047):
    m=n+1;es={p:ilog(m,p)-vp(m,p) for p in primes(m)}
    check('Mersenne_binary_prime_absent',es[2]==0)
    check('Mersenne_seventh_divisibility_root_one',all(e<7 for e in es.values()))
check('insufficient_filter_countercontrol',lcm(*(comb(8,k) for k in range(9)))==280)
out={'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(sorted(C.items())),
     'scope':'Exact classical-LCM and necessary-divisibility controls; no extension of the all-p collision scan beyond n80. Larger Mersenne rows are checked only for the proved rational-odds filter.'}
print(json.dumps(out,indent=2,sort_keys=True))
