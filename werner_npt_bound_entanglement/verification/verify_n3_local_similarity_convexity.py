"""Exact arithmetic checks for local-similarity convexity.

This is a small formula checker, not a finite proof of the universal
two-copy theorem used in the accompanying note.
"""

from fractions import Fraction as F


def index(t):
    return 9 * t[0] + 3 * t[1] + t[2]


def partial_trace(matrix, dims, traced):
    remaining = tuple(i for i in range(len(dims)) if i not in traced)
    size = 1
    for i in remaining:
        size *= dims[i]
    out = [[F(0) for _ in range(size)] for _ in range(size)]

    def digits(number):
        ans = [0] * len(dims)
        for i in range(len(dims) - 1, -1, -1):
            ans[i] = number % dims[i]
            number //= dims[i]
        return ans

    def reduced_index(t):
        ans = 0
        for i in remaining:
            ans = dims[i] * ans + t[i]
        return ans

    full_size = len(matrix)
    tuples = [digits(i) for i in range(full_size)]
    for row in range(full_size):
        for col in range(full_size):
            if all(tuples[row][i] == tuples[col][i] for i in traced):
                out[reduced_index(tuples[row])][
                    reduced_index(tuples[col])
                ] += matrix[row][col]
    return out


def norm_squared(matrix):
    return sum(value * value for row in matrix for value in row)


def endpoint_q(matrix, copies):
    dims = (3,) * copies
    value = F(0)
    for mask in range(1 << copies):
        traced = tuple(i for i in range(copies) if (mask >> i) & 1)
        value += F(-1, 2) ** len(traced) * norm_squared(
            partial_trace(matrix, dims, traced)
        )
    return value


def endpoint_b(left, right, copies):
    return F(1, 2) * (
        endpoint_q(add(left, right), copies)
        - endpoint_q(left, copies)
        - endpoint_q(right, copies)
    )


def determinant3(matrix):
    return (
        matrix[0][0]
        * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1]
        * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2]
        * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )


def psd3(matrix):
    assert all(matrix[p][r] == matrix[r][p] for p in range(3) for r in range(3))
    assert all(matrix[p][p] >= 0 for p in range(3))
    assert all(
        matrix[p][p] * matrix[r][r] - matrix[p][r] ** 2 >= 0
        for p in range(3)
        for r in range(p + 1, 3)
    )
    assert determinant3(matrix) >= 0


def outer(left, right):
    return [[a * b for b in right] for a in left]


def add(*matrices):
    return [
        [sum(matrix[i][j] for matrix in matrices) for j in range(len(matrices[0]))]
        for i in range(len(matrices[0]))
    ]


def local_block(matrix, row_symbol, col_symbol):
    out = [[F(0) for _ in range(9)] for _ in range(9)]
    for row_tail in range(9):
        for col_tail in range(9):
            out[row_tail][col_tail] = matrix[
                9 * row_symbol + row_tail
            ][9 * col_symbol + col_tail]
    return out


def local_similarity(matrix, scale):
    out = [[F(0) for _ in range(27)] for _ in range(27)]
    for row in range(27):
        for col in range(27):
            out[row][col] = (
                matrix[row][col]
                * scale[row // 9]
                / scale[col // 9]
            )
    return out


# A rational rank-two square-zero example with nontrivial local blocks.
u0 = [F(0)] * 27
u1 = [F(0)] * 27
w0 = [F(0)] * 27
w1 = [F(0)] * 27
for position, value in {
    (0, 0, 0): 1,
    (1, 0, 1): 2,
    (2, 1, 0): 1,
}.items():
    u0[index(position)] = F(value)
for position, value in {
    (0, 1, 1): 1,
    (1, 2, 0): -1,
    (2, 0, 2): 3,
}.items():
    u1[index(position)] = F(value)
for position, value in {
    (0, 0, 1): 1,
    (1, 1, 0): 1,
    (2, 2, 2): -2,
}.items():
    w0[index(position)] = F(value)
for position, value in {
    (0, 2, 0): 2,
    (1, 1, 2): 1,
    (2, 0, 1): 1,
}.items():
    w1[index(position)] = F(value)

C = add(outer(u0, w0), [[2 * x for x in row] for row in outer(u1, w1)])

# The chosen supports are disjoint, so C^2=0.
product = [
    [sum(C[i][k] * C[k][j] for k in range(27)) for j in range(27)]
    for i in range(27)
]
assert all(value == 0 for row in product for value in row)

blocks = [[local_block(C, p, q) for q in range(3)] for p in range(3)]
weights = [[endpoint_q(blocks[p][q], 2) for q in range(3)] for p in range(3)]
assert all(value >= 0 for row in weights for value in row)

diagonal_sum = add(blocks[0][0], blocks[1][1], blocks[2][2])
constant = (
    sum(weights[p][p] for p in range(3))
    - F(1, 2) * endpoint_q(diagonal_sum, 2)
)
assert endpoint_q(C, 3) == constant + sum(
    weights[p][q] for p in range(3) for q in range(3) if p != q
)

# k=(1,0,-1), evaluated exactly at exp(t)=2.
k = (1, 0, -1)
scale = (F(2), F(1), F(1, 2))
C_filtered = local_similarity(C, scale)
formula = constant + sum(
    F(2) ** (2 * (k[p] - k[q])) * weights[p][q]
    for p in range(3)
    for q in range(3)
    if p != q
)
assert endpoint_q(C_filtered, 3) == formula

second_derivative_at_zero = 4 * sum(
    (k[p] - k[q]) ** 2 * weights[p][q]
    for p in range(3)
    for q in range(3)
    if p != q
)
assert second_derivative_at_zero > 0

# The full moment matrix (not only its diagonal flow equations) is
# Hermitian.  This sample is real, so Hermitian means symmetric.
moment = [[F(0) for _ in range(3)] for _ in range(3)]
for p in range(3):
    for r in range(3):
        moment[p][r] = sum(
            endpoint_b(blocks[r][q], blocks[p][q], 2)
            - endpoint_b(blocks[q][p], blocks[q][r], 2)
            for q in range(3)
        )
assert all(moment[p][r] == moment[r][p] for p in range(3) for r in range(3))
assert all(
    moment[p][p]
    == sum(weights[p][q] - weights[q][p] for q in range(3))
    for p in range(3)
)

# The moment is the difference of two positive semidefinite Gram
# matrices.  This is the matrix-valued refinement of flow balance.
row_gram = [
    [
        sum(endpoint_b(blocks[p][q], blocks[r][q], 2) for q in range(3))
        for r in range(3)
    ]
    for p in range(3)
]
column_gram = [
    [
        sum(endpoint_b(blocks[q][p], blocks[q][r], 2) for q in range(3))
        for r in range(3)
    ]
    for p in range(3)
]
psd3(row_gram)
psd3(column_gram)
assert all(
    moment[p][r] == row_gram[r][p] - column_gram[p][r]
    for p in range(3)
    for r in range(3)
)

# The singular-Gram theorem is sharp at the exact transverse
# common-qubit spin-flip zero.  We omit normalization to stay over Q.
anchor_u0 = [F(0)] * 27
anchor_u1 = [F(0)] * 27
anchor_w0 = [F(0)] * 27
anchor_w1 = [F(0)] * 27
anchor_u0[index((0, 0, 0))] = 1
anchor_u0[index((0, 1, 1))] = 1
anchor_u1[index((1, 0, 0))] = 1
anchor_u1[index((1, 1, 1))] = -1
anchor_w0[index((0, 1, 1))] = 1
anchor_w0[index((0, 0, 0))] = -1
anchor_w1[index((1, 0, 0))] = 1
anchor_w1[index((1, 1, 1))] = 1
anchor = add(outer(anchor_u0, anchor_w0), outer(anchor_u1, anchor_w1))
assert endpoint_q(anchor, 3) == 0
anchor_blocks = [
    [local_block(anchor, p, q) for q in range(3)] for p in range(3)
]
anchor_weights = [
    [endpoint_q(anchor_blocks[p][q], 2) for q in range(3)]
    for p in range(3)
]
assert all(
    anchor_weights[p][q] == 0
    for p in range(3)
    for q in range(3)
    if p != q
)
anchor_row_gram = [
    [
        sum(
            endpoint_b(anchor_blocks[p][q], anchor_blocks[r][q], 2)
            for q in range(3)
        )
        for r in range(3)
    ]
    for p in range(3)
]
assert anchor_row_gram == [
    [F(2), F(0), F(0)],
    [F(0), F(2), F(0)],
    [F(0), F(0), F(0)],
]

# Exact factor-plane kernel alignment (Lemma 4).  On two qutrits,
# Z has range |0> tensor span{|0>,|1>}; W has range
# (|0>+2|1>+3|2>) tensor the same two-plane.  The nonorthonormal
# logical columns audit the inverse-Gram factor in the proof.
def index2(t):
    return 3 * t[0] + t[1]


z_column0 = [F(0)] * 9
z_column1 = [F(0)] * 9
w_column0 = [F(0)] * 9
w_column1 = [F(0)] * 9
z_column0[index2((0, 0))] = 1
z_column1[index2((0, 1))] = 2
for first, coefficient in enumerate((1, 2, 3)):
    w_column0[index2((first, 0))] = F(coefficient)
    w_column1[index2((first, 1))] = F(coefficient, 2)
aligned_kernel = add(
    outer(z_column0, w_column0), outer(z_column1, w_column1)
)
assert endpoint_q(aligned_kernel, 2) == 0

# Exact rank-four obstruction from Section 5.
P = [[F(int(i == j and i < 2)) for j in range(3)] for i in range(3)]
Q = [[F(int(i == j and i > 0)) for j in range(3)] for i in range(3)]
R = [[F(int(i == j == 0)) for j in range(3)] for i in range(3)]
S = [[F(int(i == j == 1)) for j in range(3)] for i in range(3)]


def kronecker(left, right):
    return [
        [
            left[i // len(right)][j // len(right)]
            * right[i % len(right)][j % len(right)]
            for j in range(len(left[0]) * len(right[0]))
        ]
        for i in range(len(left) * len(right))
    ]


A = kronecker(P, R)
B = kronecker(Q, S)
assert endpoint_q(A, 2) == 0
assert endpoint_q(B, 2) == 0
assert endpoint_q(add(A, B), 2) == 1

formal = [[F(0) for _ in range(27)] for _ in range(27)]
for i in range(9):
    for j in range(9):
        formal[i][j] = A[i][j]
        formal[9 + i][9 + j] = B[i][j]
assert endpoint_q(formal, 3) == F(-1, 2)

print("verified: exact rank-two local-similarity recursion")
print("verified: positive exact similarity Hessian", second_derivative_at_zero)
print("verified: sharp singular-Gram diagonal-collapse zero")
print("verified: exact factor-plane kernel alignment")
print("verified: balanced rank-four block obstruction")
