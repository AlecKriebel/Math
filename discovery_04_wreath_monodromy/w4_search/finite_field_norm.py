#!/usr/bin/env python3
"""Bounded-memory evaluator for the fourth-level deepest branch norm.

For each requested ``s`` in F_p, build the cubic inverse tower

    F_p -> F_p[t]/(C0) -> ...[r]/(C1) -> ...[q]/(C2)

and return ``Norm(Delta(X3))``.  Quotients need not be fields: all inversions
are checked in their finite-dimensional F_p algebras.  A specialization at
which a required element is a zero divisor is reported as exceptional.

The script performs no symbolic expansion in s and stores no object larger
than a few 27 by 27 matrices.
"""

from __future__ import annotations

import argparse
import json
import math
import resource
import sys
from dataclasses import dataclass
from typing import Iterable, Sequence


Vector = tuple[int, ...]


class SingularElement(ZeroDivisionError):
    """Raised when a requested algebra element is a zero divisor."""


def _inverse_mod(value: int, modulus: int) -> int:
    """Invert a unit modulo a prime or prime square."""
    value %= modulus
    if math.gcd(value, modulus) != 1:
        raise SingularElement("division by a nonunit in the coefficient ring")
    return pow(value, -1, modulus)


def _solve_mod(matrix: list[list[int]], rhs: list[int], modulus: int) -> list[int]:
    """Solve a square unit-determinant system modulo p or p^2."""
    size = len(matrix)
    augmented = [
        [entry % modulus for entry in row] + [rhs[index] % modulus]
        for index, row in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next(
            (
                row
                for row in range(column, size)
                if math.gcd(augmented[row][column], modulus) == 1
            ),
            None,
        )
        if pivot is None:
            raise SingularElement("zero divisor in quotient algebra")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = _inverse_mod(augmented[column][column], modulus)
        augmented[column] = [value * scale % modulus for value in augmented[column]]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            if factor:
                augmented[row] = [
                    (left - factor * right) % modulus
                    for left, right in zip(augmented[row], augmented[column])
                ]
    return [augmented[row][-1] for row in range(size)]


def _det_mod(matrix: list[list[int]], modulus: int) -> int:
    """Determinant modulo a prime or prime square.

    For a prime square, unit row and column pivots are used.  If no unit
    remains, a block of size at least two has determinant divisible by p^2;
    a final one-by-one nonunit block is retained.  This is exactly the case
    needed to differentiate a rank-(n-1) norm matrix at a modular zero.
    """
    work = [[entry % modulus for entry in row] for row in matrix]
    size = len(work)
    determinant = 1
    for column in range(size):
        pivot = next(
            (
                (row, other_column)
                for row in range(column, size)
                for other_column in range(column, size)
                if math.gcd(work[row][other_column], modulus) == 1
            ),
            None,
        )
        if pivot is None:
            remaining = size - column
            if remaining >= 2:
                return 0
            return determinant * work[column][column] % modulus
        pivot_row, pivot_column = pivot
        if pivot_row != column:
            work[column], work[pivot_row] = work[pivot_row], work[column]
            determinant = -determinant
        if pivot_column != column:
            for row in range(size):
                work[row][column], work[row][pivot_column] = (
                    work[row][pivot_column],
                    work[row][column],
                )
            determinant = -determinant
        pivot_value = work[column][column]
        determinant = determinant * pivot_value % modulus
        scale = _inverse_mod(pivot_value, modulus)
        for row in range(column + 1, size):
            factor = work[row][column] * scale % modulus
            if factor:
                for index in range(column, size):
                    work[row][index] = (
                        work[row][index] - factor * work[column][index]
                    ) % modulus
    return determinant % modulus


@dataclass(frozen=True)
class CubicAlgebra:
    """A tower of monic cubic quotients over F_p.

    At positive level, ``relation=(c0,c1,c2)`` means that the newest generator
    ``u`` obeys ``u^3 + c2*u^2 + c1*u + c0 = 0`` over ``base``.
    Elements are flat vectors formed by concatenating the three base blocks.
    """

    prime: int
    base: "CubicAlgebra | None" = None
    relation: tuple[Vector, Vector, Vector] | None = None

    @property
    def dimension(self) -> int:
        return 1 if self.base is None else 3 * self.base.dimension

    def zero(self) -> Vector:
        return (0,) * self.dimension

    def one(self) -> Vector:
        return (1,) + (0,) * (self.dimension - 1)

    def constant(self, value: int) -> Vector:
        return ((value % self.prime),) + (0,) * (self.dimension - 1)

    def add(self, left: Vector, right: Vector) -> Vector:
        return tuple((a + b) % self.prime for a, b in zip(left, right))

    def neg(self, value: Vector) -> Vector:
        return tuple((-entry) % self.prime for entry in value)

    def sub(self, left: Vector, right: Vector) -> Vector:
        return tuple((a - b) % self.prime for a, b in zip(left, right))

    def scale(self, value: Vector, scalar: int) -> Vector:
        scalar %= self.prime
        return tuple(scalar * entry % self.prime for entry in value)

    def _blocks(self, value: Vector) -> tuple[Vector, Vector, Vector]:
        assert self.base is not None
        width = self.base.dimension
        return (
            value[:width],
            value[width : 2 * width],
            value[2 * width :],
        )

    def embed(self, value: Vector) -> Vector:
        """Embed an element of ``base`` in this algebra."""
        if self.base is None:
            if len(value) != 1:
                raise ValueError("prime-field embedding expects one coordinate")
            return (value[0] % self.prime,)
        if len(value) != self.base.dimension:
            raise ValueError("incorrect base-element dimension")
        return value + (0,) * (2 * self.base.dimension)

    def generator(self) -> Vector:
        if self.base is None:
            raise ValueError("the prime field has no quotient generator")
        width = self.base.dimension
        return (0,) * width + self.base.one() + (0,) * width

    def mul(self, left: Vector, right: Vector) -> Vector:
        if self.base is None:
            return (left[0] * right[0] % self.prime,)
        assert self.relation is not None
        left_blocks = self._blocks(left)
        right_blocks = self._blocks(right)
        coefficients = [self.base.zero() for _ in range(5)]
        for i in range(3):
            for j in range(3):
                coefficients[i + j] = self.base.add(
                    coefficients[i + j],
                    self.base.mul(left_blocks[i], right_blocks[j]),
                )
        c0, c1, c2 = self.relation
        for degree in (4, 3):
            high = coefficients[degree]
            if any(high):
                for offset, relation_coefficient in enumerate((c0, c1, c2)):
                    target = degree - 3 + offset
                    coefficients[target] = self.base.sub(
                        coefficients[target],
                        self.base.mul(high, relation_coefficient),
                    )
        return coefficients[0] + coefficients[1] + coefficients[2]

    def square(self, value: Vector) -> Vector:
        return self.mul(value, value)

    def power(self, value: Vector, exponent: int) -> Vector:
        result = self.one()
        base = value
        while exponent:
            if exponent & 1:
                result = self.mul(result, base)
            base = self.square(base)
            exponent //= 2
        return result

    def basis(self) -> Iterable[Vector]:
        for index in range(self.dimension):
            yield (0,) * index + (1,) + (0,) * (self.dimension - index - 1)

    def multiplication_matrix(self, value: Vector) -> list[list[int]]:
        columns = [self.mul(value, basis_element) for basis_element in self.basis()]
        return [
            [columns[column][row] for column in range(self.dimension)]
            for row in range(self.dimension)
        ]

    def inverse(self, value: Vector) -> Vector:
        return tuple(
            _solve_mod(
                self.multiplication_matrix(value), list(self.one()), self.prime
            )
        )

    def divide(self, numerator: Vector, denominator: Vector) -> Vector:
        return self.mul(numerator, self.inverse(denominator))

    def norm(self, value: Vector) -> int:
        return _det_mod(self.multiplication_matrix(value), self.prime)

    def extend(self, coefficients: Sequence[Vector]) -> "CubicAlgebra":
        """Adjoin a root of a cubic with coefficients constant-first."""
        if len(coefficients) != 4:
            raise ValueError("a cubic requires four coefficients")
        leading_inverse = self.inverse(coefficients[3])
        monic = tuple(self.mul(coefficient, leading_inverse) for coefficient in coefficients[:3])
        return CubicAlgebra(self.prime, self, monic)


def reconstruct(
    algebra: CubicAlgebra,
    a: Vector,
    b: Vector,
    c: Vector,
    root: Vector,
) -> tuple[Vector, Vector, Vector]:
    """Inverse-resolvent reconstruction, performed inside ``algebra``."""
    point, _guards = reconstruct_with_guards(algebra, a, b, c, root)
    return point


def reconstruct_with_guards(
    algebra: CubicAlgebra,
    a: Vector,
    b: Vector,
    c: Vector,
    root: Vector,
) -> tuple[tuple[Vector, Vector, Vector], tuple[Vector, Vector, Vector]]:
    """Reconstruct a point and return the three divided-by elements."""
    two = algebra.constant(2)
    root2 = algebra.square(root)
    numerator_y = algebra.add(
        algebra.add(algebra.mul(b, root2), algebra.scale(c, 3)),
        algebra.scale(root, -6),
    )
    denominator_y = algebra.scale(root2, 2)
    y = algebra.neg(algebra.divide(numerator_y, denominator_y))
    denominator_x = algebra.sub(algebra.one(), algebra.mul(root, y))
    x = algebra.divide(root, denominator_x)
    x2 = algebra.square(x)
    x3 = algebra.mul(x2, x)
    numerator_z = algebra.sub(
        algebra.sub(algebra.mul(two, x), algebra.scale(algebra.mul(x2, y), 3)),
        c,
    )
    denominator_z = x3
    z = algebra.divide(numerator_z, denominator_z)
    return (x, y, z), (denominator_y, denominator_x, denominator_z)


def discriminant(
    algebra: CubicAlgebra, point: tuple[Vector, Vector, Vector]
) -> Vector:
    """The reduced discriminant 27a^2c^2-18abc+16a+b^3c-b^2."""
    a, b, c = point
    a2 = algebra.square(a)
    b2 = algebra.square(b)
    c2 = algebra.square(c)
    terms = [
        algebra.scale(algebra.mul(a2, c2), 27),
        algebra.scale(algebra.mul(algebra.mul(a, b), c), -18),
        algebra.scale(a, 16),
        algebra.mul(algebra.mul(b2, b), c),
        algebra.neg(b2),
    ]
    result = algebra.zero()
    for term in terms:
        result = algebra.add(result, term)
    return result


def tower_profile(modulus: int, s_value: int) -> dict[str, tuple[int, ...] | int]:
    """Return discriminant norms plus every leading/reconstruction guard."""
    field = CubicAlgebra(modulus)
    s0 = field.constant(s_value)
    target_norm = discriminant(
        field, (field.constant(1), field.constant(2), s0)
    )[0]
    # C0(t) = 2t^3 - 2t^2 + 2t - s.
    level0 = field.extend(
        (field.neg(s0), field.constant(2), field.constant(-2), field.constant(2))
    )
    t = level0.generator()
    x1, guards1 = reconstruct_with_guards(
        level0,
        level0.constant(1),
        level0.constant(2),
        level0.constant(s_value),
        t,
    )
    level1_norm = level0.norm(discriminant(level0, x1))
    leading1 = level0.scale(x1[0], 2)

    # C1(r) = 2*x1[0]*r^3 - x1[1]*r^2 + 2r - x1[2].
    level1 = level0.extend(
        (
            level0.neg(x1[2]),
            level0.constant(2),
            level0.neg(x1[1]),
            leading1,
        )
    )
    r = level1.generator()
    x1_up = tuple(level1.embed(entry) for entry in x1)
    x2, guards2 = reconstruct_with_guards(level1, *x1_up, r)
    level2_norm = level1.norm(discriminant(level1, x2))
    leading2 = level1.scale(x2[0], 2)

    # C2(q) = 2*x2[0]*q^3 - x2[1]*q^2 + 2q - x2[2].
    level2 = level1.extend(
        (
            level1.neg(x2[2]),
            level1.constant(2),
            level1.neg(x2[1]),
            leading2,
        )
    )
    q = level2.generator()
    x2_up = tuple(level2.embed(entry) for entry in x2)
    x3, guards3 = reconstruct_with_guards(level2, *x2_up, q)
    level3_norm = level2.norm(discriminant(level2, x3))
    leading3 = level2.scale(x3[0], 2)
    guard_norms = (
        *(level0.norm(guard) for guard in guards1),
        *(level1.norm(guard) for guard in guards2),
        *(level2.norm(guard) for guard in guards3),
    )
    leading_norms = (
        2 % modulus,
        level0.norm(leading1),
        level1.norm(leading2),
        level2.norm(leading3),
    )
    return {
        "discriminant_norms": (
            target_norm,
            level1_norm,
            level2_norm,
            level3_norm,
        ),
        "leading_norms": leading_norms,
        "reconstruction_guard_norms": guard_norms,
    }


def tower_norms(modulus: int, s_value: int) -> tuple[int, int, int, int]:
    """Return discriminant norms at the target and three inverse levels."""
    value = tower_profile(modulus, s_value)["discriminant_norms"]
    assert isinstance(value, tuple)
    return value


def deepest_norm(prime: int, s_value: int) -> int:
    """Evaluate Norm(Delta(X3)) at one usable value of s in F_p."""
    return tower_norms(prime, s_value)[-1]


def deepest_norm_derivative(prime: int, s_value: int) -> int:
    """Differentiate the rational deepest norm modulo ``prime``.

    All reconstruction denominators must be units at ``s_value``.  Evaluating
    over Z/p^2 at ``s`` and ``s+p`` gives

        N(s+p) - N(s) = p*N'(s) (mod p^2).
    """
    modulus = prime * prime
    at_s = deepest_norm(modulus, s_value)
    at_s_plus_p = deepest_norm(modulus, s_value + prime)
    difference = (at_s_plus_p - at_s) % modulus
    if difference % prime:
        raise AssertionError("p-adic finite difference was not divisible by p")
    return difference // prime


def _is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def _set_memory_limit(memory_mib: int) -> None:
    if memory_mib <= 0 or not hasattr(resource, "RLIMIT_AS"):
        return
    limit = memory_mib * 1024 * 1024
    try:
        resource.setrlimit(resource.RLIMIT_AS, (limit, limit))
    except (OSError, ValueError):
        # RLIMIT_AS is not effective on every supported platform.  The data
        # structures are bounded regardless, so failure to install the guard
        # is informative but not fatal.
        print("warning: could not install RLIMIT_AS guard", file=sys.stderr)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prime", type=int, default=1_000_003)
    parser.add_argument("--start", type=int, default=1)
    parser.add_argument("--count", type=int, default=1)
    parser.add_argument("--memory-mib", type=int, default=1024)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not _is_prime(args.prime):
        raise SystemExit("--prime must be prime")
    if args.count < 0:
        raise SystemExit("--count must be nonnegative")
    _set_memory_limit(args.memory_mib)
    for offset in range(args.count):
        s_value = (args.start + offset) % args.prime
        record: dict[str, int | str] = {"prime": args.prime, "s": s_value}
        try:
            record["norm"] = deepest_norm(args.prime, s_value)
            record["status"] = "ok"
        except SingularElement as error:
            record["status"] = "exceptional"
            record["reason"] = str(error)
        print(json.dumps(record, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
