#!/usr/bin/env python3
"""Exact finite controls for the authored alpha-bound investigation.
No external inputs or source corpus. Modular full column rank certifies Q-rank.
Rank deficiency modulo p alone is never used as a Q existence certificate.
"""
from fractions import Fraction as Q
from math import comb
import json
from pathlib import Path

P = 1009

def mod(q):
    q=Q(q)
    return q.numerator * pow(q.denominator,-1,P) % P

def rank_mod(rows):
    rows=[r[:] for r in rows]
    rank=0
    for c in range(len(rows[0]) if rows else 0):
        pivot=next((j for j in range(rank,len(rows)) if rows[j][c]),None)
        if pivot is None: continue
        rows[rank],rows[pivot]=rows[pivot],rows[rank]
        u=pow(rows[rank][c],-1,P)
        rows[rank]=[(z*u)%P for z in rows[rank]]
        for j in range(rank+1,len(rows)):
            u=rows[j][c]
            if u: rows[j]=[(v-u*w)%P for v,w in zip(rows[j],rows[rank])]
        rank+=1
        if rank==len(rows): break
    return rank

def interpolation(points,d,m):
    mons=[(i,j) for i in range(d+1) for j in range(d+1-i)]
    rows=[]
    for x,y in points:
        x,y=mod(x),mod(y)
        for a in range(m):
            for b in range(m-a):
                rows.append([comb(i,a)*comb(j,b)*pow(x,i-a,P)*pow(y,j-b,P)%P
                             if i>=a and j>=b else 0 for i,j in mons])
    rank=rank_mod(rows)
    return dict(d=d,m=m,rows=len(rows),columns=len(mons),rank_mod_1009=rank,
                full_column_rank=rank==len(mons))

def run():
    star=[(0,0),(0,1),(0,Q(3,2)),(1,0),(3,0),(-1,2)]
    general=[(0,0),(1,0),(0,1),(2,3),(4,2),(3,5)]
    grid=[(i,j) for i in range(3) for j in range(3)]
    output={'modulus':P,'arithmetic':'exact integers and rational input; modular rank',
            'configurations':{}}
    specs=[('four_line_star',star,[(2,1),(6,3),(10,5)],{1:3,3:7,5:11},'explicit line-product witness; see authored proof'),
           ('six_rational_points',general,[(2,1),(7,3),(11,5)],{1:3,3:8,5:12},'dimension count at degrees 3,8,12'),
           ('three_by_three_grid',grid,[(2,1),(8,3)],{1:3,3:9},'cube of product of three vertical lines')]
    for name,pts,cases,alpha,upper in specs:
        checks=[interpolation(pts,d,m) for d,m in cases]
        assert all(x['full_column_rank'] for x in checks),(name,checks)
        output['configurations'][name]={'points':[[str(x),str(y)] for x,y in pts],
          'lower_degree_checks':checks,'certified_alpha_over_Q':alpha,'upper_certificate':upper}
    # All points are distinct modulo 1009, so all jet-condition rows are valid.
    for name,pts,*_ in specs: assert len({(mod(x),mod(y)) for x,y in pts})==len(pts)
    # Verify identities with exact rational arithmetic over a bounded check window.
    count=0
    for n in range(1,9):
        for a in range(1,31):
            for r in range(1,31):
                m=n*(r-1)+1; B=r*a+(r-1)*(n-1); L=Q(a+n-1,n)
                assert B-m*L == Q((n-1)*(a-1),n)
                assert B-(a+m-1)==(r-1)*(a-1)
                if n>=2 and a<=2:
                    assert (m*L.numerator+L.denominator-1)//L.denominator >= B
                count+=1
    output['exact_identity_checks']=count
    # Reduced-plane-curve obstruction. This is only an arithmetic control;
    # its mathematical scope and proof are in PROOFS.md.
    count=0
    for a in range(2,101):
        for r in range(3,101):
            d=r*(a+1)-2; m=2*r-1
            assert d*(d-1)<Q(a*(a+1),2)*m*(m-1)
            count+=1
    output['polar_obstruction_checks']=count
    return output

if __name__=='__main__':
    result=run()
    p=Path(__file__).with_name('control_results.json')
    p.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
