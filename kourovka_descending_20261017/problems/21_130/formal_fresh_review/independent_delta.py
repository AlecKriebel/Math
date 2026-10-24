#!/usr/bin/env python3
"""Generic integer finite differences for selected newly arrived n10/11 values.

Does not use the author's optimized fixed-zero/min1 denominator formulas.
The full Vandermonde at a permutation is its sign times the integer Delta;
all binomial/factorial weights are the unoptimized multivariate formula.
"""
import datetime,hashlib,itertools,json,math,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
SOURCES=['algebraic/fixed_zero_coefficients.py','algebraic/fixed_zero_coefficients.txt','algebraic/low_exponent_coefficients.py','algebraic/low_exponent_coefficients.jsonl']

def freeze():
    manifest={'frozen_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':[]}
    for rel in SOURCES:
        b=(BASE/rel).read_bytes();p=HERE/'delta_snapshot'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
        manifest['files'].append({'path':rel,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
    (HERE/'DELTA_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')

def check(n,targets):
    start=time.monotonic()
    edges=[(i,(i+1)%n) for i in range(n)]
    pairs=[(i,j) for i,j in itertools.combinations(range(n),2) if set(edges[i]).isdisjoint(edges[j])]
    assert len(pairs)==n*(n-3)//2
    D=math.prod(math.factorial(i) for i in range(n))
    degree=n*(n-2)
    accum=[0]*len(targets);counts=[0]*len(targets);nonzero=0;checked=0
    cap0=max(t[0] for t,value in targets)
    for first in range(cap0+1):
        for tail in itertools.permutations(i for i in range(n) if i!=first):
            a=(first,)+tail;checked+=1
            s=[a[i]+a[(i+1)%n] for i in range(n)]
            h=1
            for i,j in pairs:
                z=s[j]-s[i]
                if not z:break
                h*=z
            else:
                nonzero+=1
                parity=sum(a[i]>a[j] for i,j in itertools.combinations(range(n),2))
                value=((-1)**parity)*D*h
                for u,(t,expected) in enumerate(targets):
                    if any(ai>ti for ai,ti in zip(a,t)):continue
                    counts[u]+=1
                    weight=math.prod(((-1)**(ti-ai))*math.comb(ti,ai) for ai,ti in zip(a,t))
                    accum[u]+=value*weight
    records=[]
    for (t,expected),numerator,count in zip(targets,accum,counts):
        assert len(t)==n and min(t)>=0 and max(t)<n and sum(t)==degree
        denominator=math.prod(math.factorial(ti) for ti in t)
        coefficient,remainder=divmod(numerator,denominator)
        assert remainder==0
        assert coefficient==expected,(n,t,coefficient,expected)
        records.append({'exponents':t,'coefficient':coefficient,'numerator':numerator,'denominator':denominator,'integer_division_remainder':remainder,'nonzero_accepted_permutations':count})
    return {'n':n,'checked_permutations':checked,'nonzero_Q_permutations':nonzero,'witnesses':records,'witness_gcd':math.gcd(*(r['coefficient'] for r in records)),'seconds':time.monotonic()-start}

if __name__=='__main__':
    freeze()
    jobs=[(10,[([1,7,9,9,9,9,9,9,9,9],-299280689184),([1,8,8,9,9,9,9,9,9,9],-600114405460),([1,8,9,8,9,9,9,9,9,9],-643745163834)]),(11,[([0,9,10,10,10,10,10,10,10,10,10],11098103614834),([0,10,9,10,10,10,10,10,10,10,10],189427196282499)])]
    result={'time_started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sizes':[]}
    for n,targets in jobs:
        rec=check(n,targets);result['sizes'].append(rec)
        (HERE/'delta_results.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({'n':n,'witness_gcd':rec['witness_gcd'],'coefficients':[r['coefficient'] for r in rec['witnesses']],'seconds':rec['seconds']}),flush=True)
    result['time_completed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    (HERE/'delta_results.json').write_text(json.dumps(result,indent=2)+'\n')
