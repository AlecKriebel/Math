#!/usr/bin/env python3
"""Finite ray-kernel tests; not a calculation of CM K2 values.

Enumerates abelian X,Y and a common embedded cyclic unit group U. Checks
G=(X x Y)/diag(U), the two quotient kernels, the field degrees and the
multiplicity |U| in the norm/restriction base-change identity.
Uses runtime checks rather than removable asserts.
"""
import itertools
import json
import math
from pathlib import Path


def elems(moduli):
    return list(itertools.product(*(range(m) for m in moduli)))


def add(x, y, mods):
    return tuple((a + b) % m for a, b, m in zip(x, y, mods))


def mul(k, x, mods):
    return tuple((k * a) % m for a, m in zip(x, mods))


def order(x, mods):
    return math.lcm(*(m // math.gcd(a, m) for a, m in zip(x, mods)))


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def test_case(xmods, ymods, ux, uy, u):
    mods = xmods + ymods
    X, Y = elems(xmods), elems(ymods)
    zX, zY = (0,) * len(xmods), (0,) * len(ymods)
    U = [mul(k, ux + uy, mods) for k in range(u)]
    require(len(set(U)) == u, "diagonal unit injection")
    canon = lambda a: min(add(a, v, mods) for v in U)
    G = {canon(x + y) for x in X for y in Y}
    HN = {canon(zX + y) for y in Y}
    HMf = {canon(x + zY) for x in X}
    require(len(G) == len(X) * len(Y) // u, "total ray degree")
    require(len(HN) == len(Y), "high N kernel degree")
    require(len(HMf) == len(X), "low Mf kernel degree")
    require(len(HN & HMf) == u, "compositum deficit")
    require({canon(add(a, b, mods)) for a in HN for b in HMf} == G,
            "field intersection is low ray field")
    require(len(G) // len(HN) == len(X) // u, "N/M ray degree")
    require(len(G) // len(HMf) == len(Y) // u, "Mf/M ray degree")
    # Image of HMf in G/HN is X/U_X. Each coset occurs |U| times,
    # the exact coefficient in Cor_{T/B} res_{T/K}.
    UX = [mul(k, ux, xmods) for k in range(u)]
    xcanon = lambda x: min(add(x, v, xmods) for v in UX)
    multiplicities = {}
    for x in X:
        key = xcanon(x)
        multiplicities[key] = multiplicities.get(key, 0) + 1
    require(set(multiplicities.values()) == {u}, "norm base-change coefficient")
    return {"X": list(xmods), "Y": list(ymods), "unit_order": u,
            "unit_generator_X": list(ux), "unit_generator_Y": list(uy),
            "G_order": len(G), "relative_N_degree": len(X) // u,
            "relative_Mf_degree": len(Y) // u, "compositum_deficit": u}


def main():
    choices = [(2,), (3,), (4,), (6,), (8,), (12,), (2, 2), (4, 2), (6, 2)]
    results = []
    for xm in choices:
        for ym in choices:
            for u in (1, 2, 3, 4, 6):
                # Every possible embedding of the abstract cyclic unit group.
                for ux in (x for x in elems(xm) if order(x, xm) == u):
                    for uy in (y for y in elems(ym) if order(y, ym) == u):
                        results.append(test_case(xm, ym, ux, uy, u))
    report = {
        "status": "PASS",
        "cases": len(results),
        "unit_orders": sorted({r["unit_order"] for r in results}),
        "cases_with_nontrivial_unit_correction": sum(r["unit_order"] > 1 for r in results),
        "checks_per_case": 9,
        "note": "Finite group verification only; does not prove geometric specialization or compute CM K2 values.",
        "examples": results[:3] + [r for r in results if r["unit_order"] == 4][-3:],
    }
    out = Path(__file__).with_name("UNIT_RAY_SQUARE_CHECK.json")
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
