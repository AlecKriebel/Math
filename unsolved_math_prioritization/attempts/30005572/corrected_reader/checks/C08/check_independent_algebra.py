#!/usr/bin/env python3
"""Finite checks only; the acceptance report supplies the general arguments."""
import json
from pathlib import Path

checks = []
for p in [5, 7, 11, 13, 17, 19, 23]:
    for kind in ["split", "inert", "ramified"]:
        nonsquare = next(n for n in range(1, p) if pow(n, (p - 1) // 2, p) == p - 1)
        trace, value = {"split": (1, 0), "inert": (0, nonsquare), "ramified": (0, 0)}[kind]

        def product(x, y):
            a, b = x
            c, d = y
            return ((a*c + b*d*value) % p, (a*d + b*c + b*d*trace) % p)

        def norm(x):
            a, b = x
            return (a*a + a*b*trace - b*b*value) % p

        ideals = {"zero": [(0, 0)], "whole": [(a, b) for a in range(p) for b in range(p)]}
        if kind == "split":
            ideals.update({"first": [(0, b) for b in range(p)], "second": [(a, -a % p) for a in range(p)]})
        if kind == "ramified":
            ideals["maximal"] = [(0, b) for b in range(p)]
        for name, ideal in ideals.items():
            frozen = all((norm(((1+a) % p, b)) - 1) % p == 0 for a, b in ideal)
            squarezero = all(product(x, y) == (0, 0) for x in ideal for y in ideal)
            if frozen != squarezero:
                raise RuntimeError((p, kind, name))
            checks.append({"p": p, "type": kind, "ideal": name,
                           "coefficient_ideal_vanishes_mod_p": frozen,
                           "ideal_square_zero": squarezero})

x, y = (-1, 3, -2), (2, 1, -3)
wedge = [x[i]*y[j] - x[j]*y[i] for i, j in [(0, 1), (0, 2), (1, 2)]]
if wedge != [-7, 7, -7]:
    raise RuntimeError(wedge)

# Only a counterexample to the algebraic implication, not to actual theta data.
f, coefficients = (0, 1), (9, 32)
bezout, other_bezout = (-7, 2), (25, -7)
for r in [bezout, other_bezout]:
    if sum(a*b for a, b in zip(coefficients, r)) != 1:
        raise RuntimeError("Incorrect Bezout vector")
outputs = [sum(a*b for a, b in zip(f, r)) % 7 for r in [bezout, other_bezout]]
if outputs[0] == outputs[1]:
    raise RuntimeError("Torsion model did not distinguish the choices")

result = {
    "quadratic_residue_ring_tests": checks,
    "cyclic7_wedge_coefficients": wedge,
    "cancellation_gap_model": {
        "module": "Z/7", "a": list(coefficients), "f": list(f),
        "bezout_vectors": [bezout, other_bezout], "outputs": outputs,
        "scope": "Only a counterexample to the canceled algebraic implication; not to actual auxiliary theta compatibility."
    },
    "status": "all independent checks passed"
}
output = Path(__file__).with_name("INDEPENDENT_ALGEBRA_CHECKS.json")
output.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"status": result["status"], "quadratic_cases": len(checks),
                  "cyclic7_wedge": wedge, "torsion_model_outputs": outputs}))
