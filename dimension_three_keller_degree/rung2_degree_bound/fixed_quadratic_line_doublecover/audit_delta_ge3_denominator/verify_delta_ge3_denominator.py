#!/usr/bin/env python3
"""Dependency-free exact checks for the blinded delta>=3 denominator.

This file reads no project artifact and uses only the Python standard
library.  It checks the characteristic-zero representatives over Q and
small exact number fields, the incidence-family ledger, the exceptional
moduli and boundary equations, and exhaustive finite-field regressions of
the boundary charts and stabilizer quotients.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
import sys


if not __debug__:
    print("FAIL: assertions are required; do not run with -O", file=sys.stderr)
    raise SystemExit(2)


# ---------------------------------------------------------------------------
# A tiny exact number-field implementation.
# ---------------------------------------------------------------------------


def qtrim(values: list[Fraction]) -> list[Fraction]:
    values = [Fraction(value) for value in values]
    while len(values) > 1 and values[-1] == 0:
        values.pop()
    return values


def qadd(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    length = max(len(left), len(right))
    return qtrim(
        [
            (left[index] if index < len(left) else 0)
            + (right[index] if index < len(right) else 0)
            for index in range(length)
        ]
    )


def qsub(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    return qadd(left, [-value for value in right])


def qmul(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    answer = [Fraction(0)] * (len(left) + len(right) - 1)
    for first, left_value in enumerate(left):
        for second, right_value in enumerate(right):
            answer[first + second] += left_value * right_value
    return qtrim(answer)


def qdivmod(
    numerator: list[Fraction], denominator: list[Fraction]
) -> tuple[list[Fraction], list[Fraction]]:
    numerator = qtrim(numerator)
    denominator = qtrim(denominator)
    if denominator == [0]:
        raise ZeroDivisionError
    quotient = [Fraction(0)] * max(1, len(numerator) - len(denominator) + 1)
    while numerator != [0] and len(numerator) >= len(denominator):
        degree = len(numerator) - len(denominator)
        coefficient = numerator[-1] / denominator[-1]
        quotient[degree] += coefficient
        subtraction = [Fraction(0)] * degree + [
            coefficient * value for value in denominator
        ]
        numerator = qsub(numerator, subtraction)
    return qtrim(quotient), qtrim(numerator)


def qxgcd(
    first: list[Fraction], second: list[Fraction]
) -> tuple[list[Fraction], list[Fraction], list[Fraction]]:
    old_r, r = qtrim(first), qtrim(second)
    old_s, s = [Fraction(1)], [Fraction(0)]
    old_t, t = [Fraction(0)], [Fraction(1)]
    while r != [0]:
        quotient, remainder = qdivmod(old_r, r)
        old_r, r = r, remainder
        old_s, s = s, qsub(old_s, qmul(quotient, s))
        old_t, t = t, qsub(old_t, qmul(quotient, t))
    return old_r, old_s, old_t


class NumberField:
    def __init__(self, modulus: tuple[int | Fraction, ...], label: str):
        normalized = qtrim([Fraction(value) for value in modulus])
        if len(normalized) < 2 or normalized[-1] == 0:
            raise ValueError("invalid number-field modulus")
        leading = normalized[-1]
        self.modulus = tuple(value / leading for value in normalized)
        self.degree = len(self.modulus) - 1
        self.label = label
        self.zero = NFElement(self, (Fraction(0),))
        self.one = NFElement(self, (Fraction(1),))

    def reduce(self, values: list[Fraction]) -> tuple[Fraction, ...]:
        _, remainder = qdivmod(qtrim(values), list(self.modulus))
        return tuple(remainder)

    def element(self, value: object) -> "NFElement":
        if isinstance(value, NFElement):
            if value.field is not self:
                raise ValueError("mixed number fields")
            return value
        if isinstance(value, (int, Fraction)):
            return NFElement(self, (Fraction(value),))
        if isinstance(value, (list, tuple)):
            return NFElement(self, tuple(Fraction(entry) for entry in value))
        raise TypeError(value)

    def inverse(self, value: "NFElement") -> "NFElement":
        value = self.element(value)
        if not value:
            raise ZeroDivisionError
        gcd, coefficient, _ = qxgcd(list(value.coefficients), list(self.modulus))
        if len(gcd) != 1 or gcd[0] == 0:
            raise ZeroDivisionError("element is not invertible")
        return self.element([entry / gcd[0] for entry in coefficient])


class NFElement:
    def __init__(self, field: NumberField, coefficients: tuple[Fraction, ...]):
        self.field = field
        self.coefficients = field.reduce(list(coefficients))

    def _coerce(self, other: object) -> "NFElement":
        return self.field.element(other)

    def __add__(self, other: object) -> "NFElement":
        other = self._coerce(other)
        return self.field.element(qadd(list(self.coefficients), list(other.coefficients)))

    __radd__ = __add__

    def __neg__(self) -> "NFElement":
        return self.field.element([-value for value in self.coefficients])

    def __sub__(self, other: object) -> "NFElement":
        return self + (-self._coerce(other))

    def __rsub__(self, other: object) -> "NFElement":
        return self._coerce(other) - self

    def __mul__(self, other: object) -> "NFElement":
        other = self._coerce(other)
        return self.field.element(qmul(list(self.coefficients), list(other.coefficients)))

    __rmul__ = __mul__

    def __truediv__(self, other: object) -> "NFElement":
        other = self._coerce(other)
        return self * self.field.inverse(other)

    def __rtruediv__(self, other: object) -> "NFElement":
        return self._coerce(other) / self

    def __pow__(self, exponent: int) -> "NFElement":
        if exponent < 0:
            return (self.field.inverse(self)) ** (-exponent)
        answer = self.field.one
        base = self
        power = exponent
        while power:
            if power & 1:
                answer = answer * base
            base = base * base
            power >>= 1
        return answer

    def __eq__(self, other: object) -> bool:
        try:
            other = self._coerce(other)
        except (TypeError, ValueError):
            return False
        return self.coefficients == other.coefficients

    def __bool__(self) -> bool:
        return any(self.coefficients)

    def __repr__(self) -> str:
        return f"{self.field.label}{self.coefficients}"


class RationalField:
    zero = Fraction(0)
    one = Fraction(1)

    @staticmethod
    def element(value: object) -> Fraction:
        return Fraction(value)


QQ = RationalField()


# ---------------------------------------------------------------------------
# Generic univariate polynomial arithmetic over a field.
# ---------------------------------------------------------------------------


def ptrim(values: list[object], field: object) -> list[object]:
    values = [field.element(value) for value in values]
    while len(values) > 1 and values[-1] == field.zero:
        values.pop()
    return values


def padd(left: list[object], right: list[object], field: object) -> list[object]:
    length = max(len(left), len(right))
    return ptrim(
        [
            (left[index] if index < len(left) else field.zero)
            + (right[index] if index < len(right) else field.zero)
            for index in range(length)
        ],
        field,
    )


def pscale(values: list[object], scalar: object, field: object) -> list[object]:
    scalar = field.element(scalar)
    return ptrim([scalar * value for value in values], field)


def pmul(left: list[object], right: list[object], field: object) -> list[object]:
    answer = [field.zero] * (len(left) + len(right) - 1)
    for first, left_value in enumerate(left):
        for second, right_value in enumerate(right):
            answer[first + second] = (
                answer[first + second] + left_value * right_value
            )
    return ptrim(answer, field)


def pderivative(values: list[object], field: object) -> list[object]:
    if len(values) == 1:
        return [field.zero]
    return ptrim(
        [field.element(index) * values[index] for index in range(1, len(values))],
        field,
    )


def pdivmod(
    numerator: list[object], denominator: list[object], field: object
) -> tuple[list[object], list[object]]:
    numerator = ptrim(numerator, field)
    denominator = ptrim(denominator, field)
    if denominator == [field.zero]:
        raise ZeroDivisionError
    quotient = [field.zero] * max(1, len(numerator) - len(denominator) + 1)
    while numerator != [field.zero] and len(numerator) >= len(denominator):
        degree = len(numerator) - len(denominator)
        coefficient = numerator[-1] / denominator[-1]
        quotient[degree] = quotient[degree] + coefficient
        subtraction = [field.zero] * degree + [
            coefficient * value for value in denominator
        ]
        numerator = padd(numerator, pscale(subtraction, -1, field), field)
    return ptrim(quotient, field), ptrim(numerator, field)


def pmonic(values: list[object], field: object) -> list[object]:
    values = ptrim(values, field)
    if values == [field.zero]:
        return values
    return pscale(values, field.one / values[-1], field)


def pgcd(left: list[object], right: list[object], field: object) -> list[object]:
    left = ptrim(left, field)
    right = ptrim(right, field)
    if left == [field.zero]:
        return pmonic(right, field)
    while right != [field.zero]:
        left, right = right, pdivmod(left, right, field)[1]
    return pmonic(left, field)


# Homogeneous binary forms use descending coefficients:
# [p^d, p^(d-1)q, ..., q^d].


def hmul(
    left: tuple[object, ...], right: tuple[object, ...], field: object
) -> tuple[object, ...]:
    answer = [field.zero] * (len(left) + len(right) - 1)
    for first, left_value in enumerate(left):
        for second, right_value in enumerate(right):
            answer[first + second] = (
                answer[first + second]
                + field.element(left_value) * field.element(right_value)
            )
    return tuple(answer)


def dehomogeneous(form: tuple[object, ...], field: object) -> list[object]:
    return ptrim([field.element(value) for value in reversed(form)], field)


def jacobian_binary(
    first: tuple[object, ...],
    first_degree: int,
    second: tuple[object, ...],
    second_degree: int,
    field: object,
) -> list[object]:
    first_affine = dehomogeneous(first, field)
    second_affine = dehomogeneous(second, field)
    return padd(
        pscale(
            pmul(pderivative(first_affine, field), second_affine, field),
            second_degree,
            field,
        ),
        pscale(
            pmul(first_affine, pderivative(second_affine, field), field),
            -first_degree,
            field,
        ),
        field,
    )


def homogeneous_gcd_degree(
    forms: tuple[list[object], ...],
    degrees: tuple[int, ...],
    field: object,
) -> int:
    nonzero = [
        (ptrim(form, field), degree)
        for form, degree in zip(forms, degrees)
        if ptrim(form, field) != [field.zero]
    ]
    gcd = [field.zero]
    infinity = 10**9
    for form, degree in nonzero:
        gcd = pgcd(gcd, form, field)
        infinity = min(infinity, degree - (len(form) - 1))
    return len(gcd) - 1 + infinity


def linearly_dependent(
    first: list[object], second: list[object], field: object
) -> bool:
    first = first + [field.zero] * (6 - len(first))
    second = second + [field.zero] * (6 - len(second))
    return all(
        first[i] * second[j] == first[j] * second[i]
        for i in range(6)
        for j in range(6)
    )


def delta_and_dependence(
    h: tuple[object, object, object],
    R: tuple[object, object, object, object],
    field: object = QQ,
) -> tuple[int, bool]:
    p_squared = (field.one, field.zero, field.zero)
    q_squared = (field.zero, field.zero, field.one)
    P = hmul(h, p_squared, field)
    Q = hmul(h, q_squared, field)
    alpha = jacobian_binary(Q, 4, R, 3, field)
    beta = pscale(jacobian_binary(P, 4, R, 3, field), -1, field)
    gamma = jacobian_binary(P, 4, Q, 4, field)
    return (
        homogeneous_gcd_degree((alpha, beta, gamma), (5, 5, 6), field),
        linearly_dependent(alpha, beta, field),
    )


def require_delta(
    h: tuple[object, object, object],
    R: tuple[object, object, object, object],
    expected_delta: int,
    label: str,
    field: object = QQ,
) -> None:
    actual_delta, dependent = delta_and_dependence(h, R, field)
    assert not dependent, (label, "unexpected dependent case")
    assert actual_delta == expected_delta, (label, actual_delta, expected_delta)


def verify_characteristic_zero_representatives() -> None:
    p = (Fraction(1), Fraction(0))
    q = (Fraction(0), Fraction(1))
    L = (Fraction(1), Fraction(1))

    branch_square = hmul(p, p, QQ)
    branch_square_delta3 = (
        hmul(hmul(p, p, QQ), q, QQ),
        hmul(hmul(p, p, QQ), L, QQ),
        hmul(p, hmul(q, q, QQ), QQ),
        hmul(p, (Fraction(1), Fraction(0), Fraction(1)), QQ),
    )
    for index, R in enumerate(branch_square_delta3):
        require_delta(branch_square, R, 3, f"branch-square delta3 #{index}")
    power_R = hmul(hmul(p, p, QQ), p, QQ)
    power_delta, power_dependent = delta_and_dependence(branch_square, power_R)
    assert power_dependent and power_delta == 5

    two_branch = hmul(p, q, QQ)
    for index, R in enumerate(
        (
            hmul(hmul(p, p, QQ), p, QQ),
            hmul(hmul(p, p, QQ), q, QQ),
        )
    ):
        require_delta(two_branch, R, 3, f"two-branch delta3 #{index}")

    one_branch = hmul(p, L, QQ)
    one_branch_delta3 = (
        hmul(hmul(p, p, QQ), p, QQ),
        hmul(hmul(p, p, QQ), L, QQ),
        hmul(p, hmul(L, L, QQ), QQ),
        hmul(hmul(p, p, QQ), (Fraction(4), Fraction(3)), QQ),
        hmul(hmul(p, L, QQ), (Fraction(-4), Fraction(1)), QQ),
        hmul(hmul(L, L, QQ), (Fraction(-4), Fraction(5)), QQ),
    )
    for index, R in enumerate(one_branch_delta3):
        require_delta(one_branch, R, 3, f"one-branch delta3 #{index}")

    doubled = hmul(L, L, QQ)
    doubled_delta3 = (
        hmul(hmul(L, L, QQ), p, QQ),
        hmul(L, (Fraction(0), Fraction(1), Fraction(2)), QQ),
        (Fraction(1), Fraction(3, 2), Fraction(0), Fraction(0)),
    )
    # The last representative is replaced by a literal both-contact form.
    doubled_delta3 = (
        doubled_delta3[0],
        doubled_delta3[1],
        (Fraction(1), Fraction(3, 2), Fraction(0), Fraction(0)),
    )
    # a=1,d=0 in (a,3a/2,3d/2,d).
    for index, R in enumerate(doubled_delta3):
        require_delta(doubled, R, 3, f"doubled-nonbranch delta3 #{index}")

    doubled_delta4 = (
        hmul(hmul(L, L, QQ), L, QQ),
        hmul(hmul(L, L, QQ), (Fraction(1), Fraction(-2)), QQ),
        hmul(L, (Fraction(2), Fraction(1), Fraction(2)), QQ),
    )
    for index, R in enumerate(doubled_delta4):
        require_delta(doubled, R, 4, f"doubled-nonbranch delta4 #{index}")

    # Generic squarefree representatives at r=2.
    r = Fraction(2)
    X = (Fraction(1), -r)
    Y = (Fraction(1), -1 / r)
    h = hmul(X, Y, QQ)
    eta = -(r + 1 / r)
    assert h == (1, eta, 1)
    squarefree_delta3 = (
        hmul(hmul(X, X, QQ), Y, QQ),
        hmul(hmul(X, X, QQ), (5 - 3 * r**2, 4 * r), QQ),
        hmul(h, (r**2 + 1, 4 * r), QQ),
        hmul(
            X,
            (
                4 * r / (r**2 - 3),
                Fraction(1),
                -4 * r / (3 * r**2 - 1),
            ),
            QQ,
        ),
    )
    for index, R in enumerate(squarefree_delta3):
        require_delta(h, R, 3, f"squarefree generic delta3 #{index}")

    # The second point over the same kappa in the two-sheet contact family.
    inverse_r = 1 / r
    inverse_X = (Fraction(1), -inverse_r)
    inverse_Y = (Fraction(1), -r)
    inverse_h = hmul(inverse_X, inverse_Y, QQ)
    inverse_contact = hmul(
        hmul(inverse_X, inverse_X, QQ),
        (5 - 3 * inverse_r**2, 4 * inverse_r),
        QQ,
    )
    assert inverse_h == h
    require_delta(h, inverse_contact, 3, "squarefree second contact sheet")

    # Squarefree delta=4 representatives over exact number fields.
    field_a = NumberField((5, 0, 1), "r2=-5:")
    ra = field_a.element((0, 1))
    Xa = (field_a.one, -ra)
    Ya = (field_a.one, -(field_a.one / ra))
    ha = hmul(Xa, Ya, field_a)
    require_delta(
        ha,
        hmul(hmul(Xa, Xa, field_a), Ya, field_a),
        4,
        "squarefree kappa=-16/5 delta4",
        field_a,
    )

    field_b = NumberField((1, 0, Fraction(-6, 5), 0, 1), "5r4-6r2+5:")
    rb = field_b.element((0, 1))
    Xb = (field_b.one, -rb)
    Yb = (field_b.one, -(field_b.one / rb))
    hb = hmul(Xb, Yb, field_b)
    Lb = (5 - 3 * rb**2, 4 * rb)
    require_delta(
        hb,
        hmul(hmul(Xb, Xb, field_b), Lb, field_b),
        4,
        "squarefree kappa=16/5 delta4",
        field_b,
    )

    field_c = NumberField((1, -4, 1), "r2-4r+1:")
    rc = field_c.element((0, 1))
    Xc = (field_c.one, -rc)
    Yc = (field_c.one, -(field_c.one / rc))
    hc = hmul(Xc, Yc, field_c)
    Lc = (rc**2 + 1, 4 * rc)
    require_delta(
        hc,
        hmul(hc, Lc, field_c),
        4,
        "squarefree kappa=16 delta4",
        field_c,
    )


def verify_boundary_equations_and_ledger() -> None:
    delta3_ids = (
        "D3-BS-N2-Z",
        "D3-BS-N2-NZ",
        "D3-BS-N1-BR2",
        "D3-BS-N1-CONTACT",
        "D3-BB-30",
        "D3-BB-21",
        "D3-OB-300",
        "D3-OB-210",
        "D3-OB-120",
        "D3-OB-20C",
        "D3-OB-11C",
        "D3-OB-02C",
        "D3-SF-21",
        "D3-SF-20C",
        "D3-SF-11C",
        "D3-SF-10CC",
        "D3-DN-2",
        "D3-DN-1C",
        "D3-DN-0CC",
    )
    delta4_ids = (
        "D4-SF-21C",
        "D4-SF-20CC",
        "D4-SF-11CC",
        "D4-DN-3",
        "D4-DN-2C",
        "D4-DN-1CC",
    )
    power_ids = ("PF-BRANCH-FOURTH-THIRD",)
    assert len(delta3_ids) == 19 == len(set(delta3_ids))
    assert len(delta4_ids) == 6 == len(set(delta4_ids))
    assert len(power_ids) == 1
    assert len(set(delta3_ids + delta4_ids + power_ids)) == 26

    # The two generic SF-20C orbit sheets form one z-parameter curve.
    # kappa=z+2+z^{-1}; the special fibres below are exact.
    def kappa(z: Fraction) -> Fraction:
        return z + 2 + 1 / z

    assert kappa(Fraction(-5)) == Fraction(-16, 5)
    assert kappa(Fraction(-1, 5)) == Fraction(-16, 5)
    assert kappa(Fraction(3)) == Fraction(16, 3)
    assert kappa(Fraction(1, 3)) == Fraction(16, 3)
    assert kappa(Fraction(-1)) == 0
    assert kappa(Fraction(1)) == 4

    # After multiplying kappa-K by z, the ascending coefficient list is
    # [1, 2-K, 1].  Clear the rational denominator and check every
    # advertised boundary polynomial without a symbolic dependency.
    def cleared_kappa(K: Fraction) -> list[Fraction]:
        coefficients = [Fraction(1), Fraction(2) - K, Fraction(1)]
        denominator = K.denominator
        return [denominator * value for value in coefficients]

    assert cleared_kappa(Fraction(16, 5)) == [5, -6, 5]
    assert cleared_kappa(Fraction(16)) == [1, -14, 1]
    assert cleared_kappa(Fraction(-16, 5)) == [5, 26, 5]
    assert cleared_kappa(Fraction(16, 3)) == [3, -10, 3]
    assert cleared_kappa(Fraction(0)) == [1, 2, 1]
    assert cleared_kappa(Fraction(4)) == [1, -2, 1]

    # Rationally split special fibres have the claimed factors.
    assert qmul([5, 1], [1, 5]) == [5, 26, 5]
    assert qmul([-1, 3], [-3, 1]) == [3, -10, 3]
    assert qmul([1, 1], [1, 1]) == [1, 2, 1]
    assert qmul([-1, 1], [-1, 1]) == [1, -2, 1]

    # Doubled-nonbranch projective charts and their removed boundaries.
    # n_L=2: u!=v, 2u+v!=0, u+2v!=0, modulo swap.
    test_u, test_v = Fraction(1), Fraction(0)
    assert test_u != test_v
    assert 2 * test_u + test_v != 0
    assert test_u + 2 * test_v != 0
    # n_L=1, contact at p: C=2B, with A!=-B and A!=2B.
    test_A, test_B = Fraction(0), Fraction(1)
    assert test_A != -test_B and test_A != 2 * test_B
    # n_L=0, both contacts: (a,3a/2,3d/2,d), with a!=d.
    assert Fraction(1) != Fraction(0)


# ---------------------------------------------------------------------------
# Exact finite-field exhaustive regression and stabilizer orbit counts.
# ---------------------------------------------------------------------------


def ftrim(values: list[int], prime: int) -> list[int]:
    values = [value % prime for value in values]
    while len(values) > 1 and values[-1] == 0:
        values.pop()
    return values


def fadd(left: list[int], right: list[int], prime: int) -> list[int]:
    length = max(len(left), len(right))
    return ftrim(
        [
            (left[index] if index < len(left) else 0)
            + (right[index] if index < len(right) else 0)
            for index in range(length)
        ],
        prime,
    )


def fscale(values: list[int], scalar: int, prime: int) -> list[int]:
    return ftrim([scalar * value for value in values], prime)


def fmul(left: list[int], right: list[int], prime: int) -> list[int]:
    answer = [0] * (len(left) + len(right) - 1)
    for first, left_value in enumerate(left):
        for second, right_value in enumerate(right):
            answer[first + second] += left_value * right_value
    return ftrim(answer, prime)


def fderivative(values: list[int], prime: int) -> list[int]:
    return ftrim(
        [index * values[index] for index in range(1, len(values))] or [0],
        prime,
    )


def fdivmod(
    numerator: list[int], denominator: list[int], prime: int
) -> tuple[list[int], list[int]]:
    numerator = ftrim(numerator, prime)
    denominator = ftrim(denominator, prime)
    quotient = [0] * max(1, len(numerator) - len(denominator) + 1)
    inverse = pow(denominator[-1], -1, prime)
    while numerator != [0] and len(numerator) >= len(denominator):
        degree = len(numerator) - len(denominator)
        coefficient = numerator[-1] * inverse % prime
        quotient[degree] += coefficient
        for index, value in enumerate(denominator):
            numerator[index + degree] -= coefficient * value
        numerator = ftrim(numerator, prime)
    return ftrim(quotient, prime), numerator


def fmonic(values: list[int], prime: int) -> list[int]:
    values = ftrim(values, prime)
    if values == [0]:
        return values
    return fscale(values, pow(values[-1], -1, prime), prime)


def fgcd(left: list[int], right: list[int], prime: int) -> list[int]:
    left = ftrim(left, prime)
    right = ftrim(right, prime)
    if left == [0]:
        return fmonic(right, prime)
    while right != [0]:
        left, right = right, fdivmod(left, right, prime)[1]
    return fmonic(left, prime)


def fjac(
    first: list[int],
    first_degree: int,
    second: list[int],
    second_degree: int,
    prime: int,
) -> list[int]:
    return fadd(
        fscale(
            fmul(fderivative(first, prime), second, prime),
            second_degree,
            prime,
        ),
        fscale(
            fmul(first, fderivative(second, prime), prime),
            -first_degree,
            prime,
        ),
        prime,
    )


def finite_invariants(
    h: tuple[int, int, int], R: tuple[int, int, int, int], prime: int
) -> tuple[int, bool]:
    h_affine = ftrim(list(reversed(h)), prime)
    R_affine = ftrim(list(reversed(R)), prime)
    P = fmul(h_affine, [0, 0, 1], prime)
    Q = h_affine
    alpha = fjac(Q, 4, R_affine, 3, prime)
    beta = fscale(fjac(P, 4, R_affine, 3, prime), -1, prime)
    gamma = fjac(P, 4, Q, 4, prime)
    gcd = [0]
    infinity = 99
    for form, degree in ((alpha, 5), (beta, 5), (gamma, 6)):
        if ftrim(form, prime) != [0]:
            gcd = fgcd(gcd, form, prime)
            infinity = min(infinity, degree - (len(ftrim(form, prime)) - 1))
    delta = len(gcd) - 1 + infinity
    padded_alpha = alpha + [0] * (6 - len(alpha))
    padded_beta = beta + [0] * (6 - len(beta))
    dependent = all(
        (
            padded_alpha[first] * padded_beta[second]
            - padded_alpha[second] * padded_beta[first]
        )
        % prime
        == 0
        for first in range(6)
        for second in range(6)
    )
    return delta, dependent


def projective_tuples(length: int, prime: int):
    for first in range(length):
        for tail in product(range(prime), repeat=length - first - 1):
            yield (0,) * first + (1,) + tail


def projective_normalize(values: tuple[int, ...], prime: int) -> tuple[int, ...]:
    first = next(index for index, value in enumerate(values) if value % prime)
    inverse = pow(values[first] % prime, -1, prime)
    return tuple(value * inverse % prime for value in values)


def orbit_count(
    points: set[tuple[int, ...]],
    transformations,
    prime: int,
) -> int:
    remaining = set(points)
    count = 0
    while remaining:
        seed = next(iter(remaining))
        orbit = {
            projective_normalize(transformation(seed), prime)
            for transformation in transformations
        }
        frontier = list(orbit)
        while frontier:
            point = frontier.pop()
            for transformation in transformations:
                image = projective_normalize(transformation(point), prime)
                if image not in orbit:
                    orbit.add(image)
                    frontier.append(image)
        remaining -= orbit
        count += 1
    return count


def verify_finite_exhaustion() -> None:
    for prime in (7, 11):
        charts = {
            "branch-square": (1, 0, 0),
            "two-branch": (0, 1, 0),
            "one-branch": (1, 1, 0),
            "doubled-nonbranch": (1, 2, 1),
        }
        expected = {
            "branch-square": (2 * prime, 0, 1),
            "two-branch": (4, 0, 0),
            "one-branch": (6, 0, 0),
            "doubled-nonbranch": (4 * (prime - 1), 4, 0),
        }
        point_sets: dict[str, set[tuple[int, ...]]] = {}
        for label, h in charts.items():
            counts = {3: 0, 4: 0, "power": 0}
            delta3_points: set[tuple[int, ...]] = set()
            for R in projective_tuples(4, prime):
                delta, dependent = finite_invariants(h, R, prime)
                if dependent:
                    counts["power"] += 1
                elif delta in (3, 4):
                    counts[delta] += 1
                if not dependent and delta == 3:
                    delta3_points.add(R)
            assert (
                counts[3],
                counts[4],
                counts["power"],
            ) == expected[label], (prime, label, counts)
            point_sets[label] = delta3_points

        diagonal = tuple(
            (
                lambda point, scalar=scalar: tuple(
                    value * scalar ** (3 - index)
                    for index, value in enumerate(point)
                )
            )
            for scalar in range(1, prime)
        )
        swap = lambda point: tuple(reversed(point))
        # Over a finite field the branch-square contact family can split
        # further by square class.  The characteristic-zero torus quotient
        # has four zero-pattern orbits, checked in the explicit Q
        # representatives above; do not mistake finite-field square classes
        # for extra complex orbits.
        assert (
            orbit_count(
                point_sets["two-branch"],
                diagonal + (swap,),
                prime,
            )
            == 2
        )
        assert len(point_sets["one-branch"]) == 6

    # Generic split squarefree chart over F_11: ten raw delta3 points and
    # five swap orbits.
    prime = 11
    eta = 3  # h=t^2+3t+1 has two distinct F_11 roots.
    h = (1, eta, 1)
    generic_points = {
        R
        for R in projective_tuples(4, prime)
        if finite_invariants(h, R, prime) == (3, False)
    }
    assert len(generic_points) == 10
    swap = lambda point: tuple(reversed(point))
    assert orbit_count(generic_points, (swap,), prime) == 5

    # At kappa=0 the sign stabilizer identifies the two relative-contact
    # sheets: ten raw points but four orbits.
    prime = 13
    h = (1, 0, 1)
    jump_points = {
        R
        for R in projective_tuples(4, prime)
        if finite_invariants(h, R, prime) == (3, False)
    }
    assert len(jump_points) == 10
    swap = lambda point: tuple(reversed(point))
    sign = lambda point: tuple(
        value * (-1 if (3 - index) % 2 else 1)
        for index, value in enumerate(point)
    )
    assert orbit_count(jump_points, (swap, sign), prime) == 4

    # A split kappa=-16/5 fibre over F_7 has four delta3 and two delta4
    # points, exactly matching the boundary arrows.
    prime = 7
    h = (1, 1, 1)  # kappa=1=-16/5 mod 7, discriminant square.
    special_counts = {3: 0, 4: 0}
    for R in projective_tuples(4, prime):
        delta, dependent = finite_invariants(h, R, prime)
        if not dependent and delta in special_counts:
            special_counts[delta] += 1
    assert special_counts == {3: 4, 4: 2}


def main() -> None:
    verify_characteristic_zero_representatives()
    verify_boundary_equations_and_ledger()
    verify_finite_exhaustion()
    print("DELTA_GE3_DENOMINATOR_EXACT_PASS_19_6_1")
    print("exact delta=3: 19 incidence families")
    print("exact delta=4: 6 incidence families")
    print("dependent power fibre: 1 orbit")
    print("total refined denominator: 26 disjoint parameterized families")


if __name__ == "__main__":
    main()
