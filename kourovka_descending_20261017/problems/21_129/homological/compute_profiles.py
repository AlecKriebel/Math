#!/usr/bin/env python3
"""Exact finite Coxeter-matrix and Euler calculations. Standard library only.

This computes arithmetic data, not any new quasi-isometry invariant.
Characteristic-polynomial coefficients below are in descending order.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from math import gcd, prod
import json
from pathlib import Path


@dataclass(frozen=True)
class Q5:
    a: F = F(0)
    b: F = F(0)

    def __post_init__(self):
        object.__setattr__(self, "a", F(self.a))
        object.__setattr__(self, "b", F(self.b))

    def __add__(self, other):
        other = asq(other)
        return Q5(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return Q5(-self.a, -self.b)

    def __sub__(self, other):
        return self + -asq(other)

    def __mul__(self, other):
        other = asq(other)
        return Q5(self.a * other.a + 5 * self.b * other.b,
                  self.a * other.b + self.b * other.a)

    __rmul__ = __mul__

    def __truediv__(self, rational):
        return Q5(self.a / rational, self.b / rational)

    def conjugate(self):
        return Q5(self.a, -self.b)

    def __str__(self):
        return str(self.a) if not self.b else f"({self.a})+({self.b})sqrt(5)"


def asq(x):
    return x if isinstance(x, Q5) else Q5(x)


def identity(n):
    return [[Q5(int(i == j)) for j in range(n)] for i in range(n)]


def matmul(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), Q5())
             for j in range(len(b[0]))] for i in range(len(a))]


def power(a, n):
    out = identity(len(a))
    while n:
        if n % 2:
            out = matmul(out, a)
        a = matmul(a, a)
        n //= 2
    return out


def charpoly(a):
    """Faddeev-LeVerrier over the exact field Q(sqrt(5))."""
    n = len(a)
    b, coefficients = identity(n), [Q5(1)]
    for k in range(1, n + 1):
        ab = matmul(a, b)
        c = -sum((ab[i][i] for i in range(n)), Q5()) / k
        coefficients.append(c)
        b = [[ab[i][j] + c * int(i == j) for j in range(n)] for i in range(n)]
    return coefficients


def polymul(a, b):
    out = [Q5()] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = out[i + j] + x * y
    return out


def exact_polydiv(a, b):
    """Monic polynomial exact division, descending coefficient order."""
    a = [asq(x) for x in a]
    b = [asq(x) for x in b]
    assert b[0] == Q5(1)
    out = [Q5()] * (len(a) - len(b) + 1)
    for i in range(len(out)):
        out[i] = a[i]
        for j, x in enumerate(b):
            a[i + j] = a[i + j] - out[i] * x
    assert all(x == Q5() for x in a)
    return out


def cyclotomic(n):
    out = [Q5(1)] + [Q5()] * (n - 1) + [Q5(-1)]
    for d in range(1, n):
        if n % d == 0:
            out = exact_polydiv(out, cyclotomic(d))
    return out


def coxeter_matrix(kind, n):
    cartan = [[Q5(2 * int(i == j)) for j in range(n)] for i in range(n)]
    if kind in ("F", "H"):
        edges = [(i, i + 1) for i in range(n - 1)]
    elif kind == "D":
        edges = [(i, i + 1) for i in range(n - 2)] + [(n - 3, n - 1)]
    elif kind == "E":
        edges = [(i, i + 1) for i in range(n - 2)] + [(2, n - 1)]
    else:
        raise ValueError(kind)
    for i, j in edges:
        cartan[i][j] = cartan[j][i] = Q5(-1)
    if kind == "F":
        cartan[1][2] = Q5(-2)  # nonsymmetric crystallographic Cartan matrix
    elif kind == "H":
        cartan[0][1] = cartan[1][0] = Q5(F(-1, 2), F(-1, 2))
    c = identity(n)
    for i in range(n):
        s = identity(n)
        s[i] = [s[i][j] - cartan[i][j] for j in range(n)]
        c = matmul(c, s)
    return c


DATA = {
    "F4": (12, [1, 5, 7, 11]),
    "H4": (30, [1, 11, 19, 29]),
    "D6": (10, [1, 3, 5, 5, 7, 9]),
    "E6": (12, [1, 4, 5, 7, 8, 11]),
    "D7": (12, [1, 3, 5, 6, 7, 9, 11]),
    "E7": (18, [1, 5, 7, 9, 11, 13, 17]),
    "D8": (14, [1, 3, 5, 7, 7, 9, 11, 13]),
    "E8": (30, [1, 7, 11, 13, 17, 19, 23, 29]),
}


def main():
    rows = []
    for typ, (h, exponents) in DATA.items():
        n = len(exponents)
        c = coxeter_matrix(typ[0], n)
        characteristic = charpoly(c)
        assert power(c, h) == identity(n)
        assert all(power(c, d) != identity(n) for d in range(1, h) if h % d == 0)
        if typ != "H4":
            expected = [Q5(1)]
            for m in sorted({h // gcd(h, e) for e in exponents}):
                primitive = [k * h // m for k in range(1, m + 1) if gcd(k, m) == 1]
                actual = [e for e in exponents if h // gcd(h, e) == m]
                repetitions, remainder = divmod(len(actual), len(primitive))
                assert not remainder and sorted(actual) == sorted(primitive * repetitions)
                for _ in range(repetitions):
                    expected = polymul(expected, cyclotomic(m))
            assert characteristic == expected
        else:
            # Exact H4 spectral certificate; the root selection is proved in PROFILE_TABLE.md.
            a = Q5(F(1, 2), F(-1, 2))
            assert characteristic == [Q5(1), a, a, a, Q5(1)]
            assert polymul(characteristic, [x.conjugate() for x in characteristic]) == cyclotomic(30)
        poincare = [1]  # ascending order
        for e in exponents[1:]:
            out = [0] * (len(poincare) + 1)
            for k, value in enumerate(poincare):
                out[k] += value
                out[k + 1] += e * value
            poincare = out
        chi = sum((-1) ** k * value for k, value in enumerate(poincare))
        top_l2 = prod(e - 1 for e in exponents[1:])
        assert top_l2 == (-1) ** (n - 1) * chi > 0
        rows.append({"type": typ, "rank": n, "d": n - 1, "h": h,
                     "exponents": exponents, "coxeter_characteristic_descending": [str(x) for x in characteristic],
                     "decone_poincare_ascending": poincare, "decone_euler": chi,
                     "top_l2_betti_Q": top_l2,
                     "top_two_full_laplacian_heat_exponents_P": [1, 1]})
    out = Path(__file__).with_name("profiles.json")
    out.write_text(json.dumps(rows, indent=2) + "\n")
    print("Validated exact matrix orders, characteristic polynomials, and Euler products for 8 types.")
    for row in rows:
        print(f"{row['type']}: d={row['d']}, c={row['top_l2_betti_Q']}, chi={row['decone_euler']}")


if __name__ == "__main__":
    main()
