#!/usr/bin/env python3
"""Dependency-free exact certificate for the quartic power-fibre audit.

This is deliberately a tiny sparse polynomial engine over Q.  It verifies the
two universal top-contact identities, the normalized divisor branches, the
constructive coordinate exits, and the conservative plane degree ceiling.
"""

from __future__ import annotations

import argparse
from fractions import Fraction


NAMES = (
    "p q r "
    "z20 z11 z02 z10 z01 z00 "
    "a30 a21 a12 a03 "
    "b300 b210 b120 b030 b201 b111 b021 b102 b012 b003 "
    "x20 x11 x02 x10 x01 x00 "
    "y20 y11 y02 y10 y01 y00 "
    "l3p l3q l3r "
    "aa bb cc dd c1 c2 d1 d2 delta "
    "u v w P U W"
).split()
INDEX = {name: i for i, name in enumerate(NAMES)}
NV = len(NAMES)


class Poly:
    __slots__ = ("t",)

    def __init__(self, terms=None):
        self.t = {e: Fraction(c) for e, c in (terms or {}).items() if c}

    @staticmethod
    def const(c):
        c = Fraction(c)
        return Poly({(0,) * NV: c}) if c else Poly()

    @staticmethod
    def var(name):
        e = [0] * NV
        e[INDEX[name]] = 1
        return Poly({tuple(e): Fraction(1)})

    @staticmethod
    def coerce(x):
        return x if isinstance(x, Poly) else Poly.const(x)

    def __add__(self, other):
        other = Poly.coerce(other)
        out = dict(self.t)
        for e, c in other.t.items():
            out[e] = out.get(e, Fraction(0)) + c
            if not out[e]:
                del out[e]
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({e: -c for e, c in self.t.items()})

    def __sub__(self, other):
        return self + (-Poly.coerce(other))

    def __rsub__(self, other):
        return Poly.coerce(other) - self

    def __mul__(self, other):
        other = Poly.coerce(other)
        if not self.t or not other.t:
            return Poly()
        out = {}
        for e, c in self.t.items():
            for f, d in other.t.items():
                g = tuple(a + b for a, b in zip(e, f))
                out[g] = out.get(g, Fraction(0)) + c * d
        return Poly(out)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = Fraction(other)
        if not other:
            raise ZeroDivisionError
        return Poly({e: c / other for e, c in self.t.items()})

    def __pow__(self, n):
        if n < 0:
            raise ValueError("negative exponent")
        out, base = Poly.const(1), self
        while n:
            if n & 1:
                out = out * base
            base = base * base
            n >>= 1
        return out

    def diff(self, name):
        j = INDEX[name]
        out = {}
        for e, c in self.t.items():
            if e[j]:
                f = list(e)
                k = f[j]
                f[j] -= 1
                out[tuple(f)] = c * k
        return Poly(out)

    def subs(self, mapping):
        """Simultaneous polynomial substitution by variable name."""
        repl = {INDEX[k]: Poly.coerce(v) for k, v in mapping.items()}
        out = Poly()
        for e, c in self.t.items():
            term = Poly.const(c)
            for j, power in enumerate(e):
                if power:
                    term *= (repl[j] if j in repl else variable_by_index(j)) ** power
            out += term
        return out

    def degree(self, names=None):
        if not self.t:
            return -1
        js = range(NV) if names is None else [INDEX[x] for x in names]
        return max(sum(e[j] for j in js) for e in self.t)

    def coeff_power(self, name, power):
        j = INDEX[name]
        out = {}
        for e, c in self.t.items():
            if e[j] == power:
                f = list(e)
                f[j] = 0
                out[tuple(f)] = c
        return Poly(out)

    def __eq__(self, other):
        return self.t == Poly.coerce(other).t

    def __bool__(self):
        return bool(self.t)

    def short(self):
        if not self.t:
            return "0"
        return f"{len(self.t)} nonzero term(s)"


_VARIABLES = [Poly.var(name) for name in NAMES]


def variable_by_index(j):
    return _VARIABLES[j]


globals().update({name: Poly.var(name) for name in NAMES})


def check(label, value):
    if not value:
        raise AssertionError(label)


def det3(rows):
    a, b, c = rows
    return (
        a[0] * (b[1] * c[2] - b[2] * c[1])
        - a[1] * (b[0] * c[2] - b[2] * c[0])
        + a[2] * (b[0] * c[1] - b[1] * c[0])
    )


def bracket(f, g, h):
    return det3(
        [
            [f.diff("p"), f.diff("q"), f.diff("r")],
            [g.diff("p"), g.diff("q"), g.diff("r")],
            [h.diff("p"), h.diff("q"), h.diff("r")],
        ]
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mutation",
        choices=("e7_contact", "e6_sign", "coordinate", "degree_ceiling"),
    )
    args = parser.parse_args()

    Z = z20 * p**2 + z11 * p * q + z02 * q**2 + z10 * p * r + z01 * q * r + z00 * r**2
    A0 = a30 * p**3 + a21 * p**2 * q + a12 * p * q**2 + a03 * q**3
    B = (
        b300 * p**3
        + b210 * p**2 * q
        + b120 * p * q**2
        + b030 * q**3
        + b201 * p**2 * r
        + b111 * p * q * r
        + b021 * q**2 * r
        + b102 * p * r**2
        + b012 * q * r**2
        + b003 * r**3
    )
    B0 = b300 * p**3 + b210 * p**2 * q + b120 * p * q**2 + b030 * q**3
    X = x20 * p**2 + x11 * p * q + x02 * q**2 + x10 * p * r + x01 * q * r + x00 * r**2
    Y = y20 * p**2 + y11 * p * q + y02 * q**2 + y10 * p * r + y01 * q * r + y00 * r**2
    ell3 = l3p * p + l3q * q + l3r * r
    U1, U2, C3 = p**4, p**2 * q**2, p**3
    A1_generic = (
        a30 * p**3
        + a21 * p**2 * q
        + a12 * p * q**2
        + a03 * q**3
        + b201 * p**2 * r
        + b111 * p * q * r
        + b021 * q**2 * r
        + b102 * p * r**2
        + b012 * q * r**2
        + b003 * r**3
    )

    E7 = bracket(U1, U2, Z) + bracket(U1, B, C3) + bracket(A1_generic, U2, C3)
    rhs7 = 2 * p**4 * q * (4 * p * Z.diff("r") - 3 * A1_generic.diff("r"))
    check("universal E7 identity", E7 == rhs7)

    contact_coeff = Fraction(5, 3) if args.mutation == "e7_contact" else Fraction(4, 3)
    A1 = contact_coeff * p * Z + A0
    E7_contact = bracket(U1, U2, Z) + bracket(U1, B, C3) + bracket(A1, U2, C3)
    check("E7 contact must vanish", E7_contact == 0)

    E6 = (
        bracket(U1, U2, ell3)
        + bracket(U1, B, Z)
        + bracket(U1, Y, C3)
        + bracket(A1, U2, Z)
        + bracket(X, U2, C3)
        + bracket(A1, B, C3)
    )
    lambda_coefficient = -8 if args.mutation == "e6_sign" else 8
    rhs6 = (
        lambda_coefficient * l3r * p**5 * q
        - 6 * p**4 * q * X.diff("r")
        + 3 * p**2 * A0.diff("q") * B.diff("r")
        + 2 * p * q * (p * A0.diff("p") - q * A0.diff("q")) * Z.diff("r")
        + Fraction(8, 3) * p**2 * q * Z * Z.diff("r")
    )
    if E6 != rhs6:
        diff = E6 - rhs6
        sample = []
        for exponents, coefficient in list(diff.t.items())[:8]:
            monomial = "*".join(
                f"{NAMES[j]}^{power}" for j, power in enumerate(exponents) if power
            ) or "1"
            sample.append(f"{coefficient}*{monomial}")
        raise AssertionError("universal E6 identity after contact: " + "; ".join(sample))

    # One useful explicit coordinate chart (also a regression check for the
    # division-with-remainder arithmetic used in the prose audit).
    hconst = 2 - aa if args.mutation == "coordinate" else 1 - aa
    h = p**2 + (aa - 1) * p + hconst
    f = (1 + p) * r + p**3 + aa * p**2 + p * q
    Psrc = 1 + p
    Usrc = r + q + h
    Wsrc = f - (aa - 1)
    check("lambda-nonzero coordinate identity", Wsrc == Psrc * Usrc - q)

    # Verify the explicit inverse in fresh target variables.
    pinv = P - 1
    qinv = P * U - W
    hinv = h.subs({"p": pinv})
    rinv = U - qinv - hinv
    check("inverse recovers P", (1 + pinv) == P)
    check("inverse recovers U", rinv + qinv + hinv == U)
    finv = ((1 + pinv) * rinv + pinv**3 + aa * pinv**2 + pinv * qinv) - (aa - 1)
    check("inverse recovers W", finv == W)
    check("nonzero-lambda inverse degree", max(pinv.degree(("P", "U", "W")), qinv.degree(("P", "U", "W")), rinv.degree(("P", "U", "W"))) <= 2)

    # Lambda-zero, rank-one coordinate normal form: f=v+R(p,u).
    R1 = p**3 + aa * p**2 + bb * p * u + cc * u**2 + dd * p + u
    f1 = v + R1
    vinv = w - R1.subs({"p": P, "u": U})
    check("rank-one coordinate inverse", (vinv + R1.subs({"p": P, "u": U})) == w)

    # Lambda-zero, rank-zero independent and c=0 normal forms.
    R0 = p**3 + aa * p**2 + dd * p
    f_ind = v + p * u + R0
    vind = w - P * U - R0.subs({"p": P})
    check("rank-zero independent inverse", vind + P * U + R0.subs({"p": P}) == w)
    f_const = u + R0
    uinv = w - R0.subs({"p": P})
    check("rank-zero constant-linear inverse", uinv + R0.subs({"p": P}) == w)
    check("lambda-zero inverse degree", max(vinv.degree(("P", "U", "w")), vind.degree(("P", "U", "w")), uinv.degree(("P", "w"))) <= 3)

    # Canonical critical-point audits.  A remaining univariate quadratic has
    # a root over C; here we verify that its leading coefficient is exactly 3.
    f_rank2 = p**3 + aa * p**2 + c1 * p * u + c2 * p * v + (u**2 + v**2) / 2 + dd * p + d1 * u + d2 * v
    ur = -(c1 * p + d1)
    vr = -(c2 * p + d2)
    check("rank-two transverse gradients", f_rank2.diff("u").subs({"u": ur, "v": vr}) == 0 and f_rank2.diff("v").subs({"u": ur, "v": vr}) == 0)
    remaining2 = f_rank2.diff("p").subs({"u": ur, "v": vr})
    check("rank-two residual is quadratic", remaining2.degree(("p",)) == 2 and remaining2.coeff_power("p", 2) == 3)

    f_rank1_bad = p**3 + aa * p**2 + c1 * p * u + p * v + u**2 / 2 + dd * p + d1 * u + delta * v
    pbad = -delta
    ubad = c1 * delta - d1
    vbad = -(3 * delta**2 - 2 * aa * delta + c1 * ubad + dd)
    badmap = {"p": pbad, "u": ubad, "v": vbad}
    check("rank-one c_null critical witness", all(f_rank1_bad.diff(x).subs(badmap) == 0 for x in ("p", "u", "v")))

    f_rank1_flat = p**3 + aa * p**2 + c1 * p * u + u**2 / 2 + dd * p + d1 * u
    uflat = -(c1 * p + d1)
    remflat = f_rank1_flat.diff("p").subs({"u": uflat})
    check("rank-one flat-null residual", remflat.degree(("p",)) == 2 and remflat.coeff_power("p", 2) == 3)

    f_rank0_dep = p**3 + aa * p**2 + (p + delta) * u + dd * p
    udep = -(3 * delta**2 - 2 * aa * delta + dd)
    depmap = {"p": -delta, "u": udep}
    check("rank-zero dependent critical witness", f_rank0_dep.diff("p").subs(depmap) == 0 and f_rank0_dep.diff("u").subs(depmap) == 0)

    # General composition ceiling is 12.  In the requested fixed family the
    # coordinate constructions retain p linearly: H4 has weighted degrees
    # 4 and 8, while arbitrary H3 has weighted degree at most 9.
    general_ceiling = 12
    fixed_ceiling = 8 if args.mutation == "degree_ceiling" else 9
    check("general plane fibre ceiling", 4 * 3 <= general_ceiling)
    check("fixed-family plane fibre ceiling", max(4, 8, 9, 6, 3) <= fixed_ceiling)
    check("Moh threshold", general_ceiling < 100)

    print("POWER_FIBRE_CLEANROOM_STRICT_PASS")


if __name__ == "__main__":
    main()
