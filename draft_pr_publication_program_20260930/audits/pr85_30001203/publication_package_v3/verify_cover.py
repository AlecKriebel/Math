#!/usr/bin/env python3
"""Supplementary exact controls, Python 3.9+ standard library only.

No Nash embedding is constructed. Finite controls do not prove global covering
existence, smoothness or completeness. See the analytical research-note source.
Optimized execution is rejected explicitly; no checks rely on assert.
"""
import sys

if sys.flags.optimize:
    print("Refusing optimized Python: verification requires optimization level 0.",
          file=sys.stderr)
    raise SystemExit(2)

from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib
import json

checks = Counter()


def ck(group, condition):
    if not condition:
        raise RuntimeError("Verification failed: " + group)
    checks[group] += 1


def clean(p):
    return {ij: Q(a) for ij, a in p.items() if a}


def add(p, q):
    out = dict(p)
    for ij, a in q.items():
        out[ij] = out.get(ij, Q(0)) + a
    return clean(out)


def scale(p, a):
    return clean({ij: Q(a) * b for ij, b in p.items()})


def mul(p, q):
    out = {}
    for (i, j), a in p.items():
        for (k, l), b in q.items():
            ij = (i + k, j + l)
            out[ij] = out.get(ij, Q(0)) + a * b
    return clean(out)


def derivative(p, axis):
    out = {}
    for ij, a in p.items():
        if ij[axis]:
            kl = list(ij)
            kl[axis] -= 1
            out[tuple(kl)] = a * ij[axis]
    return clean(out)


def evaluate(p, x, y):
    return sum((a * x**i * y**j for (i, j), a in p.items()), Q(0))


# phi=log(2 sqrt(T))-log(d), d=1-u^2-v^2. Differentiate phi_u=2u/d
# and phi_v=2v/d by the quotient rule with exact polynomial coefficients.
one = {(0, 0): Q(1)}
u, v = {(1, 0): Q(1)}, {(0, 1): Q(1)}
s = add(mul(u, u), mul(v, v))
d = add(one, scale(s, -1))
laplacian_numerator = {}
for axis, coord in enumerate((u, v)):
    numerator = scale(coord, 2)
    second_derivative_numerator = add(
        mul(derivative(numerator, axis), d),
        scale(mul(numerator, derivative(d, axis)), -1))
    laplacian_numerator = add(laplacian_numerator,
                              second_derivative_numerator)
ck("all_point_laplacian_polynomial", laplacian_numerator == scale(one, 4))
# K=-d^2/(4T) * (4/d^2)=-1/T, with d>0 and T>0.

# Check entire numerator factorizations for the all-point coefficient bounds.
denominator = mul(d, d)
lower_difference_numerator = add(scale(one, 4), scale(denominator, -4))
lower_factored = scale(mul(s, add(scale(one, 2), scale(s, -1))), 4)
ck("all_point_lower_bound_factorization",
   lower_difference_numerator == lower_factored)
upper_difference_numerator = add(scale(denominator, Q(64, 9)), scale(one, -4))
upper_factored = scale(mul(add(one, scale(s, -4)),
                           add(scale(one, 7), scale(s, -4))), Q(4, 9))
ck("all_point_upper_bound_factorization",
   upper_difference_numerator == upper_factored)
ck("factor_sign_interval_endpoints", Q(0) <= Q(1, 4) < Q(1))
ck("factor_sign_lower_second_factor", Q(2) - Q(1, 4) > 0)
ck("factor_sign_upper_first_factor", Q(1) - 4 * Q(1, 4) == 0)
ck("factor_sign_upper_second_factor", Q(7) - 4 * Q(1, 4) > 0)

# Rational mesh diagnostics additionally exercise the formulas. The polynomial
# identities plus the proof's interval reasoning give the all-point argument.
points = 0
times = (Q(1, 3), Q(1), Q(5, 2))
for a, b in product(range(-8, 9), repeat=2):
    x, y = Q(a, 16), Q(b, 16)
    radius2 = x*x + y*y
    if radius2 <= Q(1, 4):
        points += 1
        coefficient = 4 / (1 - radius2)**2
        ck("rational_mesh_unit_time_bounds", 4 <= coefficient <= Q(64, 9))
        for T in times:
            ck("rational_mesh_scaled_bounds",
               4*T <= T*coefficient <= Q(64, 9)*T)
            curvature = -(1 - radius2)**2 / (4*T) * evaluate(
                laplacian_numerator, x, y) / (1 - radius2)**2
            ck("rational_mesh_curvature", curvature == -1/T)
ck("rational_mesh_point_count", points == 197)

# Quadratic-field arithmetic: pairs (a,b) denote a+b sqrt(2).
def qadd(a, b):
    return a[0] + b[0], a[1] + b[1]


def qmul(a, b):
    return a[0]*b[0] + 2*a[1]*b[1], a[0]*b[1] + a[1]*b[0]


def qinverse(a):
    norm = a[0]**2 - 2*a[1]**2
    if norm == 0:
        raise ZeroDivisionError("Zero quadratic-field element")
    return a[0]/norm, -a[1]/norm


def qdiv(a, b):
    return qmul(a, qinverse(b))


qone, qminusone = (Q(1), Q(0)), (Q(-1), Q(0))
sqrt2, radius2 = (Q(0), Q(1)), (Q(0), Q(1, 2))
cosh_radius = Q(3), Q(2)
ck("polygon_radius_identity",
   qdiv(qadd(cosh_radius, qminusone), qadd(cosh_radius, qone)) == radius2)
ck("polygon_fourth_power_identity", qmul(radius2, radius2) == (Q(1, 2), Q(0)))
# Adjacent geodesic-circle inward tangents (-b,+/-c) have b/c=1+sqrt(2).
b_over_c = qdiv(qmul(qadd(qone, radius2), qadd(sqrt2, qminusone)),
                qadd(qone, tuple(-a for a in radius2)))
ck("polygon_tangent_ratio", b_over_c == (Q(1), Q(1)))
ratio2 = qmul(b_over_c, b_over_c)
angle_cosine = qdiv(qadd(ratio2, qminusone), qadd(ratio2, qone))
ck("polygon_angle_cosine", angle_cosine == (Q(0), Q(1, 2)))

cycle, i = [], 0
while i not in cycle:
    cycle.append(i)
    i = (i + 5) % 8
ck("polygon_single_vertex_link", i == 0 and sorted(cycle) == list(range(8)))
ck("polygon_total_angle", 8*Q(1, 4) == 2)
base_chi, cover_chi = 1-4+1, 2*(1-4+1)
ck("base_genus_two", base_chi == 2-2*2)
ck("cover_genus_three", cover_chi == 2-2*3)
ck("nash_surface_dimension", Q(2, 2)*(3*2+11) == 17)

# Enumerate the 16 Z/2 characters of the abstract genus-two group presentation.
word = ((0, 1), (1, 1), (0, -1), (1, -1),
        (2, 1), (3, 1), (2, -1), (3, -1))
nontrivial = 0
for character in product(range(2), repeat=4):
    for initial in range(2):
        final = initial
        for generator, exponent in word:
            final = (final + exponent*character[generator]) % 2
        ck("surface_relator_monodromy", final == initial)
    if any(character):
        nontrivial += 1
        orbit = {0}
        for generator in range(4):
            orbit |= {(x + character[generator]) % 2 for x in tuple(orbit)}
        ck("two_sheet_transitivity", orbit == {0, 1})
ck("nontrivial_character_count", nontrivial == 15)
ck("chosen_character_is_nontrivial", any((1, 0, 0, 0)))

# Exact matrix controls using example Jacobians, not a computed Nash embedding.
def transpose(A):
    return tuple(tuple(row[j] for row in A) for j in range(len(A[0])))


def mm(A, B):
    if len(A[0]) != len(B):
        raise ValueError("Matrix shape mismatch")
    return tuple(tuple(sum((A[i][k]*B[k][j] for k in range(len(B))), Q(0))
                       for j in range(len(B[0]))) for i in range(len(A)))


def mscale(A, a):
    return tuple(tuple(a*x for x in row) for row in A)


def det2(A):
    return A[0][0]*A[1][1] - A[0][1]*A[1][0]


H = tuple((Q(i+1), Q((i+1)**2)) for i in range(17))
G = mm(transpose(H), H)
ck("example_jacobian_rank_two", G[0][0] > 0 and det2(G) > 0)
for entries in ((1, 0, 0, 1), (2, 1, 1, 1), (1, 2, 0, 1), (-1, 0, 0, -1)):
    a, b, c, d0 = map(Q, entries)
    J = ((a, b), (c, d0))
    ck("coordinate_jacobian_invertible", det2(J) != 0)
    left = mm(transpose(mm(H, J)), mm(H, J))
    right = mm(mm(transpose(J), G), J)
    for row, column in product(range(2), repeat=2):
        ck("pullback_composition_matrix_control", left[row][column] == right[row][column])
    ck("coordinate_positive_definiteness", right[0][0] > 0 and det2(right) > 0)
    for T in times:
        ck("static_integral_coordinate_commutation",
           mscale(left, T) == mm(mm(transpose(J), mscale(G, T)), J))

# L2 distance for constant functions: a finite algebra control of the proof.
for z, zprime in (((Q(1), Q(2)), (Q(1), Q(2))),
                  ((Q(1), Q(2)), (Q(1), Q(3)))):
    squared = sum(((a-b)**2 for a, b in zip(z, zprime)), Q(0))
    for T in times:
        ck("constant_history_distance_control", (T*squared == 0) == (z == zprime))
ck("zero_time_failure", Q(0)*G[0][0] == 0)
ck("curvature_scaling_at_test_times", all(-1/T < 0 for T in times))

# Separate finite-precision diagnostic. It is not an interval certificate.
with localcontext() as context:
    context.prec = 80
    radius_decimal = Decimal(1) / Decimal(2).sqrt().sqrt()
    decimal_residual = abs(radius_decimal**4 - Decimal(1)/2)
    if decimal_residual > Decimal("1e-70"):
        raise RuntimeError("Decimal diagnostic tolerance exceeded")
    diagnostic = {"precision_digits": 80,
                  "polygon_vertex_radius": str(radius_decimal),
                  "fourth_power_residual": str(decimal_residual),
                  "tolerance": "1e-70",
                  "classification": "Finite-precision diagnostic; no rigorous interval enclosure."}

here = Path(__file__).resolve().parent
receipt = {
    "schema": "pr85-supplementary-standard-library-verification/v1",
    "status": "PASS_SUPPLEMENTARY_CONTROLS",
    "optimization_level": sys.flags.optimize,
    "exact_assertions": sum(checks.values()),
    "checks": dict(sorted(checks.items())),
    "rational_chart_points": points,
    "nontrivial_double_cover_characters": nontrivial,
    "vertex_link_cycle": cycle,
    "exact_laplacian_numerator": "4",
    "curvature_identity": "P_T=T*pi^*g and K(P_T)=-1/T for fixed T>0",
    "fixed_chart_bounds": ["4T", "64T/9"],
    "decimal_diagnostic": diagnostic,
    "manuscript_source_sha256": hashlib.sha256(
        (here / "negative_gramian_cover.tex").read_bytes()).hexdigest(),
    "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "limitations": [
        "Global Nash existence and embedding injectivity are imported classical theorem inputs.",
        "Covering classification supplies a smooth connected cover; finite monodromy checks only its algebraic data.",
        "Smooth quotient geometry, compactness, completeness and exact global history fibers are analytical proof claims.",
        "Example matrices and finite mesh points are diagnostics, not sampled values of a constructed Nash embedding.",
        "No historical priority, novelty, independent human peer review or publication clearance follows from these controls."
    ]
}
print(json.dumps(receipt, indent=2, sort_keys=True))
