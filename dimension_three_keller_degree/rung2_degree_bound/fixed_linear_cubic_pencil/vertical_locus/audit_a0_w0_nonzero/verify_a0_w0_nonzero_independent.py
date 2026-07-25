#!/usr/bin/env python3
"""Dependency-free hostile certificate for the a=0, W0 != 0 leaf.

The weighted determinant is built as a literal 3-by-3 determinant over a
sparse multivariate polynomial ring.  No formula or coefficient list is
imported from the candidate checker.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import hashlib
import itertools
import os
import sys


if not __debug__:
    raise SystemExit("FAIL: optimized Python disables the certificate")


MUTATION = os.environ.get("A0_W0_INDEPENDENT_MUTATION", "")
ALLOWED_MUTATIONS = {
    "",
    "wrong_U",
    "flip_factor",
    "erase_chi",
    "skip_unit_scope",
}
if MUTATION not in ALLOWED_MUTATIONS:
    raise SystemExit(f"FAIL: unknown mutation {MUTATION!r}")


SOURCE_NAMES = ("t", "x", "y", "z")
Q_NAMES = tuple(f"q{i}{j}{k}" for i in range(4) for j in range(4 - i)
                for k in (3 - i - j,))
W_NAMES = tuple(f"w{i}{j}{k}" for i in range(3) for j in range(3 - i)
                for k in (2 - i - j,))
A_NAMES = tuple(f"a{i}{j}{k}" for i in range(3) for j in range(3 - i)
                for k in (2 - i - j,))
B_NAMES = tuple(f"b{i}{j}{k}" for i in range(3) for j in range(3 - i)
                for k in (2 - i - j,))
V_NAMES = tuple(f"v{i}{j}{k}" for i in range(4) for j in range(4 - i)
                for k in (3 - i - j,))
LINEAR_NAMES = tuple(f"l{i}{j}" for i in range(1, 4) for j in range(1, 4))
LADDER_NAMES = (
    "kappa", "gamma", "alpha", "beta", "chi", "delta", "epsilon", "phi",
    "u", "v", "omega", "a20", "a11", "a02", "a10", "a01", "a00",
    "ell31", "ell32", "ell33",
)
ALL_NAMES = (
    SOURCE_NAMES + Q_NAMES + W_NAMES + A_NAMES + B_NAMES + V_NAMES
    + LINEAR_NAMES + LADDER_NAMES
)
if len(set(ALL_NAMES)) != len(ALL_NAMES):
    raise SystemExit("FAIL: polynomial-variable registry contains a collision")
INDEX = {name: i for i, name in enumerate(ALL_NAMES)}
NVAR = len(ALL_NAMES)
ZERO_MONOMIAL = (0,) * NVAR


@dataclass(frozen=True)
class SparsePoly:
    terms: dict[tuple[int, ...], Fraction]

    def __post_init__(self) -> None:
        cleaned = {m: Fraction(c) for m, c in self.terms.items() if c}
        if any(len(m) != NVAR or any(e < 0 for e in m) for m in cleaned):
            raise ValueError("invalid sparse monomial")
        object.__setattr__(self, "terms", cleaned)

    def __add__(self, other: object) -> "SparsePoly":
        rhs = as_poly(other)
        out = dict(self.terms)
        for monomial, coefficient in rhs.terms.items():
            out[monomial] = out.get(monomial, Fraction(0)) + coefficient
            if not out[monomial]:
                del out[monomial]
        return SparsePoly(out)

    __radd__ = __add__

    def __neg__(self) -> "SparsePoly":
        return SparsePoly({m: -c for m, c in self.terms.items()})

    def __sub__(self, other: object) -> "SparsePoly":
        return self + (-as_poly(other))

    def __rsub__(self, other: object) -> "SparsePoly":
        return as_poly(other) - self

    def __mul__(self, other: object) -> "SparsePoly":
        rhs = as_poly(other)
        if not self.terms or not rhs.terms:
            return ZERO
        out: dict[tuple[int, ...], Fraction] = {}
        for left_monomial, left_coefficient in self.terms.items():
            for right_monomial, right_coefficient in rhs.terms.items():
                monomial = tuple(a + b for a, b in
                                 zip(left_monomial, right_monomial))
                out[monomial] = (
                    out.get(monomial, Fraction(0))
                    + left_coefficient * right_coefficient
                )
        return SparsePoly(out)

    __rmul__ = __mul__

    def __pow__(self, exponent: int) -> "SparsePoly":
        if exponent < 0:
            raise ValueError("negative polynomial power")
        result = ONE
        base = self
        power = exponent
        while power:
            if power & 1:
                result = result * base
            base = base * base
            power >>= 1
        return result

    def diff(self, variable: str) -> "SparsePoly":
        position = INDEX[variable]
        out: dict[tuple[int, ...], Fraction] = {}
        for monomial, coefficient in self.terms.items():
            exponent = monomial[position]
            if exponent:
                reduced = list(monomial)
                reduced[position] -= 1
                out[tuple(reduced)] = coefficient * exponent
        return SparsePoly(out)

    def coeff_var(self, variable: str, exponent: int) -> "SparsePoly":
        position = INDEX[variable]
        out: dict[tuple[int, ...], Fraction] = {}
        for monomial, coefficient in self.terms.items():
            if monomial[position] == exponent:
                reduced = list(monomial)
                reduced[position] = 0
                out[tuple(reduced)] = coefficient
        return SparsePoly(out)

    def coeff_xyz(self, exponents: tuple[int, int, int]) -> "SparsePoly":
        positions = tuple(INDEX[name] for name in ("x", "y", "z"))
        out: dict[tuple[int, ...], Fraction] = {}
        for monomial, coefficient in self.terms.items():
            if tuple(monomial[p] for p in positions) == exponents:
                reduced = list(monomial)
                for position in positions:
                    reduced[position] = 0
                out[tuple(reduced)] = coefficient
        return SparsePoly(out)

    def set_zero(self, *variables: str) -> "SparsePoly":
        positions = tuple(INDEX[name] for name in variables)
        return SparsePoly({
            monomial: coefficient
            for monomial, coefficient in self.terms.items()
            if all(monomial[position] == 0 for position in positions)
        })

    def depends_on(self) -> set[str]:
        return {
            name
            for name, position in INDEX.items()
            if any(monomial[position] for monomial in self.terms)
        }

    def canonical(self) -> str:
        pieces = []
        for monomial, coefficient in sorted(self.terms.items()):
            pieces.append(
                f"{coefficient.numerator}/{coefficient.denominator}:"
                + ",".join(map(str, monomial))
            )
        return "|".join(pieces)


def as_poly(value: object) -> SparsePoly:
    if isinstance(value, SparsePoly):
        return value
    if isinstance(value, (int, Fraction)):
        coefficient = Fraction(value)
        return SparsePoly({ZERO_MONOMIAL: coefficient}) if coefficient else ZERO
    raise TypeError(f"cannot coerce {type(value)} to SparsePoly")


ZERO = SparsePoly({})
ONE = SparsePoly({ZERO_MONOMIAL: Fraction(1)})


def variable(name: str) -> SparsePoly:
    monomial = [0] * NVAR
    monomial[INDEX[name]] = 1
    return SparsePoly({tuple(monomial): Fraction(1)})


VARS = {name: variable(name) for name in ALL_NAMES}
t, x, y, z = (VARS[name] for name in SOURCE_NAMES)


def fail(label: str, detail: str = "") -> None:
    suffix = f": {detail}" if detail else ""
    raise SystemExit(f"FAIL [{label}]{suffix}")


def require_equal(label: str, actual: SparsePoly, expected: SparsePoly) -> None:
    difference = actual - expected
    if difference.terms:
        digest = hashlib.sha256(difference.canonical().encode()).hexdigest()[:16]
        fail(label, f"{len(difference.terms)} residual terms, digest {digest}")


def require(condition: bool, label: str, detail: str = "") -> None:
    if not condition:
        fail(label, detail)


def homogeneous_form(
    coefficient_names: tuple[str, ...], degree: int
) -> SparsePoly:
    result = ZERO
    for name in coefficient_names:
        i, j, k = map(int, name[-3:])
        require(i + j + k == degree, "homogeneous-form-degree", name)
        result += VARS[name] * x**i * y**j * z**k
    return result


def gradient(polynomial: SparsePoly) -> list[SparsePoly]:
    return [polynomial.diff(name) for name in ("x", "y", "z")]


def determinant3(rows: list[list[SparsePoly]]) -> SparsePoly:
    if len(rows) != 3 or any(len(row) != 3 for row in rows):
        raise ValueError("determinant3 requires a 3-by-3 matrix")
    return (
        rows[0][0] * rows[1][1] * rows[2][2]
        + rows[0][1] * rows[1][2] * rows[2][0]
        + rows[0][2] * rows[1][0] * rows[2][1]
        - rows[0][2] * rows[1][1] * rows[2][0]
        - rows[0][1] * rows[1][0] * rows[2][2]
        - rows[0][0] * rows[1][2] * rows[2][1]
    )


def jacobian3(
    first: SparsePoly, second: SparsePoly, third: SparsePoly
) -> SparsePoly:
    return determinant3([gradient(first), gradient(second), gradient(third)])


def binary_bracket(first: SparsePoly, second: SparsePoly) -> SparsePoly:
    return first.diff("x") * second.diff("y") - first.diff("y") * second.diff("x")


def weighted_matrix(
    linear: list[list[SparsePoly]],
    h2: list[SparsePoly],
    h3: list[SparsePoly],
    h4: list[SparsePoly],
) -> list[list[SparsePoly]]:
    j2 = [gradient(component) for component in h2]
    j3 = [gradient(component) for component in h3]
    j4 = [gradient(component) for component in h4]
    return [[
        linear[row][column]
        + t * j2[row][column]
        + t**2 * j3[row][column]
        + t**3 * j4[row][column]
        for column in range(3)
    ] for row in range(3)]


def generic_raw_e6() -> tuple[SparsePoly, SparsePoly, dict[str, SparsePoly]]:
    q = homogeneous_form(Q_NAMES, 3)
    w = homogeneous_form(W_NAMES, 2)
    a = homogeneous_form(A_NAMES, 2)
    b = homogeneous_form(B_NAMES, 2)
    v_form = homogeneous_form(V_NAMES, 3)
    linear = [[VARS[f"l{row}{column}"] for column in range(1, 4)]
              for row in range(1, 4)]
    u_factor = Fraction(1) if MUTATION == "wrong_U" else Fraction(4, 3)
    h2 = [a, b, w]
    h3 = [u_factor * z * w, v_form, z**3]
    h4 = [z**4, z * q, ZERO]
    raw = determinant3(weighted_matrix(linear, h2, h3, h4))
    e6 = raw.coeff_var("t", 6)
    ell3 = VARS["l31"] * x + VARS["l32"] * y + VARS["l33"] * z
    exterior = (
        jacobian3(z**4, z * q, ell3)
        + jacobian3(u_factor * z * w, z * q, w)
        + jacobian3(z**4, v_form, w)
        + jacobian3(a, z * q, z**3)
        + jacobian3(u_factor * z * w, v_form, z**3)
        + jacobian3(z**4, b, z**3)
    )
    target_sign = -1 if MUTATION == "flip_factor" else 1
    factored = target_sign * Fraction(1, 3) * z * (
        4 * w * binary_bracket(q, w)
        + 9 * z**2 * binary_bracket(a, q)
        + 12 * z**3 * binary_bracket(q, ell3)
    )
    return e6, exterior, {
        "raw": raw,
        "factor": factored,
        "q": q,
        "w": w,
        "a": a,
        "b": b,
        "v": v_form,
    }


def verify_raw_factorization() -> tuple[int, str]:
    e6, exterior, data = generic_raw_e6()
    for exponent in (9, 8, 7):
        require_equal(
            f"gauged-raw-E{exponent}",
            data["raw"].coeff_var("t", exponent),
            ZERO,
        )
    require_equal("raw-vs-exterior-E6", e6, exterior)
    require_equal("raw-vs-bracket-factor-E6", e6, data["factor"])

    cancelled_names = set(B_NAMES + V_NAMES + LINEAR_NAMES[:6] + ("l33",))
    leaked = e6.depends_on() & cancelled_names
    require(not leaked, "structural-cancellation", ", ".join(sorted(leaked)))

    # Every generic lower-jet family really entered the raw determinant.
    raw_dependencies = data["raw"].depends_on()
    for family, names in (
        ("q", Q_NAMES), ("W", W_NAMES), ("A", A_NAMES), ("B", B_NAMES),
        ("V", V_NAMES), ("linear", LINEAR_NAMES),
    ):
        missing = set(names) - raw_dependencies
        require(not missing, f"raw-retains-{family}",
                ", ".join(sorted(missing)))

    # The compact factor is equivalently a single bracket.
    q, w, a = data["q"], data["w"], data["a"]
    ell3 = VARS["l31"] * x + VARS["l32"] * y + VARS["l33"] * z
    one_bracket = Fraction(1, 3) * z * binary_bracket(
        q, 2 * w**2 - 9 * z**2 * a + 12 * z**3 * ell3
    )
    require_equal("single-bracket-form", data["factor"], one_bracket)

    digest = hashlib.sha256(e6.canonical().encode()).hexdigest()
    require(len(e6.terms) == 186, "raw-E6-term-count", str(len(e6.terms)))
    require(
        digest == "66315d214e861b16738ae96b840e1c857a794e21367d445e21cc7ba3536cb625",
        "raw-E6-fingerprint",
        digest,
    )
    return len(e6.terms), digest


def verify_binary_power_step() -> None:
    q30, q21, q12, q03 = (VARS[name] for name in
                           ("q300", "q210", "q120", "q030"))
    w20, w11, w02 = (VARS[name] for name in
                      ("w200", "w110", "w020"))
    q0 = q30*x**3 + q21*x**2*y + q12*x*y**2 + q03*y**3
    w0 = w20*x**2 + w11*x*y + w02*y**2
    bracket = binary_bracket(q0, w0)
    require_equal(
        "binary-euler-x",
        2*w0*q0.diff("x") - 3*q0*w0.diff("x"),
        y*bracket,
    )
    require_equal(
        "binary-euler-y",
        2*w0*q0.diff("y") - 3*q0*w0.diff("y"),
        -x*bracket,
    )

    kappa, gamma = VARS["kappa"], VARS["gamma"]
    lam0, lam1 = VARS["ell31"], VARS["ell32"]
    line = lam0*x + lam1*y
    require_equal(
        "power-parametrization",
        binary_bracket(kappa*line**3, gamma*line**2),
        ZERO,
    )


def normalized_ladder() -> tuple[SparsePoly, SparsePoly]:
    p = VARS
    q = (
        p["kappa"]*x**3
        + z*(p["alpha"]*x**2 + p["beta"]*x*y
             + (ZERO if MUTATION == "erase_chi" else p["chi"]*y**2))
        + z**2*(p["delta"]*x + p["epsilon"]*y)
        + p["phi"]*z**3
    )
    w = (
        p["gamma"]*x**2 + z*(p["u"]*x + p["v"]*y)
        + p["omega"]*z**2
    )
    a = (
        p["a20"]*x**2 + p["a11"]*x*y + p["a02"]*y**2
        + z*(p["a10"]*x + p["a01"]*y) + p["a00"]*z**2
    )
    ell3 = p["ell31"]*x + p["ell32"]*y + p["ell33"]*z
    phi = (
        4*w*binary_bracket(q, w)
        + 9*z**2*binary_bracket(a, q)
        + 12*z**3*binary_bracket(q, ell3)
    )
    return phi, q


def verify_six_coefficient_ladder() -> str:
    p = VARS
    phi, q = normalized_ladder()
    selected = {
        "chi": phi.coeff_xyz((3, 1, 1)),
        "r": phi.coeff_xyz((4, 0, 1)),
        "f": phi.coeff_xyz((2, 1, 2)),
        "h": phi.coeff_xyz((0, 2, 3)),
        "p": phi.coeff_xyz((3, 0, 2)),
        "q": phi.coeff_xyz((0, 1, 4)),
    }
    expected = {
        "chi": -16*p["chi"]*p["gamma"]**2,
        "r": 4*p["gamma"]*(-2*p["beta"]*p["gamma"]
                           + 3*p["kappa"]*p["v"]),
        "f": -2*(
            27*p["kappa"]*p["a02"] + 2*p["beta"]*p["gamma"]*p["v"]
            + 12*p["chi"]*p["gamma"]*p["u"]
            - 6*p["kappa"]*p["v"]**2
        ),
        "h": -2*(
            9*p["a02"]*p["beta"] - 9*p["a11"]*p["chi"]
            - 2*p["beta"]*p["v"]**2 + 4*p["chi"]*p["u"]*p["v"]
        ),
        "p": (
            -27*p["kappa"]*p["a11"]
            + 8*p["alpha"]*p["gamma"]*p["v"]
            - 12*p["beta"]*p["gamma"]*p["u"]
            - 8*p["epsilon"]*p["gamma"]**2
            + 12*p["kappa"]*p["u"]*p["v"]
        ),
        "q": (
            -9*p["a01"]*p["beta"] - 18*p["a02"]*p["delta"]
            + 18*p["a10"]*p["chi"] + 9*p["a11"]*p["epsilon"]
            + 12*p["beta"]*p["ell32"] + 4*p["beta"]*p["v"]*p["omega"]
            - 24*p["chi"]*p["ell31"] - 8*p["chi"]*p["u"]*p["omega"]
            + 4*p["delta"]*p["v"]**2 - 4*p["epsilon"]*p["u"]*p["v"]
        ),
    }
    for label in selected:
        require_equal(f"ladder-coefficient-{label}", selected[label], expected[label])

    r = 2*p["beta"]*p["gamma"] - 3*p["kappa"]*p["v"]
    f = (
        27*p["kappa"]*p["a02"] + 2*p["beta"]*p["gamma"]*p["v"]
        - 6*p["kappa"]*p["v"]**2
    )
    g = 9*p["a02"] - p["v"]**2
    h = 9*p["a02"]*p["beta"] - 2*p["beta"]*p["v"]**2
    require_equal("elimination-f-minus-vr", f - p["v"]*r, 3*p["kappa"]*g)
    require_equal("elimination-h-minus-betag", h - p["beta"]*g,
                  -p["beta"]*p["v"]**2)

    late_zeroes = ("chi", "beta", "v", "a02")
    late_p = selected["p"].set_zero(*late_zeroes)
    late_q = selected["q"].set_zero(*late_zeroes)
    relation_p = 27*p["kappa"]*p["a11"] + 8*p["gamma"]**2*p["epsilon"]
    relation_q = 9*p["a11"]*p["epsilon"]
    require_equal("late-linear-relation", late_p, -relation_p)
    require_equal("late-product-relation", late_q, relation_q)
    require_equal(
        "late-square-elimination",
        p["epsilon"]*relation_p - 3*p["kappa"]*relation_q,
        8*p["gamma"]**2*p["epsilon"]**2,
    )

    conclusion = q.set_zero("chi", "beta", "epsilon")
    expected_q = (
        p["kappa"]*x**3 + p["alpha"]*x**2*z
        + p["delta"]*x*z**2 + p["phi"]*z**3
    )
    require_equal("binary-boundary-conclusion", conclusion, expected_q)
    require(not (conclusion.depends_on() & {"y"}), "boundary-still-has-y")

    unit_scope = {"kappa", "gamma"}
    if MUTATION == "skip_unit_scope":
        unit_scope.remove("gamma")
    require(unit_scope == {"kappa", "gamma"}, "nonzero-unit-scope",
            ", ".join(sorted(unit_scope)))
    digest = hashlib.sha256(phi.canonical().encode()).hexdigest()
    require(
        digest == "d73b11f852b2fe4c9f4b7dee758fe868f028e67ce9dd470da49fc6f9361a063c",
        "ladder-Phi-fingerprint",
        digest,
    )
    return digest


def verify_sharp_boundary_witness() -> None:
    identity = [[ONE, ZERO, ZERO], [ZERO, ONE, ZERO], [ZERO, ZERO, ONE]]
    q = x**3
    w = x**2
    h2 = [ZERO, ZERO, w]
    h3 = [Fraction(4, 3)*z*w, ZERO, z**3]
    h4 = [z**4, z*q, ZERO]
    determinant = determinant3(weighted_matrix(identity, h2, h3, h4))
    expected = (
        ONE + Fraction(1, 3)*t**2*z*(8*x + 9*z)
        - Fraction(8, 3)*t**3*x**3
    )
    require_equal("sharp-boundary-witness", determinant, expected)
    for exponent in range(4, 9):
        require_equal(
            f"sharp-boundary-E{exponent}",
            determinant.coeff_var("t", exponent),
            ZERO,
        )


def main() -> None:
    raw_terms, raw_digest = verify_raw_factorization()
    verify_binary_power_step()
    ladder_digest = verify_six_coefficient_ladder()
    verify_sharp_boundary_witness()
    print(
        "PASS: independent raw determinant, E6 factorization, binary-power "
        "step, six-coefficient elimination, and sharp boundary witness"
    )
    print(f"RAW_E6_TERMS={raw_terms}")
    print(f"RAW_E6_SHA256={raw_digest}")
    print(f"LADDER_PHI_SHA256={ladder_digest}")
    print("UNIT_DIVISORS=kappa,gamma; FREE_JET_DIVISORS=none")
    print("A0_W0_NONZERO_INDEPENDENT_PASS_7C2E19")


if __name__ == "__main__":
    main()
