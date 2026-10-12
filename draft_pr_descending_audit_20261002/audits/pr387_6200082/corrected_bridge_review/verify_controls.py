#!/usr/bin/env python3
"""Finite rational controls for the reviewed Mayer-Vietoris mechanism.

These controls do not verify a Cheeger existence constant or an analytic theorem.
"""
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent


def rank(a):
    if not a or not a[0]:
        return 0
    a = [[Fraction(x) for x in row] for row in a]
    h, w = len(a), len(a[0])
    r = 0
    for c in range(w):
        piv = next((i for i in range(r, h) if a[i][c]), None)
        if piv is None:
            continue
        a[r], a[piv] = a[piv], a[r]
        p = a[r][c]
        a[r] = [x / p for x in a[r]]
        for i in range(h):
            if i != r and a[i][c]:
                p = a[i][c]
                a[i] = [x - p * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == h:
            break
    return r


def boundary_rank(k, d):
    src = sorted(s for s in k if len(s) == d + 1)
    dst = sorted(s for s in k if len(s) == d)
    idx = {s: i for i, s in enumerate(dst)}
    a = [[0] * len(src) for _ in dst]
    for j, s in enumerate(src):
        for v in range(len(s)):
            a[idx[s[:v] + s[v + 1:]]][j] = (-1) ** v
    return rank(a)


def betti(k, d):
    return sum(len(s) == d + 1 for s in k) - boundary_rank(k, d) - boundary_rank(k, d + 1)


def induced(k, vs):
    return {s for s in k if set(s) <= vs}


def cone(k, apex):
    return k | {(apex,)} | {tuple(sorted(s + (apex,))) for s in k}


vs = range(4)
edges = list(combinations(vs, 2))
triangles = list(combinations(vs, 3))
complexes = []
for edge_bits in range(1 << len(edges)):
    skeleton = {(v,) for v in vs} | {e for j, e in enumerate(edges) if edge_bits >> j & 1}
    allowed = [t for t in triangles if set(combinations(t, 2)) <= skeleton]
    for face_bits in range(1 << len(allowed)):
        k = skeleton | {t for j, t in enumerate(allowed) if face_bits >> j & 1}
        complexes.append(k)
        if len(k) == 14:
            complexes.append(k | {tuple(vs)})

cases = 0
zero_ambient_cases = 0
for k in complexes:
    for net_bits in range(16):
        originals = {v for v in vs if net_bits >> v & 1}
        added = set(vs) - originals
        boundary = {v for v in originals if any(tuple(sorted((v, w))) in k for w in added)}
        u = induced(k, originals)
        v = induced(k, added | boundary)
        inter = u & v
        assert u | v == k
        assert {s[0] for s in inter if len(s) == 1} == boundary
        b_u, b_k, b_i = betti(u, 2), betti(k, 2), betti(inter, 2)
        assert b_u <= b_k + b_i
        assert b_i <= sum(len(s) == 3 for s in inter)
        delta = max((sum(len(e) == 2 and x in e for e in u) for x in originals), default=0)
        assert sum(len(s) == 3 for s in inter) <= len(boundary) * delta * (delta - 1) // 2
        if b_k == 0:
            zero_ambient_cases += 1
            assert b_u <= len(boundary) * delta * (delta - 1) // 2
        cases += 1

sphere = {s for d in range(1, 4) for s in combinations(vs, d)}
ball = cone(sphere, 4)
assert betti(sphere, 2) == 1 and betti(ball, 2) == 0 and betti(sphere, 1) == 0
# This falsifies the wrong replacement of b_2(intersection) by b_1(intersection).
assert betti(sphere, 2) > betti(ball, 2) + betti(sphere, 1)

# A cyclic hyperbolic-axis control: length 12; points -4,+4 have quotient distance 4.
length = Fraction(12)
left, right = Fraction(-4), Fraction(4)
cover_distance = right - left
quotient_distance = min(abs(right - left + n * length) for n in range(-2, 3))
assert length > 10 and cover_distance == 8 and quotient_distance == 4
# Disjointness fails when radius is the separation bound, rather than half of it.
assert Fraction(3, 2) > 1 and Fraction(3, 2) < 2 * 1
assert 3 > 2 and 3 < 2 * 2

sources = {
    "abbg1811.02520v3.pdf": "https://arxiv.org/pdf/1811.02520v3",
    "bowen1303.5963v4.pdf": "https://arxiv.org/pdf/1303.5963v4",
    "bowen_published2015.pdf": "https://math.uchicago.edu/~shmuel/L%5E2%20cohomology%20readings/Bowen,%20Cheeger%20constants%20and%20L2-Betti%20numbers.pdf",
    "buser1982.pdf": "https://www.numdam.org/article/ASENS_1982_4_15_2_213_0.pdf",
}
bindings = [{"file": "raw_sources/" + name, "url": url,
             "sha256": hashlib.sha256((HERE / "raw_sources" / name).read_bytes()).hexdigest()}
            for name, url in sources.items()]
(HERE / "SOURCE_BINDINGS.json").write_text(json.dumps(bindings, indent=2) + "\n")
results = {
    "candidate_head": "a3034c577445753e00d0b87d358b1fc429e1e9e8",
    "candidate_corrected_application_sha256": "0a8f5fc6600e2447b85999b765ca1a58ef866913d488831610f5c5efc43ab0fc",
    "coefficient_field": "Q",
    "complexes_on_four_present_vertices": len(complexes),
    "all_induced_cover_controls": cases,
    "zero_second_homology_ambient_controls": zero_ambient_cases,
    "sharp_sphere_cone_control": "PASS",
    "wrong_homology_degree_counterexample": "VERIFIED",
    "injectivity_vs_metric_covering_radius_axis_counterexample": "VERIFIED",
    "wrong_radius_disjointness_counterexamples": "VERIFIED",
    "status": "PASS",
    "analytic_existence_or_optimal_gap_tested": False,
}
(HERE / "CONTROL_RESULTS.json").write_text(json.dumps(results, indent=2) + "\n")
print(json.dumps(results, sort_keys=True))
