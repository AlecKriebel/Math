#!/usr/bin/env python3
"""Dependency-free hostile reconstruction over F_101.

This is not a proof over C.  It independently builds the Jacobian
linear maps from sparse-polynomial arithmetic.  It proves characteristic-
zero rank lower bounds for the two canonical kernels by displaying
nonzero minors modulo 101, and stress-tests deterministic samples of the
square, split, and double-member families.  The larger characteristic
avoids the inseparability failures found by the hostile audit at 5 and 11.
"""

if not __debug__:
    raise RuntimeError("audit must not run with Python optimization")

from itertools import product


MODULUS = 101
VARIABLES = 3


def clean(poly):
    return {
        monomial: coefficient % MODULUS
        for monomial, coefficient in poly.items()
        if coefficient % MODULUS
    }


def add(left, right, scale=1):
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = (
            result.get(monomial, 0) + scale * coefficient
        ) % MODULUS
    return clean(result)


def multiply(left, right):
    result = {}
    for first, first_coefficient in left.items():
        for second, second_coefficient in right.items():
            monomial = tuple(
                first[index] + second[index]
                for index in range(VARIABLES)
            )
            result[monomial] = (
                result.get(monomial, 0)
                + first_coefficient * second_coefficient
            ) % MODULUS
    return clean(result)


def derivative(poly, variable):
    result = {}
    for monomial, coefficient in poly.items():
        exponent = monomial[variable]
        if exponent:
            reduced = list(monomial)
            reduced[variable] -= 1
            result[tuple(reduced)] = coefficient * exponent % MODULUS
    return clean(result)


def determinant_three(matrix):
    positive = add(
        add(
            multiply(multiply(matrix[0][0], matrix[1][1]), matrix[2][2]),
            multiply(multiply(matrix[0][1], matrix[1][2]), matrix[2][0]),
        ),
        multiply(multiply(matrix[0][2], matrix[1][0]), matrix[2][1]),
    )
    negative = add(
        add(
            multiply(multiply(matrix[0][2], matrix[1][1]), matrix[2][0]),
            multiply(multiply(matrix[0][1], matrix[1][0]), matrix[2][2]),
        ),
        multiply(multiply(matrix[0][0], matrix[1][2]), matrix[2][1]),
    )
    return add(positive, negative, scale=-1)


def jacobian(first, second, third):
    return determinant_three(
        [
            [derivative(first, index) for index in range(VARIABLES)],
            [derivative(second, index) for index in range(VARIABLES)],
            [derivative(third, index) for index in range(VARIABLES)],
        ]
    )


def homogeneous_monomials(degree):
    return tuple(
        (first, second, degree - first - second)
        for first in range(degree, -1, -1)
        for second in range(degree - first, -1, -1)
    )


def monomial_poly(monomial):
    return {monomial: 1}


def rank_mod(matrix):
    work = [[entry % MODULUS for entry in row] for row in matrix]
    row_count = len(work)
    column_count = len(work[0]) if work else 0
    pivot_row = 0
    for column in range(column_count):
        pivot = next(
            (
                row
                for row in range(pivot_row, row_count)
                if work[row][column]
            ),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inverse = pow(work[pivot_row][column], -1, MODULUS)
        work[pivot_row] = [
            entry * inverse % MODULUS for entry in work[pivot_row]
        ]
        for row in range(row_count):
            if row == pivot_row:
                continue
            factor = work[row][column]
            if factor:
                work[row] = [
                    (work[row][index] - factor * work[pivot_row][index])
                    % MODULUS
                    for index in range(column_count)
                ]
        pivot_row += 1
        if pivot_row == row_count:
            break
    return pivot_row


CONIC_MONOMIALS = homogeneous_monomials(2)
CUBIC_MONOMIALS = homogeneous_monomials(3)
DEGREE_EIGHT_MONOMIALS = homogeneous_monomials(8)
DEGREE_FOUR_MONOMIALS = homogeneous_monomials(4)


def conic(vector):
    return clean(
        {
            monomial: coefficient
            for monomial, coefficient in zip(CONIC_MONOMIALS, vector)
        }
    )


def line(vector):
    return clean(
        {
            monomial: coefficient
            for monomial, coefficient in zip(
                ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                vector,
            )
        }
    )


def map_matrix(first, second, output_monomials):
    columns = [
        jacobian(first, second, monomial_poly(monomial))
        for monomial in CUBIC_MONOMIALS
    ]
    return [
        [column.get(output, 0) for column in columns]
        for output in output_monomials
    ]


def top_rank(h, p, q):
    return rank_mod(
        map_matrix(
            multiply(h, p),
            multiply(h, q),
            DEGREE_EIGHT_MONOMIALS,
        )
    )


def reduced_rank(first, second):
    return rank_mod(map_matrix(first, second, DEGREE_FOUR_MONOMIALS))


def conic_gradient_matrix(vector):
    # CONIC_MONOMIALS is x^2, xy, xz, y^2, yz, z^2.
    a, b, c, d, e, f = vector
    return [
        [2 * a % MODULUS, b, c],
        [b, 2 * d % MODULUS, e],
        [c, e, 2 * f % MODULUS],
    ]


def common_direction_rank(first, second):
    return rank_mod(
        conic_gradient_matrix(first) + conic_gradient_matrix(second)
    )


def proportional(first, second):
    pivot = next((index for index, value in enumerate(second) if value), None)
    if pivot is None:
        return not any(first)
    scale = first[pivot] * pow(second[pivot], -1, MODULUS) % MODULUS
    return all(
        first[index] % MODULUS == scale * second[index] % MODULUS
        for index in range(6)
    )


def line_proportional(first, second):
    pivot = next((index for index, value in enumerate(second) if value), None)
    if pivot is None:
        return not any(first)
    scale = first[pivot] * pow(second[pivot], -1, MODULUS) % MODULUS
    return all(
        first[index] % MODULUS == scale * second[index] % MODULUS
        for index in range(3)
    )


def divisible_by_x(vector):
    # y^2, yz, z^2 coefficients vanish.
    return vector[3] == vector[4] == vector[5] == 0


def divisible_by_y(vector):
    # x^2, xz, z^2 coefficients vanish.
    return vector[0] == vector[2] == vector[5] == 0


def restriction_rank(vector):
    # Twice the symmetric matrix of r(0,y,z).
    _, _, _, d, e, f = vector
    matrix = [[2 * d % MODULUS, e], [e, 2 * f % MODULUS]]
    return rank_mod(matrix)


def restriction_null_vector(vector):
    _, _, _, d, e, f = vector
    matrix = [[2 * d % MODULUS, e], [e, 2 * f % MODULUS]]
    for candidate in product(range(MODULUS), repeat=2):
        if candidate == (0, 0):
            continue
        if all(
            sum(row[index] * candidate[index] for index in range(2))
            % MODULUS
            == 0
            for row in matrix
        ):
            return candidate
    raise AssertionError("rank-one binary restriction has no null vector")


def transverse_cross_term(vector):
    _, xy, xz, _, _, _ = vector
    null = restriction_null_vector(vector)
    return (xy * null[0] + xz * null[1]) % MODULUS


X = monomial_poly((1, 0, 0))
Y = monomial_poly((0, 1, 0))
Z = monomial_poly((0, 0, 1))
X2 = multiply(X, X)
Y2 = multiply(Y, Y)
XY = multiply(X, Y)
XZ = multiply(X, Z)
YZ = multiply(Y, Z)


generator_state = 1


def next_vector(length):
    global generator_state
    values = []
    for _ in range(length):
        generator_state = (
            48271 * generator_state + 17
        ) % 2147483647
        values.append(generator_state % MODULUS)
    return tuple(values)


def sample_square_shape(target=768):
    h = X2
    p = XY
    p_vector = (0, 1, 0, 0, 0, 0)
    tested = 0
    attempts = 0
    while tested < target:
        attempts += 1
        if attempts > 100 * target:
            raise AssertionError("square sampler failed to fill")
        vector = next_vector(6)
        if not any(vector):
            continue
        if proportional(vector, p_vector):
            continue
        if divisible_by_x(vector) or divisible_by_y(vector):
            continue
        if common_direction_rank(p_vector, vector) < 3:
            # Exactly the quadratic-composition/nonminimal locus.
            continue
        tested += 1
        if top_rank(h, p, conic(vector)) != 10:
            raise AssertionError(
                "minimal square-shape sampled counterexample over F_101: "
                f"q={vector}"
            )
    return tested


def sample_split_shape(target=768):
    h = XY
    tested = 0
    attempts = 0
    while tested < target:
        attempts += 1
        if attempts > 100 * target:
            raise AssertionError("split sampler failed to fill")
        first_line = next_vector(3)
        second_line = next_vector(3)
        if not any(first_line) or not any(second_line):
            continue
        p = multiply(X, line(first_line))
        p_vector = tuple(p.get(monomial, 0) for monomial in CONIC_MONOMIALS)
        q = multiply(Y, line(second_line))
        q_vector = tuple(
            q.get(monomial, 0) for monomial in CONIC_MONOMIALS
        )
        # gcd(x*m1, y*m2)=1: m1 is not y, m2 is not x, and
        # m1,m2 are not proportional.
        if line_proportional(first_line, (0, 1, 0)):
            continue
        if line_proportional(second_line, (1, 0, 0)):
            continue
        if line_proportional(first_line, second_line):
            continue
        if common_direction_rank(p_vector, q_vector) < 3:
            continue
        tested += 1
        if top_rank(h, p, q) != 10:
            raise AssertionError(
                "minimal distinct split sampled counterexample over F_101: "
                f"m1={first_line}, m2={second_line}"
            )
    return tested


def reconstruct_double_member_normal_forms(target=768):
    # The two ranks below are characteristic-zero certificates: the
    # displayed invariant cubics give nullity >=2 over Z, while rank 8
    # modulo 101 gives rank >=8 over Q.  The binary exception similarly
    # has four displayed invariant binary cubics and rank 6 modulo 101.
    if reduced_rank(X2, YZ) != 8:
        raise AssertionError("rank-two canonical minor vanished")
    if reduced_rank(X2, add(Y2, XZ)) != 8:
        raise AssertionError("rank-one canonical minor vanished")
    if reduced_rank(X2, Y2) != 6:
        raise AssertionError("binary nonminimal canonical rank changed")

    rank_two_count = 0
    while rank_two_count < target:
        vector = next_vector(6)
        rank = restriction_rank(vector)
        if rank != 2:
            continue
        kernel_dimension = 10 - reduced_rank(X2, conic(vector))
        if kernel_dimension != 2:
            raise AssertionError(
                f"rank-two restriction kernel defect: r={vector}"
            )
        rank_two_count += 1

    rank_one_transverse_count = 0
    rank_one_binary_count = 0
    while rank_one_binary_count < target:
        linear = next_vector(2)
        if linear == (0, 0):
            continue
        first, second = linear
        x_square, along, transverse = next_vector(3)
        if transverse == 0:
            transverse = 1
        restriction = (
            first * first % MODULUS,
            2 * first * second % MODULUS,
            second * second % MODULUS,
        )
        binary_cross = (
            along * first % MODULUS,
            along * second % MODULUS,
        )
        binary_vector = (
            x_square,
            binary_cross[0],
            binary_cross[1],
            restriction[0],
            restriction[1],
            restriction[2],
        )
        if 10 - reduced_rank(X2, conic(binary_vector)) != 4:
            raise AssertionError(
                f"nonminimal binary kernel defect: r={binary_vector}"
            )
        rank_one_binary_count += 1

        # Add a covector that is nonzero on the null direction
        # (-second, first).  This produces exactly the transverse stratum.
        if second:
            cross = (
                (binary_cross[0] + transverse) % MODULUS,
                binary_cross[1],
            )
        else:
            cross = (
                binary_cross[0],
                (binary_cross[1] + transverse) % MODULUS,
            )
        transverse_vector = (
            x_square,
            cross[0],
            cross[1],
            restriction[0],
            restriction[1],
            restriction[2],
        )
        if not transverse_cross_term(transverse_vector):
            raise AssertionError("constructed transverse coefficient vanished")
        if 10 - reduced_rank(X2, conic(transverse_vector)) != 2:
            raise AssertionError(
                f"rank-one transverse kernel defect: r={transverse_vector}"
            )
        rank_one_transverse_count += 1
    return (
        rank_two_count,
        rank_one_transverse_count,
        rank_one_binary_count,
    )


square_count = sample_square_shape()
split_count = sample_split_shape()
double_counts = reconstruct_double_member_normal_forms()

# The two same-fibre equations have no integral solution.  This is only
# an arithmetic guard; the report gives the local valuation derivation.
if 6 % 4 == 0 or 3 % 4 == 0:
    raise AssertionError("same-fibre obstruction arithmetic disappeared")

print(
    "hostile mod-101 reconstruction passed: "
    f"square={square_count}, split={split_count}, "
    f"double={double_counts}"
)
