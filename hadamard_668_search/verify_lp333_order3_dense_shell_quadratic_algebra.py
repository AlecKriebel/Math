#!/usr/bin/env python3
"""Verify the order-three dense-shell quadratic-pencil structure over F_3.

No profile phases are enumerated.  The verifier reconstructs the six
quadratic polar matrices from the physical F_37 geometry, proves that their
algebra is F_27 x F_27, verifies the universal ``sum = 2 I`` identity, and
audits the restriction of that universal form after the actual local and
aggregate affine equations for the 15- and 18-medium shells.
"""

from __future__ import annotations

from collections import Counter
from itertools import product
from typing import Iterable, Iterator, Sequence


P = 37
H = (1, 26, 10)
CLASS_COUNT = 12
QUARTETS = 6
FIELD = 3

Vector = tuple[int, ...]
Matrix = tuple[tuple[int, ...], ...]

EXPECTED_PROJECTIVE_RANKS = {6: 26, 12: 338}
EXPECTED_IDEMPOTENTS = {
    (0, 0, 0, 0, 0, 0),
    (2, 0, 2, 0, 2, 0),
    (0, 2, 0, 2, 0, 2),
    (2, 2, 2, 2, 2, 2),
}
EXPECTED_AFFINE_HISTOGRAMS = {
    15: {
        (4, 10, 10, 0): 240,
        (5, 9, 5, 4): 6_144,
        (5, 9, 7, 2): 46_080,
        (5, 9, 9, 0): 25_920,
        (6, 8, 6, 2): 276_480,
        (6, 8, 8, 0): 155_520,
    },
    18: {
        (5, 12, 11, 1): 1_080,
        (5, 12, 12, 0): 60,
        (6, 11, 6, 5): 4_096,
        (6, 11, 8, 3): 46_080,
        (6, 11, 10, 1): 53_280,
        (6, 11, 11, 0): 2_880,
    },
}
EXPECTED_SUPPORT_COUNTS = {15: 510_384, 18: 107_476}
EXPECTED_UNIVERSAL_LOWER_BOUNDS = {15: 2_025, 18: 54_675}


def mod3(value: int) -> int:
    return value % FIELD


def matrix_add(left: Matrix, right: Matrix) -> Matrix:
    return tuple(
        tuple(mod3(a + b) for a, b in zip(left_row, right_row))
        for left_row, right_row in zip(left, right)
    )


def matrix_scale(scalar: int, matrix: Matrix) -> Matrix:
    return tuple(
        tuple(mod3(scalar * value) for value in row)
        for row in matrix
    )


def matrix_multiply(left: Matrix, right: Matrix) -> Matrix:
    size = len(left)
    return tuple(
        tuple(
            sum(left[row][inner] * right[inner][column] for inner in range(size))
            % FIELD
            for column in range(size)
        )
        for row in range(size)
    )


def identity(size: int) -> Matrix:
    return tuple(
        tuple(1 if row == column else 0 for column in range(size))
        for row in range(size)
    )


def zero_matrix(size: int) -> Matrix:
    return ((0,) * size,) * size


def matrix_rank(matrix: Sequence[Sequence[int]]) -> int:
    if not matrix:
        return 0
    work = [list(map(mod3, row)) for row in matrix]
    rows = len(work)
    columns = len(work[0])
    rank = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, rows) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        if work[rank][column] == 2:
            work[rank] = [2 * value % FIELD for value in work[rank]]
        for row in range(rows):
            if row == rank or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                (left - factor * right) % FIELD
                for left, right in zip(work[row], work[rank])
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def e_multiply(
    left: tuple[int, int], right: tuple[int, int]
) -> tuple[int, int]:
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c - b * d


def e_conjugate(value: tuple[int, int]) -> tuple[int, int]:
    return value[0] - value[1], -value[1]


def e_scale(
    scalar: int, value: tuple[int, int]
) -> tuple[int, int]:
    return scalar * value[0], scalar * value[1]


def e_divide_exact(
    numerator: tuple[int, int], denominator: tuple[int, int]
) -> tuple[int, int]:
    """Exact division for the fixed small Eisenstein fixtures below."""

    # Solve numerator=denominator*(x+y*omega) by the rational inverse.
    a, b = denominator
    norm = a * a - a * b + b * b
    conjugate = e_conjugate(denominator)
    product_value = e_multiply(numerator, conjugate)
    if product_value[0] % norm or product_value[1] % norm:
        raise AssertionError("an expected Eisenstein division was not exact")
    return product_value[0] // norm, product_value[1] // norm


def mod_lambda(value: tuple[int, int]) -> int:
    """Reduce a+b*omega modulo lambda=1-omega."""

    return (value[0] + value[1]) % FIELD


def verify_actual_affine_rows() -> dict[str, object]:
    """Check the local and aggregate phase rows from exact coefficients.

    If a medium letter is ``sigma*lambda*omega^u``, its first phase
    correction is ``lambda^2*x`` with ``x=-sigma*u mod lambda``.  The four
    origin/medium contributions at an opposite quartet all have coefficient
    ``-x`` after division by lambda^2, whereas the channel aggregate has
    coefficient ``x``.  Thus row scaling gives exactly the incidence rows
    used in ``affine_restriction_invariants``.
    """

    omega = (0, 1)
    lambda_value = (1, -1)
    lambda_squared = e_multiply(lambda_value, lambda_value)
    if lambda_squared != (0, -3):
        raise AssertionError("lambda^2=-3*omega changed")
    if e_conjugate(lambda_squared) != e_multiply(
        omega, lambda_squared
    ):
        raise AssertionError("conjugate(lambda^2)=omega*lambda^2 changed")

    delta = lambda_squared
    origins = (-1, 2)
    responses = []
    for origin in origins:
        positive = e_scale(origin, delta)
        negative = e_scale(origin, e_conjugate(delta))
        responses.extend(
            (
                mod_lambda(e_divide_exact(positive, lambda_squared)),
                mod_lambda(e_divide_exact(negative, lambda_squared)),
            )
        )
    if tuple(responses) != (2, 2, 2, 2):
        raise AssertionError("the four local phase coefficients changed")
    aggregate_response = mod_lambda(
        e_divide_exact(delta, lambda_squared)
    )
    if aggregate_response != 1:
        raise AssertionError("the aggregate phase coefficient changed")
    return {
        "local_phase_row": tuple(responses),
        "aggregate_phase_coefficient": aggregate_response,
        "phase_variable": "x=-sigma*u modulo lambda",
    }


def cyclotomic_geometry() -> tuple[tuple[tuple[int, ...], ...], tuple[int, ...]]:
    classes = []
    class_of = [-1] * P
    power = 1
    for class_index in range(CLASS_COUNT):
        part = tuple(power * member % P for member in H)
        classes.append(part)
        for value in part:
            if class_of[value] != -1:
                raise AssertionError("cyclotomic classes overlap")
            class_of[value] = class_index
        power = power * 2 % P
    if set().union(*map(set, classes)) != set(range(1, P)):
        raise AssertionError("cyclotomic classes do not partition F_37^*")
    return tuple(classes), tuple(class_of)


CLASSES, CLASS_OF = cyclotomic_geometry()


def polar_matrices() -> tuple[Matrix, ...]:
    result = []
    for lag_class in range(QUARTETS):
        transition = [[0] * CLASS_COUNT for _ in range(CLASS_COUNT)]
        lag = CLASSES[lag_class][0]
        for source in range(1, P):
            target = (source + lag) % P
            if target:
                transition[CLASS_OF[source]][CLASS_OF[target]] += 1
        polar = tuple(
            tuple(
                (
                    transition[left][right]
                    + transition[right][left]
                )
                % FIELD
                for right in range(CLASS_COUNT)
            )
            for left in range(CLASS_COUNT)
        )
        if polar != tuple(zip(*polar)):
            raise AssertionError("a polar matrix is not symmetric")
        result.append(polar)
    if len(result) != QUARTETS:
        raise AssertionError("there must be six reversal-independent forms")
    return tuple(result)


POLAR = polar_matrices()


def combine(coefficients: Sequence[int]) -> Matrix:
    if len(coefficients) != QUARTETS:
        raise ValueError("a pencil coefficient has length six")
    result = zero_matrix(CLASS_COUNT)
    for coefficient, matrix in zip(coefficients, POLAR):
        result = matrix_add(result, matrix_scale(coefficient, matrix))
    return result


def projective_vectors() -> tuple[Vector, ...]:
    result = []
    for vector in product(range(FIELD), repeat=QUARTETS):
        if not any(vector):
            continue
        first = next(value for value in vector if value)
        if first == 1:
            result.append(vector)
    if len(result) != (FIELD**QUARTETS - 1) // (FIELD - 1):
        raise AssertionError("projective pencil count changed")
    return tuple(result)


PROJECTIVE = projective_vectors()


def flatten(matrix: Matrix) -> Vector:
    return tuple(value for row in matrix for value in row)


def coordinates_in_basis(matrix: Matrix) -> Vector:
    """Solve matrix=sum c_i POLAR_i, asserting that a solution exists."""

    equations = [
        [POLAR[column][row][entry] for column in range(QUARTETS)]
        + [matrix[row][entry]]
        for row in range(CLASS_COUNT)
        for entry in range(CLASS_COUNT)
    ]
    rank = 0
    pivots: list[int] = []
    for column in range(QUARTETS):
        pivot = next(
            (
                row
                for row in range(rank, len(equations))
                if equations[row][column] % FIELD
            ),
            None,
        )
        if pivot is None:
            continue
        equations[rank], equations[pivot] = equations[pivot], equations[rank]
        if equations[rank][column] % FIELD == 2:
            equations[rank] = [
                2 * value % FIELD for value in equations[rank]
            ]
        for row in range(len(equations)):
            if row == rank or not equations[row][column] % FIELD:
                continue
            factor = equations[row][column] % FIELD
            equations[row] = [
                (left - factor * right) % FIELD
                for left, right in zip(equations[row], equations[rank])
            ]
        pivots.append(column)
        rank += 1
    if rank != QUARTETS:
        raise AssertionError("the six polar matrices are dependent")
    if any(
        not any(row[:QUARTETS]) and row[QUARTETS] % FIELD
        for row in equations
    ):
        raise AssertionError("the polar span is not closed")
    result = [0] * QUARTETS
    for row, column in enumerate(pivots):
        result[column] = equations[row][QUARTETS] % FIELD
    if combine(result) != matrix:
        raise AssertionError("basis-coordinate recovery failed")
    return tuple(result)


def algebra_product(left: Vector, right: Vector) -> Vector:
    return coordinates_in_basis(
        matrix_multiply(combine(left), combine(right))
    )


def vector_add(left: Vector, right: Vector) -> Vector:
    return tuple((a + b) % FIELD for a, b in zip(left, right))


def vector_scale(scalar: int, vector: Vector) -> Vector:
    return tuple(scalar * value % FIELD for value in vector)


def span(basis: Sequence[Vector]) -> frozenset[Vector]:
    return frozenset(
        tuple(
            sum(coefficient * vector[index] for coefficient, vector in zip(coefficients, basis))
            % FIELD
            for index in range(QUARTETS)
        )
        for coefficients in product(range(FIELD), repeat=len(basis))
    )


def ideal_generated_by(idempotent: Vector) -> frozenset[Vector]:
    return frozenset(
        algebra_product(idempotent, vector)
        for vector in product(range(FIELD), repeat=QUARTETS)
    )


def verify_pencil_algebra() -> dict[str, object]:
    # Commutative closure and the exact identity coordinate.
    for left in POLAR:
        for right in POLAR:
            if matrix_multiply(left, right) != matrix_multiply(right, left):
                raise AssertionError("the polar algebra is not commutative")
            coordinates_in_basis(matrix_multiply(left, right))
    identity_coordinates = coordinates_in_basis(identity(CLASS_COUNT))
    if identity_coordinates != (2,) * QUARTETS:
        raise AssertionError("the identity coordinate changed")
    if combine((1,) * QUARTETS) != matrix_scale(2, identity(CLASS_COUNT)):
        raise AssertionError("sum of the six polar matrices is not 2I")

    rank_histogram = Counter(
        matrix_rank(combine(coefficients))
        for coefficients in PROJECTIVE
    )
    if dict(rank_histogram) != EXPECTED_PROJECTIVE_RANKS:
        raise AssertionError("the projective pencil-rank census changed")

    all_vectors = tuple(product(range(FIELD), repeat=QUARTETS))
    idempotents = {
        vector
        for vector in all_vectors
        if algebra_product(vector, vector) == vector
    }
    if idempotents != EXPECTED_IDEMPOTENTS:
        raise AssertionError("the idempotent census changed")
    e_plus = (2, 0, 2, 0, 2, 0)
    e_minus = (0, 2, 0, 2, 0, 2)
    if algebra_product(e_plus, e_minus) != (0,) * QUARTETS:
        raise AssertionError("the two primitive idempotents are not orthogonal")
    if vector_add(e_plus, e_minus) != identity_coordinates:
        raise AssertionError("the primitive idempotents do not sum to one")

    ideals = (ideal_generated_by(e_plus), ideal_generated_by(e_minus))
    for ideal, projector in zip(ideals, (e_plus, e_minus)):
        if len(ideal) != 27 or matrix_rank(tuple(ideal)) != 3:
            raise AssertionError("an idempotent ideal is not 3-dimensional")
        if projector not in ideal or (0,) * QUARTETS not in ideal:
            raise AssertionError("an idempotent ideal lost zero or its identity")
        for value in ideal:
            if value == (0,) * QUARTETS:
                continue
            if matrix_rank(combine(value)) != 6:
                raise AssertionError("a nonzero field component lost rank six")
    if ideals[0] & ideals[1] != {(0,) * QUARTETS}:
        raise AssertionError("the two field components intersect nontrivially")
    if {
        vector_add(left, right)
        for left in ideals[0]
        for right in ideals[1]
    } != set(all_vectors):
        raise AssertionError("the two field components do not span the algebra")

    # Each order-27 component has no zero divisors relative to its own
    # identity.  A finite commutative division algebra is the field F_27.
    for ideal, projector in zip(ideals, (e_plus, e_minus)):
        nonzero = ideal - {(0,) * QUARTETS}
        for left in nonzero:
            if not any(
                algebra_product(left, right) == projector
                for right in nonzero
            ):
                raise AssertionError("a component has a noninvertible element")

    return {
        "identity_coordinates": identity_coordinates,
        "projective_rank_histogram": dict(sorted(rank_histogram.items())),
        "idempotents": tuple(sorted(idempotents)),
        "component_dimensions": (3, 3),
        "component_orders": (27, 27),
        "algebra": "F_27 x F_27",
    }


LOCAL_MASKS = tuple(
    mask for mask in range(16) if mask.bit_count() != 1
)


def legal_supports(total_medium: int) -> Iterator[tuple[int, ...]]:
    chosen = [0] * QUARTETS

    def recurse(quartet: int, used: int) -> Iterator[tuple[int, ...]]:
        if quartet == QUARTETS:
            if used == total_medium:
                yield tuple(chosen)
            return
        remaining = QUARTETS - quartet - 1
        for mask in LOCAL_MASKS:
            count = mask.bit_count()
            next_used = used + count
            if next_used > total_medium:
                continue
            if next_used + 4 * remaining < total_medium:
                continue
            chosen[quartet] = mask
            yield from recurse(quartet + 1, next_used)

    yield from recurse(0, 0)


def affine_restriction_invariants(
    local_masks: Sequence[int],
    total_medium: int,
) -> tuple[int, int, int, int]:
    """Return (nonempty quartets, affine dim, q-rank, radical dim).

    The variables have already absorbed the signed medium skeleton:
    ``x_i=-sigma_i*u_i``.  Each nonempty quartet supplies the actual local
    phase equation ``sum x_i=constant``.  The two channel aggregate rows
    supply ``sum_A x_i`` and ``sum_B x_i``; their sum is the sum of the
    quartet rows, so one channel row suffices.
    """

    nonempty = tuple(
        index for index, mask in enumerate(local_masks) if mask
    )
    row_count = len(nonempty) + 1

    # Gram matrix of the independent constraint rows for the standard dot
    # product.  Local bit positions 0,1 belong to A and 2,3 to B.
    gram = [[0] * row_count for _ in range(row_count)]
    a_total = 0
    mixed = False
    for row, quartet in enumerate(nonempty):
        mask = local_masks[quartet]
        medium = mask.bit_count()
        a_count = (mask & 0b0011).bit_count()
        b_count = (mask & 0b1100).bit_count()
        mixed |= bool(a_count and b_count)
        a_total += a_count
        gram[row][row] = medium % FIELD
        gram[row][-1] = a_count % FIELD
        gram[-1][row] = a_count % FIELD
    gram[-1][-1] = a_total % FIELD
    if not mixed:
        raise AssertionError(
            "a dense support unexpectedly has no mixed-channel quartet"
        )

    constraint_rank = row_count
    affine_dimension = total_medium - constraint_rank
    gram_rank = matrix_rank(gram)
    radical_dimension = row_count - gram_rank
    restricted_rank = affine_dimension - radical_dimension
    if restricted_rank < 0:
        raise AssertionError("a restricted quadratic rank became negative")
    return (
        len(nonempty),
        affine_dimension,
        restricted_rank,
        radical_dimension,
    )


def quadratic_fiber_lower_bound(dimension: int, rank: int) -> int:
    """Uniform lower bound for q(x)=c on any affine coset over F_3."""

    main_term = FIELD ** (dimension - 1)
    if rank % 2:
        error = FIELD ** (dimension - (rank + 1) // 2)
    else:
        error = 2 * FIELD ** (dimension - rank // 2 - 1)
    return main_term - error


def verify_affine_restrictions() -> dict[int, dict[str, object]]:
    result: dict[int, dict[str, object]] = {}
    for total_medium in (15, 18):
        histogram = Counter(
            affine_restriction_invariants(mask, total_medium)
            for mask in legal_supports(total_medium)
        )
        if dict(histogram) != EXPECTED_AFFINE_HISTOGRAMS[total_medium]:
            raise AssertionError(
                f"the {total_medium}-medium affine histogram changed"
            )
        support_count = sum(histogram.values())
        if support_count != EXPECTED_SUPPORT_COUNTS[total_medium]:
            raise AssertionError("a dense-shell support count changed")
        lower_bound = min(
            quadratic_fiber_lower_bound(dimension, rank)
            for (_, dimension, rank, _), count in histogram.items()
            if count
        )
        if lower_bound != EXPECTED_UNIVERSAL_LOWER_BOUNDS[total_medium]:
            raise AssertionError("a universal quadratic fiber bound changed")
        if lower_bound <= 0:
            raise AssertionError("the universal quadratic form lost surjectivity")
        result[total_medium] = {
            "support_masks": support_count,
            "affine_rank_histogram": tuple(sorted(histogram.items())),
            "minimum_restricted_rank": min(
                key[2] for key in histogram
            ),
            "minimum_fiber_for_each_rhs": lower_bound,
        }
    return result


def main() -> None:
    affine_rows = verify_actual_affine_rows()
    algebra = verify_pencil_algebra()
    affine = verify_affine_restrictions()
    print(f"actual_affine_rows={affine_rows}")
    print(f"identity_coordinates={algebra['identity_coordinates']}")
    print(
        "projective_rank_histogram="
        f"{algebra['projective_rank_histogram']}"
    )
    print(f"idempotents={algebra['idempotents']}")
    print(f"pencil_algebra={algebra['algebra']}")
    for total_medium in (15, 18):
        data = affine[total_medium]
        print(f"medium_count={total_medium}")
        print(f"  support_masks={data['support_masks']}")
        print(
            "  affine_rank_histogram="
            f"{data['affine_rank_histogram']}"
        )
        print(
            "  minimum_restricted_rank="
            f"{data['minimum_restricted_rank']}"
        )
        print(
            "  minimum_fiber_for_each_rhs="
            f"{data['minimum_fiber_for_each_rhs']}"
        )


if __name__ == "__main__":
    main()
