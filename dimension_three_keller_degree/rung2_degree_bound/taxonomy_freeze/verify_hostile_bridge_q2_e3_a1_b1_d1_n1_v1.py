#!/usr/bin/env python3
"""Dependency-free hostile reconstruction of the fixed-cubic-line bridge.

This is intentionally independent of the SymPy and PARI/GP implementations
used by the candidate and legacy proofs.  It uses a small sparse polynomial
ring over Q implemented below.  Besides the 45-pivot bridge ledger, it starts
the exceptional nonbinary calculation from unrestricted homogeneous
coefficients and reconstructs the complete E6/E5 solution spaces, their
translation normalizations, and both determinant exits.
"""

from __future__ import annotations

from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
RUNG = HERE.parent

EXPECTED_HASHES = {
    HERE / "BRIDGE_Q2_E3_A1_B1_D1_N1_v1.md":
        "4fc9de9d57164997ab528aad08a5ccf704ccc9b8e1cb8c4adcb9c099153c7b2c",
    HERE / "FROZEN_TAXONOMY_v1.md":
        "41fccc44d23fab125819990a2b27526771fbfb62293910b98cfcf1821576d03d",
    HERE / "frozen_manifest_v1.json":
        "5a2bdd57438e9ebcca18d04c53ebc98ced2b61209e2de99674aede501c615c23",
    RUNG / "WORKING_FIXED_CUBIC_LINE_ROW.md":
        "9a10c1c103b60eb21405518074086168330a435bb5aa1770d51463a881a926ca",
    RUNG / "WORKING_BINARY_FIXED_CUBIC_LINE_ROW.md":
        "51818647fa7f57942761ca31ed80dc9dde4363ebe83166d87fc80f07861a9607",
    RUNG / "verify_fixed_cubic_line_sympy.py":
        "fdcf31dc44bda116c0e81da6a9d96abf0b92798eb8d56ec25d6c124b31d4b8b8",
    RUNG / "verify_fixed_cubic_line_pari.gp":
        "aeded24439435f5db31d2e702fe357ec0799b62a326761e514727ff77dcc61e1",
    RUNG / "audit_binary_fixed_cubic_hostile" / "REPORT.md":
        "4cea6002ca7639cf8e04aea80b86daa76655c7359e041e2e7707e50418fa7fc4",
}

QUARTIC_EXPONENTS = (
    (4, 0, 0), (3, 1, 0), (3, 0, 1), (2, 2, 0), (2, 1, 1),
    (2, 0, 2), (1, 3, 0), (1, 2, 1), (1, 1, 2), (1, 0, 3),
    (0, 4, 0), (0, 3, 1), (0, 2, 2), (0, 1, 3), (0, 0, 4),
)
CUBIC_EXPONENTS = (
    (3, 0, 0), (2, 1, 0), (1, 2, 0), (0, 3, 0), (2, 0, 1),
    (1, 1, 1), (0, 2, 1), (1, 0, 2), (0, 1, 2), (0, 0, 3),
)
QUADRATIC_EXPONENTS = (
    (2, 0, 0), (1, 1, 0), (0, 2, 0),
    (1, 0, 1), (0, 1, 1), (0, 0, 2),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    require(path.is_file(), f"missing pinned input: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _merge_monomials(
    left: tuple[tuple[str, int], ...],
    right: tuple[tuple[str, int], ...],
) -> tuple[tuple[str, int], ...]:
    powers: dict[str, int] = {}
    for name, exponent in left + right:
        powers[name] = powers.get(name, 0) + exponent
    return tuple(sorted((name, exponent) for name, exponent in powers.items()
                        if exponent))


class Poly:
    """Sparse multivariate polynomial over Q, with named indeterminates."""

    def __init__(
        self,
        terms: dict[tuple[tuple[str, int], ...], Fraction | int] | None = None,
    ) -> None:
        cleaned: dict[tuple[tuple[str, int], ...], Fraction] = {}
        for monomial, coefficient in (terms or {}).items():
            value = Fraction(coefficient)
            if value:
                cleaned[monomial] = cleaned.get(monomial, Fraction(0)) + value
        self.terms = {monomial: coefficient
                      for monomial, coefficient in cleaned.items() if coefficient}

    @classmethod
    def var(cls, name: str) -> "Poly":
        return cls({((name, 1),): Fraction(1)})

    @classmethod
    def monomial(
        cls,
        powers: dict[str, int],
        coefficient: Fraction | int = 1,
    ) -> "Poly":
        key = tuple(sorted((name, exponent) for name, exponent in powers.items()
                           if exponent))
        return cls({key: Fraction(coefficient)})

    @staticmethod
    def coerce(value: "Poly | Fraction | int") -> "Poly":
        if isinstance(value, Poly):
            return value
        return Poly({(): Fraction(value)})

    def __add__(self, other: "Poly | Fraction | int") -> "Poly":
        right = Poly.coerce(other)
        result = dict(self.terms)
        for monomial, coefficient in right.terms.items():
            result[monomial] = result.get(monomial, Fraction(0)) + coefficient
        return Poly(result)

    __radd__ = __add__

    def __neg__(self) -> "Poly":
        return Poly({monomial: -coefficient
                     for monomial, coefficient in self.terms.items()})

    def __sub__(self, other: "Poly | Fraction | int") -> "Poly":
        return self + (-Poly.coerce(other))

    def __rsub__(self, other: "Poly | Fraction | int") -> "Poly":
        return Poly.coerce(other) - self

    def __mul__(self, other: "Poly | Fraction | int") -> "Poly":
        right = Poly.coerce(other)
        result: dict[tuple[tuple[str, int], ...], Fraction] = {}
        for left_monomial, left_coefficient in self.terms.items():
            for right_monomial, right_coefficient in right.terms.items():
                monomial = _merge_monomials(left_monomial, right_monomial)
                result[monomial] = (
                    result.get(monomial, Fraction(0))
                    + left_coefficient * right_coefficient
                )
        return Poly(result)

    __rmul__ = __mul__

    def __pow__(self, exponent: int) -> "Poly":
        require(exponent >= 0, "negative polynomial exponent")
        result = Poly.coerce(1)
        base = self
        power = exponent
        while power:
            if power & 1:
                result = result * base
            base = base * base
            power >>= 1
        return result

    def derivative(self, variable: str) -> "Poly":
        result: dict[tuple[tuple[str, int], ...], Fraction] = {}
        for monomial, coefficient in self.terms.items():
            powers = dict(monomial)
            exponent = powers.get(variable, 0)
            if not exponent:
                continue
            if exponent == 1:
                del powers[variable]
            else:
                powers[variable] = exponent - 1
            key = tuple(sorted(powers.items()))
            result[key] = result.get(key, Fraction(0)) + coefficient * exponent
        return Poly(result)

    def substitute(self, replacements: dict[str, "Poly | Fraction | int"]) -> "Poly":
        result = Poly()
        for monomial, coefficient in self.terms.items():
            term = Poly.coerce(coefficient)
            for name, exponent in monomial:
                image = Poly.coerce(replacements.get(name, Poly.var(name)))
                term = term * image**exponent
            result = result + term
        return result

    def exponent(self, monomial: tuple[tuple[str, int], ...], variable: str) -> int:
        return dict(monomial).get(variable, 0)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, (int, Fraction)):
            return self.terms == Poly.coerce(other).terms
        if isinstance(other, Poly):
            return self.terms == other.terms
        return False

    def __bool__(self) -> bool:
        return bool(self.terms)

    def __repr__(self) -> str:
        return f"Poly({self.terms!r})"


ZERO = Poly()
ONE = Poly.coerce(1)


def V(name: str) -> Poly:
    return Poly.var(name)


def monomial_xyz(exponents: tuple[int, int, int]) -> Poly:
    return Poly.monomial(dict(zip(("p", "q", "r"), exponents)))


def vector_homogeneous(prefix: str, exponents: tuple[tuple[int, int, int], ...]) -> Poly:
    return sum((V(f"{prefix}{index}") * monomial_xyz(exp)
                for index, exp in enumerate(exponents)), ZERO)


def jacobian(vector: list[Poly], variables: tuple[str, str, str] = ("p", "q", "r")) -> list[list[Poly]]:
    return [[entry.derivative(variable) for variable in variables]
            for entry in vector]


def matrix_add(*matrices: list[list[Poly]]) -> list[list[Poly]]:
    return [[sum((matrix[i][j] for matrix in matrices), ZERO)
             for j in range(len(matrices[0][0]))]
            for i in range(len(matrices[0]))]


def matrix_scale(scalar: Poly, matrix: list[list[Poly]]) -> list[list[Poly]]:
    return [[scalar * entry for entry in row] for row in matrix]


def determinant3(matrix: list[list[Poly]]) -> Poly:
    return (
        matrix[0][0] * matrix[1][1] * matrix[2][2]
        + matrix[0][1] * matrix[1][2] * matrix[2][0]
        + matrix[0][2] * matrix[1][0] * matrix[2][1]
        - matrix[0][2] * matrix[1][1] * matrix[2][0]
        - matrix[0][1] * matrix[1][0] * matrix[2][2]
        - matrix[0][0] * matrix[1][2] * matrix[2][1]
    )


def permutation_sign(permutation: tuple[int, ...]) -> int:
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def determinant(matrix: list[list[Poly]]) -> Poly:
    size = len(matrix)
    result = ZERO
    for permutation in itertools.permutations(range(size)):
        term = Poly.coerce(permutation_sign(permutation))
        for row, column in enumerate(permutation):
            term = term * matrix[row][column]
        result = result + term
    return result


def weighted_determinant(
    linear: list[list[Poly]],
    quadratic: list[Poly],
    cubic: list[Poly],
    quartic: list[Poly],
) -> Poly:
    z = V("zeta")
    matrix = matrix_add(
        linear,
        matrix_scale(z, jacobian(quadratic)),
        matrix_scale(z**2, jacobian(cubic)),
        matrix_scale(z**3, jacobian(quartic)),
    )
    return determinant3(matrix)


def strip_variables(
    monomial: tuple[tuple[str, int], ...],
    names: set[str],
) -> tuple[tuple[str, int], ...]:
    return tuple((name, exponent) for name, exponent in monomial
                 if name not in names)


def coefficient_table(
    polynomial: Poly,
    zeta_degree: int | None = None,
) -> dict[tuple[int, int, int], Poly]:
    """Group by p,q,r, optionally retaining only one zeta coefficient."""
    table: dict[tuple[int, int, int], Poly] = {}
    for monomial, coefficient in polynomial.terms.items():
        powers = dict(monomial)
        if zeta_degree is not None and powers.get("zeta", 0) != zeta_degree:
            continue
        geometry = (powers.get("p", 0), powers.get("q", 0), powers.get("r", 0))
        stripped = strip_variables(monomial, {"p", "q", "r", "zeta"})
        term = Poly({stripped: coefficient})
        table[geometry] = table.get(geometry, ZERO) + term
    return {geometry: coefficient for geometry, coefficient in table.items()
            if coefficient}


def require_table(
    actual: dict[tuple[int, int, int], Poly],
    expected: dict[tuple[int, int, int], Poly],
    label: str,
) -> None:
    keys = set(actual) | set(expected)
    for key in keys:
        require(actual.get(key, ZERO) == expected.get(key, ZERO),
                f"{label}: coefficient mismatch at {key}")


def linear_rank(polynomials: list[Poly], variables: list[str]) -> int:
    index = {name: position for position, name in enumerate(variables)}
    rows: list[list[Fraction]] = []
    for polynomial in polynomials:
        row = [Fraction(0) for _ in variables]
        for monomial, coefficient in polynomial.terms.items():
            require(len(monomial) == 1 and monomial[0][1] == 1,
                    "purported linear system is not linear homogeneous")
            require(monomial[0][0] in index, "unexpected linear-system variable")
            row[index[monomial[0][0]]] += coefficient
        if any(row):
            rows.append(row)

    rank = 0
    column_count = len(variables)
    for column in range(column_count):
        pivot = next((row for row in range(rank, len(rows))
                      if rows[row][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        pivot_value = rows[rank][column]
        rows[rank] = [entry / pivot_value for entry in rows[rank]]
        for row in range(len(rows)):
            if row == rank or not rows[row][column]:
                continue
            factor = rows[row][column]
            rows[row] = [
                rows[row][j] - factor * rows[rank][j]
                for j in range(column_count)
            ]
        rank += 1
    return rank


def directional_derivative(vector: list[Poly], direction: tuple[Poly, Poly, Poly]) -> list[Poly]:
    return [
        sum((direction[index] * entry.derivative(variable)
             for index, variable in enumerate(("p", "q", "r"))), ZERO)
        for entry in vector
    ]


def matrix_from_rows(rows: list[list[Poly | int]]) -> list[list[Poly]]:
    return [[Poly.coerce(entry) for entry in row] for row in rows]


def audit_frozen_bridge() -> None:
    manifest = json.loads((HERE / "frozen_manifest_v1.json").read_text())
    require(manifest["version"] == 1, "wrong freeze version")
    require(manifest["frozen_row_count"] == 14, "wrong frozen denominator")
    pivots = [f"C{index:02d}" for index in range(45)]
    require(manifest["pivot_ids"] == pivots, "wrong frozen pivot ledger")
    rows = [row for row in manifest["rows"]
            if row["id"] == "Q2-E3-A1-B1-D1-N1"]
    require(len(rows) == 1, "frozen target row missing or duplicated")
    require(rows[0]["rank"] == 2, "wrong frozen row rank")
    require(rows[0]["tuple"] == [3, 1, 1, 1, 1], "wrong frozen row tuple")

    # All 30 early pivots have exact leading-tuple witnesses.  This
    # reconstruction uses monomial exponents only, not a CAS gcd/rank call.
    covered: set[str] = set()
    for index, exponent in enumerate(QUARTIC_EXPONENTS):
        if index <= 9:
            divisor, transverse = 0, 1
        elif index <= 13:
            divisor, transverse = 1, 0
        else:
            divisor, transverse = 2, 0
        h_exp = list(exponent)
        require(h_exp[divisor] > 0, "chosen divisor misses pivot monomial")
        h_exp[divisor] -= 1
        first_exp = tuple(h_exp[j] + (j == divisor) for j in range(3))
        second_exp = tuple(h_exp[j] + (j == transverse) for j in range(3))
        require(first_exp == exponent, "witness leading monomial mismatch")
        gcd_exp = tuple(min(first_exp[j], second_exp[j]) for j in range(3))
        require(gcd_exp == tuple(h_exp) and sum(gcd_exp) == 3,
                "witness gcd is not the required cubic")
        require(first_exp != second_exp, "residual line has rank below two")

        h = monomial_xyz(tuple(h_exp))
        ell = V(("p", "q", "r")[divisor])
        transverse_form = V(("p", "q", "r")[transverse])
        pair = [h * ell, h * transverse_form]
        jac = [[entry.derivative(variable) for variable in ("p", "q", "r")]
               for entry in pair]
        minors = [
            jac[0][i] * jac[1][j] - jac[0][j] * jac[1][i]
            for i, j in itertools.combinations(range(3), 2)
        ]
        require(any(minor for minor in minors), "witness Jacobian rank is below two")
        covered.add(f"C{index:02d}")
        covered.add(f"C{15 + index:02d}")

    require(covered == set(pivots[:30]), "early-pivot witnesses are incomplete")

    # C30--C44 have only the third component nonzero.  Every two-row
    # Jacobian minor therefore contains a zero row.
    forced_empty = set(pivots[30:])
    require(len(forced_empty) == 15, "wrong late-pivot count")
    require(covered.isdisjoint(forced_empty)
            and covered | forced_empty == set(pivots),
            "45-pivot coverage is not a partition")

    # Independent Sym^3 determinant calculation for intrinsic binary-basis
    # invariance.
    u, v = V("u"), V("v")
    aa, bb, cc, dd = (V(name) for name in ("aa", "bb", "cc", "dd"))
    first, second = aa * u + bb * v, cc * u + dd * v
    images = (first**3, first**2 * second, first * second**2, second**3)
    uv_basis = ((3, 0), (2, 1), (1, 2), (0, 3))
    sym3: list[list[Poly]] = []
    for u_degree, v_degree in uv_basis:
        row: list[Poly] = []
        for image in images:
            coefficient = ZERO
            for monomial, value in image.terms.items():
                powers = dict(monomial)
                if powers.get("u", 0) == u_degree and powers.get("v", 0) == v_degree:
                    coefficient = coefficient + Poly({
                        strip_variables(monomial, {"u", "v"}): value
                    })
            row.append(coefficient)
        sym3.append(row)
    require(determinant(sym3) == (aa * dd - bb * cc)**6,
            "independent Sym^3 determinant identity failed")


def exceptional_setup(
    normal_component: Poly,
    prefix: str,
) -> tuple[
    list[Poly], list[Poly], list[Poly], list[list[Poly]], Poly,
    list[str], list[str], list[str],
]:
    p, q, r = V("p"), V("q"), V("r")
    h = p * r**2
    quartic = [h * p, h * q, ZERO]
    up = [f"{prefix}u{index}" for index in range(20)]
    vp = [f"{prefix}v{index}" for index in range(12)]
    lp = [f"{prefix}l{index}" for index in range(3)]
    cubic = [
        vector_homogeneous(f"{prefix}u0_", CUBIC_EXPONENTS),
        vector_homogeneous(f"{prefix}u1_", CUBIC_EXPONENTS),
        ZERO,
    ]
    # Rename the helper's u0_0 notation to the compact declared names.
    rename: dict[str, Poly] = {}
    for component in range(2):
        for index in range(10):
            rename[f"{prefix}u{component}_{index}"] = V(up[10 * component + index])
    cubic = [entry.substitute(rename) for entry in cubic]
    quadratic = [
        vector_homogeneous(f"{prefix}v0_", QUADRATIC_EXPONENTS),
        vector_homogeneous(f"{prefix}v1_", QUADRATIC_EXPONENTS),
        normal_component,
    ]
    rename = {}
    for component in range(2):
        for index in range(6):
            rename[f"{prefix}v{component}_{index}"] = V(vp[6 * component + index])
    quadratic = [entry.substitute(rename) for entry in quadratic]
    linear = matrix_from_rows([
        [0, 0, 0],
        [0, 0, 0],
        [V(lp[0]), V(lp[1]), V(lp[2])],
    ])
    weighted = weighted_determinant(linear, quadratic, cubic, quartic)
    return quartic, cubic, quadratic, linear, weighted, up, vp, lp


def audit_qr_orbit() -> None:
    p, q, r = V("p"), V("q"), V("r")
    # Reconstruct the complete quadratic D_k-kernel for h=p*r^2 before
    # choosing either nonzero stabilizer orbit.
    kernel_coefficients = [f"ker{index}" for index in range(6)]
    general_quadratic = sum(
        (V(kernel_coefficients[index]) * monomial_xyz(exponent)
         for index, exponent in enumerate(QUADRATIC_EXPONENTS)),
        ZERO,
    )
    k_vector = (2 * p**2 * r, 2 * p * q * r, -2 * p * r**2)
    kernel_equation = sum(
        (k_vector[index] * general_quadratic.derivative(variable)
         for index, variable in enumerate(("p", "q", "r"))),
        ZERO,
    )
    kernel_table = coefficient_table(kernel_equation)
    require(linear_rank(list(kernel_table.values()), kernel_coefficients) == 4,
            "h=p*r^2 quadratic invariant kernel does not have dimension two")
    require(
        not sum((k_vector[index] * (p * r).derivative(variable)
                 for index, variable in enumerate(("p", "q", "r"))), ZERO)
        and not sum((k_vector[index] * (q * r).derivative(variable)
                     for index, variable in enumerate(("p", "q", "r"))), ZERO),
        "p*r and q*r are not both quadratic invariants",
    )

    quartic, cubic, quadratic, _, weighted, u, v, ell = exceptional_setup(
        q * r, "q"
    )
    U = [V(name) for name in u]
    W = [V(name) for name in v]
    L = [V(name) for name in ell]

    e6 = coefficient_table(weighted, 6)
    system_variables = u + ell
    require(linear_rank(list(e6.values()), system_variables) == 14,
            "q*r raw E6 rank is not 14")
    e6_solution = {
        u[0]: 2 * U[11], u[1]: 2 * U[12], u[2]: 2 * U[13],
        u[3]: 0, u[4]: -2 * L[1] + 2 * U[15],
        u[5]: 2 * U[16], u[6]: 0, u[7]: 2 * U[18],
        u[8]: 0, u[9]: 0, u[10]: 0, u[14]: L[0],
        u[17]: L[2], u[19]: 0,
    }
    require(all(not coefficient.substitute(e6_solution) for coefficient in e6.values()),
            "q*r proposed E6 kernel does not satisfy E6")
    free_e6 = {u[index] for index in (11, 12, 13, 15, 16, 18)} | set(ell)
    require(len(free_e6) == len(system_variables) - 14,
            "q*r E6 parametrization has wrong dimension")
    require(free_e6.isdisjoint(e6_solution),
            "q*r E6 free coordinates are not independent coordinates")

    actual_e5 = {
        key: value.substitute(e6_solution)
        for key, value in coefficient_table(weighted, 5).items()
    }
    expected_e5 = {
        (4, 1, 0): 6 * U[11]**2,
        (4, 0, 1): -8 * L[0] * U[11],
        (3, 2, 0): 12 * U[11] * U[12],
        (3, 1, 1): 8 * (
            -L[0] * U[12] - 2 * L[1] * U[11] + U[11] * U[15]
        ),
        (3, 0, 2): -4 * (
            -L[0] * L[1] + L[0] * U[15] + L[2] * U[11] - W[6]
        ),
        (2, 3, 0): 6 * (2 * U[11] * U[13] + U[12]**2),
        (2, 2, 1): 8 * (
            -L[0] * U[13] - 2 * L[1] * U[12]
            + U[11] * U[16] + U[12] * U[15]
        ),
        (2, 1, 2): 2 * (
            -2 * L[0] * U[16] + 3 * L[1]**2 - 4 * L[1] * U[15]
            - 2 * L[2] * U[12] + 2 * U[11] * U[18] + U[15]**2
            - W[0] + 2 * W[7]
        ),
        (1, 4, 0): 12 * U[12] * U[13],
        (1, 3, 1): 8 * (
            -2 * L[1] * U[13] + U[12] * U[16] + U[13] * U[15]
        ),
        (1, 2, 2): 2 * (
            -4 * L[1] * U[16] - 2 * L[2] * U[13]
            + 2 * U[12] * U[18] + 2 * U[15] * U[16]
            - W[1] + 2 * W[8]
        ),
        (1, 0, 4): 4 * (L[2] * U[18] - W[11]),
        (0, 5, 0): 6 * U[13]**2,
        (0, 4, 1): 8 * U[13] * U[16],
        (0, 3, 2): 2 * (2 * U[13] * U[18] + U[16]**2 - W[2]),
        (0, 1, 4): -2 * (U[18]**2 - W[5]),
    }
    require_table(actual_e5, expected_e5, "q*r raw E5 table")

    e5_solution = {
        u[11]: 0, u[12]: 0, u[13]: 0,
        v[6]: L[0] * (U[15] - L[1]),
        v[0]: (
            2 * W[7] - 2 * L[0] * U[16] + 3 * L[1]**2
            - 4 * L[1] * U[15] + U[15]**2
        ),
        v[1]: 2 * W[8] - 4 * L[1] * U[16] + 2 * U[15] * U[16],
        v[11]: L[2] * U[18], v[2]: U[16]**2, v[5]: U[18]**2,
    }
    # Apply the triangular substitutions in derivation order; ``substitute``
    # is deliberately simultaneous rather than recursively rewriting images.
    require(all(not coefficient.substitute(e6_solution).substitute(e5_solution)
                for coefficient in coefficient_table(weighted, 5).values()),
            "q*r complete E6/E5 parametrization does not satisfy E5")
    raw_cubic = [
        entry.substitute(e6_solution).substitute(e5_solution)
        for entry in cubic
    ]
    raw_quadratic = [
        entry.substitute(e6_solution).substitute(e5_solution)
        for entry in quadratic
    ]
    direction = (-U[18], -L[2], L[1] - U[15])
    normalized_cubic = [
        raw_cubic[index] + directional_derivative(quartic, direction)[index]
        for index in range(3)
    ]
    first_direction = directional_derivative(raw_cubic, direction)
    second_direction = directional_derivative(
        directional_derivative(quartic, direction), direction
    )
    normalized_quadratic = [
        raw_quadratic[index] + first_direction[index]
        + Fraction(1, 2) * second_direction[index]
        for index in range(3)
    ]

    aa = L[0]
    bb = 2 * L[1] - U[15]
    cc = U[16]
    xx = W[7] + L[1]**2 - U[15] * L[1]
    yy = W[8] + U[16] * (L[1] - U[15])
    dd = W[3] - 2 * U[16] * L[2] - 4 * U[15] * U[18] + 4 * U[18] * L[1]
    ee = W[4] - 2 * U[16] * U[18]
    ff = W[9] - 2 * L[0] * U[18] - U[15] * L[2]
    gg = W[10] - 2 * U[16] * L[2] - U[15] * U[18]
    expected_cubic = [
        2 * cc * p * q * r,
        r * (aa * p**2 + bb * p * q + cc * q**2),
        ZERO,
    ]
    expected_quadratic = [
        (2 * xx - 2 * aa * cc) * p**2
        + (2 * yy - 2 * bb * cc) * p * q + cc**2 * q**2
        + dd * p * r + ee * q * r,
        xx * p * q + yy * q**2 + ff * p * r + gg * q * r,
        q * r,
    ]
    require(normalized_cubic == expected_cubic,
            "q*r translation does not give the claimed cubic normal form")
    require(normalized_quadratic == expected_quadratic,
            "q*r translation does not give the claimed quadratic normal form")
    normalized_third_row = (
        L[0], L[1] + direction[2], L[2] + direction[1]
    )
    require(normalized_third_row == (aa, bb, ZERO),
            "q*r translation does not give the claimed linear third row")

    lam = [V(f"qlam{index}") for index in range(6)]
    linear = matrix_from_rows([
        lam[:3], lam[3:], [aa, bb, 0],
    ])
    determinant = weighted_determinant(
        linear, expected_quadratic, expected_cubic, quartic
    )
    for degree in (8, 7, 6, 5):
        require(not coefficient_table(determinant, degree),
                f"q*r normalized family has unexpected E{degree}")
    e4 = coefficient_table(determinant, 4)
    require(e4.get((0, 1, 3), ZERO) == lam[2],
            "q*r q*r^3 exit coefficient mismatch")
    require(e4.get((1, 0, 3), ZERO) == -2 * lam[5],
            "q*r p*r^3 exit coefficient mismatch")
    require(determinant3(linear).substitute({f"qlam{2}": 0, f"qlam{5}": 0}) == 0,
            "q*r exit does not force singular linear part")


def audit_pr_orbit() -> None:
    p, q, r = V("p"), V("q"), V("r")
    quartic, cubic, quadratic, _, weighted, u, v, ell = exceptional_setup(
        p * r, "p"
    )
    U = [V(name) for name in u]
    W = [V(name) for name in v]
    L = [V(name) for name in ell]

    e6 = coefficient_table(weighted, 6)
    system_variables = u + ell
    require(linear_rank(list(e6.values()), system_variables) == 10,
            "p*r raw E6 rank is not 10")
    e6_solution = {
        u[0]: 0, u[1]: 0, u[2]: 0, u[3]: 0,
        u[4]: 2 * L[0], u[5]: 2 * L[1], u[6]: 0,
        u[7]: 2 * L[2], u[8]: 0, u[9]: 0,
    }
    require(all(not coefficient.substitute(e6_solution) for coefficient in e6.values()),
            "p*r proposed E6 kernel does not satisfy E6")
    require(len(system_variables) - 10 == 13,
            "p*r E6 parametrization has wrong dimension")
    require(set(u[10:] + ell).isdisjoint(e6_solution)
            and len(u[10:] + ell) == 13,
            "p*r E6 free coordinates are not independent coordinates")

    actual_e5 = {
        key: value.substitute(e6_solution)
        for key, value in coefficient_table(weighted, 5).items()
    }
    expected_e5 = {
        (3, 0, 2): 2 * (-L[0]**2 + W[0]),
        (2, 1, 2): 2 * (-2 * L[0] * L[1] + W[1]),
        (1, 2, 2): 2 * (-L[1]**2 + W[2]),
        (1, 0, 4): -2 * (-L[2]**2 + W[5]),
    }
    require_table(actual_e5, expected_e5, "p*r raw E5 table")
    e5_solution = {
        v[0]: L[0]**2, v[1]: 2 * L[0] * L[1],
        v[2]: L[1]**2, v[5]: L[2]**2,
    }
    require(all(not coefficient.substitute(e6_solution).substitute(e5_solution)
                for coefficient in coefficient_table(weighted, 5).values()),
            "p*r complete E5 parametrization does not satisfy E5")

    raw_cubic = [
        entry.substitute(e6_solution).substitute(e5_solution)
        for entry in cubic
    ]
    raw_quadratic = [
        entry.substitute(e6_solution).substitute(e5_solution)
        for entry in quadratic
    ]
    direction = (-L[2], ZERO, -L[0])
    normalized_cubic = [
        raw_cubic[index] + directional_derivative(quartic, direction)[index]
        for index in range(3)
    ]
    normalized_quadratic = [
        raw_quadratic[index]
        + directional_derivative(raw_cubic, direction)[index]
        + Fraction(1, 2) * directional_derivative(
            directional_derivative(quartic, direction), direction
        )[index]
        for index in range(3)
    ]
    tau = L[1]
    D = W[3] - 4 * L[0] * L[2]
    K = W[4] - 2 * L[1] * L[2]
    require(normalized_cubic[0] == 2 * tau * p * q * r,
            "p*r translation does not normalize the first cubic component")
    require(normalized_cubic[2] == 0,
            "p*r translation created a cubic normal component")
    require(normalized_quadratic[0] == tau**2 * q**2 + D * p * r + K * q * r,
            "p*r translation does not normalize the first quadratic component")
    require(normalized_quadratic[2] == p * r,
            "p*r translation changed the quadratic normal component")
    normalized_third_row = (
        L[0] + direction[2], L[1], L[2] + direction[0]
    )
    require(normalized_third_row == (ZERO, tau, ZERO),
            "p*r translation does not normalize the linear third row")

    # Restart with independent names in the normalized family.  The second
    # cubic and quadratic components are unrestricted because translation is
    # an affine bijection on their coefficient spaces.
    tau, K, D = V("tau"), V("K"), V("D")
    up = [V(f"up{index}") for index in range(10)]
    wp = [V(f"wp{index}") for index in range(6)]
    lam = [V(f"plam{index}") for index in range(6)]
    normalized_cubic = [
        2 * tau * p * q * r,
        sum((up[index] * monomial_xyz(exponent)
             for index, exponent in enumerate(CUBIC_EXPONENTS)), ZERO),
        ZERO,
    ]
    normalized_quadratic = [
        tau**2 * q**2 + D * p * r + K * q * r,
        sum((wp[index] * monomial_xyz(exponent)
             for index, exponent in enumerate(QUADRATIC_EXPONENTS)), ZERO),
        p * r,
    ]
    linear = matrix_from_rows([
        lam[:3], lam[3:], [0, tau, 0],
    ])
    determinant = weighted_determinant(
        linear, normalized_quadratic, normalized_cubic, quartic
    )
    for degree in (8, 7, 6, 5):
        require(not coefficient_table(determinant, degree),
                f"p*r normalized family has unexpected E{degree}")
    e4_expected = {
        (0, 0, 4): 3 * K * up[9],
        (0, 1, 3): K * up[8],
        (1, 0, 3): K * up[7] - lam[2],
        (0, 2, 2): K * (tau - up[6]),
        (1, 1, 2): -tau * D - K * up[5] + lam[1],
        (2, 0, 2): -K * up[4] + lam[0],
        (0, 3, 1): -3 * K * up[3],
        (1, 2, 1): -3 * K * up[2],
        (2, 1, 1): -3 * K * up[1],
        (3, 0, 1): -3 * K * up[0],
    }
    require_table(coefficient_table(determinant, 4), e4_expected,
                  "p*r normalized E4 table")

    k_zero_solution = {
        "K": 0, "plam0": 0, "plam1": tau * D, "plam2": 0,
    }
    require(determinant3(linear).substitute(k_zero_solution) == 0,
            "p*r K=0 branch does not force singular linear part")

    A, B, C = V("A"), V("B"), V("C")
    e4_solution = {
        "up0": 0, "up1": 0, "up2": 0, "up3": 0,
        "up4": A, "up5": B, "up6": tau, "up7": C,
        "up8": 0, "up9": 0,
        "plam0": K * A, "plam1": tau * D + K * B, "plam2": K * C,
    }
    require(all(not coefficient.substitute(e4_solution)
                for coefficient in coefficient_table(determinant, 4).values()),
            "p*r K!=0 E4 parametrization does not satisfy E4")

    determinant_after_e4 = determinant.substitute(e4_solution)
    e3_expected = {
        (2, 0, 1): -2 * K * wp[0],
        (1, 1, 1): -2 * K * (-A * tau + wp[1]),
        (0, 2, 1): -2 * K * (-B * tau + wp[2]),
        (0, 0, 3): 2 * K * wp[5],
    }
    require_table(coefficient_table(determinant_after_e4, 3), e3_expected,
                  "p*r K!=0 E3 table")
    E, G = V("E"), V("G")
    e3_solution = {
        "wp0": 0, "wp1": A * tau, "wp2": B * tau,
        "wp3": E, "wp4": G, "wp5": 0,
    }
    determinant_after_e3 = determinant_after_e4.substitute(e3_solution)
    m, n, o = lam[3], lam[4], lam[5]
    e2_expected = {
        (1, 0, 1): -K * (A * C * tau - A * G + m),
        (0, 1, 1): -K * (B * C * tau - B * G - E * tau + n),
        (0, 0, 2): K * (C**2 * tau - C * G + o),
    }
    require_table(coefficient_table(determinant_after_e3, 2), e2_expected,
                  "p*r K!=0 E2 table")
    lower_solution = {
        "plam3": A * (G - C * tau),
        "plam4": E * tau + B * (G - C * tau),
        "plam5": C * (G - C * tau),
    }
    require(all(not coefficient.substitute(lower_solution)
                for coefficient in coefficient_table(determinant_after_e3, 2).values()),
            "p*r lower solution does not satisfy E2")
    require(all(not coefficient.substitute(lower_solution)
                for coefficient in coefficient_table(determinant_after_e3, 1).values()),
            "p*r lower solution does not satisfy E1")
    require(determinant3(linear).substitute(e4_solution).substitute(lower_solution) == 0,
            "p*r K!=0 branch does not force singular linear part")


def main() -> None:
    require(__debug__, "refusing optimized Python: fail-closed checks required")
    for path, expected in EXPECTED_HASHES.items():
        require(digest(path) == expected, f"pinned-input hash mismatch: {path}")
    audit_frozen_bridge()
    audit_qr_orbit()
    audit_pr_orbit()
    print(
        "PASS: independent hostile bridge reconstruction; "
        "45 pivots + complete nonbinary raw orbit solves"
    )


if __name__ == "__main__":
    main()
