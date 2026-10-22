#!/usr/bin/env python3
"""Exact algebra controls for PROOF.md; no global symplectic classification claim."""
import itertools
import json
from fractions import Fraction as Q

COUNTS = {}
def check(name, condition):
    if not condition:
        raise AssertionError(name)
    COUNTS[name] = COUNTS.get(name, 0) + 1

PAIRS = list(itertools.combinations(range(4), 2))
def matrix(form):
    m = [[Q(0) for _ in range(4)] for _ in range(4)]
    for (i,j), v in zip(PAIRS,form):
        m[i][j],m[j][i] = Q(v),-Q(v)
    return m

def coefficients(m):
    return tuple(m[i][j] for i,j in PAIRS)

def wedge(a,b):
    # Coefficient of dx0 dx1 dx2 dx3 in the wedge of two 2-forms.
    return (a[0]*b[5]+a[5]*b[0]-a[1]*b[4]-a[4]*b[1]
            +a[2]*b[3]+a[3]*b[2])

def pfaffian(a):
    return a[0]*a[5]-a[1]*a[4]+a[2]*a[3]

def determinant(m):
    out = Q(0)
    for p in itertools.permutations(range(4)):
        inversions = sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))
        term = Q((-1)**inversions)
        for i in range(4):
            term *= m[i][p[i]]
        out += term
    return out

def pullback(f,m):
    return [[sum(f[k][i]*m[k][l]*f[l][j] for k in range(4) for l in range(4))
             for j in range(4)] for i in range(4)]

def mix(a,b,t):
    return tuple((1-t)*x+t*y for x,y in zip(a,b))

def dot(a,b):
    return sum(x*y for x,y in zip(a,b))

def cross(a,b):
    return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])

# Complete exact minimum test on [0,1], independent of the proposed square-root test.
for A in range(1,11):
    for C in range(1,11):
        for B in range(-15,16):
            D = A-2*B+C
            candidates = [Q(A),Q(C)]
            if D>0:
                t = Q(A-B,D)
                if 0<t<1:
                    candidates.append(A*(1-t)**2+2*B*t*(1-t)+C*t*t)
            direct = min(candidates)>0
            criterion = B>=0 or A*C>B*B
            check('affine_criterion_exact_minimum', direct==criterion)

for a in itertools.product(range(-1,2), repeat=6):
    check('pfaffian_determinant', determinant(matrix(a))==pfaffian(a)**2)
    check('wedge_square_pfaffian', wedge(a,a)==2*pfaffian(a))

# Independent matrix pullbacks by rotations in the (y1,y2)-plane.
w = (Q(1),Q(0),Q(0),Q(0),Q(0),Q(1))
for u in range(-10,11):
    c,s = Q(1-u*u,1+u*u),Q(2*u,1+u*u)
    F = [[Q(int(i==j)) for j in range(4)] for i in range(4)]
    F[1][1],F[1][3],F[3][1],F[3][3] = c,-s,s,c
    beta = coefficients(pullback(F,matrix(w)))
    check('rotation_orientation',determinant(F)==1)
    check('rotation_pullback_formula',beta==(c,0,-s,-s,0,c))
    check('rotation_wedge_square',wedge(beta,beta)==2)
    check('rotation_cross_wedge',wedge(w,beta)==2*c)
    for k in range(11):
        t = Q(k,10)
        q = 2*((1-t)**2+2*c*t*(1-t)+t*t)
        check('rotation_segment_identity',wedge(mix(w,beta,t),mix(w,beta,t))==q)
        check('rotation_segment_nondegenerate',q>0)

F = [[Q(int(i==j))*(1 if i in (0,2) else -1) for j in range(4)] for i in range(4)]
beta = coefficients(pullback(F,matrix(w)))
check('half_turn_orientation',determinant(F)==1)
check('half_turn_antisymplectic',beta==tuple(-x for x in w))
check('half_turn_midpoint_zero',mix(w,beta,Q(1,2))==(0,)*6)
check('half_turn_endpoint_nondegenerate',wedge(beta,beta)>0)
check('equality_case_rejected',not (Q(-2)>=0 or Q(2)*Q(2)>Q(-2)**2))
check('strict_failure_detected',Q(1,4)+2*Q(-2)*Q(1,4)+Q(1,4)<0)

# T3-invariant forms: verify the wedge identity and large zero-mean perturbations.
def torus_form(a,b):
    return (a[0],a[1],a[2],b[2],-b[1],b[0])
for a in itertools.product(range(-2,3), repeat=3):
    for b in itertools.product(range(-1,2), repeat=3):
        z=torus_form(a,b)
        check('torus_wedge_identity',wedge(z,z)==2*dot(a,b))

for b in itertools.product(range(-1,2),repeat=3):
    if b==(0,0,0):
        continue
    p = cross(b,(3,-2,5))
    q = cross(b,(-4,7,1))
    for u in range(-4,5):
        sin,cos=Q(2*u,1+u*u),Q(1-u*u,1+u*u)
        a=tuple(b[i]+sin*p[i]+cos*q[i] for i in range(3))
        for k in range(6):
            s=Q(k,5)
            v=tuple((1-s)*a[i]+s*b[i] for i in range(3))
            check('torus_periodic_family_positivity',dot(v,b)==dot(b,b)>0)
            check('torus_periodic_family_wedge',wedge(torus_form(v,b),torus_form(v,b))==2*dot(b,b))

# Concrete coordinate-shear instance of a pullback family and composition order.
Fs=[]
for u in range(-2,3):
    f=[[Q(int(i==j)) for j in range(4)] for i in range(4)]
    f[1][0]=Q(u)
    f[2][0]=Q(2*u)
    Fs.append((u,f))
for i,fi in Fs:
    for j,fj in Fs:
        h=[[Q(int(k==l)) for l in range(4)] for k in range(4)]
        h[1][0]=Q(i-j)
        h[2][0]=Q(2*(i-j))
        check('pullback_composition_order',pullback(h,pullback(fj,matrix(w)))==pullback(fi,matrix(w)))

# Volume algebra only: the positive bump integral and surface area are variables.
for area in range(1,6):
    for bump in range(1,6):
        for eps in [Q(1,10),Q(1,2),Q(1)]:
            delta=eps*area*bump
            check('relative_volume_strictness',delta>0)

result = {
    'all_checks_passed': True,
    'assertions': sum(COUNTS.values()),
    'groups': COUNTS,
    'scope': 'Exact rational and exterior-algebra controls only. No numerical check resolves KP-4.96.',
    'unresolved_closed_target': True,
}
print(json.dumps(result,indent=2,sort_keys=True))
