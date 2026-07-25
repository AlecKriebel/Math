#!/usr/bin/python3
"""Independent matrix-regular-representation audit of the W5 certificate.

No code is imported from the candidate W5 evaluator or from the W4
arithmetic.  Every tower element is represented directly by its regular
multiplication matrix.  A cubic extension is formed by a 3-by-3 block
companion matrix, so this implementation is structurally different from
coefficient-vector quotient reduction.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
import os
from typing import Iterable


MUTATION = os.environ.get("AUDIT_MUTATION", "strict")
PRIME = 23
PARAMETER = 3
MODULUS2 = PRIME * PRIME


def fail(message: str) -> None:
    print(f"FAIL [{MUTATION}]: {message}")
    raise SystemExit(1)


def check(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


Matrix = list[list[int]]


def identity(size: int) -> Matrix:
    return [[1 if row == column else 0 for column in range(size)] for row in range(size)]


def zero_matrix(size: int) -> Matrix:
    return [[0] * size for _ in range(size)]


def matrix_add(left: Matrix, right: Matrix, modulus: int) -> Matrix:
    return [
        [(a + b) % modulus for a, b in zip(left_row, right_row)]
        for left_row, right_row in zip(left, right)
    ]


def matrix_neg(matrix: Matrix, modulus: int) -> Matrix:
    return [[(-entry) % modulus for entry in row] for row in matrix]


def matrix_sub(left: Matrix, right: Matrix, modulus: int) -> Matrix:
    return matrix_add(left, matrix_neg(right, modulus), modulus)


def matrix_scale(matrix: Matrix, scalar: int, modulus: int) -> Matrix:
    scalar %= modulus
    return [[scalar * entry % modulus for entry in row] for row in matrix]


def matrix_mul(left: Matrix, right: Matrix, modulus: int) -> Matrix:
    size = len(left)
    output = [[0] * size for _ in range(size)]
    for row in range(size):
        output_row = output[row]
        for middle, left_entry in enumerate(left[row]):
            if not left_entry:
                continue
            right_row = right[middle]
            for column, right_entry in enumerate(right_row):
                if right_entry:
                    output_row[column] += left_entry * right_entry
        output[row] = [entry % modulus for entry in output_row]
    return output


def matrix_power(matrix: Matrix, exponent: int, modulus: int) -> Matrix:
    result = identity(len(matrix))
    base = matrix
    remaining = exponent
    while remaining:
        if remaining & 1:
            result = matrix_mul(result, base, modulus)
        base = matrix_mul(base, base, modulus)
        remaining //= 2
    return result


def matrix_inverse(matrix: Matrix, modulus: int) -> Matrix:
    size = len(matrix)
    augmented = [
        [entry % modulus for entry in row] + identity_row
        for row, identity_row in zip(matrix, identity(size))
    ]
    for column in range(size):
        pivot = next(
            (
                row
                for row in range(column, size)
                if gcd(augmented[row][column], modulus) == 1
            ),
            None,
        )
        if pivot is None:
            raise ZeroDivisionError("nonunit regular-representation matrix")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        inverse_pivot = pow(augmented[column][column], -1, modulus)
        augmented[column] = [
            entry * inverse_pivot % modulus for entry in augmented[column]
        ]
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            if factor:
                augmented[row] = [
                    (entry - factor * pivot_entry) % modulus
                    for entry, pivot_entry in zip(augmented[row], augmented[column])
                ]
    return [row[size:] for row in augmented]


def matrix_det(matrix: Matrix, modulus: int) -> int:
    """Determinant over F_23 or Z/23^2, retaining a final p-pivot."""
    work = [[entry % modulus for entry in row] for row in matrix]
    size = len(work)
    determinant = 1
    for step in range(size):
        pivot = next(
            (
                (row, column)
                for row in range(step, size)
                for column in range(step, size)
                if gcd(work[row][column], modulus) == 1
            ),
            None,
        )
        if pivot is None:
            remaining = size - step
            if remaining >= 2:
                return 0
            return determinant * work[step][step] % modulus
        pivot_row, pivot_column = pivot
        if pivot_row != step:
            work[step], work[pivot_row] = work[pivot_row], work[step]
            determinant = -determinant
        if pivot_column != step:
            for row in range(size):
                work[row][step], work[row][pivot_column] = (
                    work[row][pivot_column],
                    work[row][step],
                )
            determinant = -determinant
        pivot_value = work[step][step]
        determinant = determinant * pivot_value % modulus
        inverse_pivot = pow(pivot_value, -1, modulus)
        for row in range(step + 1, size):
            factor = work[row][step] * inverse_pivot % modulus
            if factor:
                work[row][step] = 0
                for column in range(step + 1, size):
                    work[row][column] = (
                        work[row][column] - factor * work[step][column]
                    ) % modulus
    return determinant % modulus


def block_diagonal_three(matrix: Matrix) -> Matrix:
    width = len(matrix)
    output = zero_matrix(3 * width)
    for block in range(3):
        for row in range(width):
            output[block * width + row][block * width : (block + 1) * width] = matrix[row][:]
    return output


def set_block(output: Matrix, block_row: int, block_column: int, block: Matrix) -> None:
    width = len(block)
    for row in range(width):
        output[block_row * width + row][
            block_column * width : (block_column + 1) * width
        ] = block[row][:]


def companion_extension(
    coefficients: tuple[Matrix, Matrix, Matrix, Matrix], modulus: int
) -> tuple[Matrix, tuple[Matrix, Matrix, Matrix]]:
    """Return the generator matrix and the three monic relation coefficients."""
    c0, c1, c2, leading = coefficients
    width = len(leading)
    leading_inverse = matrix_inverse(leading, modulus)
    monic = tuple(matrix_mul(coefficient, leading_inverse, modulus) for coefficient in (c0, c1, c2))
    output = zero_matrix(3 * width)
    set_block(output, 1, 0, identity(width))
    set_block(output, 2, 1, identity(width))
    set_block(output, 0, 2, matrix_neg(monic[0], modulus))
    set_block(output, 1, 2, matrix_neg(monic[1], modulus))
    set_block(output, 2, 2, matrix_neg(monic[2], modulus))
    return output, monic


def matrices_equal(left: Matrix, right: Matrix) -> bool:
    return left == right


def discriminant(point: tuple[Matrix, Matrix, Matrix], modulus: int) -> Matrix:
    a, b, c = point
    a2 = matrix_mul(a, a, modulus)
    b2 = matrix_mul(b, b, modulus)
    c2 = matrix_mul(c, c, modulus)
    result = matrix_scale(matrix_mul(a2, c2, modulus), 27, modulus)
    result = matrix_add(
        result,
        matrix_scale(matrix_mul(matrix_mul(a, b, modulus), c, modulus), -18, modulus),
        modulus,
    )
    result = matrix_add(result, matrix_scale(a, 16, modulus), modulus)
    result = matrix_add(
        result,
        matrix_mul(matrix_mul(b2, b, modulus), c, modulus),
        modulus,
    )
    last_sign = 1 if MUTATION == "discriminant_sign" else -1
    result = matrix_add(result, matrix_scale(b2, last_sign, modulus), modulus)
    return result


def reconstruct(
    point: tuple[Matrix, Matrix, Matrix],
    root: Matrix,
    modulus: int,
) -> tuple[tuple[Matrix, Matrix, Matrix], tuple[Matrix, Matrix, Matrix]]:
    a, b, c = point
    size = len(root)
    one = identity(size)
    root2 = matrix_mul(root, root, modulus)
    numerator_y = matrix_add(matrix_mul(b, root2, modulus), matrix_scale(c, 3, modulus), modulus)
    numerator_y = matrix_add(numerator_y, matrix_scale(root, -6, modulus), modulus)
    denominator_y = matrix_scale(root2, 2, modulus)
    y = matrix_mul(numerator_y, matrix_inverse(denominator_y, modulus), modulus)
    if MUTATION != "reconstruction_y_sign":
        y = matrix_neg(y, modulus)
    denominator_x = matrix_sub(one, matrix_mul(root, y, modulus), modulus)
    x = matrix_mul(root, matrix_inverse(denominator_x, modulus), modulus)
    x2 = matrix_mul(x, x, modulus)
    x3 = matrix_mul(x2, x, modulus)
    numerator_z = matrix_sub(matrix_scale(x, 2, modulus), matrix_scale(matrix_mul(x2, y, modulus), 3, modulus), modulus)
    numerator_z = matrix_sub(numerator_z, c, modulus)
    denominator_z = x3
    z = matrix_mul(numerator_z, matrix_inverse(denominator_z, modulus), modulus)
    return (x, y, z), (denominator_y, denominator_x, denominator_z)


def forward(point: tuple[Matrix, Matrix, Matrix], modulus: int) -> tuple[Matrix, Matrix, Matrix]:
    x, y, z = point
    one = identity(len(x))
    xy = matrix_mul(x, y, modulus)
    u = matrix_add(one, xy, modulus)
    u2 = matrix_mul(u, u, modulus)
    u3 = matrix_mul(u2, u, modulus)
    x2 = matrix_mul(x, x, modulus)
    x3 = matrix_mul(x2, x, modulus)
    y2 = matrix_mul(y, y, modulus)
    four_plus = matrix_add(matrix_scale(one, 4, modulus), matrix_scale(xy, 3, modulus), modulus)
    first = matrix_add(
        matrix_mul(u3, z, modulus),
        matrix_mul(matrix_mul(y2, u, modulus), four_plus, modulus),
        modulus,
    )
    second = matrix_add(y, matrix_scale(matrix_mul(matrix_mul(x, u2, modulus), z, modulus), 3, modulus), modulus)
    second = matrix_add(
        second,
        matrix_scale(matrix_mul(matrix_mul(x, y2, modulus), four_plus, modulus), 3, modulus),
        modulus,
    )
    third = matrix_sub(matrix_scale(x, 2, modulus), matrix_scale(matrix_mul(x2, y, modulus), 3, modulus), modulus)
    third = matrix_sub(third, matrix_mul(x3, z, modulus), modulus)
    return first, second, third


@dataclass
class Profile:
    discriminants: tuple[int, ...]
    leadings: tuple[int, ...]
    guards: tuple[int, ...]


def tower(modulus: int, s_value: int, diagnostics: bool) -> tuple[tuple[Matrix, Matrix, Matrix], Profile | None]:
    one = [[1]]
    point: tuple[Matrix, Matrix, Matrix] = ([[1]], [[2 % modulus]], [[s_value % modulus]])
    discriminants = [discriminant(point, modulus)[0][0]]
    leadings = [2 % modulus]
    guards: list[int] = []

    for level in range(4):
        a, b, c = point
        cubic_c2 = b if MUTATION == "cubic_sign" else matrix_neg(b, modulus)
        root, monic = companion_extension(
            (matrix_neg(c, modulus), matrix_scale(identity(len(a)), 2, modulus), cubic_c2, matrix_scale(a, 2, modulus)),
            modulus,
        )
        embedded_old = tuple(block_diagonal_three(entry) for entry in point)
        embedded_monic = tuple(block_diagonal_three(entry) for entry in monic)
        relation = matrix_power(root, 3, modulus)
        relation = matrix_add(relation, matrix_mul(embedded_monic[2], matrix_power(root, 2, modulus), modulus), modulus)
        relation = matrix_add(relation, matrix_mul(embedded_monic[1], root, modulus), modulus)
        relation = matrix_add(relation, embedded_monic[0], modulus)
        check(relation == zero_matrix(len(root)), f"level {level + 1} companion relation")

        point, divided_by = reconstruct(embedded_old, root, modulus)
        check(forward(point, modulus) == embedded_old, f"level {level + 1} inverse reconstruction")
        # The resolvent parameter is t=x/(1+xy).
        x, y, _z = point
        recovered_root = matrix_mul(
            x,
            matrix_inverse(matrix_add(identity(len(x)), matrix_mul(x, y, modulus), modulus), modulus),
            modulus,
        )
        check(recovered_root == root, f"level {level + 1} resolvent parameter recovery")

        if diagnostics:
            guards.extend(matrix_det(guard, modulus) for guard in divided_by)
            discriminants.append(matrix_det(discriminant(point, modulus), modulus))
            leadings.append(matrix_det(matrix_scale(point[0], 2, modulus), modulus))

    profile = (
        Profile(tuple(discriminants), tuple(leadings), tuple(guards))
        if diagnostics
        else None
    )
    return point, profile


def deepest_norm(modulus: int, s_value: int) -> int:
    point, _profile = tower(modulus, s_value, diagnostics=False)
    return matrix_det(discriminant(point, modulus), modulus)


# ---------------------------------------------------------------------------
# Scalar rational-sheet and dual-number replay.
# ---------------------------------------------------------------------------


def scalar_discriminant(point: tuple[int, int, int], modulus: int) -> int:
    a, b, c = point
    return (27 * a * a * c * c - 18 * a * b * c + 16 * a + b**3 * c - b * b) % modulus


def scalar_roots(point: tuple[int, int, int], modulus: int) -> list[int]:
    a, b, c = point
    return [
        root
        for root in range(modulus)
        if (2 * a * root**3 - b * root**2 + 2 * root - c) % modulus == 0
    ]


def scalar_reconstruct(point: tuple[int, int, int], root: int, modulus: int) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    a, b, c = point
    root2 = root * root % modulus
    denominator_y = 2 * root2 % modulus
    y = -(b * root2 + 3 * c - 6 * root) * pow(denominator_y, -1, modulus) % modulus
    denominator_x = (1 - root * y) % modulus
    x = root * pow(denominator_x, -1, modulus) % modulus
    denominator_z = x**3 % modulus
    z = (2 * x - 3 * x * x * y - c) * pow(denominator_z, -1, modulus) % modulus
    return (x, y, z), (denominator_y, denominator_x, denominator_z)


def rational_zero_paths() -> list[tuple[tuple[int, ...], tuple[int, int, int]]]:
    frontier = [((1, 2, PARAMETER), ())]
    for _level in range(4):
        next_frontier = []
        for point, path in frontier:
            for root in scalar_roots(point, PRIME):
                reconstructed, guards = scalar_reconstruct(point, root, PRIME)
                if all(guards):
                    next_frontier.append((reconstructed, path + (root,)))
        frontier = next_frontier
    return [(path, point) for point, path in frontier if scalar_discriminant(point, PRIME) == 0]


@dataclass(frozen=True)
class Dual:
    value: int
    tangent: int = 0

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", self.value % PRIME)
        object.__setattr__(self, "tangent", self.tangent % PRIME)

    def __add__(self, other: "Dual | int") -> "Dual":
        other = other if isinstance(other, Dual) else Dual(other)
        return Dual((self.value + other.value) % PRIME, (self.tangent + other.tangent) % PRIME)

    __radd__ = __add__

    def __neg__(self) -> "Dual":
        return Dual(-self.value % PRIME, -self.tangent % PRIME)

    def __sub__(self, other: "Dual | int") -> "Dual":
        return self + (-other if isinstance(other, Dual) else -other)

    def __rsub__(self, other: "Dual | int") -> "Dual":
        return (other if isinstance(other, Dual) else Dual(other)) - self

    def __mul__(self, other: "Dual | int") -> "Dual":
        other = other if isinstance(other, Dual) else Dual(other)
        return Dual(
            self.value * other.value % PRIME,
            (self.tangent * other.value + self.value * other.tangent) % PRIME,
        )

    __rmul__ = __mul__

    def inverse(self) -> "Dual":
        inverse_value = pow(self.value, -1, PRIME)
        return Dual(inverse_value, -self.tangent * inverse_value * inverse_value % PRIME)

    def __truediv__(self, other: "Dual | int") -> "Dual":
        other = other if isinstance(other, Dual) else Dual(other)
        return self * other.inverse()

    def __pow__(self, exponent: int) -> "Dual":
        result = Dual(1)
        base = self
        remaining = exponent
        while remaining:
            if remaining & 1:
                result = result * base
            base = base * base
            remaining //= 2
        return result


def dual_step(point: tuple[Dual, Dual, Dual], root_value: int) -> tuple[tuple[Dual, Dual, Dual], Dual]:
    a, b, c = point
    derivative_root = (6 * a.value * root_value**2 - 2 * b.value * root_value + 2) % PRIME
    partial_parameter = (
        2 * a.tangent * root_value**3
        - b.tangent * root_value**2
        - c.tangent
    ) % PRIME
    root = Dual(root_value, -partial_parameter * pow(derivative_root, -1, PRIME))
    y = -(b * root**2 + 3 * c - 6 * root) / (2 * root**2)
    x = root / (1 - root * y)
    z = (2 * x - 3 * x**2 * y - c) / x**3
    return (x, y, z), root


def dual_discriminant(point: tuple[Dual, Dual, Dual]) -> Dual:
    a, b, c = point
    return 27 * a**2 * c**2 - 18 * a * b * c + 16 * a + b**3 * c - b**2


# ---------------------------------------------------------------------------
# Group-kernel and norm-valuation audits.
# ---------------------------------------------------------------------------


def compose(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(left[right[index]] for index in range(len(left)))


def inverse_permutation(permutation: tuple[int, ...]) -> tuple[int, ...]:
    result = [0] * len(permutation)
    for index, image in enumerate(permutation):
        result[image] = index
    return tuple(result)


def permutation_power(permutation: tuple[int, ...], exponent: int) -> tuple[int, ...]:
    result = tuple(range(len(permutation)))
    base = permutation
    remaining = exponent
    while remaining:
        if remaining & 1:
            result = compose(result, base)
        base = compose(base, base)
        remaining //= 2
    return result


def conjugate(element: tuple[int, ...], by: tuple[int, ...]) -> tuple[int, ...]:
    return compose(compose(by, element), inverse_permutation(by))


def generated_group(generators: tuple[tuple[int, ...], ...]) -> set[tuple[int, ...]]:
    identity_permutation = tuple(range(len(generators[0])))
    group = {identity_permutation}
    frontier = [identity_permutation]
    while frontier:
        element = frontier.pop()
        for generator in generators:
            product = compose(element, generator)
            if product not in group:
                group.add(product)
                frontier.append(product)
    return group


def support(permutation: tuple[int, ...]) -> set[int]:
    return {index for index, image in enumerate(permutation) if index != image}


def check_group_kernel() -> None:
    alpha = tuple((index + 1) % 243 for index in range(243))
    tau_list = list(range(243))
    tau_list[0], tau_list[81] = tau_list[81], tau_list[0]
    tau = tuple(tau_list)
    stride = 80 if MUTATION == "group_stride" else 81
    within = permutation_power(alpha, stride)
    local = generated_group((tau, conjugate(tau, within)))
    check(len(local) == 6, "a transposition and alpha^81 conjugate generate local S3")
    local_support = set().union(*(support(element) for element in local))
    check(local_support == {0, 81, 162}, "local S3 has one bottom-block support")

    supports = []
    for shift in range(81):
        moved = permutation_power(alpha, shift)
        shifted_support = {
            moved[index] for index in local_support
        }
        supports.append(shifted_support)
        check(shifted_support == {shift, shift + 81, shift + 162}, "cycle conjugate support")
    check(len(set().union(*supports)) == 243, "81 local factors cover all leaves")
    check(sum(len(block) for block in supports) == 243, "81 local factors have disjoint supports")


def check_norm_valuation() -> None:
    # Sum f_i*v_i=1 with positive residue degrees and positive valuations at
    # vanishing primes has exactly one summand, f=v=1.
    decompositions = []
    for number_of_primes in range(1, 4):
        for residues in _positive_tuples(number_of_primes, 3):
            for valuations in _positive_tuples(number_of_primes, 3):
                if sum(f * v for f, v in zip(residues, valuations)) == 1:
                    decompositions.append((residues, valuations))
    expected = [((1,), (1,))]
    if MUTATION == "valuation_split":
        expected.append(((1, 1), (1, 1)))
    check(decompositions == expected, "norm valuation one selects one rational transverse sheet")


def _positive_tuples(length: int, upper: int) -> Iterable[tuple[int, ...]]:
    if length == 0:
        yield ()
        return
    for first in range(1, upper + 1):
        for rest in _positive_tuples(length - 1, upper):
            yield (first,) + rest


def main() -> None:
    point, profile = tower(PRIME, PARAMETER, diagnostics=True)
    assert profile is not None
    expected_discriminants = (10, 22, 10, 4, 0)
    expected_leadings = (2, 14, 19, 11, 1)
    expected_guards = (18, 14, 5, 2, 8, 21, 13, 13, 7, 8, 17, 12)
    if MUTATION == "profile_discriminant":
        expected_discriminants = expected_discriminants[:-1] + (1,)
    if MUTATION == "profile_leading":
        expected_leadings = expected_leadings[:-1] + (2,)
    if MUTATION == "profile_guard":
        expected_guards = expected_guards[:-1] + (0,)
    check(profile.discriminants == expected_discriminants, "five discriminant norms")
    check(profile.leadings == expected_leadings, "five cubic-leading norms")
    check(profile.guards == expected_guards, "twelve reconstruction-guard norms")

    lifted_parameters = (3, 26, 49)
    # The strict run and the two p-adic fault modes execute all three heavy
    # 81-dimensional p^2 towers.  Later sheet/group fault modes reuse the
    # strict constants so the wrapper does not repeat an unrelated 6-second
    # certificate for every lightweight mutation.
    if MUTATION in ("strict", "p2_value", "norm_derivative"):
        lifted_norms = tuple(
            deepest_norm(MODULUS2, parameter) for parameter in lifted_parameters
        )
    else:
        lifted_norms = (460, 299, 138)
    expected_lifted = (460, 299, 138)
    if MUTATION == "p2_value":
        expected_lifted = (460, 300, 138)
    check(lifted_norms == expected_lifted, "three Z/23^2 deepest norms")
    derivative = ((lifted_norms[1] - lifted_norms[0]) % MODULUS2) // PRIME
    second_difference = ((lifted_norms[2] - lifted_norms[0]) % MODULUS2) // PRIME
    expected_derivative = 17 if MUTATION == "norm_derivative" else 16
    check(derivative == expected_derivative, "p-adic deepest-norm derivative")
    check(second_difference % PRIME == 2 * 16 % PRIME, "second p-adic lift obeys the linear law")

    zero_paths = rational_zero_paths()
    expected_path = ((10, 22, 13, 1), (22, 2, 21))
    if MUTATION == "sheet_path":
        expected_path = ((10, 22, 13, 2), (22, 2, 21))
    check(zero_paths == [expected_path], "unique rational deepest vanishing sheet")
    final_point = zero_paths[0][1]
    roots = scalar_roots(final_point, PRIME)
    check(roots == [1, 22], "final cubic has two distinct residue roots")
    a, b, _c = final_point
    derivative_values = {
        root: (6 * a * root * root - 2 * b * root + 2) % PRIME
        for root in roots
    }
    check(derivative_values == {1: 15, 22: 0}, "final cubic has one simple and one double root")

    dual_point = (Dual(1), Dual(2), Dual(3, 1))
    dual_roots = []
    for root_value in (10, 22, 13, 1):
        dual_point, dual_root = dual_step(dual_point, root_value)
        dual_roots.append(dual_root)
    deepest_dual_discriminant = dual_discriminant(dual_point)
    expected_sheet_derivative = 19 if MUTATION == "sheet_derivative" else 18
    check(deepest_dual_discriminant == Dual(0, expected_sheet_derivative),
          "direct rational-sheet discriminant derivative")
    check(tuple(root.tangent for root in dual_roots) == (7, 22, 4, 19),
          "implicit derivatives along the rational root path")

    check_norm_valuation()
    check_group_kernel()

    check(all(profile.discriminants[index] for index in range(4)),
          "all lower discriminants are units")
    check(all(profile.leadings), "all leading coefficients are units")
    check(all(profile.guards), "all reconstruction denominators are units")
    check(PRIME not in (2, 3), "the transposition is tame")

    print("PASS independent 1/3/9/27/81 matrix quotient tower")
    print("PASS profiles Delta=(10,22,10,4,0), leading=(2,14,19,11,1)")
    print("PASS all twelve reconstruction guards")
    print("PASS mod-23^2 norms (460,299,138), derivative 16")
    print("PASS rational sheet path (10,22,13,1), sheet derivative 18")
    print("PASS norm-valuation uniqueness and S3^81 kernel lemma")
    print("ALL W5 HOSTILE MATRIX-TOWER CHECKS PASSED")


if __name__ == "__main__":
    main()
