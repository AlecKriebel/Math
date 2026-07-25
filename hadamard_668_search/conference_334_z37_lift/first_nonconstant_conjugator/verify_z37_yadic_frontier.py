#!/usr/bin/env python3
"""Verify the y-adic formal frontier of the C37 conference lift.

This is a dependency-free verifier.  It proves exact statements
about any 9-by-9 C37-circulant adjacency lift D(x) of the explicit quotient
B.  Work modulo 37 and put x=1+y.  Then

    N(y) = D(1+y) - 18 I

must satisfy

    N(y)^2 = 9 y^36 J        in F_37[y]/(y^37).

The first coefficient gives 16 independent linear constraints on the 36
off-diagonal first moments.  The verifier proves, coefficientwise and
symbolically, that the y^2 and y^3 equations introduce no further formal
obstruction.  It then verifies the algebraic prerequisites for an explicit
exponential-conjugation extension through the terminal y^36 equation.
Thus all later formal matrix equations are soluble; only simultaneous
realizability by actual binary block polynomials can still obstruct a lift.
"""

from __future__ import annotations

from itertools import combinations
from math import comb, log2


P = 37
N = 9

T = [
    [0, -11, -3, 7, -3, 7, -3, 7, -1],
    [-11, -4, 7, -1, 7, -1, 7, -1, -3],
    [-3, 7, 0, -11, -3, 7, -3, 7, -1],
    [7, -1, -11, -4, 7, -1, 7, -1, -3],
    [-3, 7, -3, 7, 0, -11, -3, 7, -1],
    [7, -1, 7, -1, -11, -4, 7, -1, -3],
    [-3, 7, -3, 7, -3, 7, 0, -11, -1],
    [7, -1, 7, -1, 7, -1, -11, -4, -3],
    [-1, -3, -1, -3, -1, -3, -1, -3, 16],
]

B = [
    [
        (P - (1 if i == j else 0) - T[i][j]) // 2
        for j in range(N)
    ]
    for i in range(N)
]


def zero_matrix() -> list[list[int]]:
    return [[0] * N for _ in range(N)]


def add(
    left: list[list[int]], right: list[list[int]]
) -> list[list[int]]:
    return [
        [(left[i][j] + right[i][j]) % P for j in range(N)]
        for i in range(N)
    ]


def scale(value: int, matrix: list[list[int]]) -> list[list[int]]:
    return [[value * entry % P for entry in row] for row in matrix]


def multiply(
    left: list[list[int]], right: list[list[int]]
) -> list[list[int]]:
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(N)) % P
            for j in range(N)
        ]
        for i in range(N)
    ]


def transpose(matrix: list[list[int]]) -> list[list[int]]:
    return [list(row) for row in zip(*matrix)]


def flatten_symmetric(matrix: list[list[int]]) -> list[int]:
    return [matrix[i][j] % P for i in range(N) for j in range(i, N)]


def flatten_skew(matrix: list[list[int]]) -> list[int]:
    return [matrix[i][j] % P for i in range(N) for j in range(i + 1, N)]


def symmetric_basis() -> list[list[list[int]]]:
    result = []
    for i in range(N):
        for j in range(i, N):
            matrix = zero_matrix()
            matrix[i][j] = 1
            matrix[j][i] = 1
            result.append(matrix)
    return result


def skew_basis() -> list[list[list[int]]]:
    result = []
    for i in range(N):
        for j in range(i + 1, N):
            matrix = zero_matrix()
            matrix[i][j] = 1
            matrix[j][i] = -1 % P
            result.append(matrix)
    return result


def rref(
    rows: list[list[int]],
) -> tuple[list[list[int]], list[int]]:
    matrix = [[entry % P for entry in row] for row in rows]
    if not matrix:
        return matrix, []
    row_count = len(matrix)
    column_count = len(matrix[0])
    pivot_row = 0
    pivots: list[int] = []
    for column in range(column_count):
        selected = next(
            (
                row
                for row in range(pivot_row, row_count)
                if matrix[row][column]
            ),
            None,
        )
        if selected is None:
            continue
        matrix[pivot_row], matrix[selected] = (
            matrix[selected],
            matrix[pivot_row],
        )
        inverse = pow(matrix[pivot_row][column], -1, P)
        matrix[pivot_row] = [
            inverse * value % P for value in matrix[pivot_row]
        ]
        for row in range(row_count):
            if row == pivot_row or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (matrix[row][j] - factor * matrix[pivot_row][j]) % P
                for j in range(column_count)
            ]
        pivots.append(column)
        pivot_row += 1
    return matrix, pivots


def rank(rows: list[list[int]]) -> int:
    return len(rref(rows)[1])


def nullspace(rows: list[list[int]]) -> list[list[int]]:
    reduced, pivots = rref(rows)
    column_count = len(rows[0])
    free = [column for column in range(column_count) if column not in pivots]
    result = []
    for free_column in free:
        vector = [0] * column_count
        vector[free_column] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = -reduced[row][free_column] % P
        result.append(vector)
    return result


def linear_combination(
    coefficients: list[int], basis: list[list[list[int]]]
) -> list[list[int]]:
    result = zero_matrix()
    for coefficient, matrix in zip(coefficients, basis):
        if coefficient:
            result = add(result, scale(coefficient, matrix))
    return result


def linear_map_columns(
    source_basis: list[list[list[int]]],
    output_kind: str,
    n0: list[list[int]],
) -> list[list[int]]:
    columns = []
    for source in source_basis:
        image = add(multiply(n0, source), multiply(source, n0))
        columns.append(
            flatten_symmetric(image)
            if output_kind == "symmetric"
            else flatten_skew(image)
        )
    return [list(row) for row in zip(*columns)]


def solve_linear(
    matrix: list[list[int]], target: list[int]
) -> list[int] | None:
    augmented = [
        row[:] + [target[i] % P] for i, row in enumerate(matrix)
    ]
    reduced, pivots = rref(augmented)
    variable_count = len(matrix[0])
    for row in reduced:
        if all(value == 0 for value in row[:variable_count]) and row[-1]:
            return None
    solution = [0] * variable_count
    for row, pivot in enumerate(pivots):
        if pivot < variable_count:
            solution[pivot] = reduced[row][-1]
    return solution


def in_image(matrix: list[list[int]], target: list[int]) -> bool:
    return solve_linear(matrix, target) is not None


def matrix_from_flat(
    vector: list[int], kind: str
) -> list[list[int]]:
    basis = symmetric_basis() if kind == "symmetric" else skew_basis()
    return linear_combination(vector, basis)


def verify_quotient_and_first_layer() -> tuple[
    list[list[int]],
    list[list[list[int]]],
    list[list[list[int]]],
    list[list[int]],
    list[list[int]],
]:
    t_mod = [[entry % P for entry in row] for row in T]
    assert multiply(t_mod, t_mod) == zero_matrix()
    # A nonzero principal 4-by-4 minor has determinant 4077 = 7 mod 37.
    principal = (0, 1, 2, 4)
    minor = [[T[i][j] % P for j in principal] for i in principal]
    assert determinant(minor) == 7
    assert rank(t_mod) == 4

    inverse_two = pow(2, -1, P)
    n0 = scale(-inverse_two, t_mod)
    assert n0 == [
        [(B[i][j] - (18 if i == j else 0)) % P for j in range(N)]
        for i in range(N)
    ]
    assert multiply(n0, n0) == zero_matrix()

    symmetric = symmetric_basis()
    skew = skew_basis()
    l_symmetric = linear_map_columns(symmetric, "symmetric", n0)
    l_skew = linear_map_columns(skew, "skew", n0)
    assert rank(l_symmetric) == 24
    assert rank(l_skew) == 16

    skew_kernel_vectors = nullspace(l_skew)
    symmetric_kernel_vectors = nullspace(l_symmetric)
    assert len(skew_kernel_vectors) == 20
    assert len(symmetric_kernel_vectors) == 21
    skew_kernel = [
        matrix_from_flat(vector, "skew") for vector in skew_kernel_vectors
    ]
    symmetric_kernel = [
        matrix_from_flat(vector, "symmetric")
        for vector in symmetric_kernel_vectors
    ]
    for matrix in skew_kernel:
        assert add(multiply(n0, matrix), multiply(matrix, n0)) == zero_matrix()

    # The 21-dimensional symmetric kernel can change all nine diagonal
    # second moments independently.
    diagonal_projection = [
        [matrix[i][i] for matrix in symmetric_kernel] for i in range(N)
    ]
    assert rank(diagonal_projection) == 9
    return n0, skew_kernel, symmetric_kernel, l_symmetric, l_skew


def determinant(matrix: list[list[int]]) -> int:
    work = [[entry % P for entry in row] for row in matrix]
    result = 1
    for column in range(len(work)):
        selected = next(
            (
                row
                for row in range(column, len(work))
                if work[row][column]
            ),
            None,
        )
        if selected is None:
            return 0
        if selected != column:
            work[column], work[selected] = work[selected], work[column]
            result = -result
        pivot = work[column][column]
        result = result * pivot % P
        inverse = pow(pivot, -1, P)
        for row in range(column + 1, len(work)):
            factor = work[row][column] * inverse % P
            work[row] = [
                (work[row][j] - factor * work[column][j]) % P
                for j in range(len(work))
            ]
    return result % P


def verify_second_layer(
    skew_kernel: list[list[list[int]]],
    l_symmetric: list[list[int]],
) -> dict[tuple[int, int], list[list[int]]]:
    """Prove L(H)=-X^2 is soluble for every first moment X.

    The returned dictionary gives one symmetric preimage for every
    quadratic monomial in the 20 kernel coordinates.  Checking squares and
    polarized cross terms proves the assertion as a polynomial identity,
    not by sampling.
    """

    symmetric = symmetric_basis()
    preimages: dict[tuple[int, int], list[list[int]]] = {}
    for first in range(len(skew_kernel)):
        for second in range(first, len(skew_kernel)):
            if first == second:
                target_matrix = multiply(
                    skew_kernel[first], skew_kernel[first]
                )
            else:
                target_matrix = add(
                    multiply(skew_kernel[first], skew_kernel[second]),
                    multiply(skew_kernel[second], skew_kernel[first]),
                )
            target = [(-value) % P for value in flatten_symmetric(target_matrix)]
            solution = solve_linear(l_symmetric, target)
            assert solution is not None
            preimages[(first, second)] = linear_combination(
                solution, symmetric
            )
    assert len(preimages) == comb(20 + 1, 2)
    return preimages


def verify_third_layer(
    skew_kernel: list[list[list[int]]],
    symmetric_kernel: list[list[list[int]]],
    quadratic_preimages: dict[tuple[int, int], list[list[int]]],
    l_skew: list[list[int]],
) -> None:
    """Prove L(K)=-{X,H} is soluble for every second-layer solution.

    First check every bilinear term involving the free symmetric kernel.
    Then collect all cubic coefficients in {X,H_particular(X)} and check
    each coefficient lies in the image of L on skew matrices.
    """

    for x_basis in skew_kernel:
        for h_basis in symmetric_kernel:
            target = flatten_skew(
                add(multiply(x_basis, h_basis), multiply(h_basis, x_basis))
            )
            assert in_image(l_skew, target)

    cubic: dict[tuple[int, int, int], list[list[int]]] = {}
    for x_index, x_basis in enumerate(skew_kernel):
        for pair, h_basis in quadratic_preimages.items():
            monomial = tuple(sorted((x_index,) + pair))
            coefficient = add(
                multiply(x_basis, h_basis), multiply(h_basis, x_basis)
            )
            cubic[monomial] = add(
                cubic.get(monomial, zero_matrix()), coefficient
            )
    assert len(cubic) == comb(20 + 2, 3)
    for coefficient in cubic.values():
        assert in_image(l_skew, flatten_skew(coefficient))


def commutator(
    left: list[list[int]], right: list[list[int]]
) -> list[list[int]]:
    return add(multiply(left, right), scale(-1, multiply(right, left)))


def verify_fourth_layer_characterization(
    n0: list[list[int]],
    skew_kernel: list[list[list[int]]],
    quadratic_preimages: dict[tuple[int, int], list[list[int]]],
    l_symmetric: list[list[int]],
    l_skew: list[list[int]],
) -> None:
    """Characterize, but do not mistake, the fourth-layer cokernel.

    For arbitrary earlier free choices the fourth-layer class need not
    vanish.  Nevertheless it gives no condition on the first moment X:
    every X in ker(L|skew) is [N0,A] for a symmetric A.  With

        z = log(1+y),
        M(y) = exp(-z A) N0 exp(z A),

    one has M(y)^2=0 and M(iota(y))^T=M(y).  Since 1,...,36 are invertible
    modulo 37, this is a formal extension through degree 35.
    """

    symmetric = symmetric_basis()
    commutator_columns = [
        flatten_skew(commutator(n0, matrix)) for matrix in symmetric
    ]
    commutator_map = [list(row) for row in zip(*commutator_columns)]
    assert rank(commutator_map) == 20
    for matrix in skew_kernel:
        assert in_image(commutator_map, flatten_skew(matrix))

    # Free K lies in the same skew kernel as X.  Its contribution {X,K}
    # always dies in the symmetric cokernel.
    for first in range(len(skew_kernel)):
        for second in range(first, len(skew_kernel)):
            contribution = add(
                multiply(skew_kernel[first], skew_kernel[second]),
                multiply(skew_kernel[second], skew_kernel[first]),
            )
            assert in_image(l_symmetric, flatten_symmetric(contribution))

    # But the fourth-layer expression is not identically in the image for
    # arbitrary choices of the free symmetric second coefficient.  This
    # exact basis witness distinguishes an existential extension theorem
    # from an automatic coefficient identity.
    witness_index = 8
    x_matrix = skew_kernel[witness_index]
    h_matrix = quadratic_preimages[(witness_index, witness_index)]
    third_target = [
        -value % P
        for value in flatten_skew(
            add(
                multiply(x_matrix, h_matrix),
                multiply(h_matrix, x_matrix),
            )
        )
    ]
    k_solution = solve_linear(l_skew, third_target)
    assert k_solution is not None
    k_matrix = matrix_from_flat(k_solution, "skew")
    inverse_four = pow(4, -1, P)
    fourth_expression = add(
        add(
            multiply(h_matrix, h_matrix),
            add(
                multiply(x_matrix, k_matrix),
                multiply(k_matrix, x_matrix),
            ),
        ),
        scale(inverse_four, multiply(x_matrix, x_matrix)),
    )
    assert not in_image(
        l_symmetric, flatten_symmetric(fourth_expression)
    )


def verify_full_formal_extension(n0: list[list[int]]) -> None:
    """Verify the exact terminal correction in the full formal extension.

    In F_37[y]/(y^37), let z=log(1+y) and q=z^18.  Then q is fixed by the
    star involution z -> -z and q^2=y^36.  Since N0 annihilates J and
    J^2=9J, Q=N0+qJ has Q^2=9y^36J.

    For symmetric A, exp(-zA) Q exp(zA) has the required star symmetry.
    Conjugating the right side changes J only by O(z), which is killed by
    y^36 modulo y^37.  The commutator-rank check in the fourth-layer
    routine shows that A can realize every admissible first coefficient.
    """

    degree_bound = P

    def poly_add(left: list[int], right: list[int]) -> list[int]:
        return [
            (left[i] + right[i]) % P for i in range(degree_bound)
        ]

    def poly_multiply(left: list[int], right: list[int]) -> list[int]:
        result = [0] * degree_bound
        for i, first in enumerate(left):
            if not first:
                continue
            for j, second in enumerate(right[: degree_bound - i]):
                if second:
                    result[i + j] = (
                        result[i + j] + first * second
                    ) % P
        return result

    def poly_power(base: list[int], exponent: int) -> list[int]:
        result = [0] * degree_bound
        result[0] = 1
        factor = base
        remaining = exponent
        while remaining:
            if remaining & 1:
                result = poly_multiply(result, factor)
            factor = poly_multiply(factor, factor)
            remaining //= 2
        return result

    z = [0] * degree_bound
    for degree in range(1, degree_bound):
        z[degree] = (
            (1 if degree % 2 else -1) * pow(degree, -1, P)
        ) % P
    q = poly_power(z, 18)
    q_squared = poly_multiply(q, q)
    expected_terminal = [0] * degree_bound
    expected_terminal[36] = 1
    assert q_squared == expected_terminal

    # exp(z)=1+y and exp(-z)=(1+y)^-1 in the truncated ring.  This also
    # checks that every factorial needed by the matrix exponentials is a
    # unit modulo 37.
    exponential = [0] * degree_bound
    exponential[0] = 1
    negative_exponential = [0] * degree_bound
    negative_exponential[0] = 1
    z_power = [0] * degree_bound
    z_power[0] = 1
    factorial = 1
    for degree in range(1, degree_bound):
        z_power = poly_multiply(z_power, z)
        factorial = factorial * degree % P
        coefficient = pow(factorial, -1, P)
        exponential = poly_add(
            exponential, [coefficient * value % P for value in z_power]
        )
        negative_exponential = poly_add(
            negative_exponential,
            [
                (coefficient if degree % 2 == 0 else -coefficient)
                * value
                % P
                for value in z_power
            ],
        )
    one_plus_y = [0] * degree_bound
    one_plus_y[0] = one_plus_y[1] = 1
    inverse_one_plus_y = [
        (1 if degree % 2 == 0 else -1) % P
        for degree in range(degree_bound)
    ]
    assert exponential == one_plus_y
    assert negative_exponential == inverse_one_plus_y
    assert poly_multiply(exponential, negative_exponential) == (
        [1] + [0] * (degree_bound - 1)
    )

    all_ones = [[1] * N for _ in range(N)]
    assert multiply(n0, all_ones) == zero_matrix()
    assert multiply(all_ones, n0) == zero_matrix()
    assert multiply(all_ones, all_ones) == scale(N, all_ones)


def binomial_mod(value: int, degree: int) -> int:
    if degree == 1:
        return value % P
    if degree == 2:
        return value * (value - 1) // 2 % P
    if degree == 3:
        return value * (value - 1) * (value - 2) // 6 % P
    raise AssertionError("unsupported moment degree")


def attainable_moment_tuples(maximum_weight: int) -> list[set[int]]:
    """Return packed reachable (m1,m2,m3) tuples by subset weight."""

    states = [set() for _ in range(maximum_weight + 1)]
    states[0].add(0)
    for value in range(P):
        increments = [
            binomial_mod(value, degree) for degree in (1, 2, 3)
        ]
        for weight in range(min(maximum_weight, value + 1), 0, -1):
            destination = states[weight]
            for packed in states[weight - 1]:
                first = packed % P
                second = packed // P % P
                third = packed // (P * P)
                new_first = (first + increments[0]) % P
                new_second = (second + increments[1]) % P
                new_third = (third + increments[2]) % P
                destination.add(
                    new_first + P * (new_second + P * new_third)
                )
    return states


def verify_fixed_weight_reachability() -> list[int]:
    weights = sorted(
        {B[i][j] for i in range(N) for j in range(i + 1, N)}
    )
    assert weights == [15, 19, 20, 24]
    reachable = attainable_moment_tuples(max(weights))
    for weight in weights:
        assert len(reachable[weight]) == P**3
    return weights


def verify_exact_census() -> tuple[int, int]:
    off_diagonal_count = 1
    for i in range(N):
        for j in range(i + 1, N):
            weight = B[i][j]
            assert 0 < weight < P
            assert comb(P, weight) % P == 0
            off_diagonal_count *= comb(P, weight)

    # Translation D -> D+c sends the first moment to m+w*c.  Since every
    # off-diagonal weight is nonzero modulo 37, each of its 37 translations
    # has a different first moment.  Hence every first moment has exactly
    # C(37,w)/37 preimages.  A rank-16 homogeneous moment system therefore
    # cuts the product census by exactly 37^16.
    assert off_diagonal_count % P**16 == 0
    reduced_count = off_diagonal_count // P**16
    return off_diagonal_count, reduced_count


def verify_star_coefficients() -> None:
    # iota(y)=(1+y)^-1-1=-y+y^2-y^3+...
    # Coefficients through degree three give:
    # N1^T=-N1,
    # N2^T=N2+N1,
    # N3+N3^T=-2N2-N1.
    iota = [0, -1 % P, 1, -1 % P, 1]

    def polynomial_multiply(left: list[int], right: list[int]) -> list[int]:
        result = [0] * 5
        for i, a in enumerate(left):
            for j, b in enumerate(right):
                if i + j < 5:
                    result[i + j] = (result[i + j] + a * b) % P
        return result

    iota_squared = polynomial_multiply(iota, iota)
    iota_cubed = polynomial_multiply(iota_squared, iota)
    iota_fourth = polynomial_multiply(iota_cubed, iota)
    assert iota[1:5] == [P - 1, 1, P - 1, 1]
    assert iota_squared[1:5] == [0, 1, P - 2, 3]
    assert iota_cubed[1:5] == [0, 0, P - 1, 3]
    assert iota_fourth[1:5] == [0, 0, 0, 1]


def main() -> None:
    verify_star_coefficients()
    (
        _n0,
        skew_kernel,
        symmetric_kernel,
        l_symmetric,
        l_skew,
    ) = verify_quotient_and_first_layer()
    quadratic_preimages = verify_second_layer(
        skew_kernel, l_symmetric
    )
    verify_third_layer(
        skew_kernel,
        symmetric_kernel,
        quadratic_preimages,
        l_skew,
    )
    verify_fourth_layer_characterization(
        _n0,
        skew_kernel,
        quadratic_preimages,
        l_symmetric,
        l_skew,
    )
    verify_full_formal_extension(_n0)
    weights = verify_fixed_weight_reachability()
    off_count, reduced_count = verify_exact_census()

    print("y_adic_identity=N(y)^2=9*y^36*J")
    print("rank_N0=4")
    print("first_moment_variables=36")
    print("first_moment_linear_rank=16")
    print("first_moment_solution_dimension=20")
    print("second_layer_map_rank=24")
    print("second_layer_kernel_dimension=21")
    print("second_layer_cokernel_obstruction=identically_zero")
    print("second_layer_diagonal_freedom_rank=9")
    print("third_layer_cokernel_obstruction=identically_zero")
    print("fourth_layer_map_cokernel_dimension=21")
    print("fourth_layer_arbitrary_free_choice=not_identically_soluble")
    print("symmetric_commutator_map_rank=20")
    print("formal_extension_through_y36=terminal_corrected_exponential")
    print(f"off_diagonal_weights={weights}")
    print("fixed_weight_moment_triples=all_37^3")
    print(f"off_diagonal_ambient_count={off_count}")
    print(f"first_moment_reduced_count={reduced_count}")
    print(f"exact_reduction_factor=37^16={P**16}")
    print(f"exact_reduction_bits={16 * log2(P):.12f}")
    print("certificate=PASS")


if __name__ == "__main__":
    main()
