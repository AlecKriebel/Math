#!/usr/bin/env python3
"""Independent exact diagnostics; not a search for globally holding circles."""
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product, permutations
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
counts = {}


def ck(label, condition):
    if not condition:
        raise AssertionError(label)
    counts[label] = counts.get(label, 0) + 1


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def add(a, b):
    return tuple(x+y for x, y in zip(a, b))


def scale(t, a):
    return tuple(t*x for x in a)


directions = set()
for seed in ((Q(1), Q(0), Q(0)), (Q(3, 5), Q(4, 5), Q(0)),
             (Q(1, 3), Q(2, 3), Q(2, 3))):
    for perm in set(permutations(seed)):
        for signs in product((-1, 1), repeat=3):
            directions.add(tuple(x*s for x, s in zip(perm, signs)))
for u in directions:
    ck("rational_unit_normals", dot(u, u) == 1)

# For a box, support is explicit. Exact maximizing directions are supplied,
# so this is a finite diagnostic of the signed-distance identity, not an
# optimization approximation to an arbitrary convex body.
widths = (Q(1), Q(2), Q(3))


def support(u):
    return sum(a*abs(z) for a, z in zip(widths, u))


samples = [
    ((Q(0), Q(0), Q(0)), Q(-1), (Q(1), Q(0), Q(0))),
    ((Q(3, 4), Q(0), Q(0)), Q(-1, 4), (Q(1), Q(0), Q(0))),
    ((Q(0), Q(-3, 2), Q(0)), Q(-1, 2), (Q(0), Q(-1), Q(0))),
    ((Q(1), Q(1), Q(0)), Q(0), (Q(1), Q(0), Q(0))),
]
for t in (Q(1, 10), Q(1, 5), Q(1), Q(3)):
    samples.append(((1+3*t, 2+4*t, Q(0)), 5*t,
                    (Q(3, 5), Q(4, 5), Q(0))))
for y, signed, witness in samples:
    ck("box_support_witness", dot(witness, y)-support(witness) == signed)
    for u in directions:
        ck("box_support_upper_controls", dot(u, y)-support(u) <= signed)
    for radius in (Q(0), Q(1, 5), Q(1), Q(2)):
        ck("parallel_support_witness",
           dot(witness, y)-(support(witness)+radius) == signed-radius)

# The normal-away argument works for every point in the opposite halfspace.
# Tangential vectors need not be orthogonal: subtract the normal component.
for n in ((Q(0), Q(0), Q(1)), (Q(1, 3), Q(2, 3), Q(2, 3))):
    for raw in ((Q(1), Q(2), Q(3)), (Q(-2), Q(1), Q(0))):
        tangent = add(raw, scale(-dot(n, raw), n))
        ck("tangent_projection", dot(n, tangent) == 0)
        for h in (Q(0), Q(1, 7), Q(3)):
            gap = add(tangent, scale(h, n))
            for t in (Q(0), Q(1, 10), Q(1), Q(7)):
                new = add(gap, scale(t, n))
                ck("normal_translation_identity",
                   dot(new, new)-dot(gap, gap) == 2*h*t+t*t)
                ck("normal_translation_nonnegative", dot(new, new) >= dot(gap, gap))
ck("wrong_direction_negative_control", Q(1, 2)**2 < Q(1)**2)

# General exact version of the ball detour identity, without radicals:
# inner radius rho, thickening r, turnaround height squared h1^2=1-rho^2.
# Start with the expanded ring tangent at height squared h0^2.
for rho in (Q(1, 4), Q(1, 2), Q(3, 4), Q(4, 5), Q(7, 8)):
    for r in (Q(1, 10), Q(1, 5), Q(1, 3)):
        R = rho+r
        h1sq = 1-rho*rho
        h0sq = (1+r)**2-R*R
        ck("detour_height_order", h0sq-h1sq == 2*r*(1-rho) > 0)
        ck("inner_initial_clearance", rho*rho+h0sq-1 == 2*r*(1-rho) > 0)
        ck("inner_turnaround_contact", rho*rho+h1sq == 1)
        ck("expanded_turnaround_collision",
           R*R+h1sq-(1+r)**2 == -2*r*(1-rho) < 0)
        ck("initial_expanded_tangency", R*R+h0sq == (1+r)**2)
ck("submitted_initial_height", (1+Q(1, 5))**2-1 == Q(11, 25))
ck("submitted_turnaround_height", 1-Q(4, 5)**2 == Q(9, 25))

# Ball-only positive-clearance controls include the sharp permitted endpoint.
# For a unit-radius horizontal ring with z>=4/5, minimum norm squared is41/25.
# At r=sqrt(41)/5-1 the initial ring may touch the parallel ball; it is allowed.
ck("strict_positive_clearance", Q(41, 25) > 1)
ck("submitted_small_thickening", Q(41, 25) > (1+Q(1, 5))**2)
ck("terminal_disk_margin", Q(41, 25) < 4)
for dz in (Q(0), Q(1, 8), Q(1), Q(7)):
    ck("positive_path_height_polynomial",
       1+(Q(4, 5)+dz)**2-Q(41, 25) == Q(8, 5)*dz+dz*dz >= 0)

out = {
    "status": "PASS",
    "artifact_sha256": sha256((ROOT/"author_replay/OBSTRUCTION.md").read_bytes()).hexdigest(),
    "exact_assertions": sum(counts.values()),
    "families": counts,
    "scope": "Exact support, halfspace translation, ball-detour and positive-clearance diagnostics. These do not certify any global holding circle or the original Minkowski closure question.",
}
(ROOT/"independent_results.json").write_text(json.dumps(out, indent=2)+"\n")
print(json.dumps(out, indent=2))
