"""Finite exact-arithmetic checks; not asymptotic proofs."""
from fractions import Fraction as F
from math import comb
import itertools,json
from pathlib import Path

def C(n,k): return comb(n,k) if 0<=k<=n else 0

def plane(q):
    # Prime-order projective plane; normalize first nonzero coordinate.
    pts=[x for x in itertools.product(range(q),repeat=3) if any(x) and next(a for a in x if a)==1]
    lines=[tuple(i for i,x in enumerate(pts) if sum(a*b for a,b in zip(x,y))%q==0) for y in pts]
    assert len(pts)==q*q+q+1 and all(len(L)==q+1 for L in lines)
    assert all(sum(i in L and j in L for L in lines)==1 for i,j in itertools.combinations(range(len(pts)),2))
    return pts,lines

summary={"projective_planes":[],"tv_cases":0,"order_cases":0}
for q in (2,3):
    pts,lines=plane(q); v=len(pts); k=q+1
    sums={n:[0]*(q+2) for n in range(v+1)}
    square_sums={n:0 for n in range(v+1)}
    for mask in range(1<<v):
        n=mask.bit_count(); p=F(n,v)
        zs=[sum((mask>>i)&1 for i in L) for L in lines]
        mean=F(sum(zs),v)
        assert mean==k*p
        assert F(sum(z*z for z in zs),v)-mean**2==q*p*(1-p)
        hist=[zs.count(t) for t in range(k+1)]
        sums[n]=[a+b for a,b in zip(sums[n],hist)]
        square_sums[n]+=sum(a*a for a in hist)
    for n in range(v+1):
        probs=[F(C(k,t)*C(v-k,n-t),C(v,n)) for t in range(k+1)]
        diag=sum(F(sum(C(q,t-z)**2*C(v-2*q-1,n-2*t+z) for z in (0,1)),C(v,n)) for t in range(k+1))
        collision=sum(p*p for p in probs)
        trace=v*(1-collision)+v*(v-1)*(diag-collision)
        enumerated=F(square_sums[n],C(v,n))-sum(F(s,C(v,n))**2 for s in sums[n])
        assert trace==enumerated
        # Bernoulli shared-point covariance identity, exact rational p.
        p=F(n,v)
        a=[F(C(q,t))*p**t*(1-p)**(q-t) for t in range(q+1)]
        b=[F(C(k,t))*p**t*(1-p)**(k-t) for t in range(k+1)]
        get=lambda t:a[t] if 0<=t<=q else F(0)
        joint=sum((1-p)*get(t)**2+p*get(t-1)**2 for t in range(k+1))
        rhs=p*(1-p)*sum((get(t)-get(t-1))**2 for t in range(k+1))
        assert joint-sum(x*x for x in b)==rhs
    summary['projective_planes'].append({'q':q,'v':v,'subsets_checked':1<<v,'fixed_size_trace_cases':v+1})
for v in range(2,41):
    for n in range(1,v):
        p=F(n,v)
        for m in range(1,v//2+1):
            tv=sum(abs(F(C(n,t)*C(v-n,m-t),C(v,m))-C(m,t)*p**t*(1-p)**(m-t)) for t in range(m+1))/2
            assert tv<=F(m,v)
            summary['tv_cases']+=1
for n in range(10,100001):
    q=1
    while q*q<2*n:q*=2
    v=q*q+q+1
    assert 2*n<=q*q<8*n and F(1,10)<=F(n,v)<=F(1,2)
    assert 2*q+1<=F(v,2) and n>q+1
    summary['order_cases']+=1
summary['result']='PASS: all listed exact finite checks; no claim of proof by computation'
Path(__file__).with_name('CHECKS.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
