#!/usr/bin/env python3
"""Independent polynomial, convex-membership and continuous patch-X-ray controls."""
from fractions import Fraction as Q
from math import comb
from itertools import product
from pathlib import Path
from hashlib import sha256
import json

ROOT = Path(__file__).resolve().parent
counts = {}


def ck(name, value):
    if not value:
        raise AssertionError(name)
    counts[name] = counts.get(name, 0)+1


def clean(p):
    return {k:v for k,v in p.items() if v}


def mul(p, q):
    r = {}
    for (a,b), v in p.items():
        for (c,d), w in q.items():
            key = (a+c,b+d)
            r[key] = r.get(key,0)+v*w
    return clean(r)


def add(p, q):
    r = dict(p)
    for k,v in q.items():
        r[k] = r.get(k,0)+v
    return clean(r)


def deriv(p, axis):
    out = {}
    for k,v in p.items():
        if k[axis]:
            new = list(k)
            new[axis] -= 1
            out[tuple(new)] = v*k[axis]
    return out


def ev(p, x, y):
    return sum(v*x**a*y**b for (a,b),v in p.items())


P = [(-4,2),(-3,-1),(-2,-4),(-1,3),(1,-3),(2,4),(3,1),(4,-2)]
N = [(-4,1),(-3,-2),(-2,3),(-1,-4),(1,4),(2,-3),(3,2),(4,-1)]
D = [(1,0),(0,1),(2,1),(-1,2)]
signed = {(x+4,y+4):1 for x,y in P}
signed.update({(x+4,y+4):-1 for x,y in N})
factor = {(0,0):-1}
for b in ({(1,0):1,(0,0):-1}, {(0,1):1,(0,0):-1},
          {(1,0):1,(0,2):-1}, {(2,1):1,(0,0):-1}):
    factor = mul(factor,b)
remainder = {(4,1):1,(3,4):1,(3,3):1,(3,1):1,(2,2):-1,
             (1,3):1,(1,1):1,(1,0):1,(0,3):1}
ck("signed_polynomial_factorization", mul(factor,remainder)==signed)
for a,b in D:
    projected = {}
    for (x,y),v in signed.items():
        t = a*x+b*y
        projected[t] = projected.get(t,0)+v
    ck("identically_zero_projected_polynomial", not clean(projected))

vertices = [(2,4),(-4,2),(-2,-4),(4,-2)]


def edge_cross(a,b,p):
    return (b[0]-a[0])*(p[1]-a[1])-(b[1]-a[1])*(p[0]-a[0])


def square_inside(p):
    return all(edge_cross(vertices[i],vertices[(i+1)%4],p)>=0 for i in range(4))


for p in P:
    ck("oriented_halfplane_positive_membership", square_inside(p))
for p in N:
    ck("oriented_halfplane_negative_nonmembership", not square_inside(p))
F = {p for p in product(range(-5,6),repeat=2) if square_inside(p)}
ck("independent_lattice_count", len(F)==45)
ck("support_points_disjoint", len(set(P+N))==16)

# Expand the body polynomial, then differentiate the expansion.
phi = {}
for a,b in ((1,-3),(3,1)):
    for n in (2,8):
        phi = add(phi,{(k,n-k):comb(n,k)*a**k*b**(n-k) for k in range(n+1)})
gx,gy = deriv(phi,0),deriv(phi,1)
hxx,hxy,hyy = deriv(gx,0),deriv(gx,1),deriv(gy,1)
T = 210000000
for p in P:
    ck("expanded_polynomial_positive_membership", ev(phi,*p)<T)
for p in N:
    ck("expanded_polynomial_negative_nonmembership", ev(phi,*p)>T)

for x,y in product((Q(-2),Q(-1,3),Q(0),Q(2,3),Q(3)),repeat=2):
    u,v=x-3*y,3*x+y
    Hxx,Hxy,Hyy=ev(hxx,x,y),ev(hxy,x,y),ev(hyy,x,y)
    X,Y=ev(gx,x,y),ev(gy,x,y)
    for z,w in ((Q(1),Q(0)),(Q(0),Q(1)),(Q(2,3),Q(-4,5))):
        quadratic=Hxx*z*z+2*Hxy*z*w+Hyy*w*w
        lower=20*(z*z+w*w)
        remainder=56*u**6*(z-3*w)**2+56*v**6*(3*z+w)**2
        ck("expanded_hessian_decomposition", quadratic-lower==remainder>=0)
    ck("unique_critical_point_control", (X==0 and Y==0)==(x==0 and y==0))
    if x or y:
        numerator=Hxx*Y*Y-2*Hxy*X*Y+Hyy*X*X
        ck("positive_level_curvature_numerator", numerator>0)

eps=Q(1,1000)
upper=2*(10+4*eps)**8+2*(10+4*eps)**2
lower=(11-4*eps)**8
ck("uniform_positive_margin", upper<T)
ck("uniform_negative_margin", lower>T)
for h in product((-eps,Q(0),eps),repeat=2):
    for p in P:
        ck("expanded_translated_positive", ev(phi,p[0]+h[0],p[1]+h[1])<=upper)
    for p in N:
        ck("expanded_translated_negative", ev(phi,p[0]+h[0],p[1]+h[1])>=lower)

# Directly intersect a line a*x+b*y=s with each translated open square.
# Parameter direction (-b,a) has fixed speed sqrt(a^2+b^2); cancel that common
# factor when comparing X-rays within a direction. Open parallel-edge endpoints
# are handled explicitly, rather than inferred from almost-everywhere equality.
def patch_parameter_length(a,b,s,p):
    origin=(s/a,Q(0)) if a else (Q(0),s/b)
    direction=(-b,a)
    lo=hi=None
    for o,d,c in zip(origin,direction,p):
        offset=o-c
        if not d:
            if abs(offset)>=eps:
                return Q(0)
            continue
        ends=sorted(((-eps-offset)/d,(eps-offset)/d))
        lo=ends[0] if lo is None else max(lo,ends[0])
        hi=ends[1] if hi is None else min(hi,ends[1])
    return max(Q(0),hi-lo)


for a,b in D:
    knots=sorted({a*p[0]+b*p[1]+eps*(a*s+b*t)
                  for p in P+N for s,t in product((-1,1),repeat=2)})
    probes=set(knots)
    probes.update((x+y)/2 for x,y in zip(knots,knots[1:]))
    probes.update((knots[0]-1,knots[-1]+1))
    for s in probes:
        left=sum(patch_parameter_length(a,b,s,p) for p in P)
        right=sum(patch_parameter_length(a,b,s,p) for p in N)
        ck("direct_continuous_patch_xray", left==right)

# The removed patches create an explicit segment witnessing nonconvexity of E.
for p in P:
    for sign in (-1,1):
        end=(p[0]+sign*eps,p[1])
        ck("hole_segment_endpoint_inside_body", ev(phi,*end)<T)
        ck("hole_segment_endpoint_not_removed",
           all(max(abs(end[0]-q[0]),abs(end[1]-q[1]))>=eps for q in P))

out={
    "status":"PASS",
    "artifact_sha256":sha256((ROOT/"author_replay/KNOWN_COUNTEREXAMPLE.md").read_bytes()).hexdigest(),
    "exact_assertions":sum(counts.values()),
    "families":counts,
    "scope":"Exact polynomial factorization, oriented-halfplane and expanded-Hessian controls, rational strict margins, and direct continuous patch-X-ray checks. The written finite-sum and finite-null-union arguments supply the unrestricted profile quantifiers.",
}
(ROOT/"independent_results.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
