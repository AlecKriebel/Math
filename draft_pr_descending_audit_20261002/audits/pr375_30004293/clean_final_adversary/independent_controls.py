#!/usr/bin/env python3
"""Independent finite falsifiers. No author implementation is imported."""
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
import json, hashlib, pathlib, datetime

HERE=pathlib.Path(__file__).resolve().parent
def hist(B):
    h=Counter({0:1})
    for x in B:
        old=h.copy()
        for s,n in old.items(): h[s+x]+=n
    return h
def maximum(B): return max(hist(B).values())

def main():
    finite=0
    for bits in product((0,1),repeat=12):
        B=tuple(n+1 for n,b in enumerate(bits) if b)
        m=maximum(B)
        assert sum(hist(B).values())==2**len(B)
        for x in B:
            C=tuple(y for y in B if y!=x)
            assert maximum(C)<=m<=2*maximum(C)
            finite+=1
        C=tuple(x for x in B if x<=6)
        E=tuple(x for x in B if x>6)
        assert m>=maximum(C)*maximum(E)
    rel=0
    for h in range(2,8):
        for S in combinations(range(1,13),h):
            for signs in product((-1,1),repeat=h):
                if sum(x*s for x,s in zip(S,signs))==0:
                    assert S[-2]*(h-1)>=S[-1]
                    rel+=1
    tilts=0
    for N in range(1,11):
        for z in (Fraction(1,2),Fraction(1),Fraction(2),Fraction(3)):
            brute=Fraction(0)
            marg=[Fraction(0) for _ in range(N)]
            for bits in product((0,1),repeat=N):
                p=Fraction(1)
                for n,b in enumerate(bits,1):p*=Fraction(1,n) if b else Fraction(n-1,n)
                weight=p*z**sum(bits);brute+=weight
                for i,b in enumerate(bits):marg[i]+=b*weight
            analytic=Fraction(1)
            for n in range(1,N+1):analytic*=1+(z-1)/n
            assert brute==analytic
            for n in range(1,N+1):assert marg[n-1]/brute==z/(n+z-1)
            tilts+=1
    sources=[]
    for name in ('OWR','FGKv3','FGKpublished','MaoSongv2','divisorPower'):
        p=HERE/'tmp'/f'{name}.pdf'
        sources.append({'file':p.name,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    return {'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'meaning':'finite falsification controls, not asymptotic proof','finite_modification_checks':finite,'all_4096_subsets_of_1_to_12_tensor_checks':4096,'nonzero_all_signed_relation_checks':rel,'exact_tilt_populations':tilts,'sources':sources}
if __name__=='__main__': print(json.dumps(main(),indent=2))
