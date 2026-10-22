#!/usr/bin/env python3
"""Exact finite controls for EP-100. Python 3.10+, standard library only.
No finite test in this file certifies the general conjecture.
"""
if not __debug__:
    raise RuntimeError('Run without -O: this checker requires active assertions.')

from fractions import Fraction as F
from itertools import combinations, product
from math import isqrt
import json

class Q23:
    """Q(sqrt(2),sqrt(3)), in the basis 1,sqrt(2),sqrt(3),sqrt(6)."""
    def __init__(self, *c):
        if len(c)==1 and isinstance(c[0],Q23): self.c=c[0].c
        else: self.c=tuple(F(x) for x in c)+(F(0),)*(4-len(c))
        if len(self.c)!=4: raise ValueError('four coefficients required')
    def __add__(self,o):
        o=Q23(o); return Q23(*(a+b for a,b in zip(self.c,o.c)))
    __radd__=__add__
    def __neg__(self): return Q23(*(-x for x in self.c))
    def __sub__(self,o): return self+-Q23(o)
    def __rsub__(self,o): return Q23(o)+-self
    def __mul__(self,o):
        o=Q23(o); c=[F(0)]*4
        for i in range(4):
            for j in range(4):
                common=i&j; factor=(2 if common&1 else 1)*(3 if common&2 else 1)
                c[i^j]+=self.c[i]*o.c[j]*factor
        return Q23(*c)
    __rmul__=__mul__
    def __truediv__(self,o): return Q23(*(v/F(o) for v in self.c))
    def __pow__(self,k):
        if not isinstance(k,int) or k<0: raise ValueError('nonnegative integer exponent')
        z=Q23(1)
        for _ in range(k): z=z*self
        return z
    def __eq__(self,o): return self.c==Q23(o).c
    def __hash__(self): return hash(self.c)
    def interval(self,places=20):
        den=10**places; lo=hi=self.c[0]
        for coefficient,rad in zip(self.c[1:],(2,3,6)):
            a=isqrt(rad*den*den); left,right=F(a,den),F(a+1,den)
            assert left*left<rad<right*right
            if coefficient<0: left,right=right,left
            lo+=coefficient*left; hi+=coefficient*right
        return lo,hi
    def sign(self):
        if all(c==0 for c in self.c): return 0
        for places in (5,10,20,40,80,160):
            lo,hi=self.interval(places)
            if lo>0: return 1
            if hi<0: return -1
        raise ArithmeticError('interval inconclusive; never use a float fallback')
    def __lt__(self,o): return (self-Q23(o)).sign()<0
    def __le__(self,o): return (self-Q23(o)).sign()<=0
    def __gt__(self,o): return (self-Q23(o)).sign()>0
    def __ge__(self,o): return (self-Q23(o)).sign()>=0
    def __repr__(self): return 'Q23'+repr(self.c)

S2,S3=Q23(0,1),Q23(0,0,1)

def rational_gap_at_least_one(a,b):
    """For rational a>=b>=0, decide sqrt(a)-sqrt(b)>=1 exactly."""
    a,b=F(a),F(b)
    if not a>=b>=0: raise ValueError('ordered nonnegative radicands required')
    t=a-b-1
    return t>=0 and t*t>=4*b

def rational_configuration(points):
    pts=[tuple(map(F,p)) for p in points]
    if any(len(p)!=2 for p in pts): raise ValueError('the target is planar')
    if len(set(pts))!=len(pts): raise ValueError('points must be distinct')
    ds=sorted({sum((a-b)**2 for a,b in zip(p,q)) for p,q in combinations(pts,2)})
    admissible=(not ds or ds[0]>=1) and all(rational_gap_at_least_one(b,a) for a,b in zip(ds,ds[1:]))
    return {'admissible':admissible,'squared_distances':ds}

def piepmeyer():
    # Reconstruction of the construction credited by Erdős (1995) to Piepmeyer.
    x=(1+S2)*(S2*S3-S2)/2
    a=x*S3/3; b=a+x; c=-a-b
    U=[(Q23(1),Q23(0)),(Q23(F(-1,2)),S3/2),(Q23(F(-1,2)),-S3/2)]
    P=[(r*u,r*v) for r in (a,b,c) for u,v in U]
    assert len(set(P))==9
    lengths=[x,1+S2,2+S2,2+S2+x]
    assert (2+S3)*x==lengths[-1]
    assert 1<x and x<2
    assert 1+S2-x>1
    assert lengths[2]-lengths[1]==1
    assert lengths[3]-lengths[2]==x
    assert F(1249,1000)<x<F(1250,1000)
    assert F(4663,1000)<lengths[-1]<F(4664,1000)<5
    counts=[0]*4
    for p,q in combinations(P,2):
        square=sum(((u-v)**2 for u,v in zip(p,q)),Q23(0))
        hits=[i for i,r in enumerate(lengths) if square==r*r]
        assert len(hits)==1
        counts[hits[0]]+=1
    assert counts==[6,18,6,6]
    # The normalized gap is 1/x<1. Multiplying by x>0 is an exact certificate.
    assert x>1
    # Third circle centers agree with the defining four endpoints.
    for i in range(3):
        ci=P[6+i]; endpoints=[P[j] for j in range(6) if j%3!=i]
        sq={sum(((u-v)**2 for u,v in zip(ci,p)),Q23(0)) for p in endpoints}
        assert len(sq)==1
    return {'points':9,'pairs_checked':36,'distinct_distances':4,'multiplicities':counts,
            'minimum_distance_interval':['1249/1000','1250/1000'],
            'diameter_interval':['4663/1000','4664/1000'],
            'minimum_gap':'1','unit_minimum_rescaling_rejected':True,
            'status':'credited known construction; not an asymptotic counterexample'}

def controls():
    # Independent integer-radicand root-gap tests, with boundary and wrong-sign controls.
    root_tests=0
    for a in range(51):
        for b in range(a+1):
            # Rational squares give an independent direct comparison.
            assert rational_gap_at_least_one(a*a,b*b)==(a-b>=1)
            root_tests+=1
    assert not rational_gap_at_least_one(F(1,4),0)
    assert rational_gap_at_least_one(4,1)
    assert not rational_gap_at_least_one(2,1)
    tri=[(0,0),(3,0),(0,4)]
    assert rational_configuration(tri)['admissible']
    assert not rational_configuration([(F(x,3),F(y,3)) for x,y in tri])['admissible']
    assert rational_configuration([(i,0) for i in range(21)])['admissible']
    assert not rational_configuration([(0,0),(1,0),(0,1),(1,1)])['admissible']
    for bad in [[(0,0),(0,0)],[(0,0,0),(1,0,0)]]:
        try: rational_configuration(bad)
        except ValueError: pass
        else: raise AssertionError('bad geometry accepted')
    # Every subset of the safely scaled 3 by 3 grid.
    base=list(product(range(0,17,8),repeat=2)); subsets=0
    for mask in range(1<<9):
        P=[p for i,p in enumerate(base) if mask>>i&1]
        assert rational_configuration(P)['admissible']; subsets+=1
    # General grid family represented by its exactly enumerated displacement spectrum.
    grid_count=0; gap_count=0
    for size in range(2,51):
        a=size-1; scale=4*a
        qs=sorted({scale*scale*(u*u+v*v) for u in range(size) for v in range(size) if u or v})
        assert qs[0]>=1 and qs[-1]==32*a**4
        for q,r in zip(qs,qs[1:]):
            assert rational_gap_at_least_one(r,q);gap_count+=1
        # The specific near-horizontal gap forces any valid scale >2a.
        assert (a*a+1)-a*a==1
        assert rational_gap_at_least_one((2*a)**2*(a*a+1),(2*a)**2*a*a) is False
        grid_count+=1
    # Separated spectra: each radius has <=2 floor(m)+1 neighbours within m.
    spectrum_cases=0
    for gaps in product((F(1),F(3,2),F(2)),repeat=5):
        S=[F(1)]
        for gap in gaps:S.append(S[-1]+gap)
        assert len(S)<=int(S[-1])
        for m in (F(1),F(3,2),F(2),F(7,3),F(3)):
            for r in S:
                assert sum(abs(r-s)<=m for s in S)<=2*(m.numerator//m.denominator)+1
                spectrum_cases+=1
    # Unit-pair geometry for independently enumerated rational points:
    # distance difference in {0,1,-1} => baseline or perpendicular bisector.
    geometry_cases=0
    for den in (1,2,3):
        for ix,iy in product(range(-12,13),repeat=2):
            x,y=F(ix,den),F(iy,den); r2=x*x+y*y; s2=(x-1)**2+y*y
            delta_one=(r2-s2-1)**2==4*s2 and r2-s2-1>=0
            delta_minus=(s2-r2-1)**2==4*r2 and s2-r2-1>=0
            if r2==s2 or delta_one or delta_minus:
                assert y==0 or x==F(1,2)
            geometry_cases+=1
    # Q23 operations and ordering controls are exact; distinguish coefficients.
    assert S2*S2==2 and S3*S3==3 and (S2*S3)**2==6
    assert (S2-1)*(S2+1)==1 and Q23().sign()==0
    assert Q23(-1)<0 and S2>1 and S3>S2
    return {'passed':True,'radical_gap_square_controls':root_tests,
            'scaled_grid_subsets':subsets,'grid_family_sizes':grid_count,
            'grid_spectrum_adjacent_gaps':gap_count,'radius_neighbour_controls':spectrum_cases,
            'unit_pair_coordinate_controls':geometry_cases,
            'normalization_3_4_5_rejected':True,'unscaled_unit_square_rejected':True,
            'duplicate_points_rejected':True,'wrong_dimension_rejected':True,
            'piepmeyer':piepmeyer(),
            'scope':'Exact finite controls and a complete nine-point reconstruction; general conjecture unresolved.'}

if __name__=='__main__': print(json.dumps(controls(),indent=2,sort_keys=True))
