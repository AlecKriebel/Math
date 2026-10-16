#!/usr/bin/env python3
"""Exact independent Cartesian boundary test for the k407 period convention.

This is a finite algebraic certificate, not a proof of the even primitive theorem.
No submitted checker or mathematical helper is imported.  The library directory
is passed explicitly so the frozen submission need not be modified.
"""
import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--library-dir", required=True)
ap.add_argument("--output", required=True)
args = ap.parse_args()
sys.path.insert(0, args.library_dir)
import sympy as sp

assert sp.__version__ == "1.14.0"
assert not sys.flags.optimize
checks = []

def clean(z):
    return sp.simplify(sp.radsimp(sp.expand(z)))

def equal(z, name):
    z = clean(z)
    assert z == 0, (name, z)
    checks.append(name)

def nonzero(z, name):
    z = clean(z)
    assert z.is_zero is False, (name, z)
    checks.append(name)
    return z

def positive(z, name):
    z = clean(z)
    assert z.is_positive is True, (name, z)
    checks.append(name)

def vector(x, y):
    return sp.Matrix([x, y])

def coords(p):
    return [str(clean(z)) for z in p]

alpha, beta = sp.Integer(8), sp.Integer(3)
lam = sp.Rational(72, 25)
focus = vector(sp.sqrt(alpha - beta), 0)
G = sp.diag(1 / alpha, 1 / beta)
H = sp.diag(1 / (alpha - lam), 1 / (beta - lam))
positive(lam, "strict nesting: lambda positive")
positive(beta - lam, "strict elliptical caustic: beta minus lambda positive")

def certify(points, name):
    n = len(points)
    assert n == 3
    for i, p in enumerate(points):
        equal((p.T * G * p)[0] - 1, f"{name}: vertex {i} on original ellipse")
        for j in range(i):
            nonzero((p - points[j]).dot(p - points[j]), f"{name}: distinct vertices {i},{j}")
        q = points[(i + 1) % n]
        d = q - p
        den = (d.T * H * d)[0]
        positive(den, f"{name}: caustic edge quadratic {i} positive")
        t = clean(-(p.T * H * d)[0] / den)
        positive(t, f"{name}: tangent contact {i} after start")
        positive(1 - t, f"{name}: tangent contact {i} before end")
        contact = p + t * d
        equal((contact.T * H * contact)[0] - 1, f"{name}: exact caustic tangency {i}")
        equal((contact.T * H * d)[0], f"{name}: derivative at tangent contact {i}")
        incoming = p - points[(i - 1) % n]
        outgoing = q - p
        ni = G * p
        vin = incoming / sp.sqrt(incoming.dot(incoming))
        vout = outgoing / sp.sqrt(outgoing.dot(outgoing))
        reflection = vin - 2 * vin.dot(ni) / ni.dot(ni) * ni
        for j in range(2):
            equal(vout[j] - reflection[j], f"{name}: physical specular reflection {i}:{j}")

    outer = []
    for i, p in enumerate(points):
        q = points[(i + 1) % n]
        rows = sp.Matrix.vstack((G * p).T, (G * q).T)
        nonzero(rows.det(), f"{name}: finite original tangent intersection {i}")
        r = rows.inv() * sp.ones(2, 1)
        r = r.applyfunc(clean)
        equal((G * p).dot(r) - 1, f"{name}: first named original tangent {i}")
        equal((G * q).dot(r) - 1, f"{name}: second named original tangent {i}")
        outer.append(r)

    def antipedal(outer_list):
        vertices = []
        dets = []
        for i, r in enumerate(outer_list):
            t = outer_list[(i + 1) % len(outer_list)]
            nr, nt = r - focus, t - focus
            rows = sp.Matrix.vstack(nr.T, nt.T)
            dets.append(nonzero(rows.det(), f"{name}: finite focal antipedal intersection {len(outer_list)}:{i}"))
            u = rows.inv() * vector(nr.dot(r), nt.dot(t))
            u = u.applyfunc(clean)
            equal(nr.dot(u - r), f"{name}: first named focal antipedal line {len(outer_list)}:{i}")
            equal(nt.dot(u - t), f"{name}: second named focal antipedal line {len(outer_list)}:{i}")
            vertices.append(u)
        centroid = sum(vertices, sp.zeros(2, 1)) / len(vertices)
        return vertices, centroid.applyfunc(clean), dets

    vertices, centroid, dets = antipedal(outer)
    repeated_vertices, repeated_mean, repeated_dets = antipedal(outer * 2)
    for j in range(2):
        equal(repeated_mean[j] - centroid[j], f"{name}: twice-traversed listed N6 mean unchanged:{j}")
    for i in range(6):
        for j in range(2):
            equal(repeated_vertices[i][j] - vertices[i % 3][j], f"{name}: repeated N6 vertex {i}:{j}")
    return {
        "original_vertices": [coords(p) for p in points],
        "outer_original_tangent_intersections": [coords(p) for p in outer],
        "focal_antipedal_vertices": [coords(p) for p in vertices],
        "focal_normal_determinants": [str(d) for d in dets],
        "vertex_centroid": coords(centroid),
        "twice_traversed_listed_N6_centroid": coords(repeated_mean),
        "least_period": 3,
        "all_intersections_finite": True,
        "physical_billiard_reflections_verified": True,
        "same_fixed_strict_elliptical_caustic": True,
    }, centroid

right_vertex_triangle = [
    vector(2 * sp.sqrt(2), 0),
    vector(-8 * sp.sqrt(2) / 5, 3 * sp.sqrt(3) / 5),
    vector(-8 * sp.sqrt(2) / 5, -3 * sp.sqrt(3) / 5),
]
top_vertex_triangle = [
    vector(0, sp.sqrt(3)),
    vector(8 * sp.sqrt(3) / 5, -sp.sqrt(3) / 5),
    vector(-8 * sp.sqrt(3) / 5, -sp.sqrt(3) / 5),
]
a, c1 = certify(right_vertex_triangle, "right vertex phase")
b, c2 = certify(top_vertex_triangle, "top vertex phase")
difference = (c1 - c2).applyfunc(clean)
nonzero(difference.dot(difference), "two phases have different arithmetic vertex centroids")
equal(c1[1], "right vertex phase centroid lies on focal axis")
nonzero(c2[1], "top vertex phase centroid leaves focal axis")

body = Path(__file__).read_bytes()
report = {
    "schema": "root-pr259-exact-period-boundary-certificate-v1",
    "UTC": datetime.now(timezone.utc).isoformat(),
    "status": "PASS_EXACT_COUNTEREXAMPLE_TO_LISTED_EVEN_WITH_ODD_LEAST_PERIOD",
    "original_ellipse_squared_semiaxes": ["8", "3"],
    "caustic_parameter_lambda": "72/25",
    "caustic_squared_semiaxes": ["128/25", "3/25"],
    "fixed_original_focus": coords(focus),
    "phases": [a, b],
    "centroid_difference": coords(difference),
    "assertion_count": len(checks),
    "checks": checks,
    "checker": {"bytes": len(body), "sha256": hashlib.sha256(body).hexdigest()},
    "sympy": sp.__version__,
    "scope": "Falsifies the extension to an even vertex-list length obtained by twice traversing a genuine least-period-three orbit. Does not falsify the submitted even least-period theorem or establish how the primary source convention must be interpreted.",
    "comparison_is_exact_algebraic": True,
    "all_period_theorem_verified": False,
    "provider_writes": 0,
    "primary_Git_writes": 0,
}
Path(args.output).write_text(json.dumps(report, sort_keys=True, indent=2) + "\n")
print(json.dumps({k: report[k] for k in ("status", "assertion_count", "centroid_difference")}, sort_keys=True))
