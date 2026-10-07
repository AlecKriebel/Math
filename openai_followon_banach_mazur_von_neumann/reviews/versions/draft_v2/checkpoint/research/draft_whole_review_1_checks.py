"""Independent exact noncommutative check of family295's central homotopy.

Algebra: M_2(C) direct sum C. Coefficient module: the M_2(C) summand.
Integer matrix-unit arithmetic tests all cochain basis vectors in degrees 0--3.
This is a finite mechanism check, not proof of the infinite-dimensional input.
"""
from itertools import product
from pathlib import Path
import json

ZERO = (0, 0, 0, 0)


def add(u, v, factor=1):
    return tuple(a + factor * b for a, b in zip(u, v))


def alg_mul(a, b):
    if a == 4 or b == 4:
        return 4 if a == b == 4 else None
    i, j = divmod(a, 2)
    k, ell = divmod(b, 2)
    return 2 * i + ell if j == k else None


def action(a, value, right=False):
    out = [0] * 4
    for b, coefficient in enumerate(value):
        c = alg_mul(b, a) if right else alg_mul(a, b)
        if c is not None and c != 4:
            out[c] += coefficient
    return tuple(out)


def differential(f, n):
    def result(xs):
        value = action(xs[0], f(xs[1:]))
        for j in range(n):
            merged = alg_mul(xs[j], xs[j + 1])
            if merged is not None:
                value = add(value, f(xs[:j] + (merged,) + xs[j + 2:]), (-1) ** (j + 1))
        return add(value, action(xs[-1], f(xs[:-1]), right=True), (-1) ** (n + 1))
    return result


def homotopy(f, n):
    if n <= 1:
        return lambda xs: ZERO
    def result(xs):
        value = ZERO
        for i in range(n - 1):
            if all(x != 4 for x in xs[:i]) and xs[i] == 4:
                value = add(value, f(xs[:i] + (4, 4) + xs[i + 1:]), (-1) ** (i + 1))
        return value
    return result


rows = []
for n in range(4):
    tuples = list(product(range(5), repeat=n))
    count = 0
    for basis in tuples:
        for output in range(4):
            unit = tuple(int(j == output) for j in range(4))
            f = lambda xs, basis=basis, unit=unit: unit if xs == basis else ZERO
            jd = homotopy(differential(f, n), n + 1)
            dj = (lambda xs: ZERO) if n == 0 else differential(homotopy(f, n), n - 1)
            for xs in tuples:
                cut = f(xs) if all(x != 4 for x in xs) else ZERO
                assert add(dj(xs), jd(xs)) == add(f(xs), cut, -1), (n, basis, output, xs)
                count += 4
    rows.append({"degree": n, "cochain_basis_size": len(tuples) * 4,
                 "scalar_equations": count, "passed": True})

result = {"scope": "Exact finite noncommutative homotopy check only.",
          "algebra": "M_2(C) direct sum C", "module": "M_2(C) first summand", "rows": rows,
          "scalar_equations": sum(row["scalar_equations"] for row in rows), "passed": True}
target = Path(__file__).with_suffix(".json")
target.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
