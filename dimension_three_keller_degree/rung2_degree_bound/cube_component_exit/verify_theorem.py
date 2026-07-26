#!/usr/bin/env python3
"""Self-contained exact checks for the cube-component coordinate theorem."""

from __future__ import annotations

import argparse
from fractions import Fraction


NAMES = "x u v w A cu cv du dv d delta X U W".split()
IDX = {name: i for i, name in enumerate(NAMES)}
NV = len(NAMES)


class Poly:
    def __init__(self, terms=None):
        self.terms = {e: Fraction(c) for e, c in (terms or {}).items() if c}

    @staticmethod
    def constant(c):
        c = Fraction(c)
        return Poly({(0,) * NV: c}) if c else Poly()

    @staticmethod
    def variable(name):
        e = [0] * NV
        e[IDX[name]] = 1
        return Poly({tuple(e): Fraction(1)})

    @staticmethod
    def coerce(value):
        return value if isinstance(value, Poly) else Poly.constant(value)

    def __add__(self, other):
        other = Poly.coerce(other)
        out = dict(self.terms)
        for exponent, coefficient in other.terms.items():
            out[exponent] = out.get(exponent, Fraction(0)) + coefficient
            if out[exponent] == 0:
                del out[exponent]
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({e: -c for e, c in self.terms.items()})

    def __sub__(self, other):
        return self + (-Poly.coerce(other))

    def __rsub__(self, other):
        return Poly.coerce(other) - self

    def __mul__(self, other):
        other = Poly.coerce(other)
        out = {}
        for e, c in self.terms.items():
            for f, d0 in other.terms.items():
                g0 = tuple(a + b for a, b in zip(e, f))
                out[g0] = out.get(g0, Fraction(0)) + c * d0
        return Poly(out)

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        scalar = Fraction(scalar)
        if scalar == 0:
            raise ZeroDivisionError
        return Poly({e: c / scalar for e, c in self.terms.items()})

    def __pow__(self, power):
        if power < 0:
            raise ValueError("negative exponent")
        result, base = Poly.constant(1), self
        while power:
            if power & 1:
                result *= base
            base *= base
            power >>= 1
        return result

    def derivative(self, name):
        j = IDX[name]
        out = {}
        for exponent, coefficient in self.terms.items():
            if exponent[j]:
                reduced = list(exponent)
                multiplier = reduced[j]
                reduced[j] -= 1
                out[tuple(reduced)] = coefficient * multiplier
        return Poly(out)

    def substitute(self, replacements):
        replacements = {IDX[name]: Poly.coerce(value) for name, value in replacements.items()}
        variables = [Poly.variable(name) for name in NAMES]
        result = Poly()
        for exponent, coefficient in self.terms.items():
            term = Poly.constant(coefficient)
            for j, power in enumerate(exponent):
                if power:
                    term *= replacements.get(j, variables[j]) ** power
            result += term
        return result

    def degree(self, names):
        if not self.terms:
            return -1
        js = [IDX[name] for name in names]
        return max(sum(exponent[j] for j in js) for exponent in self.terms)

    def coefficient(self, name, power):
        j = IDX[name]
        out = {}
        for exponent, coefficient in self.terms.items():
            if exponent[j] == power:
                reduced = list(exponent)
                reduced[j] = 0
                out[tuple(reduced)] = coefficient
        return Poly(out)

    def __eq__(self, other):
        return self.terms == Poly.coerce(other).terms


globals().update({name: Poly.variable(name) for name in NAMES})


def require(condition, label):
    if not condition:
        raise AssertionError(label)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mutation",
        choices=("rank2_lead", "coordinate_sign", "degree_boundary"),
    )
    args = parser.parse_args()

    cubic_coefficient = 4 if args.mutation == "rank2_lead" else 3
    base = x**3 + A * x**2 + d * x

    # Rank two: solve the two transverse derivatives.  The remaining
    # derivative is a genuine quadratic with leading coefficient three.
    rank2 = (
        x**3
        + A * x**2
        + cu * x * u
        + cv * x * v
        + (u**2 + v**2) / 2
        + d * x
        + du * u
        + dv * v
    )
    u2 = -(cu * x + du)
    v2 = -(cv * x + dv)
    sub2 = {"u": u2, "v": v2}
    require(rank2.derivative("u").substitute(sub2) == 0, "rank-two u equation")
    require(rank2.derivative("v").substitute(sub2) == 0, "rank-two v equation")
    residual2 = rank2.derivative("x").substitute(sub2)
    require(residual2.degree(("x",)) == 2, "rank-two residual degree")
    require(
        residual2.coefficient("x", 2) == cubic_coefficient,
        "rank-two leading coefficient",
    )

    # Rank one, nonzero x coefficient in the flat direction: an explicit
    # critical point after normalizing that coefficient to one.
    rank1_transverse = (
        x**3
        + A * x**2
        + cu * x * u
        + x * v
        + u**2 / 2
        + d * x
        + du * u
        + delta * v
    )
    x1 = -delta
    u1 = cu * delta - du
    v1 = -(3 * delta**2 - 2 * A * delta + cu * u1 + d)
    sub1 = {"x": x1, "u": u1, "v": v1}
    require(
        all(rank1_transverse.derivative(name).substitute(sub1) == 0 for name in ("x", "u", "v")),
        "rank-one transverse critical point",
    )

    # Rank one, completely flat direction: the residual is again quadratic.
    rank1_flat = base + cu * x * u + u**2 / 2 + du * u
    uflat = -(cu * x + du)
    residual_flat = rank1_flat.derivative("x").substitute({"u": uflat})
    require(residual_flat.degree(("x",)) == 2, "rank-one flat residual degree")
    require(residual_flat.coefficient("x", 2) == 3, "rank-one flat leading coefficient")

    # Rank-one coordinate chart f=v+R(x,u), including the inverse.
    remainder1 = base + cu * x * u + A * u**2 + du * u
    f1 = v + remainder1
    sign = 1 if args.mutation == "coordinate_sign" else -1
    vinverse = W + sign * remainder1.substitute({"x": X, "u": U})
    require(
        vinverse + remainder1.substitute({"x": X, "u": U}) == W,
        "rank-one coordinate inverse",
    )
    require(vinverse.degree(("X", "U", "W")) <= 3, "rank-one inverse degree")

    # Rank-zero independent coefficient vectors: f=g(x)+xu+v.
    f0_independent = base + x * u + v
    v0 = W - (base + x * u).substitute({"x": X, "u": U})
    require(v0 + (base + x * u).substitute({"x": X, "u": U}) == W, "rank-zero independent inverse")
    require(v0.degree(("X", "U", "W")) <= 3, "rank-zero independent degree")

    # Rank-zero c=0,d!=0: f=g(x)+v.
    vconst = W - base.substitute({"x": X})
    require(vconst + base.substitute({"x": X}) == W, "rank-zero constant inverse")

    # Rank-zero dependent vectors: d=delta*c gives a critical point.
    rank0_dependent = base + (x + delta) * u
    udep = -(3 * delta**2 - 2 * A * delta + d)
    dep = {"x": -delta, "u": udep}
    require(rank0_dependent.derivative("x").substitute(dep) == 0, "rank-zero dependent x")
    require(rank0_dependent.derivative("u").substitute(dep) == 0, "rank-zero dependent u")

    # Degree transfer and exact boundary checks.
    requested_d = 36 if args.mutation == "degree_boundary" else 35
    require(3 * requested_d <= 105, "degree-35 arithmetic")
    require(3 * requested_d < 108, "plane floor 108")
    require(3 * 36 == 108, "degree-36 boundary")
    require(3 * 33 == 99 and 99 < 100, "Moh fallback d=33")
    require(3 * 34 == 102 and not (102 < 100), "Moh fallback boundary")

    print("CUBE_COMPONENT_THEOREM_EXACT_PASS")


if __name__ == "__main__":
    main()
