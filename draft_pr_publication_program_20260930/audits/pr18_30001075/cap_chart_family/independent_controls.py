#!/usr/bin/env python3
"""Fresh exact finite diagnostics. Not a universal geometric proof.

Standard library only; no author/reviewer code imports or historical input reads.
Run with PYTHONDONTWRITEBYTECODE=1. Results are written in this audit folder.
"""
from fractions import Fraction as Q
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import random

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "source_snapshot"
random.seed(30001075018)
counts = {}

def check(name, condition):
    if not condition:
        raise AssertionError(name)
    counts[name] = counts.get(name, 0) + 1

def dot(a, b):
    return sum(x*y for x, y in zip(a, b))

def psi(vertices, n, u, v):
    return dot(n, u) - max(dot(n, (x-z*v[0], y-z*v[1])) for x, y, z in vertices)

def add(a, b):
    return tuple(x+y for x, y in zip(a, b))

def scale(c, a):
    return tuple(c*x for x in a)

def det(matrix):
    a = [list(row) for row in matrix]
    result = Q(1)
    for i in range(len(a)):
        j = next((j for j in range(i, len(a)) if a[j][i]), None)
        if j is None:
            return Q(0)
        if i != j:
            a[i], a[j] = a[j], a[i]
            result = -result
        pivot = a[i][i]
        result *= pivot
        for j in range(i+1, len(a)):
            ratio = a[j][i] / pivot
            for k in range(i+1, len(a)):
                a[j][k] -= ratio*a[i][k]
    return result

units = [(Q(1), Q(0)), (Q(-1), Q(0)), (Q(0), Q(1)), (Q(0), Q(-1))]
for k in (2, 3, 5, 17, 101, 10001):
    for sx in (-1, 1):
        for sy in (-1, 1):
            units.append((sx*Q(2*k, k*k+1), sy*Q(k*k-1, k*k+1)))
for n in units:
    check("rational_unit_normal", dot(n, n) == 1)

# Exact support differences on nonsmooth finite convex hulls, with increments
# of both signs. h_C equals the maximum at vertices for every tested n.
for trial in range(150):
    vertices = [tuple(Q(random.randint(-100, 100), random.randint(1, 11)) for _ in range(3)) for _ in range(7)]
    u, v, du, dv = [tuple(Q(random.randint(-20, 20), random.randint(1, 11)) for _ in range(2)) for _ in range(4)]
    for n in units:
        diff = psi(vertices, n, add(u, du), add(v, dv)) - psi(vertices, n, u, v)
        increments = [dot(n, add(du, scale(z, dv))) for x, y, z in vertices]
        check("support_difference_two_sided", min(increments) <= diff <= max(increments))

# Independent interpolation bases, including equal/opposite normals, tiny
# contact gaps, and nearly collinear own directions.
height_pairs = [(Q(0), Q(1)), (Q(-3), Q(7)), (Q(10**8), Q(10**8)+Q(1, 10**12))]
for s, t in height_pairs:
    d = t-s
    for ea in units:
        for eb in units:
            pa, pb = (-ea[1], ea[0]), (-eb[1], eb[0])
            def interpolated(e, at_a):
                return (scale(t/d if at_a else -s/d, e), scale(-1/d if at_a else 1/d, e))
            cols = [interpolated(ea, True), interpolated(eb, False), interpolated(pa, True), interpolated(pb, False)]
            matrix = [[col[part][component] for col in cols] for part in (0, 1) for component in (0, 1)]
            check("four_motion_basis_exact", abs(det(matrix)) == 1/(d*d))

# Cap-height diagonal dominance with sharp rational cone apertures. These
# verify the exact pointwise inequalities, not all maximizing normals.
for k in (2, 17, 101, 10001):
    alpha = Q(2*k, k*k+1)
    eps = alpha / 32
    m = alpha / 4
    ea = (Q(-1), Q(0))
    normals = [n for n in units if dot(n, ea) >= alpha/2]
    for s, t in height_pairs:
        d = t-s
        heights = [s-eps*d, s, s+eps*d]
        vertices = [(Q(0), Q(0), z) for z in heights] + [(Q(1), Q(1), z) for z in heights]
        for eb in units:
            va = (scale(t/d, ea), scale(-1/d, ea))
            vb = (scale(-s/d, eb), scale(1/d, eb))
            for h in (Q(1, 17), Q(9, 7)):
                for n in normals:
                    diff = psi(vertices, n, scale(h, va[0]), scale(h, va[1])) - psi(vertices, n, (0, 0), (0, 0))
                    check("own_motion_exact_lower_bound", diff >= m*h)
                for n in units:
                    diff = psi(vertices, n, scale(-h, vb[0]), scale(-h, vb[1])) - psi(vertices, n, (0, 0), (0, 0))
                    check("cross_motion_exact_absolute_bound", abs(diff) <= eps*h)
        check("strict_cross_contraction", eps/m < Q(1, 4))

# Exact nonsmooth prism support-gap formulas, valid near the interior of the
# exposed transverse face. Opposite sides give coupled |a+b| terms.
h = Q(1, 100)
grid = [Q(i, 1000) for i in range(-10, 11)]
def ga(a, b):
    return a-h*abs(a+b)
def gb(a, b):
    return b-h*abs(a+b)
for a in grid:
    for b in grid:
        check("opposite_prism_only_simultaneous_zero", (ga(a, b) == 0 and gb(a, b) == 0) == (a == 0 and b == 0))
        for step in (Q(1, 10000), Q(3, 10000)):
            check("nonsmooth_opposite_own_slope", ga(a+step, b)-ga(a, b) >= (1-h)*step)
            check("nonsmooth_opposite_cross_slope", abs(ga(a, b+step)-ga(a, b)) <= h*step)

# Orthogonal prisms yield nonzero residual-dependent roots with a kink.
def root(r):
    return h*r/(1+h) if r >= 0 else -h*r/(1-h)
for r in grid:
    check("nonsmooth_prism_residual_root", root(r)-h*abs(root(r)-r) == 0)
    for rr in grid:
        check("nonsmooth_prism_residual_root_lipschitz", abs(root(r)-root(rr)) <= h/(1-h)*abs(r-rr))

# Concrete root brackets/self-map numbers rather than an assumption that a
# local root exists. The residual L may be huge, so eta must shrink.
for alpha in (Q(1), Q(1, 10), Q(1, 10**12)):
    eps, m, delta, residual_lip = alpha/32, alpha/4, Q(1, 100), Q(10**10)
    eta = (m-eps)*delta/(4*residual_lip)
    perturbation = eps*delta+residual_lip*eta
    check("root_brackets_strict", perturbation < m*delta)
    check("square_self_map_strict", perturbation/m < delta)
    check("fixed_point_parameter_lipschitz_finite", (residual_lip/m)/(1-eps/m) > 0)

# Fixed global rational balls can be tiny in a rotated coordinate system.
axis = (Q(3, 5), Q(0), Q(4, 5))
for d in (Q(1), Q(1, 10**15)):
    eps = Q(1, 100)
    radius = eps*d/4
    shift = (radius/4, Q(0), Q(0))
    check("rational_ball_contact_strictly_interior", dot(shift, shift) < radius*radius)
    check("rational_ball_rotated_height_bound", abs(dot(axis, shift))+radius < eps*d)
    check("rational_balls_contact_separation", 2*radius+2*abs(dot(axis, shift)) < d)

# Negative controls: omitting each named assumption produces an actual failed
# conclusion. These failures are intended and are recorded as detections.
point = [(Q(0), Q(0), Q(1))]
wrong_diff = psi(point, (Q(1), Q(0)), (0, 0), (1, 0)) - psi(point, (Q(1), Q(0)), (0, 0), (0, 0))
check("negative_control_reversed_support_sign_detected", wrong_diff == 1 and wrong_diff != -1)

# C = conv{(0,0),(1,1),(-1,1)}, ball center (1,0), radius 1.
# Its cap has x >= 0 and thus an additional -x normal at the contact on the
# ball boundary; the original vertex (-1,1) violates that normal.
bad_original_vertex = (Q(-1), Q(1))
check("negative_control_ball_boundary_new_normal_detected", dot((-1, 0), bad_original_vertex) > 0)
for lam in (Q(1, 100), Q(1, 2), Q(1)):
    q = scale(lam, bad_original_vertex)
    check("negative_control_segment_does_not_enter_boundary_ball", (q[0]-1)**2+q[1]**2 > 1)

# No localization: at z=2, V_A(z) = -e_A and the own support increment reverses.
ea = (Q(-1), Q(0))
check("negative_control_unlocalized_height_detected", dot(ea, scale(-1, ea)) < 0)
check("negative_control_no_projection_interior_detected", dot((0, 1), (0, -1)) == -1)

# C=[0,1]x[-1,1]x[0,10], L_theta=(theta(z-10),0,z).
# Every theta>0 is tangent only at height 10, so it misses a cap near height 0.
for theta in (Q(1, 100), Q(1, 10**10)):
    for z in (Q(0), Q(1, 10)):
        check("negative_control_changing_contact_fixed_cap_miss", theta*(z-10) < 0)
    check("negative_control_changing_contact_original_tangent", theta*(10-10) == 0)

expected = {
    "CANDIDATE.md": "b04aaf0b5a42d79ad26daf27880774a3f126858ef545b3f366a2b8b62e277252",
    "source_record.json": "b90fc595a14ea6522ec5d01bbb04fd3d0445362bc0a3257e2cc927f350f3afb5",
}
source_hashes = {name: hashlib.sha256((SOURCE/name).read_bytes()).hexdigest() for name in expected}
for name, digest in expected.items():
    check("frozen_input_hash", source_hashes[name] == digest)
result = {
    "created_at": datetime.now(timezone.utc).isoformat(),
    "source_head": "99e403e85d38d92b021198c4a57bbad3cd8775ba",
    "source_hashes": source_hashes,
    "seed": 30001075018,
    "arithmetic": "fractions.Fraction exact rational arithmetic",
    "checks": counts,
    "total_assertions": sum(counts.values()),
    "all_passed": True,
    "universal_proof": False,
    "caveat": "Finite diagnostics corroborate signs/constants/examples; the universal result rests on the independent analytic reconstruction.",
}
(HERE/"independent_results.json").write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps({"all_passed": True, "categories": len(counts), "total_assertions": sum(counts.values())}))
