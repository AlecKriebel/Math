"""Exact finite-group checks used in the independent duality argument.

Only monomial matrices with cube-root phases are used.  (p, r) means
e_j -> omega**r[j] e_p[j].  No floating-point arithmetic or external code.
This checks the finite algebra input, not Poincare duality or the genus.
"""

from itertools import product
import json


IDENTITY = ((0, 1, 2), (0, 0, 0))
A = ((1, 2, 0), (0, 0, 0))
B = ((0, 1, 2), (0, 1, 2))


def multiply(u, v):
    p, r = u
    q, s = v
    return tuple(p[q[j]] for j in range(3)), tuple(
        (s[j] + r[q[j]]) % 3 for j in range(3)
    )


def power(u, n):
    result = IDENTITY
    for _ in range(n):
        result = multiply(result, u)
    return result


def inverse(u):
    return power(u, 2)


def commutator(u, v):
    return multiply(multiply(multiply(u, v), inverse(u)), inverse(v))


def projective(u):
    p, r = u
    return p, tuple((n - r[0]) % 3 for n in r)


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


group = {IDENTITY}
frontier = [IDENTITY]
while frontier:
    u = frontier.pop()
    for generator in [A, B]:
        v = multiply(u, generator)
        if v not in group:
            group.add(v)
            frontier.append(v)

center = {u for u in group if all(multiply(u, v) == multiply(v, u) for v in group)}
commutators = {commutator(u, v) for u, v in product(group, repeat=2)}
projective_group = {projective(u) for u in group}
scalars = {((0, 1, 2), (j, j, j)) for j in range(3)}

require(len(group) == 27, "wrong group order")
require(all(power(u, 3) == IDENTITY for u in group), "wrong exponent")
require(center == scalars == commutators, "wrong center or commutator subgroup")
require(len(projective_group) == 9, "wrong quotient order")
require(power(A, 3) == power(B, 3) == IDENTITY, "wrong generator orders")
require(commutator(A, B) != IDENTITY, "extension became abelian")
require(all(
    projective(multiply(u, v)) == projective(multiply(v, u))
    for u, v in product(group, repeat=2)
), "projective quotient is not abelian")

labels = list(product(range(3), repeat=3))


def matrix(g):
    a, b, c = g
    return multiply(multiply(power(A, a), power(B, b)), ((0, 1, 2), (c, c, c)))


def label_multiply(g, h):
    a, b, c = g
    d, e, s = h
    return (a + d) % 3, (b + e) % 3, (c + s + b * d) % 3


def cochain(g):
    a, b, c = g
    return (c - a * b) % 3


require({matrix(g) for g in labels} == group, "normal forms do not give group")
for g, h in product(labels, repeat=2):
    gh = label_multiply(g, h)
    require(matrix(gh) == multiply(matrix(g), matrix(h)), "wrong multiplication law")
    coboundary = (cochain(h) - cochain(gh) + cochain(g)) % 3
    require(coboundary == (g[0] * h[1]) % 3, "cup product is not the coboundary")

print(json.dumps({
    "arithmetic": "exact monomial permutations and exponents in F_3",
    "group_order": len(group),
    "exponent": 3,
    "center_order": len(center),
    "commutator_subgroup_order": len(commutators),
    "projective_quotient_order": len(projective_group),
    "abelianization_order": len(group) // len(commutators),
    "A_and_B_order": [3, 3],
    "nontrivial_commutator": commutator(A, B),
    "extension_restricts_split_on_coordinate_cyclics": True,
    "extension_is_nonsplit": True,
    "normal_form_product_pairs_checked": len(labels) ** 2,
    "cup_coboundary_pairs_checked": len(labels) ** 2,
    "scope": "finite algebra input only; see DUALITY_DETECTOR_PROOF.md",
}, indent=2))
