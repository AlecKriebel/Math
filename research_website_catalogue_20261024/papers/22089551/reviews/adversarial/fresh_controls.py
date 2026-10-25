#!/usr/bin/env python3
"""Independent finite falsification controls, using no archived code.

These are not a proof of the universal recurrence theorem. The top-complex
control searches directly for either witness, rather than implementing the
manuscript's branch classifier. All discrete identities use exact fractions.
"""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
from itertools import product, combinations
from math import factorial, log, prod
from pathlib import Path
import json,time

ROOT=Path(__file__).resolve().parent
START=time.monotonic()

def complexes(d):
    return tuple(y for y in product(range(3),repeat=d) if sum(y)<=2)

def dot(a,b): return sum(x*y for x,y in zip(a,b))
def ff(x,y):
    if any(a<b for a,b in zip(x,y)): return 0
    return prod(prod(range(a-b+1,a+1)) for a,b in zip(x,y))
def plus(a,b): return tuple(x+y for x,y in zip(a,b))
def minus(a,b): return tuple(x-y for x,y in zip(a,b))
def fac(x): return prod(factorial(a) for a in x)

def independent_alternative(ys,w,I):
    heights=[dot(w,y) for y in ys]
    if len(set(heights))==1: return 'nonnegative_invariant'
    for k,s in enumerate(ys):
        for j,c in enumerate(ys):
            if heights[k]>heights[j] and all(s[a]<=c[a] for a in range(len(w)) if a not in I):
                return 'available_pair'
    # A certificate search independent of the paper's J/companion construction.
    for ell in product((-1,0,1),repeat=len(w)):
        if any(ell[i]<0 for i in I) or not any(ell[i]>0 for i in I): continue
        if len({dot(ell,y) for y in ys})==1:
            return 'signed_or_coordinate_invariant'
    raise AssertionError(('no valid alternative',ys,w,sorted(I)))

def atlas():
    universe=complexes(3)
    weights=set()
    for den in (3,7):
        for nums in product(range(den+1),repeat=3):
            if sum(nums)==den: weights.add(tuple(F(n,den) for n in nums))
    counts=Counter(); slow=0; total=0
    for w in sorted(weights):
        support={i for i in range(3) if w[i]}
        for mask in range(1,8):
            I={i for i in range(3) if mask>>i&1}
            if not support<=I: continue
            for ymask in range(1,1<<len(universe)):
                ys=tuple(y for i,y in enumerate(universe) if ymask>>i&1)
                counts[independent_alternative(ys,w,I)]+=1
                total+=1; slow+=bool(I-support)
    # More species and asymmetric scales, deterministically sampled, including
    # zero normalized weights that remain members of the divergent set.
    import random
    rng=random.Random(22089551)
    extra=Counter()
    for _ in range(3000):
        d=rng.randrange(4,8); univ=complexes(d)
        nums=[rng.randrange(4) for _ in range(d)]
        if not any(nums): nums[0]=1
        w=tuple(F(a,sum(nums)) for a in nums)
        I={i for i,a in enumerate(nums) if a or rng.randrange(2)}
        ys=tuple(rng.sample(univ,rng.randrange(1,len(univ)+1)))
        extra[independent_alternative(ys,w,I)]+=1
    return {'three_species_cases':total,'normalized_weights':len(weights),'zero_weight_divergent_cases':slow,
            'witness_counts':dict(counts),'higher_dimension_cases':3000,'higher_dimension_witnesses':dict(extra)}

def exact_identities():
    count=0; ys=complexes(3)
    for rho in product(range(3),repeat=3):
        for t in ys:
            x=plus(rho,t)
            for s in ys:
                if not ff(x,s): continue
                for u in ys:
                    new=plus(minus(x,s),u)
                    assert F(fac(minus(new,u)),fac(rho))==F(ff(x,t),ff(x,s))
                    if s==t: assert minus(new,u)==rho
                    count+=1
    return count

def episode(channels,rho,path):
    # Sum the rewards of every terminal branch directly, rather than backward
    # recursion. All source/channel probabilities are exact rational numbers.
    reward=0.0; reach=F(1); phases=[]
    for j,t in enumerate(path):
        x=plus(rho,t)
        rates=[k*ff(x,s) for s,u,k in channels]
        total=sum(rates); assert total>0
        immediate=0.0
        designated=None if j==len(path)-1 else next(i for i,(s,u,k) in enumerate(channels) if s==t and u==path[j+1])
        for i,(s,u,k) in enumerate(channels):
            if not rates[i]: continue
            ratio=F(ff(x,t),ff(x,s))
            change=log(ratio.numerator)-log(ratio.denominator)
            immediate+=float(rates[i]/total)*change
            reward+=float(reach*rates[i]/total)*change
            if i==designated: assert ratio==1
        phases.append(immediate)
        if designated is not None: reach*=rates[designated]/total
    return reward,phases

def episode_controls():
    out=[]
    # The paper's motivating boundary example, including large scale separation.
    a=(1,0);b=(0,1);ab=(1,1);z=(0,0)
    channels=[(z,ab,F(2)),(ab,b,F(3)),(b,z,F(7))]
    for n in (100,10000,10**8):
        reward,phases=episode(channels,(n,0),[z,ab,b])
        assert reward<0
        out.append({'example':'missing-pure-A boundary','n':n,'episode_drift':reward,'drift_over_log_n':reward/log(n)})
    # Rate degeneration: fixed m must become outward as final rate tends to 0.
    for m in (2,7,30):
        ch=[(z,a,F(2)),(a,ab,F(5)),(ab,z,F(1,10**12))]
        reward,_=episode(ch,(m-1,0),[a,ab,z])
        aa=F(2,2+5*m)*log(m); pp=F(5*m,2+5*m)
        expected=float(aa*(1+pp))
        assert reward>0 and abs(reward-expected)<1e-9
        out.append({'example':'rate-degeneration','m':m,'drift':reward,'limit':expected})
    # Unit-rate double-species cycles; direct branch sum checks -2/d^d.
    for d in range(2,7):
        zero=(0,)*d
        ys=[tuple(2 if i==j else 0 for i in range(d)) for j in range(d)]
        cyc=[zero]+ys
        ch=[(cyc[i],cyc[(i+1)%len(cyc)],F(1)) for i in range(len(cyc))]
        # The stated error is O_d(log(N)/N), not a uniform relative error in d.
        # Use a larger N for the small leading coefficient at d=6.
        n=10**12; reward,_=episode(ch,(n,)*d,ys+[zero])
        expected=-2/(d**d)
        assert abs(reward/log(n)-expected)<1e-7*abs(expected)
        out.append({'example':'unit-rate attenuation','d':d,'normalized_drift':reward/log(n),'expected':expected})
    return out

def lifted_returns():
    count=0
    for d in (1,2,3):
        ys=complexes(d)
        for x in product(range(4),repeat=d):
            for j,s in enumerate(ys):
                if not ff(x,s): continue
                rho=minus(x,s)
                # Cycle starts at s, takes its forward edge, then the entire
                # directed return path. Every lift keeps precisely rho.
                state=x
                for k in range(len(ys)):
                    src=ys[(j+k)%len(ys)];dst=ys[(j+k+1)%len(ys)]
                    assert state==plus(rho,src) and ff(state,src)>0
                    state=plus(minus(state,src),dst)
                    assert all(v>=0 for v in state)
                assert state==x
                count+=1
    return count

def finite_lattice_control():
    states=[(4,0),(2,2),(0,4)]
    ch=[((2,0),(0,2),F(2)),((0,2),(2,0),F(3))]
    pi=[F(9,49),F(36,49),F(4,49)]
    Q=[[F(0) for _ in states] for _ in states]
    for i,x in enumerate(states):
        for s,t,k in ch:
            rate=k*ff(x,s)
            if rate:
                nxt=plus(minus(x,s),t);j=states.index(nxt)
                Q[i][j]+=rate;Q[i][i]-=rate
    assert sum(pi)==1
    assert all(sum(pi[i]*Q[i][j] for i in range(3))==0 for j in range(3))
    assert all(ff((1,0),s)==0 for s,t,k in ch)
    return {'closed_parity_class':states,'stationary_probability':[str(v) for v in pi],
            'absorbing_state':[1,0],'stationary_balance_exact':True}

result={'started_utc':datetime.now(timezone.utc).isoformat(),'independent_code':True,
        'identity_checks':exact_identities(),'lifted_cycle_checks':lifted_returns(),
        'top_alternative':atlas(),'episode_controls':episode_controls(),
        'finite_lattice':finite_lattice_control()}
result['elapsed_seconds']=time.monotonic()-START
result['limits']='Finite identities and controls only; universal recurrence is assessed analytically in REVIEW.md.'
(ROOT/'fresh_controls.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
