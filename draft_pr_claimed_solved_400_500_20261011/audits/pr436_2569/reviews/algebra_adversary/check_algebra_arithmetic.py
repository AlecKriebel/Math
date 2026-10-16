#!/usr/bin/env python3
"""Targeted exact replay of the reviewed algebraic scalar identities.

Enumerates SL2(F5) and computes element orders/squares. Character values and
modular input vectors are the mathematical inputs individually source-checked
in PROOF_RECONSTRUCTION.md; this does not reconstruct their representations or
prove their irreducibility from class functions alone. Explicit failure checks
remain active under python -O. Writes only the explicitly chosen own output.
"""
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import json


def require(condition, label):
    if not condition:
        raise RuntimeError(label)


def multiply(x, y):
    a, b, c, d = x
    e, f, g, h = y
    return ((a*e+b*g) % 5, (a*f+b*h) % 5,
            (c*e+d*g) % 5, (c*f+d*h) % 5)


identity = (1, 0, 0, 1)
central = (4, 0, 0, 4)
group = [x for x in product(range(5), repeat=4)
         if (x[0]*x[3]-x[1]*x[2]) % 5 == 1]
require(len(group) == 120, "determinant-one group order")


def element_order(g):
    power = identity
    for n in range(1, 121):
        power = multiply(power, g)
        if power == identity:
            return n
    raise RuntimeError("element order bound")


orders = {g: element_order(g) for g in group}
counts = dict(sorted(Counter(orders.values()).items()))
require(counts == {1:1, 2:1, 3:20, 4:30, 5:24, 6:20, 10:24},
        "element order counts")
require({g for g in group if orders[g] == 2} == {central},
        "unique involution")
plus = {1:4, 2:4, 3:1, 4:0, 5:-1, 6:1, 10:-1}
minus = {1:4, 2:-4, 3:1, 4:0, 5:-1, 6:-1, 10:1}
norm = Fraction(sum(minus[orders[g]]**2 for g in group), 120)
indicator = Fraction(sum(minus[orders[multiply(g,g)]] for g in group), 120)
orthogonality = Fraction(sum(plus[orders[g]]*minus[orders[g]] for g in group), 120)
forced = {g: 2*plus[orders[g]] if orders[g] % 2 else 0 for g in group}
require(all(forced[g] == plus[orders[g]]+minus[orders[g]] for g in group),
        "forced character equality")
multiplicity = Fraction(sum(forced[g]*minus[orders[g]] for g in group), 120)
require(norm == 1 and indicator == -1 and orthogonality == 0 and multiplicity == 1,
        "character scalar identities")
quotient_rows = [(4,2,0), (4,3,0), (0,0,1)]
reductions = [(1,0,0), (1,1,0), (0,0,1)]  # V1,V5,V4
coefficients = [(4,4,0), (2,6,0), (0,0,2)]
targets = [tuple(2*v for v in row) for row in quotient_rows]
for target, coeff in zip(targets, coefficients):
    require(all(c >= 0 for c in coeff), "positive coefficients")
    actual = tuple(sum(coeff[i]*reductions[i][j] for i in range(3))
                   for j in range(3))
    require(actual == target, "positive witness equality")
dimensions = [sum(a*b for a,b in zip(t, (1,4,4))) for t in targets]
require(dimensions == [24,32,8], "PIM dimensions")
require(sum(a*b for a,b in zip(dimensions, (1,2,4))) == 120,
        "regular module dimensions")
result = {
    "scope": "Scalar verification from source-checked character/modular inputs; not a representation-existence proof or full package replay",
    "SL2F5_order": len(group), "element_order_counts": counts,
    "character_norm": str(norm), "Frobenius_Schur_indicator": str(indicator),
    "degree4_inner_product": str(orthogonality),
    "forced_quaternionic_multiplicity": str(multiplicity),
    "witness_rows": targets, "witness_coefficients_V1_V5_V4": coefficients,
    "PIM_dimensions": dimensions,
    "all_explicit_failure_checks_passed": True,
}
output = Path(__file__).with_name("algebra_arithmetic_results.json")
output.write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps(result, indent=2))
