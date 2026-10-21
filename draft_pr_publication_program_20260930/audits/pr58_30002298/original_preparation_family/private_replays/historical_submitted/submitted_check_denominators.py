#!/usr/bin/env python3
"""Exact controls for the credited Fantappie/algebraic-vertex characterization.

Uses SymPy. This checks finite rational identities and geometric examples;
it does not replace the published general polyhedral valuation theorem.
"""
from collections import Counter
from itertools import product
from pathlib import Path
import json
import sys
import sympy as s

counts = Counter()
cases = []

def check(condition, category):
    assert bool(condition), category
    counts[category] += 1

def dot(v, u):
    return sum(a*b for a, b in zip(v, u))

def transformed(simplices, d):
    u = s.symbols('u0:' + str(d))
    terms = []
    cone = {}
    for simplex in simplices:
        origin = s.Matrix(simplex[0])
        det = abs(s.det(s.Matrix.hstack(
            *(s.Matrix(v)-origin for v in simplex[1:]))))
        check(det > 0, 'nondegenerate_simplex')
        terms.append(det/s.prod(1-dot(v, u) for v in simplex))
        for v in simplex:
            edges = [tuple(b-a for a, b in zip(v, w))
                     for w in simplex if w != v]
            coefficient = (-1)**d * det/s.prod(dot(w, u) for w in edges)
            cone[v] = cone.get(v, 0) + coefficient
    F = s.cancel(sum(terms))
    cone = {v: s.cancel(c) for v, c in cone.items()}
    check(s.cancel(F-sum(c/(1-dot(v, u)) for v, c in cone.items())) == 0,
          'simplex_to_cone_identity')
    numerator, denominator = s.fraction(F)
    constant = denominator.subs(dict.fromkeys(u, 0))
    check(constant != 0, 'denominator_regular_at_zero')
    omega = s.expand(denominator/constant)
    surviving = []
    for v, c in cone.items():
        if all(a == 0 for a in v):
            check(1-dot(v, u) == 1, 'origin_factor_is_a_unit')
            continue
        L = 1-dot(v, u)
        appears = s.rem(s.Poly(omega, *u), s.Poly(L, *u)).is_zero
        check(appears == (c != 0), 'pole_matches_tangent_coefficient')
        j = next(i for i, a in enumerate(v) if a)
        substitution = (s.Integer(1)-sum(v[i]*u[i] for i in range(d) if i != j))/v[j]
        restriction = s.cancel(c.subs(u[j], substitution))
        check((restriction != 0) == (c != 0), 'homogeneous_residue_restriction')
        if appears:
            surviving.append(v)
            check(s.gcd(s.Poly(omega, *u), s.Poly(L**2, *u)).total_degree() == 1,
                  'simple_pole_multiplicity')
    predicted = s.prod(1-dot(v, u) for v in surviving)
    check(s.expand(omega-predicted) == 0, 'complete_reduced_denominator')
    check(s.gcd(s.Poly(numerator, *u), s.Poly(denominator, *u)).total_degree() == 0,
          'coprime_reduced_fraction')
    return u, F, cone, omega

def run(name, simplices, d, expected_vertices):
    print('Checking ' + name, file=sys.stderr, flush=True)
    u, F, cone, omega = transformed(simplices, d)
    nonzero = [v for v in expected_vertices if any(v)]
    expected = s.prod(1-dot(v, u) for v in nonzero)
    check(s.expand(omega-expected) == 0, 'expected_geometric_denominator')
    cases.append({'name': name, 'dimension': d, 'simplices': len(simplices),
                  'triangulation_vertices': len(cone),
                  'nonzero_pole_vertices': len(nonzero)})
    return u, F, cone, omega

for d in (1, 2, 3):
    for shift in (tuple(0 for _ in range(d)), tuple(i+2 for i in range(d))):
        simplex = [shift] + [tuple(shift[j]+int(i == j) for j in range(d))
                             for i in range(d)]
        run('simplex_'+str(d)+'_'+str(shift), [simplex], d, simplex)

# A convex square with an artificial center vertex in its triangulation.
square = [(1, 1), (3, 1), (3, 3), (1, 3)]
center = (2, 2)
triangles = [[center, square[i], square[(i+1) % 4]] for i in range(4)]
_, _, cone, _ = run('square_with_Steiner_center', triangles, 2, square)
check(cone[center] == 0, 'artificial_vertex_cancels')

# Three unit squares form an L-shaped polygon. Straight-edge subdivision
# points cancel, while the reentrant corner remains a pole vertex.
triangles = []
for x, y in ((2, 3), (3, 3), (2, 4)):
    a, b, c, d = (x, y), (x+1, y), (x+1, y+1), (x, y+1)
    triangles.extend([[a, b, c], [a, c, d]])
boundary = [(2, 3), (4, 3), (4, 4), (3, 4), (3, 5), (2, 5)]
_, _, cone, _ = run('nonconvex_L_shape', triangles, 2, boundary)
check(cone[(3, 4)] != 0, 'reentrant_vertex_survives')

# Opposite simplices: the common-apex tangent coefficient cancels exactly
# in odd dimensions. Dimension 3 is the original source's example.
for d in (1, 2, 3):
    for shift in (tuple(0 for _ in range(d)), tuple(i+2 for i in range(d))):
        plus = [shift] + [tuple(shift[j]+int(i == j) for j in range(d))
                         for i in range(d)]
        minus = [shift] + [tuple(shift[j]-int(i == j) for j in range(d))
                          for i in range(d)]
        expected = plus[1:] + minus[1:] + ([] if d % 2 else [shift])
        u, F, cone, omega = run('opposite_'+str(d)+'_'+str(shift),
                                [plus, minus], d, expected)
        check((cone[shift] == 0) == bool(d % 2), 'opposite_cone_parity')
        if d == 3:
            L = 1-dot(shift, u)
            explicit = 2*(L**2+sum(u[i]*u[j] for i in range(3)
                                  for j in range(i+1, 3)))/s.prod(L**2-x*x for x in u)
            check(s.cancel(F-explicit) == 0, 'source_tetrahedra_formula')
            vertex_product = s.prod(1-dot(v, u) for v in set(plus+minus))
            check((s.expand(omega-vertex_product) == 0) == (not any(shift)),
                  'literal_origin_exception')

# A signed line-cone decomposition of positive plus negative orthants in R^3.
# Each proper subset of coordinate halfspaces is invariant in a missing direction.
for signs in product((0, 1), repeat=3):
    h1, h2, h3 = signs
    lhs = h1*h2*h3 + (1-h1)*(1-h2)*(1-h3)
    rhs = 1-h1-h2-h3+h1*h2+h1*h3+h2*h3
    check(lhs == rhs, 'signed_line_cone_indicator_identity')

result = {'status': 'PASS', 'exact_assertions': sum(counts.values()),
          'sympy_version': s.__version__, 'categories': dict(counts), 'cases': cases,
          'scope': 'Finite exact diagnostics; the general characterization is credited to published work.'}
Path(__file__).with_name('check_results.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
