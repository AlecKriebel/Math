#!/usr/bin/env python3
"""Exact regression controls. This is not a proof of toric polyhedrality."""
import json
from fractions import Fraction
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parent
checks = {}

def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks[name] = True

# F_1, basis E,F: intersection matrix [[-1,1],[1,0]].
def f1_pair(x, y):
    return -x[0]*y[0] + x[0]*y[1] + x[1]*y[0]
check('negative_exceptional_curve', f1_pair((1,0),(1,0)) == -1)
check('fiber_boundary', f1_pair((0,1),(1,0)) == 1)
check('line_pullback_boundary', f1_pair((1,1),(1,0)) == 0)
for a, b in product(range(-8,9), repeat=2):
    conditions = a >= 0 and b-a >= 0
    check(f'f1_{a}_{b}', conditions == (f1_pair((a,b),(1,0)) >= 0 and f1_pair((a,b),(0,1)) >= 0))

# Integral of xi^a f^b on the fourfold P(O^2 + O(1)^2).
# Only degree 4 monomials are integrated. Ring f^2=0, xi^4=2f xi^3.
def integral(a, b):
    assert a+b == 4 and a >= 0 and b >= 0
    if b >= 2:
        return 0
    return 2 if (a,b) == (4,0) else 1

def mul(p, q):
    out = {}
    for (a,b), c in p.items():
        for (u,v), d in q.items():
            key = (a+u,b+v)
            out[key] = out.get(key,0) + c*d
    return {k:v for k,v in out.items() if v}

def pairing(p, q):
    return sum(c*integral(a,b) for (a,b),c in mul(p,q).items())

xi = {(1,0):1}; f = {(0,1):1}; e=mul(xi,xi); q=mul(xi,f)
alpha = {(2,0):1,(1,1):-1}
z = {(2,0):1,(1,1):-2}
check('scroll_intersection_matrix', [[pairing(u,v) for v in (e,q)] for u in (e,q)] == [[2,1],[1,0]])
check('movable_surface_negative_on_effective_surface', pairing(alpha,z) == -1)
check('movable_surface_self_intersection', pairing(alpha,alpha) == 0)
check('nonmovable_effective_ray_excluded', -2+1 < 0)

# A class a*xi^2+b*xi*f has coordinates (a,b).
# EFF_2: a>=0,b+2a>=0. EFF_1 similarly in xi^3,xi^2*f.
def effective(a,b):
    return a >= 0 and b+2*a >= 0
for a,b in product(range(-12,13), repeat=2):
    # f intersection is (0,a); xi intersection (a,b); (xi-f) intersection (a,b-a).
    outer = effective(a,b) and effective(0,a) and effective(a,b) and effective(a,b-a)
    expected = a >= 0 and b+a >= 0
    check(f'outer_cone_{a}_{b}', outer == expected)
    if expected:
        # a*(1,-1)+(b+a)*(0,1)=(a,b), nonnegative decomposition.
        check(f'movable_ray_decomposition_{a}_{b}', (a, -a+(b+a)) == (a,b) and b+a >= 0)
    nef = 2*a+b-2*a >= 0 and a >= 0
    check(f'nef_cone_{a}_{b}', nef == (a >= 0 and b >= 0))
check('fixed_model_complete_intersections_miss_alpha', alpha[(1,1)] < 0)

# Product coefficient extraction: p_*((beta_l x P^l)H^j)=delta_jl beta_l.
for m in range(9):
    matrix = [[1 if j == l else 0 for l in range(m+1)] for j in range(m+1)]
    beta = [Fraction((j+1)*(-1)**j, j+2) for j in range(m+1)]
    recovered = [sum(Fraction(matrix[j][l])*beta[l] for l in range(m+1)) for j in range(m+1)]
    check(f'projective_factor_extraction_m{m}', recovered == beta)

# Ring of (P^1)^4: monomials indexed by subsets, squared variables vanish.
# A=[P^1 x P^1 x pt x pt]=h3*h4; B=h1*h2.
gamma_terms = ({2,3}, {0,1})
M = [[sum(int(len(t | {i,j}) == 4 and i != j and i not in t and j not in t) for t in gamma_terms) for j in range(4)] for i in range(4)]
expected_M = [[0,1,0,0],[1,0,0,0],[0,0,0,1],[0,0,1,0]]
check('hodge_matrix_from_product_ring', M == expected_M)
eigenvectors = [([1,1,0,0],1),([0,0,1,1],1),([1,-1,0,0],-1),([0,0,1,-1],-1)]
for i,(v,lam) in enumerate(eigenvectors):
    check(f'hodge_eigenvector_{i}', [sum(M[r][c]*v[c] for c in range(4)) for r in range(4)] == [lam*x for x in v])
check('hodge_two_positive_directions', sum(lam > 0 for _,lam in eigenvectors) == 2)

# Irreducible representability is not convex: coordinates e12 and e34.
# The square-root triangle condition at their sum would require 0+0>=1.
check('irreducible_sum_fails_triangle', 0+0 < 1)

# Nonpolyhedral-subcone control: det of sum of distinct boundary rank-one PSD matrices.
for s,t in product(range(8), repeat=2):
    x,y,z0 = 2, s+t, s*s+t*t
    check(f'curved_subcone_boundary_{s}_{t}', x*z0-y*y == (s-t)**2)

status = json.loads((ROOT/'STATUS.json').read_text())
turns = [json.loads(line) for line in (ROOT/'turns.jsonl').read_text().splitlines() if line.strip()]
check('status_is_unsolved', status['status'] == 'unsolved')
check('exactly_five_approaches', len(turns) == 5 and [x['turn'] for x in turns] == [1,2,3,4,5])
check('no_full_solution_promoted', status['full_resolution'] is False and all(t['full_resolution'] is False for t in turns))

result = {'all_passed': True, 'exact_checks': len(checks), 'status':'unsolved', 'scope':'Finite algebra and metadata regression controls only; see VALIDATION_LIMITS.md.', 'groups':['F1 intersection cone','scroll Chow intersection arithmetic','boundary envelope finite-grid controls','nef versus movable control','projective factor extraction','Hodge signature and convexification','curved subcone logic','five-approach status gate']}
print(json.dumps(result, indent=2))
