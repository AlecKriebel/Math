"""Exact, dependency-free controls for the classical pedal-area priority audit.

These controls establish only the stated algebraic identities and boundary
examples. They do not establish historical priority or the target all-N theorem.
"""
from fractions import Fraction as F
import json


def add(p, q):
    return tuple(x+y for x, y in zip(p, q))


def sub(p, q):
    return tuple(x-y for x, y in zip(p, q))


def mul(c, p):
    return tuple(c*x for x in p)


def dot(p, q):
    return sum(x*y for x, y in zip(p, q))


def det(p, q):
    return p[0]*q[1]-p[1]*q[0]


def area(v):
    return sum(det(p, q) for p, q in zip(v, v[1:]+v[:1]))/2


def intersect(r, s):
    d = det(r, s)
    if not d:
        raise ValueError("Consecutive lines must intersect")
    return ((s[1]-r[1])/d, (r[0]-s[0])/d)


def pedal(r, m):
    return add(m, mul((1-dot(r, m))/dot(r, r), r))


def weights(r):
    return [2*det(p, q)*dot(p, q)/(dot(p, p)*dot(q, q))
            for p, q in zip(r, r[1:]+r[:1])]


def check(condition, label):
    if not condition:
        raise RuntimeError(label)


def ellipse_normals(v):
    return [(p[0]/4, p[1]) for p in v]


def phase_control(v, scale_squared):
    """Actual vertices are sqrt(scale_squared)*v; ellipse axes are 2,1."""
    r = ellipse_normals(v)
    w = weights(r)
    t = [intersect(p, q) for p, q in zip(r, r[1:]+r[:1])]
    a = scale_squared*area(v)
    ap = area(t)/scale_squared
    b0 = area([mul(1/dot(p, p), p) for p in r])/scale_squared
    for i, p in enumerate(v):
        check(scale_squared*(p[0]**2/4+p[1]**2) == 1, "Boundary")
        chord = intersect(p, v[(i+1) % len(v)])
        check((F(16, 5)*chord[0]**2+F(1, 5)*chord[1]**2)
              / scale_squared == 1, "Same proper confocal caustic")
        incoming = sub(p, v[i-1])
        outgoing = sub(v[(i+1) % len(v)], p)
        reflected = sub(incoming, mul(2*dot(incoming, r[i])/dot(r[i], r[i]), r[i]))
        check(det(reflected, outgoing) == 0 and dot(reflected, outgoing) > 0,
              "Physical reflection")
    check(sum(w) == 0, "Four-periodic radial coefficient")
    return {"A": str(a), "A_prime": str(ap), "B_0": str(b0),
            "A_A_prime": str(a*ap), "A_prime_B_0": str(ap*b0),
            "S": str(sum(w))}


axis = [(F(2), F(0)), (F(0), F(1)), (F(-2), F(0)), (F(0), F(-1))]
rectangle = [(F(4), F(1)), (F(-4), F(1)), (F(-4), F(-1)), (F(4), F(-1))]
phase1 = phase_control(axis, F(1))
phase2 = phase_control(rectangle, F(1, 5))
check(phase1["A_A_prime"] == phase2["A_A_prime"] == "32", "Credited product")
check(phase1["A_prime_B_0"] == "32" and phase2["A_prime_B_0"] == "50",
      "Steiner plus AA-prime alone is insufficient outside target parity")

# Rational, centrally symmetric outer-ellipse tangent hexagon; no Poncelet
# assertion is made for this control. It verifies the exact signed formula.
vertices = []
for t in [F(0), F(1, 2), F(2)]:
    vertices.append((2*(1-t*t)/(1+t*t), 2*t/(1+t*t)))
vertices += [mul(-1, p) for p in vertices[:]]
r = ellipse_normals(vertices)
t = [intersect(p, q) for p, q in zip(r, r[1:]+r[:1])]
w = weights(r)
ap = area(t)
b0 = area([pedal(p, (F(0), F(0))) for p in r])
moment = tuple(sum(wi*vi[j] for wi, vi in zip(w, t)) for j in (0, 1))
check(moment == (0, 0), "Central weighted first moment")
for m in [(F(0), F(0)), (F(3, 7), F(-5, 9)), (F(6), F(2))]:
    bm = area([pedal(p, m) for p in r])
    check(4*(2*bm-ap) == sum(dot(sub(m, vi), sub(m, vi))*wi
                             for vi, wi in zip(t, w)), "Steiner signed formula")
    check(bm == b0+dot(m, m)*sum(w)/8, "Radial formula factor")

# A zero quadratic coefficient need not supply a finite curvature centroid.
# This noncentral trapezoid has S=0 and a nonzero weighted first moment.
trap = [(F(0), F(0)), (F(2), F(0)), (F(1), F(1)), (F(0), F(1))]
# General lines n.z=h; orthogonal projection does not require h=1.
trap_lines = [((F(0), F(1)), F(0)), ((F(1), F(1)), F(2)),
              ((F(0), F(1)), F(1)), ((F(1), F(0)), F(0))]
trap_w = weights([n for n, h in trap_lines])
trap_t = trap[1:]+trap[:1]
trap_moment = tuple(sum(wi*vi[j] for wi, vi in zip(trap_w, trap_t)) for j in (0, 1))


def trap_area(m):
    return area([add(m, mul((h-dot(n, m))/dot(n, n), n)) for n, h in trap_lines])


check(sum(trap_w) == 0 and trap_moment != (0, 0), "Zero-S caveat")
check(trap_area((F(0), F(0))) == F(1, 2)
      and trap_area((F(1), F(0))) == F(3, 4), "Linear degenerate level set")

# A simple affine change of coordinates does not preserve Euclidean pedals.
mapped_old_foot = (F(1), F(1, 2))
new_foot = pedal((F(1, 2), F(1)), (F(0), F(0)))
check(new_foot == (F(2, 5), F(4, 5)) and new_foot != mapped_old_foot,
      "Affine metric bridge")

print(json.dumps({"status": "PASS", "scope": "Exact classical controls only",
                  "excluded_N4_phase1": phase1, "excluded_N4_phase2": phase2,
                  "central_hexagon_pedal_points_checked": 3,
                  "trapezoid_S": str(sum(trap_w)),
                  "trapezoid_weighted_moment": [str(x) for x in trap_moment],
                  "trapezoid_B0": str(trap_area((F(0), F(0)))),
                  "trapezoid_B10": str(trap_area((F(1), F(0)))),
                  "affine_projection_noncommutation": True}, indent=2))
