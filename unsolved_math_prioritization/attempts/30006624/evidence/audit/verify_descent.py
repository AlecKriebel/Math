#!/usr/bin/env python3
"""Exact supplemental descent identities and genuinely inexact median controls."""
import argparse
from fractions import Fraction as Q
from itertools import combinations_with_replacement, product
import json
import os
import sys

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def add(*vectors):
    return tuple(sum(v[i] for v in vectors) for i in range(11))

def scale(c, v):
    return tuple(c*x for x in v)

def sub(v, w):
    return add(v, scale(-1, w))

def norm(a, b):
    return sum(abs(x-y) for x,y in zip(a,b))

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--mutation', choices=['drop_error_in_lower_bound','oversized_tolerance','duplicate_source_pair'])
    args = p.parse_args()
    # Coordinates: ax,bx,cx,ab,bc,ca,ay,by,cy,r,eta. Certificates are
    # polynomial identities with nonnegative combinations of metric slacks.
    units = [tuple(Q(i==j) for i in range(11)) for j in range(11)]
    ax,bx,cx,ab,bc,ca,ay,by,cy,r,eta = units
    s = scale(Q(1,2), sub(add(ax,bx),ab))
    f = sub(add(ax,bx,cx),scale(Q(1,2),add(ab,bc,ca)))
    delta = sub(add(ax,bx,cx),add(ay,by,cy))
    lower = scale(Q(1,2),add(sub(add(ay,r),ax),sub(add(by,r),bx),sub(add(ab,eta),add(ay,by))))
    upper = scale(Q(1,2),add(sub(add(ax,eta),add(ay,r)),sub(add(bx,eta),add(by,r)),sub(add(ay,by),ab)))
    improvement = add(sub(add(ax,eta),add(ay,r)),sub(add(bx,eta),add(by,r)),sub(add(cx,r),cy))
    require(lower == add(r,scale(-1,s),scale(Q(1,2),eta)), 'Lower-travel certificate failed')
    require(upper == sub(add(s,eta),r), 'Upper-travel certificate failed')
    require(improvement == add(delta,scale(-1,r),scale(2,eta)), 'Defect-decrease certificate failed')
    eab,ebc,eca = sub(add(ax,bx),ab),sub(add(bx,cx),bc),sub(add(cx,ax),ca)
    require(sub(scale(3,s),f) == scale(Q(1,2),add(sub(eab,ebc),sub(eab,eca))), 'Largest-defect certificate failed')
    # Substitute eta=s/10, then check the nonnegative combinations giving
    # delta>=3s/4, delta>=f/4, and 19delta>=15r.
    low = sub(r,scale(Q(19,20),s))
    imp = add(delta,scale(-1,r),scale(Q(1,5),s))
    require(add(low,imp) == sub(delta,scale(Q(3,4),s)), 'Three-quarter certificate failed')
    require(add(low,imp,scale(Q(1,4),sub(scale(3,s),f))) == sub(delta,scale(Q(1,4),f)), 'Contraction certificate failed')
    require(add(scale(19,imp),scale(4,low)) == sub(scale(19,delta),scale(15,r)), 'Summable-travel certificate failed')
    samples = 0
    points = list(product((Q(0),Q(1)),repeat=3))
    for a,b,c in combinations_with_replacement(points,3):
        perimeter = norm(a,b)+norm(b,c)+norm(c,a)
        defect = lambda w: norm(a,w)+norm(b,w)+norm(c,w)-perimeter/2
        for x in points:
            if defect(x)==0:
                continue
            u,v = max(((a,b),(b,c),(c,a)),key=lambda uv:norm(uv[0],x)+norm(uv[1],x)-norm(*uv))
            step = (norm(u,x)+norm(v,x)-norm(u,v))/2
            tolerance = step/10
            center = tuple(sorted((u[i],v[i],x[i]))[1] for i in range(3))
            for coordinate,sign in product(range(3),(-1,1)):
                y = tuple(center[i]+(sign*tolerance/2 if i==coordinate else 0) for i in range(3))
                errors = [norm(p,y)+norm(y,q)-norm(p,q) for p,q in ((u,v),(v,x),(x,u))]
                require(all(0<=e<=tolerance for e in errors) and max(errors)>0, 'Inexact median fixture failed')
                travel = norm(x,y)
                change = defect(x)-defect(y)
                lower_factor = Q(1) if args.mutation=='drop_error_in_lower_bound' else Q(19,20)
                require(lower_factor*step<=travel<=Q(11,10)*step, 'CONTROL REJECTED: approximate error is needed in the travel bound')
                require(defect(y)<=Q(3,4)*defect(x), 'Contraction failed')
                require(travel<=Q(19,15)*change, 'Summable-travel bound failed')
                samples += 1
    # A tolerance as large as s permits an actual increase of target defect.
    a=b=(Q(0),Q(0)); c=x=(Q(1),Q(0)); y=(Q(0),Q(1,2))
    errors = [norm(p,y)+norm(y,q)-norm(p,q) for p,q in ((a,b),(b,x),(x,a))]
    require(errors == [Q(1)]*3, 'Large-tolerance fixture failed')
    delta_bad = norm(a,x)+norm(b,x)+norm(c,x)-norm(a,y)-norm(b,y)-norm(c,y)
    require(delta_bad==Q(-1,2), 'Large-tolerance failure must be a real ascent')
    if args.mutation=='oversized_tolerance':
        require(delta_bad>=Q(1,4), 'CONTROL REJECTED: tolerance=s allows defect ascent')
    # Repeating pair ab in place of ca accepts b in every metric space.
    d = lambda i,j: Q(0) if i==j else Q(1)
    a,b,x = 0,1,2; y=b; tolerance=Q(1,20)
    duplicate_errors=[d(p,y)+d(y,q)-d(p,q) for p,q in ((a,b),(b,x),(a,b))]
    correct_errors=[d(p,y)+d(y,q)-d(p,q) for p,q in ((a,b),(b,x),(x,a))]
    require(duplicate_errors==[Q(0)]*3 and correct_errors==[Q(0),Q(0),Q(1)], 'Source-normalization fixture failed')
    if args.mutation=='duplicate_source_pair':
        require(all(e<=tolerance for e in correct_errors), 'CONTROL REJECTED: repeated pair omits a necessary interval')
    print(json.dumps({'status':'PASS','uid':os.getuid(),'euid':os.geteuid(),'optimization':sys.flags.optimize,
        'symbolic_identities':7,'genuinely_inexact_cases':samples,
        'scope':'Exact linear certificates and finite inexact controls; not a globalization proof'},sort_keys=True))

if __name__=='__main__':
    main()
