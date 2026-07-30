#!/usr/bin/env python3
"""Exact obstruction to the scalar Fierz fourth-moment closure.

Everything is computed with fractions.  The local Fierz matrices are kept
unnormalized; ``den`` records the product of their squared Hilbert--Schmidt
norms, so every reported quantity is exactly the one for the normalized
tensor-Fierz label.
"""

from fractions import Fraction as F
from itertools import combinations, product


N = 3
SITES = range(N)


def matrix_unit(i, j, value=1):
    return {(i, j): F(value)}


def add_local(*matrices):
    out = {}
    for matrix in matrices:
        for key, value in matrix.items():
            out[key] = out.get(key, F(0)) + value
    return {key: value for key, value in out.items() if value}


# (raw matrix, squared HS norm, parity), where parity 0 is symmetric and
# parity 1 is skew.
LOCAL_FIERZ = []
for i in range(3):
    LOCAL_FIERZ.append((matrix_unit(i, i), 1, 0))
for i, j in combinations(range(3), 2):
    LOCAL_FIERZ.append(
        (add_local(matrix_unit(i, j), matrix_unit(j, i)), 2, 0)
    )
for i, j in combinations(range(3), 2):
    LOCAL_FIERZ.append(
        (add_local(matrix_unit(i, j), matrix_unit(j, i, -1)), 2, 1)
    )


def apply_local(matrix, column):
    return {row: value for (row, col), value in matrix.items() if col == column}


def apply_tensor(tensor_matrices, basis_word):
    local_images = [
        apply_local(matrix, column)
        for matrix, column in zip(tensor_matrices, basis_word)
    ]
    if any(not image for image in local_images):
        return {}
    out = {}
    for choices in product(*[tuple(image.items()) for image in local_images]):
        row = tuple(choice[0] for choice in choices)
        value = F(1)
        for _, coefficient in choices:
            value *= coefficient
        out[row] = out.get(row, F(0)) + value
    return {key: value for key, value in out.items() if value}


def sparse_add_to(target, source, scale=F(1)):
    for key, value in source.items():
        target[key] = target.get(key, F(0)) + scale * value
        if not target[key]:
            del target[key]


def outer(left_columns, right_columns):
    """Return sum_j |left_j><right_j| for real sparse columns."""
    out = {}
    for left, right in zip(left_columns, right_columns):
        for row, left_value in left.items():
            for col, right_value in right.items():
                key = (row, col)
                out[key] = out.get(key, F(0)) + left_value * right_value
    return {key: value for key, value in out.items() if value}


def partial_trace(matrix, traced):
    traced = frozenset(traced)
    remaining = tuple(i for i in SITES if i not in traced)
    out = {}
    for (row, col), value in matrix.items():
        if any(row[i] != col[i] for i in traced):
            continue
        key = (
            tuple(row[i] for i in remaining),
            tuple(col[i] for i in remaining),
        )
        out[key] = out.get(key, F(0)) + value
    return {key: value for key, value in out.items() if value}


def hs_inner(left, right):
    return sum(
        value * right.get(key, F(0)) for key, value in left.items()
    )


def endpoint_bilinear(left, right):
    value = F(0)
    for size in range(N + 1):
        coefficient = F(-1, 2) ** size
        for traced in combinations(SITES, size):
            value += coefficient * hs_inner(
                partial_trace(left, traced), partial_trace(right, traced)
            )
    return value


def basis_column(word):
    return {word: F(1)}


U_WORDS = ((0, 0, 0), (0, 0, 1))
V_WORDS = ((1, 1, 0), (1, 1, 1))
U_COLUMNS = tuple(basis_column(word) for word in U_WORDS)
V_COLUMNS = tuple(basis_column(word) for word in V_WORDS)

# C0 = |000><110| + |001><111| and
# L^{tensor 3}(C0) = W0 = -|002><112|.
C0 = outer(U_COLUMNS, V_COLUMNS)
W0 = {((0, 0, 2), (1, 1, 2)): F(-1)}

assert hs_inner(C0, C0) == 2
assert endpoint_bilinear(C0, C0) == 0
assert hs_inner(W0, W0) == 1
assert hs_inner(C0, W0) == 0


def remove_projection(column, support_words):
    return {
        word: value
        for word, value in column.items()
        if word not in support_words
    }


sum_a = F(0)
sum_b = F(0)
sum_abs_p = F(0)
sum_abs_r = F(0)
sum_signed_r = F(0)
reconstructed_w = {}
parity_groups = {}

for labels in product(LOCAL_FIERZ, repeat=N):
    raw_matrices = tuple(label[0] for label in labels)
    denominator = 1
    parity_word = []
    for _, norm_squared, parity in labels:
        denominator *= norm_squared
        parity_word.append(parity)
    parity_word = tuple(parity_word)
    skew_count = sum(parity_word)
    weight = F(3**skew_count, 8)
    eta = -1 if skew_count % 2 else 1

    # X_T=(I-P_U)T V and Z_T=(I-P_V)T U, for the raw T.
    x_columns = tuple(
        remove_projection(apply_tensor(raw_matrices, word), U_WORDS)
        for word in V_WORDS
    )
    z_columns = tuple(
        remove_projection(apply_tensor(raw_matrices, word), V_WORDS)
        for word in U_WORDS
    )

    # Sigma=I_2 for the unnormalized C0.
    d_left = outer(x_columns, V_COLUMNS)
    d_right = outer(U_COLUMNS, z_columns)
    normal = outer(x_columns, z_columns)

    a_value = endpoint_bilinear(d_left, d_left) / denominator
    b_value = endpoint_bilinear(d_right, d_right) / denominator
    p_value = endpoint_bilinear(d_left, d_right) / denominator
    r_value = hs_inner(W0, normal) / denominator

    sum_a += weight * a_value
    sum_b += weight * b_value
    sum_abs_p += weight * abs(p_value)
    sum_abs_r += weight * abs(r_value)
    sum_signed_r += eta * weight * r_value

    sparse_add_to(
        reconstructed_w, normal, F(eta) * weight / denominator
    )

    group = parity_groups.setdefault(parity_word, [F(0)] * 5)
    group[0] += weight * a_value
    group[1] += weight * b_value
    group[2] += weight * abs(p_value)
    group[3] += weight * abs(r_value)
    group[4] += eta * weight * r_value


EXPECTED_GROUPS = {
    (0, 0, 0): [F(25, 32), F(25, 32), 0, F(1, 32), F(-1, 32)],
    (0, 0, 1): [F(51, 32), F(51, 32), 0, F(3, 32), F(3, 32)],
    (0, 1, 0): [F(3, 2), F(3, 2), 0, F(3, 32), F(-3, 32)],
    (0, 1, 1): [F(99, 32), F(99, 32), 0, F(9, 32), F(9, 32)],
    (1, 0, 0): [F(3, 2), F(3, 2), 0, F(3, 32), F(-3, 32)],
    (1, 0, 1): [F(99, 32), F(99, 32), 0, F(9, 32), F(9, 32)],
    (1, 1, 0): [F(45, 16), F(45, 16), 0, F(9, 32), F(-9, 32)],
    (1, 1, 1): [F(189, 32), F(189, 32), 0, F(27, 32), F(27, 32)],
}

assert parity_groups == {
    key: [F(value) for value in values]
    for key, values in EXPECTED_GROUPS.items()
}
assert reconstructed_w == W0
assert sum_a == F(649, 32)
assert sum_b == F(649, 32)
assert sum_abs_p == 0
assert sum_abs_r == 2
assert sum_signed_r == 1

# The proposed scalar closure has left side 649/32 and natural residual
# target ||W0||^2=1.  It therefore fails by 617/32.  Normalizing C0
# divides every quadratic/fourth-moment quantity here by two.
assert (sum_a * sum_b) == F(649, 32) ** 2
assert F(649, 32) - hs_inner(W0, W0) == F(617, 32)
assert F(649, 64) - F(1, 2) == F(617, 64)

# The direct coherent leakage channel saturates the exact 2x2 Hessian:
# D_X=|002><110|, D_Z=|000><112|, N=|002><112|.
d_x = {((0, 0, 2), (1, 1, 0)): F(1)}
d_z = {((0, 0, 0), (1, 1, 2)): F(1)}
normal_channel = {((0, 0, 2), (1, 1, 2)): F(1)}
assert endpoint_bilinear(d_x, d_x) == 1
assert endpoint_bilinear(d_z, d_z) == 1
assert endpoint_bilinear(d_x, d_z) == 0
assert abs(hs_inner(W0, normal_channel)) == 1

print("exact Fierz fourth-moment zero obstruction: verified")
print("sum w A = sum w B =", sum_a)
print("sum w |p| =", sum_abs_p)
print("sum w |r| =", sum_abs_r)
print("sum eta w r = ||W||^2 =", sum_signed_r)
print("scalar closure gap (unnormalized) =", F(617, 32))
