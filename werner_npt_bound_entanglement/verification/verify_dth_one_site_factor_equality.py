#!/usr/bin/env python3
"""Dependency-free exact check of a physical DTH equality point.

The point belongs to the one-site-factor/common-local-qubit-support face
isolated by the unrestricted complex physical search.  All arrays below use
``Fraction`` arithmetic.  We remove the square roots from the Hodge and
bivector conventions as follows:

    E_p = sqrt(2) A_p,
    D_z = D_integer / (2 sqrt(2)),
    W   = W_integer / sqrt(2),
    D_z W = D_integer W_integer / 4.

The chosen normalized data are

    z = e0 tensor (3 |00> + 4 |11>) / 5,
    q = (4 |00> + 3 |11>) / 5,
    u = e1 tensor q,
    v = e2 tensor q.

The script proves exactly the support and Omega equations, objective 1/8,
square zero, rank two, the two equal singular values 1/4, and the active
spectral relation D_z^* D_z U = U/8.
"""

from fractions import Fraction as F


D = 27


def epsilon(p, a, i):
    if len({p, a, i}) < 3:
        return 0
    inversions = sum(
        x > y
        for position, x in enumerate((p, a, i))
        for y in (p, a, i)[position + 1 :]
    )
    return -1 if inversions % 2 else 1


def zeros(rows, columns=None):
    columns = rows if columns is None else columns
    return [[F(0) for _ in range(columns)] for _ in range(rows)]


def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def matmul(left, right):
    right_t = transpose(right)
    return [
        [sum(x * y for x, y in zip(row, column)) for column in right_t]
        for row in left
    ]


def matvec(matrix, vector):
    return [sum(x * y for x, y in zip(row, vector)) for row in matrix]


def outer(left, right):
    return [[x * y for y in right] for x in left]


def subtract(left, right):
    return [
        [x - y for x, y in zip(left_row, right_row)]
        for left_row, right_row in zip(left, right)
    ]


def trace(matrix):
    return sum(matrix[i][i] for i in range(len(matrix)))


def frobenius_squared(matrix):
    return sum(value * value for row in matrix for value in row)


def rank(matrix):
    work = [row[:] for row in matrix]
    rows = len(work)
    columns = len(work[0]) if rows else 0
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(pivot_row, rows) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row:
                continue
            coefficient = work[row][column]
            if coefficient:
                work[row] = [
                    x - coefficient * y
                    for x, y in zip(work[row], work[pivot_row])
                ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def basis(index, dimension):
    out = [F(0)] * dimension
    out[index] = F(1)
    return out


def kron_vector(left, right):
    return [x * y for x in left for y in right]


def hodge_integer(z):
    """Return sum z_pqr E_p tensor E_q tensor E_r exactly."""
    out = zeros(D)
    for p in range(3):
        for q in range(3):
            for r in range(3):
                coefficient = z[9 * p + 3 * q + r]
                if not coefficient:
                    continue
                for a in range(3):
                    for b in range(3):
                        for c in range(3):
                            row = 9 * a + 3 * b + c
                            for i in range(3):
                                ep = epsilon(p, a, i)
                                if not ep:
                                    continue
                                for j in range(3):
                                    eq = epsilon(q, b, j)
                                    if not eq:
                                        continue
                                    for k in range(3):
                                        er = epsilon(r, c, k)
                                        if er:
                                            column = 9 * i + 3 * j + k
                                            out[row][column] += (
                                                coefficient * ep * eq * er
                                            )
    return out


def main():
    e0, e1, e2 = (basis(index, 3) for index in range(3))
    xi = [F(0)] * 9
    xi[0], xi[4] = F(3, 5), F(4, 5)
    q = [F(0)] * 9
    q[0], q[4] = F(4, 5), F(3, 5)
    z = kron_vector(e0, xi)
    u = kron_vector(e1, q)
    v = kron_vector(e2, q)

    assert sum(x * x for x in z) == 1
    assert sum(x * x for x in u) == 1
    assert sum(x * x for x in v) == 1
    assert sum(x * y for x, y in zip(u, v)) == 0

    d_integer = hodge_integer(z)
    w_integer = subtract(outer(u, v), outer(v, u))
    product = matmul(d_integer, w_integer)

    # W^* z = 0 and Tr(D_z W)=0; the omitted scalar factors are nonzero.
    assert matvec(transpose(w_integer), z) == [F(0)] * D
    assert trace(product) == 0

    # D_z W = product/4.
    assert frobenius_squared(product) / 16 == F(1, 8)
    assert matmul(product, product) == zeros(D)
    assert rank(product) == 2

    # D_z^*D_z = D_integer^T D_integer / 8.
    gram_integer = matmul(transpose(d_integer), d_integer)
    assert matvec(gram_integer, u) == u
    assert matvec(gram_integer, v) == v

    # N=D_zW has two nonzero squared singular values.  Rank two together
    # with these first two power sums proves that both are exactly 1/16.
    product_gram = matmul(transpose(product), product)
    product_gram_squared = matmul(product_gram, product_gram)
    assert trace(product_gram) / 16 == F(1, 8)
    assert trace(product_gram_squared) / 256 == F(1, 128)

    print("exact one-site-factor DTH equality certificate passed")
    print("support = Omega = 0")
    print("rank(D_z W) = 2, (D_z W)^2 = 0")
    print("singular values(D_z W) = 1/4, 1/4")
    print("||D_z W||_F^2 = 1/8")
    print("D_z^* D_z U = U/8")


if __name__ == "__main__":
    main()
