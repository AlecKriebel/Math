#!/usr/bin/env python3
"""Deterministic exact controls. No external files or third-party packages needed.
Finite controls supplement, but do not replace, the proofs in PROOFS.md.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
from math import factorial, isqrt
import json

class I:
    def __init__(self, lo, hi=None):
        self.lo, self.hi = F(lo), F(lo if hi is None else hi)
        assert self.lo <= self.hi
    def __add__(self, b):
        b = b if isinstance(b,I) else I(b)
        return I(self.lo+b.lo,self.hi+b.hi)
    __radd__=__add__
    def __neg__(self): return I(-self.hi,-self.lo)
    def __sub__(self,b): return self+-b if isinstance(b,I) else self+(-F(b))
    def __rsub__(self,b): return I(b)+-self
    def __mul__(self,b):
        b=b if isinstance(b,I) else I(b)
        v=[x*y for x in [self.lo,self.hi] for y in [b.lo,b.hi]]
        return I(min(v),max(v))
    __rmul__=__mul__
    def __truediv__(self,b):
        b=b if isinstance(b,I) else I(b)
        assert not b.lo<=0<=b.hi
        return self*I(1/b.hi,1/b.lo)
    def sqrt(self):
        assert self.lo>=0
        scale=10**60
        lo=isqrt(self.lo.numerator*scale*scale//self.lo.denominator)
        hi=isqrt(self.hi.numerator*scale*scale//self.hi.denominator)+1
        return I(F(lo,scale),F(hi,scale))
    def public_bounds(self, digits=10):
        # Widen to simple rational decimal-scale endpoints without float conversion.
        s=10**digits
        return [str(F(self.lo.numerator*s//self.lo.denominator,s)),
                str(F(-((-self.hi.numerator*s)//self.hi.denominator),s))]

def atan(q, terms):
    vals=[(-1)**j*q**(2*j+1)/F(2*j+1) for j in range(terms+1)]
    a=sum(vals[:-1],F(0)); b=a+vals[-1]
    return I(min(a,b),max(a,b))

def point_trig(x, sine):
    # For 0<=x<=1, terms decrease; adjacent partial sums enclose sin/cos.
    assert 0<=x<=1
    vals=[F((-1)**j)*x**(2*j+int(sine))/factorial(2*j+int(sine)) for j in range(17)]
    a=sum(vals[:-1],F(0)); b=a+vals[-1]
    return I(min(a,b),max(a,b))

def sin_i(x):
    assert 0<=x.lo<=x.hi<=1
    return I(point_trig(x.lo,True).lo,point_trig(x.hi,True).hi)
def cos_i(x):
    assert 0<=x.lo<=x.hi<=1
    return I(point_trig(x.hi,False).lo,point_trig(x.lo,False).hi)

def spectra(points):
    assert len(set(points))==len(points)
    return Counter((p[0]-q[0])**2+(p[1]-q[1])**2 for p,q in combinations(points,2))

def hull(points):
    p=sorted(set(points))
    if len(p)<2:return p
    def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    def half(p):
        a=[]
        for q in p:
            while len(a)>1 and cross(a[-2],a[-1],q)<=0:a.pop()
            a.append(q)
        return a
    return half(p)[:-1]+half(p[::-1])[:-1]

def extrema_certificate():
    pi=16*atan(F(1,5),90)-4*atan(F(1,239),30)
    assert F(314159,100000)<pi.lo<pi.hi<F(314160,100000)
    alpha=pi/21
    D=2*cos_i(alpha/2);d=2*cos_i(3*alpha/2);c=cos_i(alpha)
    r=-c+(c*c+d*d-1).sqrt();delta=1-r
    inequalities={
        'r_positive':r.lo>0,'r_less_than_one':r.hi<1,'delta_positive':delta.lo>0,
        'inner_chord_exceeds_delta':(2*r*sin_i(alpha)-delta).lo>0,
        'inner_ring_patch_separation':(r-3*delta).lo>0,
        'outer_ring_patch_separation':(1-3*delta).lo>0,
        'inner_diameter_below_second':(d-r*D).lo>0,
        'second_below_diameter':(D-d).lo>0,
        'patch_diameter_below_second':(d-4*delta).lo>0,
        'all_patch_ring_distances_below_second':(d-1-2*delta).lo>0,
    }
    assert all(inequalities.values())
    H=[(i,j) for i in range(-2,3) for j in range(-2,3) if max(abs(i),abs(j),abs(i+j))<=2]
    hs=Counter((i-u)**2+(i-u)*(j-v)+(j-v)**2 for (i,j),(u,v) in combinations(H,2))
    assert len(H)==19 and min(hs)==1 and hs[1]==42
    assert all(i*i+i*j+j*j<=4 for i,j in H)
    # Exact ring index-class counts, independent of trig approximations.
    ringsteps=Counter(min((i-j)%21,(j-i)%21) for i,j in combinations(range(21),2))
    crosssteps=Counter(min((i-j)%21,(j-i)%21) for i,j in product(range(21),repeat=2))
    assert ringsteps[10]==21 and ringsteps[9]==21
    assert crosssteps[10]==42 and crosssteps[0]==21
    return {'points':61,'minimum_multiplicity':hs[1]+crosssteps[0],
            'second_largest_multiplicity':ringsteps[9]+crosssteps[10],
            'diameter_multiplicity':ringsteps[10],
            'patch_pair_count':sum(hs.values()),'patch_squared_distance_coefficients':dict(sorted(hs.items())),
            'strict_interval_checks':inequalities,
            'rational_enclosures':{k:v.public_bounds() for k,v in [('pi',pi),('r',r),('delta',delta),('D',D),('D2',d)]}}

def grid_controls():
    G=list(product(range(4),repeat=2));counts=Counter();min_sparse=10**6;counterexamples=0
    hull_tests=line_tests=0
    for n in range(5,17):
        for Q in combinations(G,n):
            a=spectra(Q);counts[n]+=1
            sparse=sum(v<=n for v in a.values());min_sparse=min(min_sparse,sparse)
            counterexamples+=sparse<2
            assert a[max(a)]<=n
            if len(a)>=n//2+1:assert sparse>=2
            # CDL's whole-set second-largest bound, with degenerate layers retained.
            h1=hull(Q);h2=hull(set(Q)-set(h1));hull_tests+=1
            bound=min(F(3,2)*(len(h1)+len(h2)),F(4,3)*len(h1)+2*len(h2),2*len(h1)+len(h2))
            assert a[sorted(a)[-2]]<=bound
            # Every row/column as a candidate line. This is a limited finite test,
            # not an exhaustive test of every possible collinear subset.
            l=max(max(Counter(q[0] for q in Q).values()),max(Counter(q[1] for q in Q).values()))
            if l>=n//2+1 or F(l)>=F(n,3)+4:
                assert sparse>=2;line_tests+=1
    assert counterexamples==0
    return {'grid':'{0,1,2,3}^2','subsets_by_cardinality':dict(counts),
            'total_subsets':sum(counts.values()),'counterexamples':counterexamples,
            'minimum_sparse_classes':min_sparse,'hull_bound_controls':hull_tests,
            'row_column_sufficient_condition_controls':line_tests}

def circle_controls():
    # Rational parametrization of a unit circle, 10 distinct vertices.
    C=[(F(1-t*t,1+t*t),F(2*t,1+t*t)) for t in range(-4,5)]+[(F(-1),F(0))]
    extras=[(F(a),F(b)) for a,b in product(range(-2,3),repeat=2) if a*a+b*b!=1]
    cases=0;center_cases=0;outside_cases=0;inside_cases=0
    for m in range(4,11):
        for Q in combinations(C,m):
            qa=spectra(Q);assert all(v<=m for v in qa.values())
            for p in extras:
                a=qa.copy()
                for q in Q:a[(p[0]-q[0])**2+(p[1]-q[1])**2]+=1
                n=m+1;assert sum(v<=n for v in a.values())>=2
                cases+=1
                rho=p[0]*p[0]+p[1]*p[1]
                center_cases+=rho==0;inside_cases+=0<rho<1;outside_cases+=rho>1
                if rho!=0:assert max(a.values())<=m+2
    # Include strictly interior noncentral outliers, not present in integer extras.
    for Q in combinations(C,6):
        for p in [(F(1,3),F(0)),(F(1,4),F(1,5))]:
            a=spectra(Q+(p,));assert sum(v<=7 for v in a.values())>=2
            cases+=1;inside_cases+=1
    return {'circle_vertices':len(C),'cases':cases,'center_cases':center_cases,
            'noncentral_interior_cases':inside_cases,'exterior_cases':outside_cases,
            'counterexamples':0}

def algebra_controls():
    count=0
    for m in range(4,1001):
        x=1+F(6,m-1);y=F(6*m,m-1)
        assert y==m*(x-1)
        assert m*(1+4*x+x*x)==6*m+y*y
        # y>(1+sqrt(x))^2 iff (y-1-x)>0 and (y-1-x)^2>4x.
        assert y-1-x>0 and (y-1-x)**2>4*x
        count+=1
    # Polynomial coefficients of m(1+4x+x^2)-6m-m^2(x-1)^2,
    # evaluated against -m(x-1)((m-1)(x-1)-6) at many exact rational inputs.
    identities=0
    for m in range(3,41):
        for x in [F(j,7) for j in range(30)]:
            assert m*(1+4*x+x*x)-6*m-m*m*(x-1)**2 == -m*(x-1)*((m-1)*(x-1)-6)
            identities+=1
    # Four-point rhombus in triangular coordinates: squared-distance ratio 1:3.
    T=[(0,0),(1,0),(0,1),(1,1)]
    a=Counter((i-u)**2+(i-u)*(j-v)+(j-v)**2 for (i,j),(u,v) in combinations(T,2))
    assert a=={1:5,3:1}
    # The counting-critical n=8 profile is a necessary arithmetic pattern,
    # not a geometrically realized example or a general result for n=8.
    assert 1+3*9==8*7//2
    return {'radial_moment_contradiction_values':count,'moment_polynomial_checks':identities,
            'n4_boundary_squared_distances':dict(a),'n8_critical_arithmetic_profile':[1,9,9,9]}

def main():
    result={'problem_id':30006556,'general_problem_solved':False,
            'independent_audit':False,'arithmetic':'exact integers and fractions; rigorous analytic enclosures',
            'extrema_obstruction':extrema_certificate(),'algebra':algebra_controls(),
            'grid':grid_controls(),'one_circle':circle_controls()}
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
