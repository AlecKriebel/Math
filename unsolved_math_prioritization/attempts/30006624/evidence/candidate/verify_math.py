#!/usr/bin/env python3
"""Exact finite controls for the authored report; no network or file writes.

These checks do not prove the unresolved globalization theorem or the topology
of the infinite examples. All requirements remain active under -O and -OO.
"""
import argparse
from fractions import Fraction as Q
from itertools import product, combinations_with_replacement
import json
import os
import sys


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def l1(a, b):
    return sum(abs(x-y) for x,y in zip(a,b))


def median_set(points, distance, a, b, c):
    return [m for m in points if all(distance(x,m)+distance(m,y)==distance(x,y)
                                    for x,y in ((a,b),(b,c),(c,a)))]


def cycle_distance(n, a, b):
    k=abs(a-b)
    return min(k,n-k)


def integral(x):
    return x+x*x/2


def weighted(p, q):
    x,y=p; u,v=q
    require(abs(y-v)<2, 'Formula used beyond proved vertical range')
    return abs(integral(x)-integral(u))+(1+min(x,u))*abs(y-v)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--mutation', choices=['accept_circle','flatten_weight','ball_closed','unique_geodesic','overclaim_uniqueness','wrong_descent_constant'])
    args=parser.parse_args()
    # Positive median controls include repetitions, not merely distinct triples.
    grid=list(product(range(3),repeat=3))
    triples=0
    for a,b,c in combinations_with_replacement(grid,3):
        expected=tuple(sorted((a[i],b[i],c[i]))[1] for i in range(3))
        require(median_set(grid,l1,a,b,c)==[expected], 'l1 cube median failed')
        triples+=1
    # C4 VERTICES are median; its continuous perimeter is not. C6 catches that.
    for a,b,c in combinations_with_replacement(range(4),3):
        require(len(median_set(range(4),lambda x,y:cycle_distance(4,x,y),a,b,c))==1,
                'C4 vertex control failed')
    c6=median_set(range(6),lambda x,y:cycle_distance(6,x,y),0,2,4)
    require(c6==[], 'C6 equilateral triple should have no median')
    if args.mutation=='accept_circle':
        require(len(c6)==1, 'CONTROL REJECTED: continuous-circle surrogate is not median')
    # K_{2,3} is modular but not median: the descent lemma proves existence only.
    def k23(a,b):
        return 0 if a==b else (1 if (a<2)!=(b<2) else 2)
    k23_counts=[len(median_set(range(5),k23,a,b,c))
                for a,b,c in combinations_with_replacement(range(5),3)]
    require(min(k23_counts)>=1 and max(k23_counts)==2, 'K23 modularity control failed')
    if args.mutation=='overclaim_uniqueness':
        require(max(k23_counts)==1, 'CONTROL REJECTED: modularity alone does not imply uniqueness')
    # Constructive descent controls with exact medians (eta may safely be zero).
    small=list(product(range(2),repeat=3));descent_cases=0
    for a,b,c in combinations_with_replacement(small,3):
        perimeter=l1(a,b)+l1(b,c)+l1(c,a)
        f=lambda x:Q(l1(a,x)+l1(b,x)+l1(c,x))-Q(perimeter,2)
        for x in small:
            if f(x)==0:continue
            pairs=((a,b),(b,c),(c,a))
            u,v=max(pairs,key=lambda uv:l1(uv[0],x)+l1(uv[1],x)-l1(*uv))
            s=Q(l1(u,x)+l1(v,x)-l1(u,v),2)
            y=tuple(sorted((u[i],v[i],x[i]))[1] for i in range(3))
            r=l1(x,y);delta=f(x)-f(y)
            require(f(x)/3<=s<=f(x), 'largest-pair defect inequality failed')
            require(Q(19,20)*s<=r<=Q(11,10)*s, 'travel bound failed')
            require(f(y)<=Q(3,4)*f(x) and r<=Q(19,15)*delta, 'descent bounds failed')
            if args.mutation=='wrong_descent_constant':
                require(f(y)<=Q(1,2)*f(x), 'CONTROL REJECTED: unproved stronger descent constant')
            descent_cases+=1
    # Arbitrary small rational conformal triples; evaluate the exact interval gap.
    weighted_cases=0
    for denominator in (4,8,16,32,64):
        a=Q(1,4); b=a+Q(1,denominator); k=Q(1,denominator)
        A=(a,Q(0));B=(b,Q(0));C=(b,k)
        distance=l1 if args.mutation=='flatten_weight' else weighted
        gap=distance(A,B)+distance(B,C)-distance(A,C)
        require(gap==(b-a)*k and gap>0,
                'CONTROL REJECTED: nonzero conformal interval defect missing')
        for j in range(denominator+1):
            x=a+(b-a)*Q(j,denominator); W=(x,Q(0))
            lhs=weighted(B,W)+weighted(W,C)-weighted(B,C)
            require(lhs==(b-x)*(2+b+x-k), 'weighted segment identity failed')
            require((lhs==0)==(x==b), 'weighted interval uniqueness failed')
            weighted_cases+=1
        require(l1(A,B)+l1(B,C)==l1(A,C), 'constant-weight positive control failed')
    # Small open ball counterexample: endpoints have norm 2 < 5/2; median norm 3.
    pts=((1,1,0),(1,0,1),(0,1,1)); center=(0,0,0)
    m=tuple(sorted(p[i] for p in pts)[1] for i in range(3))
    require(all(l1(center,p)<Q(5,2) for p in pts), 'ball endpoint control failed')
    require(l1(center,m)>Q(5,2), 'ball nonclosure control failed')
    if args.mutation=='ball_closed':
        require(l1(center,m)<Q(5,2), 'CONTROL REJECTED: metric balls need not be median-closed')
    # Distinct monotone paths have exactly the same endpoint distance.
    path1=((0,0),(1,0),(1,1));path2=((0,0),(0,1),(1,1))
    length=lambda path:sum(l1(a,b) for a,b in zip(path,path[1:]))
    require(path1!=path2 and length(path1)==length(path2)==2,
            'nonunique l1 geodesic control failed')
    if args.mutation=='unique_geodesic':
        require(path1==path2, 'CONTROL REJECTED: unique median does not imply unique geodesic')
    # The canonical CAT(0) diagonal metrics have unequal SQUARED values.
    require(Q(2)**2!=Q(2), 'diagonal chart metric obstruction failed')
    # Circle anchor separation and shrinking diameter are independent quantities.
    for n in range(1,51):
        diameter=Q(1,3*n)
        require(diameter>0 and diameter<=Q(1,3), 'circle diameter failed')
        require(Q(2)>diameter, 'branch anchor separation failed')
    # Slit-plane pair-distance/gap arithmetic; topology proved in text.
    for n in range(1,51):
        x=-Q(1,n)
        require(2*(2-x)>4, 'slit-plane median obstruction failed')
    print(json.dumps({'status':'PASS','uid':os.geteuid(),'optimization':sys.flags.optimize,
        'l1_grid_triples':triples,'weighted_interval_cases':weighted_cases,'descent_cases':descent_cases,
        'controls':['l1_grid','C4_vertices','C6_empty_median','constant_weight',
                    'nonclosed_ball','nonunique_geodesics','diagonal_metric',
                    'shrinking_circle_arithmetic','slit_plane_arithmetic','K23_modular_nonmedian','summable_descent'],
        'scope':'Exact finite arithmetic only; no globalization claim'},sort_keys=True))

if __name__=='__main__':
    main()
