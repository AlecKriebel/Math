"""Dependency-free exact checks for the scalar-reflection frontier."""

from fractions import Fraction as F
from itertools import combinations, product


def zero(rows, cols):
    return [[F(0) for _ in range(cols)] for _ in range(rows)]


def eye(n):
    out = zero(n, n)
    for i in range(n):
        out[i][i] = F(1)
    return out


def add(*matrices):
    rows, cols = len(matrices[0]), len(matrices[0][0])
    return [
        [sum(matrix[i][j] for matrix in matrices) for j in range(cols)]
        for i in range(rows)
    ]


def scale(value, matrix):
    return [[value * entry for entry in row] for row in matrix]


def multiply(left, right):
    rows, inner, cols = len(left), len(right), len(right[0])
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(inner))
            for j in range(cols)
        ]
        for i in range(rows)
    ]


def trace(matrix):
    return sum(matrix[i][i] for i in range(len(matrix)))


def hs_squared(matrix):
    return sum(entry * entry for row in matrix for entry in row)


def digits(index, dims):
    out = [0] * len(dims)
    for site in range(len(dims) - 1, -1, -1):
        out[site] = index % dims[site]
        index //= dims[site]
    return tuple(out)


def flat_index(values, dims):
    answer = 0
    for value, dim in zip(values, dims):
        answer = dim * answer + value
    return answer


def embedded_reduction(matrix, dims, keep):
    """Partial trace to keep, tensored with identity on its complement."""
    keep = tuple(keep)
    missing = tuple(site for site in range(len(dims)) if site not in keep)
    dimension = 1
    for dim in dims:
        dimension *= dim
    answer = zero(dimension, dimension)
    for row in range(dimension):
        row_digits = digits(row, dims)
        for col in range(dimension):
            col_digits = digits(col, dims)
            if any(row_digits[site] != col_digits[site] for site in missing):
                continue
            value = F(0)
            missing_dims = tuple(dims[site] for site in missing)
            for traced_values in product(
                *(range(dim) for dim in missing_dims)
            ):
                rr = list(row_digits)
                cc = list(col_digits)
                for site, traced_value in zip(missing, traced_values):
                    rr[site] = traced_value
                    cc[site] = traced_value
                value += matrix[
                    flat_index(rr, dims)
                ][flat_index(cc, dims)]
            answer[row][col] = value
    return answer


def simultaneous_partial_trace(matrix, dims, traced):
    """Trace matching row/column tensor sites of a coefficient matrix."""
    traced = tuple(traced)
    keep = tuple(site for site in range(len(dims)) if site not in traced)
    keep_dims = tuple(dims[site] for site in keep)
    out_dimension = 1
    for dim in keep_dims:
        out_dimension *= dim
    answer = zero(out_dimension, out_dimension)
    for row_values in product(*(range(dim) for dim in keep_dims)):
        for col_values in product(*(range(dim) for dim in keep_dims)):
            value = F(0)
            traced_dims = tuple(dims[site] for site in traced)
            for traced_values in product(
                *(range(dim) for dim in traced_dims)
            ):
                rr = [0] * len(dims)
                cc = [0] * len(dims)
                for site, digit in zip(keep, row_values):
                    rr[site] = digit
                for site, digit in zip(keep, col_values):
                    cc[site] = digit
                for site, digit in zip(traced, traced_values):
                    rr[site] = cc[site] = digit
                value += matrix[
                    flat_index(rr, dims)
                ][flat_index(cc, dims)]
            answer[
                flat_index(row_values, keep_dims)
            ][flat_index(col_values, keep_dims)] = value
    return answer


# Map identity, in the tensor basis where a mask records the sites carrying e.
target = {
    0b111: F(6),
    0b011: F(-3),
    0b101: F(-3),
    0b110: F(-3),
    0b001: F(2),
    0b010: F(2),
    0b100: F(2),
    0b000: F(-4, 3),
}
expanded = {mask: F(0) for mask in range(8)}
expanded[0b111] += F(3, 2)
for mask in range(8):
    identity_count = 3 - mask.bit_count()
    expanded[mask] += F(9, 2) * F(-2, 3) ** identity_count
assert expanded == target

# Choi sector parity collapse.
assert [
    F(3, 2) + F(9, 2) * ((-1) ** entangled_count)
    for entangled_count in range(4)
] == [F(6), F(-3), F(6), F(-3)]


# Bell-spectator state R=P_{Phi_3}^{12} tensor P_{Phi_2}^{K3}.
dims_state = (2, 3, 3, 3)  # K,1,2,3
state_dimension = 54
R = zero(state_dimension, state_dimension)
P12 = zero(state_dimension, state_dimension)
QK3 = zero(state_dimension, state_dimension)
for row in range(state_dimension):
    k, a, b, c = digits(row, dims_state)
    for col in range(state_dimension):
        ell, d, e, f = digits(col, dims_state)
        p_entry = F(1, 3) if a == b and d == e else F(0)
        q_entry = (
            F(1, 2)
            if k == c and ell == f and k < 2 and ell < 2
            else F(0)
        )
        P12[row][col] = p_entry if k == ell and c == f else F(0)
        QK3[row][col] = q_entry if a == d and b == e else F(0)
        R[row][col] = p_entry * q_entry

assert multiply(R, R) == R
assert trace(R) == 1
assert multiply(P12, QK3) == R

rho_k12 = embedded_reduction(R, dims_state, (0, 1, 2))
rho_k13 = embedded_reduction(R, dims_state, (0, 1, 3))
rho_k23 = embedded_reduction(R, dims_state, (0, 2, 3))
rho_k1 = embedded_reduction(R, dims_state, (0, 1))
rho_k2 = embedded_reduction(R, dims_state, (0, 2))
rho_k3 = embedded_reduction(R, dims_state, (0, 3))

A = add(
    scale(F(3), eye(state_dimension)),
    scale(F(2), rho_k12),
    scale(F(2), rho_k13),
    scale(F(2), rho_k23),
    scale(F(-3), rho_k1),
    scale(F(-3), rho_k2),
    scale(F(-3), rho_k3),
)
A_formula = add(
    scale(F(2), eye(state_dimension)),
    P12,
    scale(F(-5, 3), QK3),
)
assert A == A_formula
assert multiply(A, R) == scale(F(4, 3), R)
assert trace(multiply(R, add(A, scale(F(-3, 2), R)))) == F(-1, 6)

# The exact joint spectral table for A-(4/3)R.
assert {
    (p, q): F(2) + p - F(5, 3) * q - F(4, 3) * p * q
    for p, q in product((0, 1), repeat=2)
} == {
    (0, 0): F(2),
    (1, 0): F(3),
    (0, 1): F(1, 3),
    (1, 1): F(0),
}


# Rank-two coefficient equality C=P_{Phi_3}^{12} tensor P_2^{3}.
dims_coefficient = (3, 3, 3)
coefficient_dimension = 27
C = zero(coefficient_dimension, coefficient_dimension)
for row in range(coefficient_dimension):
    a, b, c = digits(row, dims_coefficient)
    for col in range(coefficient_dimension):
        d, e, f = digits(col, dims_coefficient)
        if a == b and d == e and c == f and c < 2:
            C[row][col] = F(1, 3)

assert multiply(C, C) == C
assert trace(C) == 2
assert hs_squared(C) == 2

q_value = F(0)
sites = range(3)
for cardinality in range(4):
    for traced in combinations(sites, cardinality):
        reduced = simultaneous_partial_trace(C, dims_coefficient, traced)
        q_value += F(-2, 3) ** cardinality * hs_squared(reduced)
assert q_value == F(-2, 3)
assert q_value == -F(1, 3) * hs_squared(C)

# Independent exact sector weights from the tensor factors.
w0 = F(1, 9) * F(4, 3)
w1 = F(1, 9) * F(2, 3)
w2 = F(8, 9) * F(4, 3)
w3 = F(8, 9) * F(2, 3)
assert (w0, w1, w2, w3) == (
    F(4, 27),
    F(2, 27),
    F(32, 27),
    F(16, 27),
)
assert w0 + w1 + w2 + w3 == 2
assert w0 + w2 == F(2, 3) * 2
assert (w1 + w3) - (w0 + w2) == q_value

print(
    "verified scalar-reflection map/Choi identities, exact c=3/2 "
    "counterexample, and sharp c=4/3 rank-two equality"
)
