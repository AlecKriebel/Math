#!/usr/bin/env python3
"""Exact finite diagnostics; not a proof of the open coding-radius problem."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import factorial
from pathlib import Path
import json
checks = {}
def check(label, condition):
    assert condition, label
    checks[label] = checks.get(label, 0) + 1
@lru_cache(None)
def building(w):
    if not w: return 1
    if any(a == b for a,b in zip(w,w[1:])): return 0
    return sum(building(w[:i]+w[i+1:]) for i in range(len(w)))
def prob(q,w):
    if q == 4: return F(building(w), 2**len(w)*factorial(len(w)+1))
    if q == 3: return F(2*building(w), factorial(len(w)+2))
    raise ValueError(q)
def determinant(a):
    a = [[F(v) for v in row] for row in a]
    result = F(1)
    for i in range(len(a)):
        j=next(j for j in range(i,len(a)) if a[j][i])
        if i!=j: a[i],a[j]=a[j],a[i];result=-result
        pivot=a[i][i];result*=pivot
        for j in range(i+1,len(a)):
            t=a[j][i]/pivot
            for k in range(i+1,len(a)):a[j][k]-=t*a[i][k]
            a[j][i]=F(0)
    return result
ranks=[]
for q,k in [(4,1),(3,2)]:
    for n in range(6):
        words=list(product(range(q),repeat=n))
        check('cylinder_normalization',sum(prob(q,w) for w in words)==1)
        for w in words:
            check('left_consistency',sum(prob(q,(a,)+w) for a in range(q))==prob(q,w))
            check('right_consistency',sum(prob(q,w+(a,)) for a in range(q))==prob(q,w))
            check('nonnegative',prob(q,w)>=0)
    for a in range(1,3):
        for b in range(1,3):
            for u in product(range(q),repeat=a):
                for v in product(range(q),repeat=b):
                    lhs=sum(prob(q,u+z+v) for z in product(range(q),repeat=k))
                    check('separated_blocks',lhs==prob(q,u)*prob(q,v))
    for n in range(1,25):
        w=tuple(i%2 for i in range(n))
        expected=F(1,2*factorial(n+1)) if q==4 else F(2**n,factorial(n+2))
        check('alternating_word_law',prob(q,w)==expected)
        ratio=prob(q,w+(n%2,))/prob(q,w)
        check('alternating_continuation',ratio==(F(1,n+2) if q==4 else F(2,n+3)))
    for n in range(1,9):
        # Explicit Hankel minor: u_i=(01)^i, v_j alternating length j, starting 0.
        a=[[prob(q,(0,1)*i+tuple(t%2 for t in range(j))) for j in range(n)] for i in range(1,n+1)]
        d=determinant(a);sgn=(-1)**(n*(n-1)//2)
        vf=1
        for r in range(1,n):vf*=factorial(r)
        den=1
        for i in range(1,n+1):den*=factorial(2*i+n+(q==3))
        expected=F(sgn*2**(n*(n-1)//2)*vf,2**n*den) if q==4 else F(sgn*2**(2*n*n)*vf,den)
        check('hankel_minor_formula',d==expected and d!=0)
        ranks.append({'colors':q,'size':n,'determinant':str(d)})
# Heavy-delay construction: selected bit coordinates are injective for every selector vector.
for ns in product(range(5),repeat=5):
    coords=[(i+n,n) for i,n in enumerate(ns)]
    check('heavy_delay_injective',len(set(coords))==5)
for r in range(1,100):
    # pmf telescopes; exact residual tail after N, rather than finite approximation.
    p=sum(F(1,(n+1)*(n+2)) for n in range(r+1))
    check('heavy_delay_tail',1-p==F(1,r+2))
# Conditional-dependence trap for X_i=U_i xor U_{i+1}, P(U_i=1)=1/3.
# E_n: X_1=...=X_{2m-1}=1. Compare the two observable boundary values X_{2m}=b.
p=F(1,3)
conditional=[]
for m in range(1,6):
    n=2*m
    weights=[F(0),F(0)];ones=[F(0),F(0)]
    for bits in product((0,1),repeat=n+2):
        if any(bits[i]==bits[i+1] for i in range(1,n)):continue
        weight=p**sum(bits)*(1-p)**(len(bits)-sum(bits))
        b=bits[n]^bits[n+1];weights[b]+=weight
        if bits[0]!=bits[1]:ones[b]+=weight
    values=[ones[b]/weights[b] for b in (0,1)]
    check('conditional_bridge',values==[1-2*p+2*p*p,2*p*(1-p)])
    conditional.append({'m':m,'conditional_probabilities':list(map(str,values))})
# Synchronizing word for a primitive matrix with no constant one-step supported map.
P=[[F(1,2),F(1,2),F(0)],[F(0),F(1,2),F(1,2)],[F(1,2),F(0),F(1,2)]]
f1=(0,1,0);f2=(1,1,2)
check('sync_no_single_step',all(not all(P[x][s]>0 for x in range(3)) for s in range(3)))
check('sync_word',len({f2[f1[x]] for x in range(3)})==1)
delta=F(1)
for f in (f1,f2):
    for x in range(3):
        check('sync_supported',P[x][f[x]]>0)
        delta*=P[x][f[x]]
check('sync_probability',delta==F(1,64))
# Direct check of the finite dependence of this example is NOT asserted.
result={'status':'PASS_FINITE_DIAGNOSTICS','assertions':sum(checks.values()),'checks':checks,'hankel_minors':ranks,'conditional_bridge':conditional,'sync_word_probability':str(delta),'limitations':['Finite cylinder checks do not establish an infinite-process theorem.','Hankel minors obstruct finite-state, not countable-state, hidden Markov representations.','The synchronizing example is a primitive Markov chain, not asserted finitely dependent.','No coding-radius lower bound for either critical coloring is proved.']}
text=json.dumps(result,indent=2,sort_keys=True)+'\n'
if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
    path=Path(__file__).with_name('results.json')
    if args.write:path.write_text(text)
    else:assert path.read_text()==text,'recorded results differ'
    print(json.dumps({'status':result['status'],'assertions':result['assertions'],'recorded_results_match':True}))
