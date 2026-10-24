#!/usr/bin/env python3
"""Independent packed-exponent expansion and exact coefficient extraction.

No imports from the reviewed code. Factor order is the reverse of the source
implementation, and exponent vectors are packed into hexadecimal digits.
Selected coefficients are also checked via integer finite differences.
"""
import datetime
import hashlib
import itertools
import json
import math
import time
from pathlib import Path

HERE=Path(__file__).resolve().parent
EXPECTED={
3:[([0,1,2],1)],
4:[([0,2,3,3],4)],
5:[([1,3,3,4,4],14),([0,4,3,4,4],-24)],
6:[([2,3,5,5,4,5],182),([2,4,5,5,3,5],-476),([0,4,5,5,5,5],-520)],
7:[([1,5,6,5,6,6,6],-1454),([4,4,5,5,5,6,6],1570)],
8:[([4,6,5,7,7,6,6,7],-108696),([3,4,6,7,7,7,7,7],-2270792)],
9:[([0,7,8,8,8,8,8,8,8],-137176976),([1,7,8,7,8,8,8,8,8],-1261141910)]}

def disjoint_edges(n):
    result=[]
    for a,b in itertools.combinations(range(n),2):
        if {a,(a+1)%n}.isdisjoint({b,(b+1)%n}): result.append((a,b))
    assert len(result)==n*(n-3)//2
    return result

def factors(n):
    fs=[]
    for a,b in itertools.combinations(range(n),2):
        fs.append([(a,-1),(b,1)])
    for a,b in disjoint_edges(n):
        # Endpoints disjoint: there are exactly four different variables.
        fs.append([(a,-1),((a+1)%n,-1),(b,1),((b+1)%n,1)])
    assert len(fs)==n*(n-2)
    return fs

def expand_packed(n):
    p={0:1}
    peak=1
    for f in reversed(factors(n)):
        q={}
        for e,c in p.items():
            for i,s in f:
                if ((e>>(4*i))&15)==n-1: continue
                ee=e+(1<<(4*i))
                q[ee]=q.get(ee,0)+s*c
        p={e:c for e,c in q.items() if c}
        peak=max(peak,len(p))
    unpack=lambda e:tuple((e>>(4*i))&15 for i in range(n))
    p={unpack(e):c for e,c in p.items()}
    assert all(sum(e)==n*(n-2) and max(e)<n for e in p)
    return p,peak

def integer_value(a):
    n=len(a)
    v=math.prod(a[j]-a[i] for i,j in itertools.combinations(range(n),2))
    s=[a[i]+a[(i+1)%n] for i in range(n)]
    return v*math.prod(s[j]-s[i] for i,j in disjoint_edges(n))

def finite_difference(t):
    n=len(t); total=0; accepted=0; nonzero=0
    for a in itertools.permutations(range(n)):
        if any(a[i]>t[i] for i in range(n)): continue
        accepted+=1
        value=integer_value(a)
        if value:
            nonzero+=1
            total+=value*math.prod(((-1)**(t[i]-a[i]))*math.comb(t[i],a[i]) for i in range(n))
    divisor=math.prod(math.factorial(e) for e in t)
    coefficient,remainder=divmod(total,divisor)
    assert remainder==0
    return {'coefficient':coefficient,'numerator':total,'denominator':divisor,'accepted_permutations':accepted,'nonzero_permutations':nonzero}

def main():
    results={'time_started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'packed exponents; all factors reversed; independent finite differences','sizes':[]}
    for n in range(3,10):
        start=time.monotonic()
        p,peak=expand_packed(n)
        content=math.gcd(*p.values())
        witnesses=[]
        for t,expected in EXPECTED[n]:
            fd=finite_difference(t)
            actual=p[tuple(t)]
            assert actual==fd['coefficient']==expected,(n,t,actual,fd,expected)
            witnesses.append({'t':t,'expected':expected,'expansion':actual,'finite_difference':fd})
        entry={'n':n,'support':len(p),'content':content,'peak_support':peak,'witness_gcd':math.gcd(*(w['expansion'] for w in witnesses)),'witnesses':witnesses,'elapsed_seconds':time.monotonic()-start}
        if n>=8:
            source=HERE/'snapshot'/'algebraic'/'polynomial'/f'slack_n{n}.json'
            raw=source.read_bytes();data=json.loads(raw)
            old={tuple(e):c for e,c in data['terms']}
            assert len(old)==len(data['terms']),'duplicate source exponents'
            assert p==old,'full support mismatch'
            assert content==data['content']
            entry['compared_full_source_sha256']=hashlib.sha256(raw).hexdigest()
            entry['exact_full_support_match']=True
        results['sizes'].append(entry)
        (HERE/'coefficient_results.json').write_text(json.dumps(results,indent=2)+'\n')
        print(json.dumps({key:entry[key] for key in ['n','support','content','witness_gcd','peak_support','elapsed_seconds']}),flush=True)
    results['time_completed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
    (HERE/'coefficient_results.json').write_text(json.dumps(results,indent=2)+'\n')

if __name__=='__main__': main()
