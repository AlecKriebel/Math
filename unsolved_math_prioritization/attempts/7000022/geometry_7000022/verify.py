#!/usr/bin/env python3
"""Exact finite controls for AMR-069-0022; this is not a conjecture proof.

Python 3.10+, standard library only. Every asserted radical comparison uses
rational enclosures. Floats occur only in human-readable diagnostic output.
"""

from collections import Counter
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import combinations, permutations
from math import isqrt
from pathlib import Path
import json


@dataclass(frozen=True)
class I:
    lo: Q
    hi: Q

    def __post_init__(self):
        assert self.lo <= self.hi

    def __add__(self, other):
        other = interval(other)
        return I(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return I(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + -interval(other)

    def __rsub__(self, other):
        return interval(other) + -self

    def __mul__(self, other):
        other = interval(other)
        p = [a*b for a in (self.lo,self.hi) for b in (other.lo,other.hi)]
        return I(min(p), max(p))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = interval(other)
        assert not other.lo <= 0 <= other.hi
        return self * I(1/other.hi, 1/other.lo)

    def __rtruediv__(self, other):
        return interval(other) / self

    def square(self):
        if self.lo >= 0:
            return I(self.lo*self.lo, self.hi*self.hi)
        if self.hi <= 0:
            return I(self.hi*self.hi, self.lo*self.lo)
        return I(Q(0), max(self.lo*self.lo,self.hi*self.hi))

    def certificate(self):
        return {"lower":str(self.lo), "upper":str(self.hi),
                "approximate_midpoint":float((self.lo+self.hi)/2)}


def interval(x):
    return x if isinstance(x,I) else I(Q(x),Q(x))


def sqrt_interval(x, bits=100):
    x = Q(x)
    assert x >= 0
    scale = 1 << bits
    k = isqrt((x.numerator*scale*scale)//x.denominator)
    lo, hi = Q(k,scale), Q(k+1,scale)
    assert lo*lo <= x < hi*hi
    if lo*lo == x:
        return I(lo,lo)
    return I(lo,hi)


def atan_inverse(q,n=90):
    # Alternating series at x=1/q. The next term brackets the remainder.
    total = sum((Q((-1)**k, (2*k+1)*q**(2*k+1)) for k in range(n)), Q(0))
    next_term = Q((-1)**n, (2*n+1)*q**(2*n+1))
    return I(min(total,total+next_term), max(total,total+next_term))


def sub(a,b):
    return tuple(x-y for x,y in zip(a,b))


def cross(a,b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2],
            a[0]*b[1]-a[1]*b[0])


def norm2(a):
    return sum((x*x for x in a),Q(0))


def norm(a):
    return sqrt_interval(norm2(a))


def triangle(a,b,c):
    return norm(cross(sub(b,a),sub(c,a)))/2


def main():
    # Machin's identity: pi=16 atan(1/5)-4 atan(1/239).
    pi = 16*atan_inverse(5)-4*atan_inverse(239)
    assert Q(333,106) < pi.lo < pi.hi < Q(355,113)
    target, meanwidth, projection = 1/(2*pi), pi/16, 2/(3*pi)
    assert Q(1,8) < target.lo
    assert target.hi < meanwidth.lo < meanwidth.hi < projection.lo
    mean_square = pi.square()/16
    assert Q(1,2) < mean_square.lo < mean_square.hi < Q(2,3)

    # Four noncoplanar rational configurations, with all three tours checked.
    tetrahedra = [
        [(0,0,0),(1,0,0),(0,1,0),(0,0,1)],
        [(1,0,0),(0,1,Q(1,10)),(-1,0,0),(0,-1,Q(1,10))],
        [(1,0,0),(0,1,1),(-1,0,0),(0,-1,1)],
        [(1,0,0),(0,1,3),(-1,0,0),(0,-1,3)],
    ]
    tetra_checks = 0
    for raw in tetrahedra:
        v = [tuple(map(Q,p)) for p in raw]
        area = sum((triangle(*(v[i] for i in f)) for f in combinations(range(4),3)),interval(0))
        for tail in permutations(range(1,4)):
            if tail[0] > tail[-1]:
                continue
            tour = (0,)+tail
            edges = [sub(v[tour[(i+1)%4]],v[tour[i]]) for i in range(4)]
            for i in range(4):
                e,f=edges[i],edges[(i+1)%4]
                assert norm2(cross(e,f)) <= norm2(e)*norm2(f)
            length=sum((norm(e) for e in edges),interval(0))
            assert area.hi < (length.square()/8).lo
            tetra_checks += 1
    assert tetra_checks == 12
    # Exact degenerate equality example: square side 1, L=4, doubled area=2.
    assert Q(4)**2/8 == Q(2)

    # Enumerate all unoriented Hamiltonian tours of the rational octahedron.
    h = Q(1,10)
    s,r2,d = sqrt_interval(1+h*h),sqrt_interval(2),2*sqrt_interval(h*h+Q(1,2))
    le = 2*h+2*s+3*r2
    lb = 4*s+2*r2
    area = 4*sqrt_interval(1+2*h*h)
    assert (lb-le).lo > 0
    assert (d+r2-2*s).lo > 0
    assert area.hi < (le.square()/(2*pi)).lo
    v=[(Q(1),Q(0),Q(0)),(Q(0),Q(1),Q(0)),(-Q(1),Q(0),Q(0)),
       (Q(0),-Q(1),Q(0)),(Q(0),Q(0),h),(Q(0),Q(0),-h)]
    face_sum=sum((triangle(v[p],v[i],v[(i+1)%4])
                  for p in (4,5) for i in range(4)),interval(0))
    assert face_sum.lo <= area.hi and area.lo <= face_sum.hi
    for p in (4,5):
        for i in range(4):
            assert norm2(cross(sub(v[i],v[p]),sub(v[(i+1)%4],v[p]))) == 1+2*h*h
    classes=Counter()
    min_tours=[]
    for tail in permutations(range(1,6)):
        if tail[0] > tail[-1]:
            continue
        tour=(0,)+tail
        counts=[0,0,0,0] # pole-pole, spoke, adjacent equator, opposite equator
        for a,b in zip(tour,tour[1:]+tour[:1]):
            if a>=4 and b>=4: k=0
            elif a>=4 or b>=4: k=1
            elif (a-b)%4 in (1,3): k=2
            else: k=3
            counts[k]+=1
        counts=tuple(counts)
        classes[counts]+=1
        expr=counts[0]*2*h+counts[1]*s+counts[2]*r2+counts[3]*2
        if counts==(1,2,3,0):
            min_tours.append(tour)
        else:
            assert expr.lo > le.hi
        # Boundary distance lower bound, sufficient for all cycles.
        intrinsic_lower=counts[0]*d+counts[1]*s+counts[2]*r2+counts[3]*2
        if counts!=(0,4,2,0):
            assert intrinsic_lower.lo > lb.hi
    assert sum(classes.values())==60
    assert classes==Counter({(0,4,2,0):16,(0,4,1,1):16,(0,4,0,2):4,
                             (1,2,3,0):8,(1,2,2,1):8,(1,2,1,2):8})
    assert len(min_tours)==8

    # The tree cone has identically zero face Jacobians, not merely small area.
    o=(Q(0),Q(0),Q(0))
    e=[(Q(1),Q(0),Q(0)),(Q(0),Q(1),Q(0)),(Q(0),Q(0),Q(1))]
    walk=[o,e[0],o,e[1],o,e[2],o]
    assert sum(norm2(sub(b,a)) for a,b in zip(walk,walk[1:]))==6
    for a,b in zip(walk,walk[1:]):
        assert cross(a,sub(b,a)) == o
    tree_area=(3+sqrt_interval(3))/2
    assert tree_area.lo>0
    assert tree_area.hi < (36/(2*pi)).lo

    result={
        "problem_id":7000022,
        "status":"all_exact_controls_passed",
        "arithmetic":"fractions and outward radical intervals; Machin alternating-series pi interval",
        "checks":{
            "coefficient_ordering":True,
            "projected_length_moment_obstruction":True,
            "tetrahedron_tours_checked":tetra_checks,
            "square_sharpness":True,
            "octahedron_unoriented_tours":60,
            "octahedron_minimizing_tours":8,
            "octahedron_all_minimizers_have_interior_pole_edge":True,
            "octahedron_boundary_tour_strictly_longer":True,
            "octahedron_is_not_target_counterexample":True,
            "octahedron_face_area_identity":True,
            "tree_spanning_cone_jacobians_exactly_zero":True,
            "tree_hull_area_positive":True,
            "tree_is_not_target_counterexample":True,
        },
        "octahedron_tour_classes":[{"counts":list(k),"count":classes[k]} for k in sorted(classes)],
        "certificates":{
            "pi":pi.certificate(),
            "target_coefficient":target.certificate(),
            "meanwidth_coefficient":meanwidth.certificate(),
            "projection_coefficient":projection.certificate(),
            "meanwidth_factor_over_target":(pi.square()/8).certificate(),
            "meanwidth_slack_threshold":(Q(1,4)-1/(pi*r2)).certificate(),
            "octahedron_euclidean_length":le.certificate(),
            "octahedron_boundary_length":lb.certificate(),
            "octahedron_gap":(lb-le).certificate(),
            "octahedron_area":area.certificate(),
            "octahedron_target_margin":(le.square()/(2*pi)-area).certificate(),
            "tree_hull_area":tree_area.certificate(),
        },
        "limitations":["No general n-vertex inequality is certified by enumeration.",
                       "Analytic proofs and imported classical theorems require mathematical review.",
                       "This script does not verify literature novelty or solve the full target."]
    }
    path=Path(__file__).resolve().with_name("CHECK_RESULTS.json")
    path.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":result["status"],"checks":result["checks"]},indent=2))


if __name__=="__main__":
    main()
