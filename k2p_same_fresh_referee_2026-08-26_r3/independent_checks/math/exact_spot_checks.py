#!/usr/bin/env python3
"""Fresh exact spot checks for the r2 K2P mathematical review.

This file imports no code, classifier, graph object, or expected certificate
from the submitted package.  All formulas and graph encodings below are
transcribed directly from the printed theorem statements and re-derived here.
"""

from __future__ import annotations

import json
from fractions import Fraction as F
from itertools import product
from math import comb

import sympy as sp


def in_dplus(s: F, g: F) -> bool:
    return 0 < s < 1 and 0 < g < 1 and g > 2 * s - 1


def in_ct(s: F, g: F) -> bool:
    return 0 < s < 1 and s * s < g < 1


def domain_checks() -> dict:
    points = [
        (F(9, 10), F(8_000_001, 10_000_000)),
        (F(1, 10_000), F(1, 10_000_000)),
        (F(999, 1000), F(998_001_001, 1_000_000_000)),
    ]
    assert all(in_dplus(*p) for p in points)
    assert in_ct(*points[-1])

    splits = []
    for s, g in points:
        margin = min(1 - g, 1 - 2 * s + g, 1 - s)
        eps = margin / 3
        a = (s / (1 - eps), g / (1 - eps))
        b = (1 - eps, 1 - eps)
        assert in_dplus(*a) and in_dplus(*b)
        assert a[0] * b[0] == s and a[1] * b[1] == g
        splits.append((a, b))

    # Product closure: the displayed positive remainder proves G > 2S-1
    # when s1,s2 > 1/2; the other case is automatic.
    s1, s2 = sp.symbols("s1 s2")
    remainder = sp.expand((2 * s1 - 1) * (2 * s2 - 1) - (2 * s1 * s2 - 1))
    assert sp.expand(remainder - 2 * (s1 - 1) * (s2 - 1)) == 0

    # A deliberately asymmetric simultaneous CT bridge-gluing test.
    A1, B1, A2, B2 = F(3, 100), F(5), F(7), F(1, 100)
    L = max(F(1), B1 / (A1 * A1), B2 / (A2 * A2))
    U = min(F(1), B1, B2)
    s = F(1, 1_000_000)
    g = (L * s * s + U) / 2
    assert L * s * s < g < U
    assert in_ct(s, g)
    assert in_ct(s / A1, g / B1)
    assert in_ct(s / A2, g / B2)

    return {
        "boundary_points": [[str(x), str(y)] for x, y in points],
        "strict_subdivisions": [
            [[str(x) for x in a], [str(x) for x in b]] for a, b in splits
        ],
        "product_remainder": str(remainder),
        "ct_gluing": {
            "L": str(L), "U": str(U), "s": str(s), "g": str(g),
            "transformed_1": [str(s / A1), str(g / B1)],
            "transformed_2": [str(s / A2), str(g / B2)],
        },
    }


def completion_counts() -> dict:
    cores = ((2, 1, 1), (5, 1, 2), (5, 1, 2), (6, 2, 4), (6, 2, 2))

    def count(k: int, incoming: int) -> int:
        return sum(
            repairs * sum(
                comb(sinks, j) * comb(k - incoming - j + segments - 1, segments - 1)
                for j in range(sinks + 1)
            )
            for segments, sinks, repairs in cores
        )

    got = {
        "C(3,1)": count(3, 1),
        "C(3,0)": count(3, 0),
        "C(4,1)": count(4, 1),
        "C(4,0)": count(4, 0),
        "C(5,1)": count(5, 1),
        "C(5,0)": count(5, 0),
    }
    assert got == {
        "C(3,1)": 289, "C(3,0)": 831, "C(4,1)": 831,
        "C(4,0)": 1983, "C(5,1)": 1983, "C(5,0)": 4155,
    }
    assert 6 * (got["C(4,1)"] + got["C(4,0)"]) * 24 == 405_216
    assert 4 * (got["C(5,1)"] + got["C(5,0)"]) * 120 == 2_946_240
    assert 2 * (got["C(3,1)"] + got["C(3,0)"]) * 6 == 13_440
    return got


def edge(h: int, s, g):
    return 1 if h == 0 else (g if h == 2 else s)


def quartet_checks() -> dict:
    ss = sp.symbols("s1:5")
    gi = sp.symbols("gI")
    topologies = {"A": {0, 1}, "B": {0, 2}, "C": {0, 3}}
    words = {
        "CCCC": (1, 1, 1, 1), "CCTT": (1, 1, 3, 3),
        "CTTC": (1, 3, 3, 1), "CTCT": (1, 3, 1, 3),
    }

    def q(t, word):
        h = 0
        for i in topologies[t]:
            h ^= word[i]
        return sp.prod(ss) * (gi if h == 2 else 1)

    table = {}
    for t in topologies:
        v = {name: q(t, word) for name, word in words.items()}
        fa = sp.expand(v["CCCC"] - v["CCTT"])
        gb = sp.expand(v["CCCC"] - v["CCTT"] - v["CTTC"] + v["CTCT"])
        table[t] = {"F_A": str(fa), "G_B": str(gb)}
    P = sp.prod(ss)
    assert [sp.expand(q(t, words["CCCC"]) - q(t, words["CCTT"])) for t in "ABC"] == [0, sp.expand(P * (1 - gi)), sp.expand(P * (1 - gi))]
    assert [sp.expand(q(t, words["CCCC"]) - q(t, words["CCTT"]) - q(t, words["CTTC"]) + q(t, words["CTCT"])) for t in "ABC"] == [0, sp.expand(2 * P * (1 - gi)), 0]
    return table


def sunlet_and_triangle_checks() -> dict:
    symbols = sp.symbols(
        "a_s a_g b_s b_g c_s c_g d_s d_g e_s e_g f_s f_g delta"
    )
    (a_s, a_g, b_s, b_g, c_s, c_g, d_s, d_g, e_s, e_g,
     f_s, f_g, delta) = symbols
    spectra = {
        "a": (1, a_s, a_g, a_s), "b": (1, b_s, b_g, b_s),
        "c": (1, c_s, c_g, c_s), "d": (1, d_s, d_g, d_s),
        "e": (1, e_s, e_g, e_s), "f": (1, f_s, f_g, f_s),
    }

    def q(x, y, z):
        assert x ^ y ^ z == 0
        return sp.expand(
            spectra["a"][x] * spectra["b"][y] * spectra["c"][z]
            * (delta * spectra["f"][y] * spectra["d"][z]
               + (1 - delta) * spectra["f"][x] * spectra["e"][z])
        )

    xs, xg = q(1, 1, 0), q(2, 2, 0)
    ys, yg = q(1, 0, 1), q(2, 0, 2)
    zs, zg = q(0, 1, 1), q(0, 2, 2)
    u, v, w = q(1, 2, 3), q(1, 3, 2), q(2, 1, 3)
    ti = sp.factor(v * v * xg - xs * xs * yg * zg)
    expected = sp.factor(
        -a_s**2 * b_s**2 * a_g * b_g * c_g**2 * f_s**2
        * delta * (1 - delta) * d_g * e_g * (1 - f_g)**2
    )
    assert sp.expand(ti - expected) == 0

    witness = {
        a_s: F(1, 2), a_g: F(1, 2), b_s: F(1, 2), b_g: F(1, 2),
        c_s: F(1, 2), c_g: F(1, 2), d_s: F(1, 2), d_g: F(1, 2),
        e_s: F(1, 2), e_g: F(1, 2), f_s: F(1, 3), f_g: F(1, 3),
        delta: F(1, 2),
    }
    outputs = (xs, xg, ys, yg, zs, zg, u, v, w)
    jac = sp.Matrix(outputs).jacobian(symbols).subs(witness)
    assert jac.rank() == 9

    j0 = sp.Matrix([
        [1, 1, 0, 1], [1, 0, 1, sp.Rational(1, 4)],
        [0, 1, 1, sp.Rational(1, 4)], [1, 1, 1, 1],
    ])
    jp = sp.Matrix([
        [1, 1, 0, 0, 1], [1, 0, 1, sp.Rational(3, 4), sp.Rational(1, 4)],
        [0, 1, 1, sp.Rational(1, 4), sp.Rational(1, 4)], [-1, 1, 0, 0, 0],
        [-1, 0, 1, sp.Rational(1, 2), -sp.Rational(1, 2)],
    ])
    assert j0.det() == -sp.Rational(1, 2)
    assert jp.det() == -sp.Rational(1, 4)
    return {
        "Ti_factor": str(ti),
        "triangle_outputs": [str(sp.factor(x.subs(witness))) for x in outputs],
        "triangle_rank": jac.rank(),
        "J0_det": str(j0.det()), "Jperp_det": str(jp.det()),
    }


def network_map(arcs, parents, internal_edges):
    params = []
    es = {}
    for u, v in internal_edges:
        pair = sp.symbols(f"s_{u}_{v} g_{u}_{v}")
        es[(u, v)] = pair
        params.extend(pair)
    ls = {r: sp.symbols(f"lambda_{r}") for r in parents}
    params.extend(ls.values())
    patterns = ((0,0,0),(0,1,1),(0,2,2),(1,0,1),(1,1,0),(1,2,3),(1,3,2),(2,0,2),(2,1,3),(2,2,0))
    leaf_index = {"L0": 0, "L1": 1, "L2": 2}
    out = []
    for pattern in patterns:
        total = 0
        for bits in product((0, 1), repeat=len(parents)):
            selected = set(arcs)
            weight = 1
            for (r, (p0, p1)), bit in zip(parents.items(), bits):
                keep, drop = ((p0, r), (p1, r)) if bit == 0 else ((p1, r), (p0, r))
                selected.remove(drop)
                weight *= ls[r] if bit == 0 else 1 - ls[r]
            children = {}
            for u, v in selected:
                children.setdefault(u, []).append(v)
            memo = {}
            def descendants(v):
                if v in memo:
                    return memo[v]
                ans = {leaf_index[v]} if v in leaf_index else set().union(*(descendants(c) for c in children.get(v, ())))
                memo[v] = ans
                return ans
            term = weight
            for e, (s, g) in es.items():
                if e in selected:
                    h = 0
                    for i in descendants(e[1]):
                        h ^= pattern[i]
                    term *= edge(h, s, g)
            total += term
        out.append(sp.factor(total))
    return tuple(out), tuple(params), es, ls


def weak_checks() -> dict:
    arcs1 = (("r","S"),("r","L0"),("S","U"),("S","V"),("U","X"),("V","Z"),("Z","X"),("U","V"),("Z","L1"),("X","L2"))
    edges1 = (("r","S"),("S","U"),("S","V"),("U","X"),("V","Z"),("Z","X"),("U","V"))
    out1, par1, es1, ls1 = network_map(arcs1, {"V": ("S","U"), "X": ("Z","U")}, edges1)
    arcs2 = (("r","S"),("r","L0"),("S","U"),("S","X0"),("V","X0"),("U","X1"),("V","X1"),("U","V"),("X0","L1"),("X1","L2"))
    edges2 = (("r","S"),("S","U"),("S","X0"),("V","X0"),("U","X1"),("V","X1"),("U","V"))
    out2, par2, es2, ls2 = network_map(arcs2, {"X1": ("V","U"), "X0": ("V","S")}, edges2)
    w1 = {z: F(1, 7) for pair in es1.values() for z in pair}
    w1.update({ls1["V"]: F(1, 8), ls1["X"]: F(15996, 16339)})
    w2 = {z: F(1, 4) for pair in es2.values() for z in pair}
    w2.update({ls2["X1"]: F(1, 2), ls2["X0"]: F(1, 6)})
    vals1 = tuple(sp.factor(x.subs(w1)) for x in out1)
    vals2 = tuple(sp.factor(x.subs(w2)) for x in out2)
    expected1 = (1,F(64009,457492),F(64009,457492),F(6400,39229939),F(1,1372),F(4048,39229939),F(4048,39229939),F(6400,39229939),F(4048,39229939),F(1,1372))
    expected2 = (1,F(15,1024),F(15,1024),F(5,512),F(27,512),F(9,4096),F(9,4096),F(5,512),F(9,4096),F(27,512))
    assert vals1 == expected1 and vals2 == expected2
    rank1 = sp.Matrix(out1[1:]).jacobian(par1).subs(w1).rank()
    rank2 = sp.Matrix(out2[1:]).jacobian(par2).subs(w2).rank()
    assert rank1 == rank2 == 9

    delta = F(1, 2**30)
    p1 = (F(86779,80)*delta, F(320,253)*delta, F(114373,20240)*delta)
    p2 = (F(16,3)*delta, F(32,9)*delta, F(96,5)*delta)
    scaled1, scaled2 = [F(1)], [F(1)]
    patterns = ((0,0,0),(0,1,1),(0,2,2),(1,0,1),(1,1,0),(1,2,3),(1,3,2),(2,0,2),(2,1,3),(2,2,0))
    for vals, pendants, dest in ((vals1,p1,scaled1),(vals2,p2,scaled2)):
        for val, pat in zip(vals[1:], patterns[1:]):
            factor = F(1)
            for i,h in enumerate(pat):
                if h: factor *= pendants[i]
            dest.append(F(val) * factor)
    expected_common = [F(1)] + [delta**2]*4 + [F(4,5)*delta**3]*2 + [delta**2] + [F(4,5)*delta**3] + [delta**2]
    assert scaled1 == scaled2 == expected_common

    us, ug, vs, vg = sp.symbols("us ug vs vg", positive=True)
    obs = sp.Matrix([us/vs, us*vs, ug/vg, ug*vg])
    cherry_det = sp.factor(obs.jacobian((us,vs,ug,vg)).det())
    assert cherry_det == 4*ug*us/(vg*vs)
    actual = {us:F(2,5),ug:F(4,9),vs:F(3,7),vg:F(5,11)}
    assert in_ct(actual[us],actual[ug]) and in_ct(actual[vs],actual[vg])
    assert sp.factor(cherry_det.subs(actual)) == F(2464,675)
    return {
        "normalized_1": list(map(str, vals1)), "normalized_2": list(map(str, vals2)),
        "ranks": [rank1, rank2], "common_tensor": list(map(str, scaled1)),
        "cherry_det": str(cherry_det), "cherry_det_witness": "2464/675",
    }


def main() -> None:
    result = {
        "independence": "no submitted code or artifact imported",
        "domain": domain_checks(),
        "completion_counts": completion_counts(),
        "quartets": quartet_checks(),
        "sunlet_triangle": sunlet_and_triangle_checks(),
        "weak_sharpness": weak_checks(),
        "status": "PASS",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
