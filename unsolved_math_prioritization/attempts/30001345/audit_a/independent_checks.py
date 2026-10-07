#!/usr/bin/env python3
"""Exact, independent checks for the displayed nine-line deformation.
Uses only Python's standard library; calculations lie in Q[w]/(w^2+w+1).
The analytic flatness, normalization and boundary proofs are in AUDIT.md.
"""
from fractions import Fraction as Q
from itertools import combinations
from collections import Counter
import json

class K:
    __slots__ = ('a', 'b')
    def __init__(self, a=0, b=0):
        self.a, self.b = Q(a), Q(b)
    @staticmethod
    def coerce(x):
        return x if isinstance(x, K) else K(x)
    def __add__(self, other):
        z = K.coerce(other); return K(self.a+z.a, self.b+z.b)
    __radd__ = __add__
    def __neg__(self): return K(-self.a, -self.b)
    def __sub__(self, other): return self + -K.coerce(other)
    def __rsub__(self, other): return K.coerce(other) + -self
    def __mul__(self, other):
        z = K.coerce(other)
        return K(self.a*z.a-self.b*z.b,
                 self.a*z.b+self.b*z.a-self.b*z.b)
    __rmul__ = __mul__
    def conjugate(self): return K(self.a-self.b, -self.b)
    def norm(self): return self.a*self.a-self.a*self.b+self.b*self.b
    def inv(self):
        assert self
        n = self.norm(); c = self.conjugate()
        return K(c.a/n, c.b/n)
    def __truediv__(self, other): return self*K.coerce(other).inv()
    def __rtruediv__(self, other): return K.coerce(other)*self.inv()
    def __bool__(self): return bool(self.a or self.b)
    def __eq__(self, other):
        z = K.coerce(other); return self.a == z.a and self.b == z.b
    def __hash__(self): return hash((self.a, self.b))
    def __pow__(self, n):
        assert isinstance(n, int) and n >= 0
        value = K(1)
        for _ in range(n): value *= self
        return value
    def encode(self): return [str(self.a), str(self.b)]

one, zero, w = K(1), K(), K(0,1)
roots = (one, w, w*w)
assert w*w+w+one == 0 and w**3 == 1
assert len(set(roots)) == 3
for z in [K(a,b) for a in range(-3,4) for b in range(-3,4) if a or b]:
    assert z*z.inv() == 1 and z*z.conjugate() == z.norm()

def dot(a,b): return sum((x*y for x,y in zip(a,b)), zero)
def cross(a,b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2],
            a[0]*b[1]-a[1]*b[0])
def proj(p):
    first = next(x for x in p if x)
    return tuple(x/first for x in p)

lines = [(one,-z,zero) for z in roots]
lines += [(zero,one,-z) for z in roots]
lines += [(-z,zero,one) for z in roots]
assert len(set(map(proj, lines))) == 9
pair_points = [proj(cross(a,b)) for a,b in combinations(lines,2)]
points = set(pair_points)
assert len(pair_points) == 36 and len(points) == 12
assert Counter(Counter(pair_points).values()) == {3:12}
assert Counter(sum(not dot(l,p) for l in lines) for p in points) == {3:12}
expected = {proj((one,zero,zero)), proj((zero,one,zero)),
            proj((zero,zero,one))}
expected |= {proj((a,b,one)) for a in roots for b in roots}
assert points == expected
ell = (one, K(2), K(4))
assert all(dot(ell,p) for p in points)
affine = {tuple(c/dot(ell,p) for c in p[:2]) for p in points}
assert len(affine) == 12
# Every singular point lies within sqrt(2)|t| after scaling by t.
assert all(x.norm()+y.norm() <= 2 for x,y in affine)

# For each projective form aX+bY+cZ, substitute 4Z=t-x-2y.
family_lines = [(4*a-c,4*b-2*c,c) for a,b,c in lines]
# Directions are constant in t; none are parallel or coincident.
assert all(a[0]*b[1]-a[1]*b[0] for a,b in combinations(family_lines,2))
assert all(sum(not(a*x+b*y+c) for a,b,c in family_lines)==3 for x,y in affine)
assert all(any(not(a*x+b*y+c) for x,y in affine) for a,b,c in family_lines)
# Full quadratic and cubic jets at each point: constant, linear and quadratic
# vanish; homogeneous cubic is a nonzero scalar times three distinct forms.
for p in affine:
    zeros = [l for l in family_lines if not (l[0]*p[0]+l[1]*p[1]+l[2])]
    nonzeros = [l for l in family_lines if l not in zeros]
    assert len(zeros)==3 and len(nonzeros)==6
    scalar = one
    for a,b,c in nonzeros: scalar *= a*p[0]+b*p[1]+c
    assert scalar
    assert all(a[0]*b[1]-a[1]*b[0] for a,b in combinations(zeros,2))

# Sparse polynomial arithmetic in x,y,t over Q(w).
def pmul(p,q):
    result={}
    for e,c in p.items():
        for f,d in q.items():
            k=tuple(e[i]+f[i] for i in range(3))
            result[k]=result.get(k,zero)+c*d
    return {k:v for k,v in result.items() if v}
def padd(p,q):
    result=dict(p)
    for e,c in q.items(): result[e]=result.get(e,zero)+c
    return {k:v for k,v in result.items() if v}
def scale(p,a): return {e:c*a for e,c in p.items() if c*a}
def power(p,n):
    result={(0,0,0):one}
    for _ in range(n): result=pmul(result,p)
    return result
X={(1,0,0):one}; Y={(0,1,0):one}; T={(0,0,1):one}
S=padd(padd(T,scale(X,-1)),scale(Y,-2))
F=pmul(pmul(padd(power(X,3),scale(power(Y,3),-1)),
                 padd(scale(power(Y,3),64),scale(power(S,3),-1))),
                 padd(power(S,3),scale(power(X,3),-64)))
product={(0,0,0):one}
for a,b,c in family_lines:
    product=pmul(product,{(1,0,0):a,(0,1,0):b,(0,0,1):c})
# The first three forms were multiplied by 4; other factors give the displayed F.
assert product == scale(F,64)
assert F[(9,0,0)] == -65
assert all(c.b==0 for c in F.values())
assert all(sum(e)==9 for e in F)

out={
 'field':'Q[w]/(w^2+w+1)',
 'projective_lines':len(lines),
 'line_pairs':len(pair_points),
 'distinct_projective_intersections':len(points),
 'point_multiplicity_histogram':{'3':12},
 'pairwise_direction_determinants_nonzero':36,
 'chart_avoids_all_intersections':True,
 'affine_singularity_norm_squared_upper_bound':2,
 'exact_family_product_matches_displayed_polynomial':True,
 'x_degree':9,
 'x_leading_coefficient':-65,
 'central_delta':9*8//2,
 'nearby_delta':12*(3*2//2),
 'central_rough_M':9-2,
 'nearby_rough_M':12*(3-2),
 'nearby_minus_central_rough_M':12-7,
 'all_assertions_passed':True
}
print(json.dumps(out,indent=2))
