#!/usr/bin/env python3
"""Exact mixed-* consistency audit for the DTH five-replica obstruction.

Only the Python standard library is used.  The checker proves, in the local
[4,1] x [4,1] x [3,2] block, that

* the first-Pluecker source has dimension seven;
* xi and zeta have first-bivector flattening ranks 7 and 11;
* both have an explicit negative 2 x 2 principal minor after partial
  transpose on replicas 1,2; and
* no nonzero positive operator supported on this entire seven-dimensional
  source can have positive partial transpose.

Here \"block\" means the seven-dimensional binary highest-weight carrier.
The assertion does not exclude partial-transpose or support-map cancellation
through off-diagonal coherences with other carriers.

The last assertion is a 49-pivot rational certificate.  If a product-basis
coordinate is absent from the source, the corresponding diagonal entry of a
partially transposed supported density is zero.  Positivity then forces the
whole row to vanish.  Those exact row equations have full rank on all 7 x 7
coefficient matrices (even without Hermiticity).
"""

from fractions import Fraction as F
from itertools import combinations, permutations


LABELS = tuple(range(5))
EDGES = tuple(combinations(LABELS, 2))


def add(*vectors):
    out = {}
    for vector in vectors:
        for key, value in vector.items():
            out[key] = out.get(key, F(0)) + value
            if not out[key]:
                del out[key]
    return out


def scale(value, vector):
    value = F(value)
    return {key: value * coefficient for key, coefficient in vector.items()
            if value * coefficient}


def transposition(first, second):
    permutation = list(LABELS)
    permutation[first], permutation[second] = permutation[second], permutation[first]
    return tuple(permutation)


def sign(permutation):
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def point_f(index):
    return {index: F(1), 4: F(-1)}


def edge_r(a, b, c, d):
    out = {}
    for edge, coefficient in (
        ((a, c), 1), ((a, d), -1), ((b, c), -1), ((b, d), 1)
    ):
        edge = tuple(sorted(edge))
        out[edge] = out.get(edge, F(0)) + coefficient
        if not out[edge]:
            del out[edge]
    return out


def tensor3(first, second, third):
    return {
        (i, j, edge): x * y * z
        for i, x in first.items()
        for j, y in second.items()
        for edge, z in third.items()
        if x * y * z
    }


def apply_global_permutation(vector, permutation):
    out = {}
    for (i, j, edge), coefficient in vector.items():
        new_edge = tuple(sorted((permutation[edge[0]], permutation[edge[1]])))
        key = (permutation[i], permutation[j], new_edge)
        out[key] = out.get(key, F(0)) + coefficient
        if not out[key]:
            del out[key]
    return out


def antisymmetrize_first_four(vector):
    out = {}
    for permutation4 in permutations(range(4)):
        permutation = tuple(permutation4) + (4,)
        out = add(out, scale(F(sign(permutation4), 24),
                             apply_global_permutation(vector, permutation)))
    return out


def source_projector(vector):
    out = scale(F(1, 2), add(
        vector,
        scale(-1, apply_global_permutation(vector, transposition(0, 1))),
    ))
    out = scale(F(1, 2), add(
        out,
        scale(-1, apply_global_permutation(out, transposition(2, 3))),
    ))
    return scale(F(1, 2), add(
        out,
        apply_global_permutation(out, (2, 3, 0, 1, 4)),
    ))


def first_pluecker_projector(vector):
    # On the pair-antisymmetric, pair-symmetric source, A_4 is a subprojection.
    return add(source_projector(vector), scale(-1, antisymmetrize_first_four(vector)))


def reduce_and_insert(vector, pivots):
    """Insert a sparse row into an exact echelon basis."""
    vector = dict(vector)
    while vector:
        pivot = min(vector)
        if pivot not in pivots:
            coefficient = vector[pivot]
            pivots[pivot] = {
                key: value / coefficient for key, value in vector.items()
            }
            return True
        coefficient = vector[pivot]
        vector = add(vector, scale(-coefficient, pivots[pivot]))
    return False


def independent_indices(vectors):
    pivots = {}
    indices = []
    for index, vector in enumerate(vectors):
        if reduce_and_insert(vector, pivots):
            indices.append(index)
    return indices


R_BASIS = (
    edge_r(0, 1, 2, 3),
    edge_r(0, 1, 2, 4),
    edge_r(0, 2, 1, 3),
    edge_r(0, 2, 1, 4),
    edge_r(0, 3, 1, 4),
)


def build_block_basis():
    seeds = [
        first_pluecker_projector(tensor3(point_f(i), point_f(j), r))
        for i in range(4)
        for j in range(4)
        for r in R_BASIS
    ]
    return [seeds[index] for index in independent_indices(seeds)]


def jucys_five(vector):
    return add(*(
        apply_global_permutation(vector, transposition(replica, 4))
        for replica in range(4)
    ))


def build_xi():
    f0, f1, f2, f3 = (point_f(i) for i in range(4))
    r0123 = edge_r(0, 1, 2, 3)
    r0124 = edge_r(0, 1, 2, 4)
    r0423 = edge_r(0, 4, 2, 3)
    return add(
        scale(-1, add(tensor3(f1, f1, r0123), tensor3(f3, f3, r0123))),
        tensor3(f3, f3, r0124),
        scale(-1, tensor3(f2, f2, r0124)),
        tensor3(f1, f1, r0423),
        scale(-1, tensor3(f0, f0, r0423)),
    )


def replica_state(key, replica):
    i, j, edge = key
    return (int(replica == i), int(replica == j), int(replica in edge))


def flatten_rational(vector):
    rows = {}
    for key, coefficient in vector.items():
        row = tuple(replica_state(key, r) for r in (0, 1))
        column = tuple(replica_state(key, r) for r in (2, 3, 4))
        rows.setdefault(row, {})[column] = coefficient
    return rows


# Arithmetic in Q(sqrt(231)), represented by a+b sqrt(231).
ZERO_Q = (F(0), F(0))


def qadd(left, right):
    return (left[0] + right[0], left[1] + right[1])


def qneg(value):
    return (-value[0], -value[1])


def qmul(left, right):
    return (
        left[0] * right[0] + 231 * left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def qinv(value):
    denominator = value[0] ** 2 - 231 * value[1] ** 2
    assert denominator
    return (value[0] / denominator, -value[1] / denominator)


def quadratic_rank(rows):
    rows = [dict(row) for row in rows]
    pivots = {}
    rank = 0
    for row in rows:
        while row:
            pivot = min(row)
            if pivot not in pivots:
                inverse = qinv(row[pivot])
                row = {key: qmul(inverse, value) for key, value in row.items()}
                pivots[pivot] = row
                rank += 1
                break
            coefficient = row[pivot]
            correction = {
                key: qneg(qmul(coefficient, value))
                for key, value in pivots[pivot].items()
            }
            combined = dict(row)
            for key, value in correction.items():
                combined[key] = qadd(combined.get(key, ZERO_Q), value)
                if combined[key] == ZERO_Q:
                    del combined[key]
            row = combined
    return rank


def zeta_prime(xi_plus, xi_minus):
    # zeta' = sqrt(231) xi_+ + 11 xi_- = sqrt(11) zeta.
    return {
        key: (11 * xi_minus.get(key, F(0)), xi_plus.get(key, F(0)))
        for key in set(xi_plus) | set(xi_minus)
        if (11 * xi_minus.get(key, F(0)), xi_plus.get(key, F(0))) != ZERO_Q
    }


def flatten_quadratic(vector):
    rows = {}
    for key, coefficient in vector.items():
        row = tuple(replica_state(key, r) for r in (0, 1))
        column = tuple(replica_state(key, r) for r in (2, 3, 4))
        rows.setdefault(row, {})[column] = coefficient
    return rows


def coefficient_matrices(block_basis):
    matrices = []
    for vector in block_basis:
        matrix = {}
        for key, coefficient in vector.items():
            row = tuple(replica_state(key, r) for r in (0, 1))
            column = tuple(replica_state(key, r) for r in (2, 3, 4))
            matrix[row, column] = matrix.get((row, column), F(0)) + coefficient
        matrices.append(matrix)
    return matrices


def ppt_zero_diagonal_rank(matrices):
    """Rank of the forced PT-row equations on arbitrary 7 x 7 X."""
    dimension = len(matrices)
    rows = sorted({row for matrix in matrices for row, _ in matrix})
    columns = sorted({column for matrix in matrices for _, column in matrix})
    occupied = set().union(*(set(matrix) for matrix in matrices))
    absent = [
        (row, column)
        for row in rows
        for column in columns
        if (row, column) not in occupied
    ]

    pivots = {}
    generated = 0
    processed = 0
    for row, alpha in absent:
        # If p=(row,alpha) is absent, positivity of rho^Gamma forces
        # (rho^Gamma)_{p,q}=0 for every q=(other_row,beta).  Its coefficient
        # on X_ab is M_a(other_row,alpha) M_b(row,beta).
        left_vectors = []
        for other_row in rows:
            vector = {
                a: matrix.get((other_row, alpha), F(0))
                for a, matrix in enumerate(matrices)
                if matrix.get((other_row, alpha), F(0))
            }
            if vector:
                left_vectors.append(vector)
        right_vectors = []
        for beta in columns:
            vector = {
                b: matrix.get((row, beta), F(0))
                for b, matrix in enumerate(matrices)
                if matrix.get((row, beta), F(0))
            }
            if vector:
                right_vectors.append(vector)

        left_basis = [left_vectors[i] for i in independent_indices(left_vectors)]
        right_basis = [right_vectors[i] for i in independent_indices(right_vectors)]
        for left in left_basis:
            for right in right_basis:
                equation = {
                    (a, b): x * y
                    for a, x in left.items()
                    for b, y in right.items()
                    if x * y
                }
                generated += 1
                reduce_and_insert(equation, pivots)
        processed += 1
        if len(pivots) == dimension ** 2:
            break

    return {
        "rank": len(pivots),
        "rows": len(rows),
        "columns": len(columns),
        "occupied": len(occupied),
        "absent": len(absent),
        "processed": processed,
        "generated": generated,
    }


def main():
    block_basis = build_block_basis()
    assert len(block_basis) == 7
    for vector in block_basis:
        assert not antisymmetrize_first_four(vector)

    xi = build_xi()
    jxi = jucys_five(xi)
    xi_plus = scale(F(1, 2), add(xi, scale(F(1, 2), jxi)))
    xi_minus = scale(F(1, 2), add(xi, scale(F(-1, 2), jxi)))
    zeta = zeta_prime(xi_plus, xi_minus)

    xi_flat = flatten_rational(xi)
    xi_rank = len(independent_indices(list(xi_flat.values())))
    zeta_flat = flatten_quadratic(zeta)
    zeta_rank = quadratic_rank(list(zeta_flat.values()))
    assert xi_rank == 7
    assert zeta_rank == 11

    row0 = ((0, 0, 0), (0, 0, 1))
    row1 = ((0, 0, 0), (0, 1, 0))
    column0 = ((0, 0, 0), (0, 0, 1), (1, 1, 0))
    column1 = ((0, 0, 1), (0, 0, 0), (1, 0, 1))

    # On PT basis states (row0,column1),(row1,column0), both diagonal
    # entries vanish.  The displayed off-diagonal is nonzero.
    assert xi_flat.get(row0, {}).get(column1, F(0)) == 0
    assert xi_flat.get(row1, {}).get(column0, F(0)) == 0
    xi_off_diagonal = (
        xi_flat[row1][column1] * xi_flat[row0][column0]
    )
    assert xi_off_diagonal == -2
    assert -(xi_off_diagonal ** 2) == -4

    assert zeta_flat.get(row0, {}).get(column1, ZERO_Q) == ZERO_Q
    assert zeta_flat.get(row1, {}).get(column0, ZERO_Q) == ZERO_Q
    zeta_off_diagonal = qmul(
        zeta_flat[row1][column1], zeta_flat[row0][column0]
    )
    assert zeta_off_diagonal == (F(-165), F(-33, 4))
    zeta_minor = qneg(qmul(zeta_off_diagonal, zeta_off_diagonal))
    assert zeta_minor == (F(-687159, 16), F(-5445, 2))

    certificate = ppt_zero_diagonal_rank(coefficient_matrices(block_basis))
    assert certificate["rows"] == 30
    assert certificate["columns"] == 66
    assert certificate["occupied"] == 180
    assert certificate["absent"] == 1800
    assert certificate["rank"] == 49

    print("exact DTH mixed-* consistency audit")
    print("first-Pluecker local-block dimension = 7")
    print(f"rank_12:345(xi) = {xi_rank}")
    print(f"rank_12:345(zeta) = {zeta_rank}")
    print("xi PT principal minor = -4")
    print("zeta PT principal minor =")
    print("  -687159/16 - (5445/2) sqrt(231) < 0")
    print("block product grid = 30 x 66; occupied = 180; absent = 1800")
    print("forced zero-diagonal PT equations have rank 49 on M_7")
    print("there is no nonzero PPT density supported in this binary carrier")
    print("cross-carrier coherence cancellation is not tested")


if __name__ == "__main__":
    main()
