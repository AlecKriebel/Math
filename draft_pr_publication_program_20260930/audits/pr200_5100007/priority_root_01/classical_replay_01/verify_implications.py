"""Exact checks supporting this priority audit; these are not novelty evidence."""
from fractions import Fraction
from math import gcd
import json
from pathlib import Path


def norm_divisor(n, tau):
    step = Fraction(2 * tau, n)
    m = n // gcd(n, 2)
    poles = {}
    generic = step != Fraction(1, 2)
    terms = [(Fraction(1, 2), 2), (Fraction(0), -2)]
    if generic:
        terms = [(Fraction(1, 2), 2),
                 (Fraction(1, 2) + step, 1),
                 (Fraction(1, 2) - step, 1), (Fraction(0), -4)]
    for j in range(m):
        for x, multiplicity in terms:
            x = (x - j * step) % 1
            poles[x] = poles.get(x, 0) + multiplicity
    return {x: order for x, order in poles.items() if order}

checked = 0
for n in range(3, 121):
    for tau in range(1, (n + 1) // 2):
        if gcd(n, tau) != 1:
            continue
        step = Fraction(2 * tau, n)
        m = n // gcd(n, 2)
        group = {(j * step) % 1 for j in range(m)}
        assert len(group) == m
        assert (Fraction(1, 2) in group) == (n % 4 == 0)
        assert (not norm_divisor(n, tau)) == (n % 4 == 0)
        checked += 1

# For a focus (sqrt(3), 0), the squared product of the distances
# from one antipodal pair (x,y),(-x,-y) is rational in x^2,y^2.
def antipodal_squared_product(x2, y2):
    return (x2 + y2 + 3) ** 2 - 12 * x2

rectangle_r_squared = antipodal_squared_product(Fraction(4), Fraction(1)) ** 2
parallelogram_r_squared = (antipodal_squared_product(Fraction(4), Fraction(1, 3)) *
                           antipodal_squared_product(Fraction(4), Fraction(3)))
assert rectangle_r_squared == 16 ** 2
assert parallelogram_r_squared == Fraction(52, 3) ** 2
assert rectangle_r_squared != parallelogram_r_squared
# Tangency of x/4 + sqrt(3)y/2 = 1 to x^2/4+y^2=1:
assert 4 * Fraction(1, 4) ** 2 + Fraction(3, 4) == 1

result = {
    "status": "all exact assertions passed",
    "primitive_torsion_cases_checked": checked,
    "n_range": [3, 120],
    "norm_divisor_vanishes_iff_4_divides_n": True,
    "chasles_nonimplication_control": {
        "rectangle_full_focal_product": "16",
        "oblique_parallelogram_full_focal_product": "52/3",
        "interpretation": "Both circumscribe the same ellipse; this is not a k115 counterexample."
    },
    "limitation": "Finite arithmetic checks supplement the written general argument; no novelty conclusion."
}
Path(__file__).with_name("VALIDATION.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
