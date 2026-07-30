"""Exact checks for lossless scalar/one-body elimination in the full dual."""

from fractions import Fraction as F


def zero(rows, cols):
    return [[F(0) for _ in range(cols)] for _ in range(rows)]


def eye(n):
    out = zero(n, n)
    for i in range(n):
        out[i][i] = F(1)
    return out


def add(*matrices):
    return [
        [
            sum(matrix[i][j] for matrix in matrices)
            for j in range(len(matrices[0][0]))
        ]
        for i in range(len(matrices[0]))
    ]


def scale(value, matrix):
    return [[value * entry for entry in row] for row in matrix]


def multiply(left, right):
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(len(right)))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def adjoint(matrix):
    return [list(row) for row in zip(*matrix)]


def hs_squared(matrix):
    return sum(entry * entry for row in matrix for entry in row)


def trace(matrix):
    return sum(matrix[i][i] for i in range(len(matrix)))


def kron(left, right):
    rows = len(left) * len(right)
    cols = len(left[0]) * len(right[0])
    out = zero(rows, cols)
    for i in range(len(left)):
        for j in range(len(left[0])):
            for k in range(len(right)):
                for ell in range(len(right[0])):
                    out[i * len(right) + k][j * len(right[0]) + ell] = (
                        left[i][j] * right[k][ell]
                    )
    return out


def matrix_unit(row, col, dimension=3):
    out = zero(dimension, dimension)
    out[row][col] = F(1)
    return out


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


def embedded_trace(matrix, dims, traced_site):
    """e_i(X)=I_i tensor Tr_i X, with original tensor ordering."""
    dimension = 1
    for dim in dims:
        dimension *= dim
    out = zero(dimension, dimension)
    for row in range(dimension):
        rr = digits(row, dims)
        for col in range(dimension):
            cc = digits(col, dims)
            if rr[traced_site] != cc[traced_site]:
                continue
            value = F(0)
            for traced_value in range(dims[traced_site]):
                rrr = list(rr)
                ccc = list(cc)
                rrr[traced_site] = traced_value
                ccc[traced_site] = traced_value
                value += matrix[
                    flat_index(rrr, dims)
                ][flat_index(ccc, dims)]
            out[row][col] = value
    return out


def vectorize_columns(matrix):
    """Physical index first, logical column second."""
    return [
        [matrix[row][col]]
        for row in range(len(matrix))
        for col in range(len(matrix[0]))
    ]


# The coefficients 24, 12, and 2 are exactly the original degree
# weights after accounting for the untouched identity factors.
assert F(8, 9) * 27 == 24
assert F(4, 3) * 9 == 12
assert F(2, 3) * 3 == 2

# The computational code plane V=(|000>,|111>).
V = zero(27, 2)
V[0][0] = F(1)
V[13][1] = F(1)
assert multiply(adjoint(V), V) == eye(2)
bold_v = vectorize_columns(V)
R = multiply(bold_v, adjoint(bold_v))

dims_output = (3, 3, 3, 2)
S = add(
    eye(54),
    scale(F(-1, 12), embedded_trace(R, dims_output, 0)),
    scale(F(-1, 12), embedded_trace(R, dims_output, 1)),
    scale(F(-1, 12), embedded_trace(R, dims_output, 2)),
    scale(F(1, 24), R),
)

# Independently build L W^{-1} L^* from the scalar vector and the
# Hilbert--Schmidt projection onto each local traceless matrix space.
local_frame = scale(F(1, 24), R)
for site in range(3):
    site_frame = zero(54, 54)
    for row in range(3):
        for col in range(3):
            factors = [eye(3), eye(3), eye(3)]
            factors[site] = matrix_unit(row, col)
            local = kron(kron(factors[0], factors[1]), factors[2])
            local_v = vectorize_columns(multiply(local, V))
            site_frame = add(
                site_frame, multiply(local_v, adjoint(local_v))
            )
    local_frame = add(
        local_frame,
        scale(F(1, 12), add(site_frame, scale(F(-1, 3), R))),
    )
assert S == add(eye(54), scale(F(-1), local_frame))

E10 = matrix_unit(1, 0)
E02 = matrix_unit(0, 2)
E12 = matrix_unit(1, 2)
H = add(
    matrix_unit(0, 0),
    scale(F(-1, 2), matrix_unit(1, 1)),
    scale(F(-1, 2), matrix_unit(2, 2)),
)

B12_a = kron(E10, H)
B12_b = add(
    kron(E10, E10),
    scale(F(1, 2), kron(E02, E02)),
    scale(F(1, 2), kron(E12, E12)),
)
assert trace(E10) == trace(E02) == trace(E12) == trace(H) == 0
assert hs_squared(B12_a) == hs_squared(B12_b) == F(3, 2)

B_a = kron(B12_a, eye(3))
B_b = kron(B12_b, eye(3))
Y_a = multiply(B_a, V)
Y_b = multiply(B_b, V)
assert hs_squared(Y_a) == hs_squared(Y_b) == 1
assert trace(multiply(adjoint(V), Y_a)) == 0
assert trace(multiply(adjoint(V), Y_b)) == 0

y_a = vectorize_columns(Y_a)
y_b = vectorize_columns(Y_b)
assert multiply(S, y_a) == scale(F(11, 12), y_a)
assert multiply(S, y_b) == y_b

# Full Schur energies and minimized deficits.
assert F(12, 11) * hs_squared(Y_a) == F(12, 11)
assert hs_squared(Y_b) == 1
assert F(3) - F(12, 11) == F(21, 11)
assert F(3) - 1 == 2

# Direct audit of the optimal one-body correction for direction a.
A1 = scale(F(1, 11), E10)
A1_embedded = kron(kron(A1, eye(3)), eye(3))
low_output = multiply(A1_embedded, V)
assert low_output == scale(F(1, 11), Y_a)
direct_deficit = (
    F(2) * hs_squared(B12_a)
    + F(12) * hs_squared(A1)
    - hs_squared(add(Y_a, low_output))
)
assert direct_deficit == F(21, 11)

# Direction b is orthogonal to the scalar and every one-body frame.
for site in range(3):
    assert multiply(embedded_trace(R, dims_output, site), y_b) == zero(54, 1)
assert multiply(R, y_b) == zero(54, 1)

print(
    "verified exact full-dual low-sector Schur operator and the "
    "two-direction reflection obstruction"
)
