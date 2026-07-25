#!/usr/bin/env python3
"""Dependency-free exact checks for the marked h != s orbit taxonomy.

The proof of completeness is the linear-algebra argument in REPORT.md.  This
script is a regression certificate for the canonical matrices, discriminant
polynomials, unique-double-line assertions, and residual stabilizer actions.
It uses only Python's standard library and exact rational/modular arithmetic.
"""

from fractions import Fraction
from itertools import product


Q = Fraction


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def matrix(rows):
    return tuple(tuple(Q(value) for value in row) for row in rows)


def transpose(A):
    return tuple(zip(*A))


def matmul(A, B):
    return tuple(
        tuple(sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0])))
        for i in range(len(A))
    )


def congruence(A, M):
    return matmul(transpose(M), matmul(A, M))


def determinant3(A):
    return (
        A[0][0] * A[1][1] * A[2][2]
        + A[0][1] * A[1][2] * A[2][0]
        + A[0][2] * A[1][0] * A[2][1]
        - A[0][2] * A[1][1] * A[2][0]
        - A[0][1] * A[1][0] * A[2][2]
        - A[0][0] * A[1][2] * A[2][1]
    )


def rank_fraction(A):
    work = [list(row) for row in A]
    rows = len(work)
    columns = len(work[0])
    rank = 0
    for column in range(columns):
        pivot = next((i for i in range(rank, rows) if work[i][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        pivot_value = work[rank][column]
        work[rank] = [entry / pivot_value for entry in work[rank]]
        for i in range(rows):
            if i == rank:
                continue
            factor = work[i][column]
            if factor:
                work[i] = [
                    work[i][j] - factor * work[rank][j] for j in range(columns)
                ]
        rank += 1
    return rank


# A bivariate polynomial in A,B is a dictionary (degree_A,degree_B) -> Q.
def poly_add(left, right):
    result = dict(left)
    for monomial, coefficient in right.items():
        result[monomial] = result.get(monomial, Q(0)) + coefficient
        if result[monomial] == 0:
            del result[monomial]
    return result


def poly_neg(poly):
    return {monomial: -coefficient for monomial, coefficient in poly.items()}


def poly_mul(left, right):
    result = {}
    for (i, j), a in left.items():
        for (k, ell), b in right.items():
            monomial = (i + k, j + ell)
            result[monomial] = result.get(monomial, Q(0)) + a * b
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def poly_matrix_entry(s_entry, h_entry):
    result = {}
    if s_entry:
        result[(1, 0)] = s_entry
    if h_entry:
        result[(0, 1)] = h_entry
    return result


def determinant3_polynomial(A):
    positive = [
        poly_mul(poly_mul(A[0][0], A[1][1]), A[2][2]),
        poly_mul(poly_mul(A[0][1], A[1][2]), A[2][0]),
        poly_mul(poly_mul(A[0][2], A[1][0]), A[2][1]),
    ]
    negative = [
        poly_mul(poly_mul(A[0][2], A[1][1]), A[2][0]),
        poly_mul(poly_mul(A[0][1], A[1][0]), A[2][2]),
        poly_mul(poly_mul(A[0][0], A[1][2]), A[2][1]),
    ]
    result = {}
    for term in positive:
        result = poly_add(result, term)
    for term in negative:
        result = poly_add(result, poly_neg(term))
    return result


def pencil_discriminant(S, H):
    entries = tuple(
        tuple(poly_matrix_entry(S[i][j], H[i][j]) for j in range(3))
        for i in range(3)
    )
    return determinant3_polynomial(entries)


S = matrix(
    [
        [1, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]
)
T = matrix(
    [
        [0, 0, 0],
        [0, 0, Q(1, 2)],
        [0, Q(1, 2), 0],
    ]
)
S_PLUS_T = matrix(
    [
        [1, 0, 0],
        [0, 0, Q(1, 2)],
        [0, Q(1, 2), 0],
    ]
)
U = matrix(
    [
        [0, 0, Q(1, 2)],
        [0, 1, 0],
        [Q(1, 2), 0, 0],
    ]
)


def check_canonical_invariants():
    forms = {
        "P21-HR2": (T, 2, 2, {(1, 2): Q(-1, 4)}),
        "P21-HSM": (
            S_PLUS_T,
            3,
            2,
            {(1, 2): Q(-1, 4), (0, 3): Q(-1, 4)},
        ),
        "P3-HSM": (U, 3, 1, {(0, 3): Q(-1, 4)}),
    }
    for name, (H, expected_rank, expected_restriction_rank, expected_disc) in forms.items():
        require(rank_fraction(H) == expected_rank, f"{name}: wrong rank(h)")
        restriction = tuple(tuple(H[i][j] for j in (1, 2)) for i in (1, 2))
        require(
            rank_fraction(restriction) == expected_restriction_rank,
            f"{name}: wrong rank(h|x=0)",
        )
        require(
            pencil_discriminant(S, H) == expected_disc,
            f"{name}: wrong pencil discriminant",
        )


def rank_mod(A, prime):
    work = [[int(entry) % prime for entry in row] for row in A]
    rows = len(work)
    columns = len(work[0])
    rank = 0
    for column in range(columns):
        pivot = next((i for i in range(rank, rows) if work[i][column] % prime), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        inverse = pow(work[rank][column], -1, prime)
        work[rank] = [(entry * inverse) % prime for entry in work[rank]]
        for i in range(rows):
            if i == rank:
                continue
            factor = work[i][column] % prime
            if factor:
                work[i] = [
                    (work[i][j] - factor * work[rank][j]) % prime
                    for j in range(columns)
                ]
        rank += 1
    return rank


def modular_matrix(A, prime):
    return tuple(
        tuple(
            (entry.numerator * pow(entry.denominator, -1, prime)) % prime
            for entry in row
        )
        for row in A
    )


def modular_linear_combination(a, A, b, B, prime):
    return tuple(
        tuple((a * A[i][j] + b * B[i][j]) % prime for j in range(3))
        for i in range(3)
    )


def projective_line(prime):
    return [(1, value) for value in range(prime)] + [(0, 1)]


def check_unique_double_line_modular():
    # Odd characteristics are used only as exact fault-sensitive regressions.
    for prime in (5, 7):
        s = modular_matrix(S, prime)
        for name, H in (("P21-HR2", T), ("P21-HSM", S_PLUS_T), ("P3-HSM", U)):
            h = modular_matrix(H, prime)
            rank_one_points = [
                (a, b)
                for a, b in projective_line(prime)
                if rank_mod(modular_linear_combination(a, s, b, h, prime), prime) == 1
            ]
            require(
                rank_one_points == [(1, 0)],
                f"{name} over F_{prime}: double line is not unique",
            )


def matmul_mod(A, B, prime):
    return tuple(
        tuple(
            sum(A[i][k] * B[k][j] for k in range(len(B))) % prime
            for j in range(len(B[0]))
        )
        for i in range(len(A))
    )


def transpose_mod(A):
    return tuple(zip(*A))


def congruence_mod(A, M, prime):
    return matmul_mod(transpose_mod(M), matmul_mod(A, M, prime), prime)


def determinant2_mod(a, b, c, d, prime):
    return (a * d - b * c) % prime


def proportional_scale(A, B, prime):
    """Return scale with A = scale*B, or None."""
    scale = None
    for i in range(3):
        for j in range(3):
            if B[i][j] % prime:
                candidate = A[i][j] * pow(B[i][j], -1, prime) % prime
                if scale is None:
                    scale = candidate
                elif scale != candidate:
                    return None
            elif A[i][j] % prime:
                return None
    return scale


def parabolic_matrices(prime):
    """All GL3 matrices with pullback x -> a*x."""
    for a in range(1, prime):
        for u, v in product(range(prime), repeat=2):
            for b, c, d, e in product(range(prime), repeat=4):
                if determinant2_mod(b, c, d, e, prime) == 0:
                    continue
                yield (
                    (a, 0, 0),
                    (u, b, c),
                    (v, d, e),
                )


def check_pair_stabilizer_actions():
    prime = 5
    s = modular_matrix(S, prime)
    expected = {
        "P21-HR2": set(range(1, prime)),
        "P21-HSM": {1},
        # The complex image is all C^*: over F_p the formula is a square.
        "P3-HSM": {1, 4},
    }
    observed = {name: set() for name in expected}
    h_forms = {
        "P21-HR2": modular_matrix(T, prime),
        "P21-HSM": modular_matrix(S_PLUS_T, prime),
        "P3-HSM": modular_matrix(U, prime),
    }
    for M in parabolic_matrices(prime):
        transformed_s = congruence_mod(s, M, prime)
        scale_s = proportional_scale(transformed_s, s, prime)
        require(scale_s is not None and scale_s != 0, "parabolic matrix lost s")
        for name, h in h_forms.items():
            transformed_h = congruence_mod(h, M, prime)
            scale_h = proportional_scale(transformed_h, h, prime)
            if scale_h is None or scale_h == 0:
                continue
            observed[name].add(scale_s * pow(scale_h, -1, prime) % prime)
    require(observed == expected, f"wrong residual scaling images: {observed}")


def check_explicit_p3_translation():
    mu = Q(7, 3)
    translation = matrix(
        [
            [1, 0, 0],
            [0, 1, 0],
            [mu, 0, 1],
        ]
    )
    transformed_s = congruence(S, translation)
    transformed_u = congruence(U, translation)
    expected_u = tuple(
        tuple(U[i][j] + mu * S[i][j] for j in range(3)) for i in range(3)
    )
    require(transformed_s == S, "P3 translation does not preserve s")
    require(transformed_u == expected_u, "P3 translation does not send u to u+mu*s")


def check_second_double_line_failure():
    # If rank(h|x=0)=1 but the xz coupling vanishes, h=A*x^2+y^2,
    # and the pencil contains the second double line y^2.
    A = Q(11, 5)
    y_squared = matrix([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
    bad_h = tuple(
        tuple(A * S[i][j] + y_squared[i][j] for j in range(3))
        for i in range(3)
    )
    recovered = tuple(
        tuple(bad_h[i][j] - A * S[i][j] for j in range(3))
        for i in range(3)
    )
    require(recovered == y_squared, "failed to recover the second double line")
    require(rank_fraction(recovered) == 1, "recovered member is not rank one")


def main():
    check_canonical_invariants()
    check_unique_double_line_modular()
    check_pair_stabilizer_actions()
    check_explicit_p3_translation()
    check_second_double_line_failure()
    print(
        "PASS: 3 marked-pair types, discriminants, unique double lines, "
        "and residual companion actions verified"
    )


if __name__ == "__main__":
    main()
