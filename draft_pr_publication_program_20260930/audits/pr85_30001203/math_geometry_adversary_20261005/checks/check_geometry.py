#!/usr/bin/env python3
"""Independent exact checks of elementary identities in the geometric review.

Run with the Python standard library only. This does not construct or test the
Nash embedding, prove covering classification, or infer smoothness from samples.
Those assertions are established in PROOF.md or imported from pinned sources.
"""

from fractions import Fraction as Q
import json


def clean(p):
    return {ij: Q(a) for ij, a in p.items() if a}


def add(p, q):
    r = dict(p)
    for ij, a in q.items():
        r[ij] = r.get(ij, Q(0)) + a
    return clean(r)


def scale(p, a):
    return clean({ij: a * c for ij, c in p.items()})


def mul(p, q):
    r = {}
    for (i, j), a in p.items():
        for (k, l), b in q.items():
            ij = (i + k, j + l)
            r[ij] = r.get(ij, Q(0)) + a * b
    return clean(r)


def derivative(p, axis):
    r = {}
    for ij, a in p.items():
        if ij[axis]:
            kl = list(ij)
            kl[axis] -= 1
            r[tuple(kl)] = a * ij[axis]
    return clean(r)


one = {(0, 0): Q(1)}
u = {(1, 0): Q(1)}
v = {(0, 1): Q(1)}
s = add(mul(u, u), mul(v, v))
d = add(one, scale(s, -1))

# For phi = log(2 sqrt(T)) - log(d), phi_u=2u/d and phi_v=2v/d.
# Each quotient derivative has denominator d^2; check the entire polynomial
# numerator of phi_uu + phi_vv, rather than finitely many evaluations.
laplacian_numerator = {}
for axis, coord in enumerate((u, v)):
    p = scale(coord, 2)
    numerator = add(mul(derivative(p, axis), d),
                    scale(mul(p, derivative(d, axis)), -1))
    laplacian_numerator = add(laplacian_numerator, numerator)
assert laplacian_numerator == scale(one, 4)
# K = -e^(-2phi) Delta(phi) = -(d^2/(4T))*(4/d^2) = -1/T.

# Quadratic field Q(sqrt(2)): independent exact check of the explicit polygon's
# disk radius and the angle between its two geodesic tangents at a vertex.
def qadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


def qmul(a, b):
    return (a[0] * b[0] + 2 * a[1] * b[1],
            a[0] * b[1] + a[1] * b[0])


def qinverse(a):
    norm = a[0] ** 2 - 2 * a[1] ** 2
    return (a[0] / norm, -a[1] / norm)


def qdiv(a, b):
    return qmul(a, qinverse(b))


qone, qminusone = (Q(1), Q(0)), (Q(-1), Q(0))
sqrt2 = (Q(0), Q(1))
vertex_radius_squared = (Q(0), Q(1, 2))
cosh_radius = (Q(3), Q(2))
assert qdiv(qadd(cosh_radius, qminusone), qadd(cosh_radius, qone)) == vertex_radius_squared
assert qmul(vertex_radius_squared, vertex_radius_squared) == (Q(1, 2), Q(0))
# In the disk: centers of adjacent side circles are (a,+/-b),
# a=(1+r^2)/(2r), b=a*tan(pi/8), and c=a-r=(1-r^2)/(2r).
# The inward tangents are (-b,+/-c), so cos(alpha)=(b^2-c^2)/(b^2+c^2).
qneg_s = tuple(-a for a in vertex_radius_squared)
b_over_c = qdiv(qmul(qadd(qone, vertex_radius_squared), qadd(sqrt2, qminusone)),
                qadd(qone, qneg_s))
assert b_over_c == (Q(1), Q(1))
ratio_squared = qmul(b_over_c, b_over_c)
interior_angle_cosine = qdiv(qadd(ratio_squared, qminusone), qadd(ratio_squared, qone))
assert interior_angle_cosine == (Q(0), Q(1, 2))  # sqrt(2)/2 = cos(pi/4)

# Opposite sides i and i+4 are glued with boundary orientation reversed.
# The 'next' ray at corner i is glued to the 'previous' ray at corner i+5.
cycle = []
i = 0
while i not in cycle:
    cycle.append(i)
    i = (i + 5) % 8
assert i == 0 and sorted(cycle) == list(range(8))
angle_sum_in_pi_units = 8 * Q(1, 4)
assert angle_sum_in_pi_units == 2
chi_base = 1 - 4 + 1
chi_cover = 2 * chi_base
genus_base = (2 - chi_base) // 2
genus_cover = (2 - chi_cover) // 2
assert (genus_base, genus_cover) == (2, 3)

# The generator images in S_2 give transitive two-sheet monodromy. The surface
# relator is [a1,b1][a2,b2], each commutator is the identity.
identity, swap = (0, 1), (1, 0)


def compose(a, b):
    return tuple(a[b[i]] for i in range(2))


def inverse(a):
    return tuple(a.index(i) for i in range(2))


def commutator(a, b):
    return compose(compose(compose(a, b), inverse(a)), inverse(b))


relator = compose(commutator(swap, identity), commutator(identity, identity))
assert relator == identity
assert {identity[0], swap[0]} == {0, 1}

# On s=u^2+v^2 in [0,1/4], lambda(s)=4/(1-s)^2 is increasing;
# its endpoint values therefore establish the exact global bounds in each chart.
lower = Q(4)
upper = Q(4) / (1 - Q(1, 4)) ** 2
assert upper == Q(64, 9)
n = 2
nash_dimension = Q(n, 2) * (3 * n + 11)
assert nash_dimension == 17

result = {
    "status": "PASS",
    "exact_polynomial_laplacian_numerator": "4",
    "curvature_identity": "K(T*g)=-1/T for every fixed T>0",
    "polygon_vertex_radius_squared": "sqrt(2)/2",
    "polygon_interior_angle_cosine": "sqrt(2)/2",
    "vertex_link_cycle": cycle,
    "total_corner_angle_in_pi_units": str(angle_sum_in_pi_units),
    "base_euler_characteristic": chi_base,
    "cover_euler_characteristic": chi_cover,
    "base_genus": genus_base,
    "cover_genus": genus_cover,
    "two_sheet_relator_permutation": list(relator),
    "monodromy_transitive": True,
    "fixed_chart_metric_eigenvalue_bounds": [str(lower), str(upper)],
    "nash_original_compact_dimension": int(nash_dimension),
    "limits": [
        "Nash embedding is imported, not computationally constructed.",
        "Cover existence uses pinned Hatcher theorem; permutation check tests its data.",
        "Smooth vertex and geodesic completeness are proved in PROOF.md.",
        "No empirical samples substitute for the global polynomial identity."
    ]
}
print(json.dumps(result, indent=2))
