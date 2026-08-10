"""Small exact sparse-polynomial tools for the root/cut clean-room audit.

This module is intentionally self-contained.  In particular, it does not
import any project Fourier, sign, factorization, or certificate code.
"""

from __future__ import annotations

import ast
import itertools
import math
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from hashlib import sha256
from typing import Iterable, Mapping, Sequence


Exponent = tuple[int, ...]


@dataclass(frozen=True)
class Polynomial:
    width: int
    terms: tuple[tuple[Exponent, Fraction], ...]

    @classmethod
    def from_dict(
        cls, width: int, values: Mapping[Exponent, int | Fraction]
    ) -> "Polynomial":
        cleaned = tuple(
            sorted(
                (tuple(monomial), Fraction(coefficient))
                for monomial, coefficient in values.items()
                if coefficient
            )
        )
        if any(len(monomial) != width for monomial, _ in cleaned):
            raise ValueError("wrong monomial width")
        return cls(width, cleaned)

    @classmethod
    def constant(cls, width: int, value: int | Fraction) -> "Polynomial":
        coefficient = Fraction(value)
        return cls.from_dict(width, {(0,) * width: coefficient} if coefficient else {})

    @classmethod
    def variable(cls, width: int, index: int) -> "Polynomial":
        exponent = [0] * width
        exponent[index] = 1
        return cls.from_dict(width, {tuple(exponent): 1})

    def dictionary(self) -> dict[Exponent, Fraction]:
        return dict(self.terms)

    def __bool__(self) -> bool:
        return bool(self.terms)

    def _coerce(self, other: "Polynomial" | int | Fraction) -> "Polynomial":
        if isinstance(other, Polynomial):
            if other.width != self.width:
                raise ValueError("polynomials belong to different rings")
            return other
        return Polynomial.constant(self.width, other)

    def __add__(self, other: "Polynomial" | int | Fraction) -> "Polynomial":
        right = self._coerce(other)
        values = self.dictionary()
        for monomial, coefficient in right.terms:
            values[monomial] = values.get(monomial, Fraction()) + coefficient
        return Polynomial.from_dict(self.width, values)

    __radd__ = __add__

    def __neg__(self) -> "Polynomial":
        return Polynomial.from_dict(
            self.width, {monomial: -coefficient for monomial, coefficient in self.terms}
        )

    def __sub__(self, other: "Polynomial" | int | Fraction) -> "Polynomial":
        return self + (-self._coerce(other))

    def __rsub__(self, other: "Polynomial" | int | Fraction) -> "Polynomial":
        return self._coerce(other) - self

    def __mul__(self, other: "Polynomial" | int | Fraction) -> "Polynomial":
        right = self._coerce(other)
        values: dict[Exponent, Fraction] = defaultdict(Fraction)
        for left_exp, left_coefficient in self.terms:
            for right_exp, right_coefficient in right.terms:
                values[tuple(a + b for a, b in zip(left_exp, right_exp))] += (
                    left_coefficient * right_coefficient
                )
        return Polynomial.from_dict(self.width, values)

    __rmul__ = __mul__

    def __pow__(self, exponent: int) -> "Polynomial":
        if not isinstance(exponent, int) or exponent < 0:
            raise ValueError("polynomial powers must be nonnegative integers")
        result = Polynomial.constant(self.width, 1)
        base = self
        remaining = exponent
        while remaining:
            if remaining & 1:
                result *= base
            remaining >>= 1
            if remaining:
                base *= base
        return result

    def divide_constant(self, denominator: int | Fraction) -> "Polynomial":
        denominator = Fraction(denominator)
        if not denominator:
            raise ZeroDivisionError
        return Polynomial.from_dict(
            self.width,
            {
                monomial: coefficient / denominator
                for monomial, coefficient in self.terms
            },
        )

    def variables(self) -> set[int]:
        return {
            index
            for monomial, _ in self.terms
            for index, exponent in enumerate(monomial)
            if exponent
        }

    def constant_value(self) -> Fraction:
        if self.variables():
            raise ValueError("polynomial is not constant")
        return self.dictionary().get((0,) * self.width, Fraction())


class ExpressionParser:
    """Parse the deliberately small polynomial language in the JSON files."""

    def __init__(self, names: Sequence[str]):
        self.names = tuple(names)
        self.variables = {
            name: Polynomial.variable(len(self.names), index)
            for index, name in enumerate(self.names)
        }
        self.variable_denominators = 0

    def parse(self, expression: str) -> Polynomial:
        return self._convert(ast.parse(expression, mode="eval").body)

    def _convert(self, node: ast.AST) -> Polynomial:
        width = len(self.names)
        if isinstance(node, ast.Constant) and isinstance(node.value, int):
            return Polynomial.constant(width, node.value)
        if isinstance(node, ast.Name) and node.id in self.variables:
            return self.variables[node.id]
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -self._convert(node.operand)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.UAdd):
            return self._convert(node.operand)
        if isinstance(node, ast.BinOp):
            left = self._convert(node.left)
            if isinstance(node.op, ast.Add):
                return left + self._convert(node.right)
            if isinstance(node.op, ast.Sub):
                return left - self._convert(node.right)
            if isinstance(node.op, ast.Mult):
                return left * self._convert(node.right)
            if isinstance(node.op, ast.Pow):
                if not (
                    isinstance(node.right, ast.Constant)
                    and isinstance(node.right.value, int)
                ):
                    raise ValueError("noninteger exponent")
                return left ** node.right.value
            if isinstance(node.op, ast.Div):
                denominator = self._convert(node.right)
                if denominator.variables():
                    self.variable_denominators += 1
                    raise ValueError("nonconstant denominator")
                return left.divide_constant(denominator.constant_value())
        raise ValueError(f"unsupported expression: {ast.dump(node)}")


def bernstein_decomposition(
    polynomial: Polynomial, variable_indices: Iterable[int]
) -> tuple[tuple[int, ...], dict[tuple[int, ...], Polynomial]]:
    """Return exact tensor-product Bernstein coefficients on [0,1]^k."""

    indices = tuple(variable_indices)
    if len(indices) != len(set(indices)):
        raise ValueError("duplicate Bernstein variable")
    degrees = tuple(
        max((monomial[index] for monomial, _ in polynomial.terms), default=0)
        for index in indices
    )
    result: dict[tuple[int, ...], Polynomial] = {}
    for beta in itertools.product(*(range(degree + 1) for degree in degrees)):
        values: dict[Exponent, Fraction] = defaultdict(Fraction)
        for monomial, coefficient in polynomial.terms:
            alpha = tuple(monomial[index] for index in indices)
            if any(a > b for a, b in zip(alpha, beta)):
                continue
            multiplier = Fraction(1)
            for a, b, degree in zip(alpha, beta, degrees):
                multiplier *= Fraction(math.comb(b, a), math.comb(degree, a))
            residual = list(monomial)
            for index in indices:
                residual[index] = 0
            values[tuple(residual)] += coefficient * multiplier
        result[tuple(beta)] = Polynomial.from_dict(polynomial.width, values)
    return degrees, result


def strict_bernstein_sign(
    polynomial: Polynomial, variable_indices: Iterable[int] | None = None
) -> tuple[int | None, dict[str, object]]:
    indices = tuple(
        sorted(polynomial.variables())
        if variable_indices is None
        else variable_indices
    )
    if set(indices) != polynomial.variables():
        raise ValueError("symbolic variables remain outside Bernstein conversion")
    degrees, coefficients = bernstein_decomposition(polynomial, indices)
    values = [coefficient.constant_value() for coefficient in coefficients.values()]
    positive = all(value >= 0 for value in values) and any(value > 0 for value in values)
    negative = all(value <= 0 for value in values) and any(value < 0 for value in values)
    sign = 1 if positive else -1 if negative else 0 if not any(values) else None
    return sign, {
        "degrees": list(degrees),
        "coefficient_count": len(values),
        "minimum": str(min(values, default=Fraction())),
        "maximum": str(max(values, default=Fraction())),
    }


def polynomial_sha256(polynomial: Polynomial) -> str:
    payload = repr(polynomial.terms).encode()
    return sha256(payload).hexdigest()


def text_sha256(text: str) -> str:
    return sha256(text.encode()).hexdigest()
