#!/usr/bin/env python3
"""Independent exact finite controls; infinite coupling quantifiers need proof."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,hashlib
checks={}
def ck(name,truth):
    assert truth,name
    checks[name]='PASS'
def flip_law(n):
    law={}
    for x0 in (-1,1):
        for flips in product((-1,1),repeat=n):
            w=F(1,2);path=[x0]
            for k,xi in enumerate(flips):
                w*= F(1,k+2) if xi==-1 else F(k+1,k+2)
                path.append(path[-1]*xi)
            law[tuple(path)]=w
    return law
laws={n:flip_law(n) for n in range(1,10)}
# Conditional expectation is checked for every positive-probability history,
# rather than merely multiplying a two-state matrix.
for n,law in laws.items():
    ck(f'mass_{n}',sum(law.values())==1)
    ck(f'fair_last_{n}',sum(w*x[-1] for x,w in law.items())==0)
    for m in range(n):
        masses={};moments={}
        for x,w in law.items():
            prefix=x[:m+1]
            masses[prefix]=masses.get(prefix,F(0))+w
            moments[prefix]=moments.get(prefix,F(0))+w*x[-1]
        rho=F(m*(m+1),n*(n+1))
        for j,prefix in enumerate(sorted(masses)):
            ck(f'conditional_{n}_{m}_{j}',moments[prefix]/masses[prefix]==prefix[-1]*rho)
        ck(f'max_finite_history_correlation_{n}_{m}',sum(abs(v) for v in moments.values())==rho)
# Anticipative fair signs B=X0 times an arbitrary Walsh monomial of early
# flips. Every subset at horizon H=4 is checked beyond that horizon.
H=4
for n in range(H,10):
    law=laws[n]
    for mask in range(2**H):
        def B(x):
            b=x[0]
            for k in range(H):
                if mask>>k&1:b*=x[k]*x[k+1]
            return b
        meanB=sum(w*B(x) for x,w in law.items())
        corr=sum(w*x[n]*B(x) for x,w in law.items())
        basecorr=sum(w*x[H]*B(x) for x,w in law.items())
        ck(f'anticipative_B_fair_{n}_{mask}',meanB==0)
        ck(f'anticipative_tower_{n}_{mask}',corr==F(H*(H+1),n*(n+1))*basecorr)
        ck(f'anticipative_mismatch_{n}_{mask}',sum(w for x,w in law.items() if x[n]!=B(x))==(1-corr)/2)
# Exact shifted-window laws by marginalization of a common full path.
for n in range(0,6):
    for r in range(0,5):
        N=max(1,n+r);law=laws[N];win={}
        for x,w in law.items():win[x[n:n+r+1]]=win.get(x[n:n+r+1],F(0))+w
        const=[(-1,)*(r+1),(1,)*(r+1)]
        tv=sum(abs(w-(F(1,2) if word in const else 0)) for word,w in win.items())/2
        ck(f'window_TV_{n}_{r}',tv==F(r,n+r+1))
        ck(f'no_flip_window_{n}_{r}',sum(win[w] for w in const)==F(n+1,n+r+1))
# Finite metric inequality for every window and arbitrary constant sign B.
J=5;weights=[F(1,2**(j+1)) for j in range(J+1)]
for idx,x in enumerate(product((-1,1),repeat=J+1)):
    rhs=sum(weights[j]*(x[j]!=x[0]) for j in range(J+1))
    for b in (-1,1):
        D=sum(weights[j]*(x[j]!=b) for j in range(J+1));I=int(x[0]!=b)
        ck(f'metric_pointwise_{idx}_{b}',abs(D-I*sum(weights))<=rhs)
# Exact mismatch at any bounded offset, including the initial zero factor.
for n in range(0,40):
    for shift in range(0,9):
        if shift==0:p=F(0)
        else:p=(1-F(n*(n+1),(n+shift)*(n+shift+1)))/2
        ck(f'offset_bound_{n}_{shift}',p<=F(shift,n+shift+1)<=F(shift,n+1))
for M in range(0,40):
    ck(f'offset_union_sum_{M}',sum(range(M+1))==M*(M+1)//2)
for n in range(1,80):
    p=(1-F(n*(n+1),2*n*(2*n+1)))/2
    ck(f'double_time_gap_{n}',p==F(3*n+1,4*(2*n+1)) and F(1,3)<=p<F(3,8))
result={'passed':len(checks),'failed':0,'arithmetic':'exact Fraction, no numerical simulation','reviewed_sha256':hashlib.sha256(Path(__file__).with_name('PARTIAL.md').read_bytes()).hexdigest(),'scope':'Finite-history, anticipative-sign and metric controls only; arbitrary infinite couplings and limits are audited in REVIEW.md.','checks':checks}
Path(__file__).with_name('independent_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'}))
