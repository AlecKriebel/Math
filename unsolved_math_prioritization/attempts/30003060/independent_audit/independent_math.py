#!/usr/bin/env python3
"""Independent finite diagnostics; no author imports. Exact column elimination and Mobius counts."""
from fractions import Fraction
from itertools import product
import json
import sys

def need(condition, message):
    if not condition:
        raise RuntimeError(message)

def rank(columns, p):
    pivots = {}
    for values in columns:
        v = [c % p if p else Fraction(c) for c in values]
        for i, row in sorted(pivots.items()):
            if v[i]:
                c = v[i]
                v = [(x-c*y) % p if p else x-c*y for x,y in zip(v,row)]
        nz = next((i for i,x in enumerate(v) if x), None)
        if nz is not None:
            t = pow(int(v[nz]), -1, p) if p else 1/v[nz]
            pivots[nz] = [(t*x) % p if p else t*x for x in v]
    return len(pivots)

def mobius(n):
    sign = 1
    d = 2
    while d*d <= n:
        if n % d == 0:
            n //= d
            sign = -sign
            if n % d == 0:
                return 0
        else:
            d += 1
    return -sign if n > 1 else sign

def necklace_counts(r,n):
    counts = {}
    for d in range(1,n+1):
        if n % d == 0:
            total = sum(mobius(e)*r**(d//e) for e in range(1,d+1) if d%e==0)
            need(total%d==0, 'primitive necklace count nonintegral')
            counts[d] = total//d
    need(sum(d*c for d,c in counts.items())==r**n,'necklace partition failure')
    return counts

def matrix_case(r,n,p):
    ws = list(product(range(r),repeat=n)); idx={w:i for i,w in enumerate(ws)}
    columns=[]; squared=[]
    for w in ws:
        t=w[-1:]+w[:-1]; tt=t[-1:]+t[:-1]
        v=[0]*len(ws); u=v.copy()
        v[idx[w]]+=1;v[idx[t]]-=1
        u[idx[w]]+=1;u[idx[t]]-=2;u[idx[tt]]+=1
        columns.append(v);squared.append(u)
    b=rank(columns,p);bb=rank(squared,p);h=len(ws)-b;hi=b-bb
    # ker(delta)=ker(b) intersection im(b); its dimension is rank(b)-rank(b^2).
    return {'hk0':h,'hk1':h,'delta_rank':h-hi,'hi0':hi,'hi1':hi}

def witness(p):
    w=(0,)*(p-1)+(1,); orbit=[];u=w
    for i in range(p):
        orbit.append(u);u=u[-1:]+u[:-1]
    need(u==w and len(set(orbit))==p,'nonprimitive orbit')
    boundary={}; certificate={}
    for i,u in enumerate(orbit):
        t=u[-1:]+u[:-1]
        boundary[u]=boundary.get(u,0)+1;boundary[t]=boundary.get(t,0)-1
        # sum_i w_i - p*w_0 = sum_{j=0}^{p-2} (p-1-j)*(w_{j+1}-w_j).
        if i<p-1:
            certificate[t]=certificate.get(t,0)+p-1-i
            certificate[u]=certificate.get(u,0)-(p-1-i)
    need(all(x==0 for x in boundary.values()),'integer telescoping failure')
    target={u:1 for u in orbit};target[w]-=p
    need(all(certificate.get(u,0)==target.get(u,0) for u in set(target)|set(certificate)), 'commutator certificate failure')
    need(all((certificate.get(u,0)-1)%p==0 for u in orbit),'positive characteristic quotient failure')
    # A proper nonempty segment is not a cycle; the two surviving endpoints differ.
    removed_boundary = dict(boundary)
    removed_boundary[orbit[0]] -= 1
    removed_boundary[orbit[1]] += 1
    need(any(v % p for v in removed_boundary.values()), 'deleted term incorrectly remains a cycle')
    return {'p':p,'terms':len(orbit),'integer_boundary_zero':True,'integer_commutator_certificate':True,'rational_coinvariant_value':p,'Fp_coinvariant_value':0,'deleted_term_fails_cycle':True}

def main():
    need(sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode,'use -I -S -B')
    cases=[]
    for r,limit in [(1,8),(2,7),(3,4)]:
        for n in range(1,limit+1):
            counts=necklace_counts(r,n)
            for p in [0,2,3,5,7,11]:
                actual=matrix_case(r,n,p)
                h=sum(counts.values());hi=sum(v for d,v in counts.items() if p and d%p==0)
                expect={'hk0':h,'hk1':h,'delta_rank':h-hi,'hi0':hi,'hi1':hi}
                need(actual==expect,'matrix square / necklace mismatch')
                cases.append({'generators':r,'total_weight':n,'characteristic':p,**actual})
    witnesses=[witness(p) for p in [2,3,5,7,11,13,17,19,23,29,31]]
    need(matrix_case(2,2,2)['hi1']==1,'F2 witness')
    need(matrix_case(2,2,3)['hi1']==0,'odd characteristic minimal witness must fail')
    need(matrix_case(2,3,3)['hi1']==2,'F3 weight3 two primitive necklaces')
    need(matrix_case(2,3,0)['hi1']==0,'characteristic zero control')
    print(json.dumps({'status':'PASS','method':'rank(b)-rank(b^2) by exact column elimination, independently checked with Mobius necklace counts','matrix_necklace_cases':len(cases),'prime_witnesses':len(witnesses),'cases':cases,'witnesses':witnesses,'limits':'Bounded controls do not replace the universal algebraic proof.'},sort_keys=True,indent=2))

if __name__=='__main__':main()
