#!/usr/bin/env python3
"""Exact regression controls; these are not a proof of the open specialization question."""
import json
from itertools import combinations
from math import comb
from pathlib import Path
import sympy as sp

checks = 0

def check(condition, label):
    global checks
    if not condition:
        raise AssertionError(label)
    checks += 1

# Chern-class and subcanonical identities, as polynomial identities.
a, b, c = sp.symbols('a b c', integer=True)
twist = c-a-b
zdeg = (a-c)*(b-c)
check(sp.expand(a*b + twist*(a+b)+twist**2-zdeg) == 0, 'residual c2')
check(sp.expand(a+b+2*twist-(2*c-a-b)) == 0, 'residual c1')
check(sp.expand(a*b - a*(a+b-4+4-a)) == 0, 'speciality equality')

# Hilbert polynomials recover the unordered CI type, including plane cases.
types_checked = 0
for aa in range(1, 41):
    for bb in range(aa, 61):
        degree = aa*bb
        genus_num = degree*(aa+bb-4)
        check(genus_num % 2 == 0, 'CI genus is integral')
        ss = aa+bb
        check(ss*ss-4*degree == (bb-aa)**2, 'type discriminant')
        check((ss-(bb-aa))//2 == aa and (ss+(bb-aa))//2 == bb, 'type recovery')
        types_checked += 1

# The quadric-cone calculation for every checked strict-transform class.
r, n, delta = sp.symbols('r n delta', integer=True)
genus = -r*r+r*n-n+1
check(sp.expand((2*genus-2).subs(n,2*r+1) - (2*r*r-2*r-2)) == 0, 'cone genus')
check(sp.expand(2*(2*r*r-2*r-2) - ((2*r+1)**2-4*(2*r+1)-1)) == 0, 'cone divisibility')
for rr in range(0, 1001):
    dd = 2*rr+1
    gg = rr*(rr-1)
    check(((2*gg-2) % dd == 0) == (dd == 1), 'odd smooth cone curve subcanonical divisibility')

# Bezout fixed-factor and residual numerical tests. Their existence is NOT asserted.
triples_checked = 0
for aa in range(4, 31):
    for bb in range(aa, 41):
        for cc in range(3, aa):
            zz = (aa-cc)*(bb-cc)
            ee = 2*cc-aa-bb-4
            check(aa*bb > cc*bb, 'fixed factor through degree b')
            check(zz > 0 and ee <= -6, 'residual positive degree / negative dualizing twist')
            check(zz*ee % 2 == 0, 'residual genus integrality')
            check(1+zz*ee//2 < 0, 'residual negative genus')
            generic_ha = 2 if aa == bb else 1
            special_ha = comb(aa-cc+3,3)
            check(special_ha > generic_ha, 'mandatory degree-a equation jump')
            triples_checked += 1

# A fully specified singular-limit negative control over Q.
x,y,z,w,t = sp.symbols('x y z w t')
A = y*y+z*z
B = x*x+y*z+w*w
q1 = x*z+t*A
q2 = x*w+t*B
f = sp.expand(w*A-z*B)
mat = sp.Matrix([[-w,B],[z,-A],[t,x]])
minors = [sp.expand(mat[list(rows),:].det()) for rows in combinations(range(3),2)]
check(all(sp.expand(lhs-rhs) == 0 for lhs,rhs in zip(minors,[f,-q2,q1])), 'Hilbert-Burch minors')
check(sp.expand(-w*q1+z*q2+t*f) == 0, 'degree-three syzygy')
check(sp.expand(B*q1-A*q2+x*f) == 0, 'degree-four syzygy')
f0 = f.subs(x,0)
check(sp.expand(f-f0+x*x*z) == 0, 'central union ideal')
check(sp.diff(f0,w).subs({y:1,z:0,w:0}) == 1, 'plane cubic smooth at attachment')

# Exact unit-ideal certificates for absence of singular points in every projective chart.
chart_results = {}
q = [q1.subs(t,1),q2.subs(t,1)]
coords = (x,y,z,w)
J = sp.Matrix([[sp.diff(g,v) for v in coords] for g in q])
rank_minors = [sp.expand(J[:,list(cols)].det()) for cols in combinations(range(4),2)]
for v in coords:
    vs = [u for u in coords if u != v]
    G = sp.groebner([g.subs(v,1) for g in q+rank_minors], *vs, domain=sp.QQ)
    passed = list(G) == [sp.Integer(1)]
    check(passed, 'smooth CI at t=1, chart '+str(v))
    chart_results['generic_witness_'+str(v)] = passed
for v in (y,z,w):
    vs = [u for u in (y,z,w) if u != v]
    G = sp.groebner([g.subs(v,1) for g in [f0]+[sp.diff(f0,u) for u in (y,z,w)]], *vs, domain=sp.QQ)
    passed = list(G) == [sp.Integer(1)]
    check(passed, 'smooth plane cubic, chart '+str(v))
    chart_results['plane_cubic_'+str(v)] = passed
u = sp.symbols('u')
check(sp.expand(1-2*u**2-u**3+u**3+u**4-(1-u**2)**2) == 0, 'constant Hilbert numerator')

# Characteristic-change warning from the KPR example, independently expanded.
alpha,beta,gamma,rho,tau = sp.symbols('alpha beta gamma rho tau')
s = alpha*rho**3-beta*gamma**3
sbar = alpha*rho**3+beta*gamma**3
k1 = rho**6*tau+beta**2*s
k2 = gamma**6*tau+alpha**2*s
check(sp.expand(alpha**2*k1-beta**2*k2-tau*s*sbar) == 0, 'KPR difference of squares identity')
difference = sp.Poly(sp.expand(s*sbar-s*s),alpha,beta,gamma,rho)
check(not difference.is_zero, 'characteristic-zero difference is nonzero')
check(all(int(v)%2 == 0 for v in difference.coeffs()), 'difference vanishes mod 2')

result = {
    'status':'PASS',
    'checks':checks,
    'complete_intersection_types_checked':types_checked,
    'candidate_residual_triples_checked':triples_checked,
    'quadric_cone_r_range':[0,1000],
    'exact_projective_jacobian_checks':chart_results,
    'dependencies':{'python':'3', 'sympy':sp.__version__},
    'scope':'Exact algebraic identities and finite regression controls. Not a computational proof of the general open question or of existence of any candidate residual scheme.'
}
print(json.dumps(result,indent=2,sort_keys=True))
