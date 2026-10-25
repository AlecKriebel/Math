"""Independent exact arithmetic corroboration; not a universal proof."""
from fractions import Fraction
import json
import math


def singular_spaces(dimension, k, q, kind, epsilon):
    count = Fraction(1)
    for j in range(k):
        d = dimension - 2 * j
        if kind == "Sp":
            vectors = q**d - 1
        elif d % 2:
            vectors = q ** (d - 1) - 1
        else:
            m = d // 2
            vectors = (q ** (m - 1) + epsilon) * (q**m - epsilon)
        count *= Fraction(vectors, q ** (k - j) - 1)
    return count


cases = 0
for q in (3, 5, 7, 9, 11):
    for kind in ("Sp", "O"):
        for dimension in range(1, 41):
            if kind == "Sp" and dimension % 2:
                continue
            for epsilon in (-1, 1):
                witt = dimension // 2
                if kind == "O" and dimension % 2 == 0 and epsilon == -1:
                    witt -= 1
                for k in range(witt + 1):
                    count = singular_spaces(dimension, k, q, kind, epsilon)
                    sigma = -1 if kind == "Sp" else 1
                    exponent = k * dimension - (3 * k * k + sigma * k) // 2
                    assert count.denominator == 1
                    assert Fraction(1, 2) * q**exponent <= count <= 8 * q**exponent
                    cases += 1

for minimum, factor in ((8192, 576), (32768, 1536)):
    assert minimum >= factor * (1 + math.log(minimum))
    assert 1 - factor / minimum > 0

assert Fraction(7, 8) ** 4 > Fraction(1, 2)
assert Fraction(7, 6) ** 4 / (2 * Fraction(8, 3) ** 2) == Fraction(2401, 18432)
assert Fraction(2401, 18432) > Fraction(1, 8)
assert Fraction(16) * 128 / 21 < 128
assert -Fraction(1, 2) + Fraction(1, 16) + Fraction(1, 14) < -Fraction(1, 3)

print(json.dumps({"status": "PASS", "singular_subspace_cases": cases,
                  "universal_mathematics_certified": False}, indent=2))
