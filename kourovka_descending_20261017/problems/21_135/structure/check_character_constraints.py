#!/usr/bin/env python3
"""Exact arithmetic only; no group-theoretic conclusion from packet feasibility."""
from collections import Counter
from functools import reduce
from math import factorial,gcd,lcm
import json
from pathlib import Path

def partitions(n, bound=None):
    if n == 0:
        yield ()
        return
    for a in range(min(n, bound or n), 0, -1):
        for tail in partitions(n-a,a):
            yield (a,)+tail

def transpose(part):
    return tuple(sum(x>j for x in part) for j in range(part[0]))

def symmetric_degree(part):
    den=1
    trans=transpose(part)
    for i,row in enumerate(part):
        for j in range(row):
            den*=row-j+trans[j]-i-1
    num=factorial(sum(part))
    assert num%den==0
    return num//den

def alternating_degrees(n):
    out=Counter(); seen=set()
    for part in partitions(n):
        if part in seen: continue
        trans=transpose(part); seen.update([part,trans])
        d=symmetric_degree(part)
        if part==trans:
            assert d%2==0
            out[d//2]+=2
        else: out[d]+=1
    assert sum(m*d*d for d,m in out.items())==factorial(n)//2
    return out

def product(a,b):
    out=Counter()
    for d,m in a.items():
        for e,k in b.items(): out[d*e]+=m*k
    return out

def power(a,k):
    out=Counter({1:1})
    for _ in range(k): out=product(out,a)
    return out

def primes(n):
    out=[]; p=2
    while p*p<=n:
        if n%p==0:
            out.append(p)
            while n%p==0:n//=p
        p+=1
    if n>1:out.append(n)
    return out

def statistics(a):
    n=sum(m*d*d for d,m in a.items()); L=lcm(*a)
    return {'order':n,'lcm_degrees':L,'ito_gap':n//L,
        'multiplicity_gcd':gcd(*a.values()),
        'linear_multiplicity':a[1],
        'prime_free_square_masses':{str(p):sum(m*d*d for d,m in a.items() if d%p) for p in primes(n)}}

def bounded_witness(items,target,small_cutoff=1000000):
    # Binary package small weights, exact bitsets; greedy only selects the large
    # weights. Any returned witness is checked independently below.
    small=[(w,c,d) for w,c,d in items if w<=small_cutoff]
    large=sorted([(w,c,d) for w,c,d in items if w>small_cutoff],reverse=True)
    cap=sum(w*c for w,c,d in small)
    remaining=target; chosen=Counter()
    for w,c,d in large:
        take=min(c,remaining//w)
        chosen[d]+=take; remaining-=take*w
    if remaining>cap:return None
    bits=1; stages=[]
    mask=(1<<(remaining+1))-1
    for w,c,d in small:
        chunk=1
        while c:
            take=min(chunk,c); c-=take; chunk*=2
            shift=w*take
            old=bits
            bits=(bits | (bits<<shift))&mask
            stages.append((old,shift,take,d))
    if not ((bits>>remaining)&1):return None
    for old,shift,take,d in reversed(stages):
        if not ((old>>remaining)&1):
            chosen[d]+=take; remaining-=shift
    assert remaining==0
    return {d:c for d,c in chosen.items() if c}

def central_two_packet(a):
    n=sum(m*d*d for d,m in a.items())
    assert n%8==0
    even={d:m for d,m in a.items() if d%2==0}
    total=sum(m*(d*d//4) for d,m in even.items())
    # Search for omitted even-degree characters, leaving exactly n/2 mass in
    # the nontrivial central-character sector. All odd degrees stay principal.
    omitted=bounded_witness([(d*d//4,m,d) for d,m in even.items()],total-n//8)
    if omitted is None:return None
    faithful={d:m-omitted.get(d,0) for d,m in even.items() if m>omitted.get(d,0)}
    assert all(0<=m<=a[d] and d%2==0 for d,m in faithful.items())
    assert sum(m*d*d for d,m in faithful.items())==n//2
    principal={d:m-faithful.get(d,0) for d,m in a.items() if m>faithful.get(d,0)}
    assert principal[1]==1
    assert sum(m*d*d for d,m in principal.items())==n//2
    return {'principal_sector':principal,'nontrivial_sector':faithful,
       'warning':'Numerical central C2 necessary conditions only; not a group or a counterexample.'}

def main():
    a5=alternating_degrees(5); a7=alternating_degrees(7)
    assert a5==Counter({1:1,3:2,4:1,5:1})
    assert a7==Counter({1:1,6:1,10:2,14:2,15:1,21:1,35:1})
    records=[]
    for n,base in [(5,a5),(7,a7)]:
        for k in range(1,7):
            data=power(base,k)
            records.append({'group':f'A{n}^{k}','degrees':dict(sorted(data.items())),**statistics(data)})
    packet=central_two_packet(power(a7,3))
    result={'method':'Hook-length formula and Sn-to-An restriction; direct-product degree convolution; exact integers',
        'records':records,'central_C2_numeric_packet_A7_cubed':packet}
    path=Path(__file__).with_name('character_constraints_results.json')
    path.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'records':len(records),'A7_cubed_central_packet_found':packet is not None,
       'output':str(path)},sort_keys=True))
if __name__=='__main__':main()
