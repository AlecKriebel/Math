#!/usr/bin/env python3
"""Exact corroborating calculations; not a verifier for the geometric theorems."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

checks = []
negative_controls = []


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)


def reject(name, false_claim):
    if false_claim:
        raise AssertionError("False shortcut survived: " + name)
    negative_controls.append({"shortcut": name, "rejected": True})


def quadric_euler(d):
    if d not in range(101):
        raise ValueError("Dimension must be between 0 and 100")
    if d < 2:
        return 2
    return 2 + quadric_euler(d - 2)


def weight(euler, discrepancy):
    if discrepancy <= -1:
        raise ValueError("Not a log-terminal discrepancy")
    return F(euler, discrepancy + 1)


def prod_pair(a, b):
    # Pairs contain ordinary and stringy Euler characteristic.
    return (a[0] * b[0], a[1] * b[1])


# Sparse polynomials in x,y,w1,w2,w3,v1,v2,v3, with rational coefficients.
NVAR = 8


def const(c):
    return {(0,) * NVAR: F(c)} if c else {}


def var(i):
    e = [0] * NVAR
    e[i] = 1
    return {tuple(e): F(1)}


def add(*polys):
    out = {}
    for p in polys:
        for e, c in p.items():
            out[e] = out.get(e, F(0)) + c
    return {e: c for e, c in out.items() if c}


def scale(c, p):
    return {e: F(c) * a for e, a in p.items() if c * a}


def mul(p, q):
    out = {}
    for e, c in p.items():
        for f, d in q.items():
            ef = tuple(a + b for a, b in zip(e, f))
            out[ef] = out.get(ef, F(0)) + c * d
    return {e: c for e, c in out.items() if c}


def square(p):
    return mul(p, p)


def run():
    checks.clear()
    negative_controls.clear()
    check("Q3 Euler characteristic", quadric_euler(3) == 4)
    check("Q4 Euler characteristic", quadric_euler(4) == 6)
    for d in range(21):
        check(f"quadric parity formula dimension {d}",
              quadric_euler(d) == d + 1 + (d % 2 == 0))
    cone = (F(1), weight(quadric_euler(3), 2))
    check("affine quadric cone stringy value", cone == (F(1), F(4, 3)))
    check("affine quadric cone strict deficit", cone[1] - cone[0] == F(1, 3))
    torus = (F(0), F(0))
    check("literal-statement product has both Euler numbers zero",
          prod_pair(cone, torus) == (F(0), F(0)))
    special = (F(5), F(4) + weight(4, 2))
    general = (F(6), F(6))
    check("projective singular quadric stringy value", special[1] == F(16, 3))
    check("projective singular quadric deficit", special[1] - special[0] == F(1, 3))
    check("resolution upper bound", special[1] < F(8))
    check("Grassmannian Gr(2,5) cone arithmetic", F(10, 5) == 2)
    for ex in range(1, 5):
        for ez in range(1, 5):
            for dx in (F(0), F(1, 3), F(2)):
                for dz in (F(0), F(2, 5), F(1)):
                    lhs = (ex + dx) * (ez + dz) - ex * ez
                    rhs = dx * ez + dz * ex + dx * dz
                    check("product deficit identity", lhs == rhs)
                    check("positive-factor equality test", (lhs == 0) == (dx == dz == 0))
    # Symbolically check the entire unipotent quadratic-form calculation.
    x, y = var(0), var(1)
    w = [var(i) for i in range(2, 5)]
    v = [var(i) for i in range(5, 8)]
    q_w = add(*(square(a) for a in w))
    q_v = add(*(square(a) for a in v))
    dot = add(*(mul(a, b) for a, b in zip(w, v)))
    x_new = add(x, scale(-1, dot), scale(F(-1, 2), mul(y, q_v)))
    w_new = [add(a, mul(y, b)) for a, b in zip(w, v)]
    original = add(scale(2, mul(x, y)), q_w)
    transformed = add(scale(2, mul(x_new, y)), *(square(a) for a in w_new))
    check("symbolic Borel-open-orbit transformation preserves q", transformed == original)
    check("toric determinant-one control", 1 * 1 - 0 * 0 == 1)
    check("nonunimodular toric control has index two", 1 * 2 - 0 * 1 == 2)
    reject("omit the +1 in a stringy denominator", F(4, 2) == cone[1])
    reject("all stringy Euler numbers in this class are integral", cone[1].denominator == 1)
    reject("positive weight and nonnegative Euler imply local contribution >=1", weight(1, 1) >= 1)
    reject("ordinary Euler invariant in the proper flat quadric family", special[0] == general[0])
    reject("stringy Euler invariant in the proper flat quadric family", special[1] == general[1])
    reject("Euler deficit invariant in the proper flat quadric family",
           special[1] - special[0] == general[1] - general[0])
    reject("a singular factor always forces a positive product deficit",
           prod_pair(cone, torus)[1] > prod_pair(cone, torus)[0])
    reject("smooth even-dimensional quadric has one cell in every even degree",
           quadric_euler(4) == 5)
    reject("simplicial implies unimodular", 2 == 1)
    return {
        "schema": "stringy-30002003-exact-checks-v1",
        "all_checks_passed": True,
        "exact_checks": len(checks),
        "negative_controls_rejected": len(negative_controls),
        "controls": negative_controls,
        "values": {
            "affine_quadric_cone": {"ordinary": "1", "stringy": "4/3", "deficit": "1/3"},
            "cone_times_Cstar": {"ordinary": "0", "stringy": "0", "deficit": "0"},
            "projective_special_quadric": {"ordinary": "5", "stringy": "16/3", "deficit": "1/3"},
            "projective_smooth_quadric": {"ordinary": "6", "stringy": "6", "deficit": "0"}
        },
        "limits": "Finite exact corroboration only. The written proofs establish geometry; no universal conjecture is computationally certified."
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-results", action="store_true")
    parser.add_argument("--check-manifest", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    result = run()
    output = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.write_results:
        (root / "CHECK_RESULTS.json").write_text(output)
    if args.check_manifest:
        manifest = json.loads((root / "AUTHOR_MANIFEST.json").read_text())
        for entry in manifest["files"]:
            raw = (root / entry["path"]).read_bytes()
            assert len(raw) == entry["bytes"], entry["path"]
            assert hashlib.sha256(raw).hexdigest() == entry["sha256"], entry["path"]
        print("AUTHOR_MANIFEST: all listed sizes and SHA-256 hashes match")
    print(output, end="")
