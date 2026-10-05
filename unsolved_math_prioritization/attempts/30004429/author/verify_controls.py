#!/usr/bin/env python3
"""Exact finite controls for 30004429. No external packages or source datasets."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json


def mixture_q(n, k, lam=F(1, 2)):
    p, q = F(1, 4), F(3, 4)
    lo = (1-lam) * p**k * (1-p)**(n-k)
    hi = lam * q**k * (1-q)**(n-k)
    return (p*lo+q*hi)/(lo+hi)


def mixture_controls():
    p, q = F(1, 4), F(3, 4)
    cases = 0
    gaps = []
    for n in range(0, 8):
        for k in range(2*n+1):
            prev_lo, prev_hi = mixture_q(2*n,k), mixture_q(2*n,k)
            for m in range(n, n+15):
                extra = 2*(m-n)
                lo = mixture_q(2*m,k)
                hi = mixture_q(2*m,k+extra)
                assert p <= lo <= prev_lo <= prev_hi <= hi <= q
                prev_lo, prev_hi = lo, hi
                cases += 1
            gaps.append(hi-lo)
    # At balanced inner data, an explicit finite extension already gives > 0.49.
    gap = mixture_q(24,22)-mixture_q(24,2)
    assert gap > F(49,100)
    # Rare evidence raises covariance in a finite FKG mixture family.
    evidence = []
    for k in (1,4,8,12):
        lam=F(1,1+3**k)
        posterior = lam*q**k / ((1-lam)*p**k+lam*q**k)
        assert posterior == F(1,2)
        before=lam*(1-lam)*(q-p)**2
        after=posterior*(1-posterior)*(q-p)**2
        assert after == F(1,16)
        evidence.append({'k':k,'covariance_before':str(before),'covariance_after':str(after)})
        for N in range(2,9):
            w=[(1-lam)*p**r*(1-p)**(N-r)+lam*q**r*(1-q)**(N-r) for r in range(N+1)]
            assert all(w[r+1]**2<=w[r]*w[r+2] for r in range(N-1))
    return {'status':'PASS','annulus_monotonicity_cases':cases,'finite_gap':str(gap),'rare_evidence':evidence,
            'scope':'Finite rational checks of separate mixture countercontrols; not an Ising almost-Gibbs test.'}


def ising_control():
    # Rectangle 5 x 3, all nearest-neighbor external spins plus.
    # e^(2 beta)=2, so unnormalized exact weights are 2^(E-disagreements).
    sites=[(x,y) for y in range(-1,2) for x in range(-2,3)]
    index={s:i for i,s in enumerate(sites)}
    edges=[]
    boundary=[]
    for s,i in index.items():
        x,y=s
        for t in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if t in index:
                if i<index[t]:edges.append((i,index[t]))
            else:boundary.append(i)
    E=len(edges)+len(boundary)
    totals={row:0 for row in product((0,1),repeat=5)}
    for spins in product((0,1),repeat=len(sites)):
        d=sum(spins[i]!=spins[j] for i,j in edges)+sum(spins[i]==0 for i in boundary)
        row=tuple(spins[index[(x,0)]] for x in range(-2,3))
        totals[row] += 1 << (E-d)
    def marginal(obs, center=None):
        return sum(w for row,w in totals.items() if all(row[i]==s for i,s in obs.items()) and (center is None or row[2]==center))
    def cond(obs):
        return F(marginal(obs,1),marginal(obs))
    q={b:cond(dict(zip((0,1,3,4),b))) for b in product((0,1),repeat=4)}
    comparisons=0
    for a in q:
        for b in q:
            if all(x<=y for x,y in zip(a,b)):
                assert q[a]<=q[b]
                comparisons+=1
    brackets=[]
    for left,right in product((0,1),repeat=2):
        inner={1:left,3:right}
        qs=[]
        weights=[]
        for lo,hi in product((0,1),repeat=2):
            obs={**inner,0:lo,4:hi}
            qs.append(cond(obs));weights.append(marginal(obs))
        lower,upper=qs[0],qs[-1]
        assert lower==min(qs) and upper==max(qs)
        assert lower<=cond(inner)<=upper
        assert cond(inner)==sum(x*w for x,w in zip(qs,weights))/sum(weights)
        brackets.append({'inner':[left,right],'lower':str(lower),'central':str(cond(inner)),'upper':str(upper)})
    c=F(1,17)  # e^(8 beta)=16
    assert all(c<=v<=1-c for v in q.values())
    return {'status':'PASS','free_spins':len(sites),'configurations':2**len(sites),'interior_edges':len(edges),
            'boundary_edges':len(boundary),'monotonicity_comparisons':comparisons,'brackets':brackets,
            'scope':'One exact 5-by-3 plus-boundary box at beta=log(2)/2; no infinite-volume or phase-transition extrapolation.'}


def markov_control():
    P=((F(4,5),F(1,5)),(F(1,3),F(2,3)))
    pi=(F(5,8),F(3,8))
    assert all(sum(pi[a]*P[a][b] for a in (0,1))==pi[b] for b in (0,1))
    cases=0
    for m in (1,2,3):
        for ext in product((0,1),repeat=2*m):
            left,right=ext[m-1],ext[m]
            w=[]
            for center in (0,1):
                word=ext[:m]+(center,)+ext[m:]
                weight=pi[word[0]]
                for a,b in zip(word,word[1:]):weight*=P[a][b]
                w.append(weight)
            actual=w[1]/sum(w)
            predicted=P[left][1]*P[1][right]/sum(P[left][a]*P[a][right] for a in (0,1))
            assert actual==predicted
            cases+=1
    return {'status':'PASS','cases':cases,'scope':'Full-support stationary Markov-chain control: neighbors alone determine the two-sided singleton conditional.'}


def main():
    results={'problem_id':'30004429','result':'PASS','arithmetic':'Exact Python fractions and integers',
             'mixture_controls':mixture_controls(),'ising_finite_control':ising_control(),'markov_control':markov_control(),
             'mathematical_status':'NO RESOLUTION; controls do not prove the target infinite-volume almost-sure limit.'}
    path=Path(__file__).resolve().with_name('CHECK_RESULTS.json')
    path.write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({'result':'PASS','output':path.name,'controls':3,'target_resolved':False}))

if __name__=='__main__':main()
