#!/usr/bin/env python3
"""Exact sparse-rational Hessian audit at a generic DTH equality point.

The calculation reconstructs the isolated-cluster second variation of

    Phi(z) = (1/2) sum_{j=1}^4 s_j(D_z)^2

at z=e0 tensor (3|00>+4|11>)/5.  Every operation uses ``Fraction``;
the fixed square roots in the Hodge matrices have been cleared.  Sparse
dictionaries keep the dependency-free audit small and fast.
"""

from fractions import Fraction as F


N = 27
S = F(3, 5)
T = F(4, 5)


def epsilon(p, a, i):
    positive = ((0, 1, 2), (1, 2, 0), (2, 0, 1))
    negative = ((0, 2, 1), (2, 1, 0), (1, 0, 2))
    return int((p, a, i) in positive) - int((p, a, i) in negative)


def sp_add(*matrices):
    out = {}
    for matrix in matrices:
        for key, value in matrix.items():
            out[key] = out.get(key, F(0)) + value
            if not out[key]:
                del out[key]
    return out


def sp_scale(value, matrix):
    return {key: value * entry for key, entry in matrix.items() if value * entry}


def sp_transpose(matrix):
    return {(j, i): value for (i, j), value in matrix.items()}


def sp_mul(left, right):
    by_row = {}
    for (k, j), value in right.items():
        by_row.setdefault(k, []).append((j, value))
    out = {}
    for (i, k), x in left.items():
        for j, y in by_row.get(k, ()):
            out[i, j] = out.get((i, j), F(0)) + x * y
    return {key: value for key, value in out.items() if value}


def sp_trace(matrix):
    return sum(matrix.get((i, i), F(0)) for i in range(N))


def sp_identity():
    return {(i, i): F(1) for i in range(N)}


def sp_outer(left, right, row_offset=0, column_offset=0):
    return {
        (row_offset + i, column_offset + j): x * y
        for i, x in enumerate(left)
        for j, y in enumerate(right)
        if x and y
    }


def hodge_integer(z):
    """Return Dhat_z=(2 sqrt(2))D_z as a sparse rational matrix."""
    out = {}
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
                                            key = (row, 9 * i + 3 * j + k)
                                            out[key] = out.get(key, F(0)) + (
                                                coefficient * ep * eq * er
                                            )
    return {key: value for key, value in out.items() if value}


def coordinate(index):
    vector = [F(0)] * N
    vector[index] = F(1)
    return vector


def tangent_basis():
    """An orthonormal complex basis of z0-perp, with semantic labels."""
    out = []
    q_perp = [F(0)] * N
    q_perp[0], q_perp[4] = T, -S
    out.append(("slice0_qperp", q_perp))
    for rest in (1, 2, 3, 5, 6, 7, 8):
        out.append((f"slice0_{rest}", coordinate(rest)))
    for local in (1, 2):
        offset = 9 * local
        xi = [F(0)] * N
        xi[offset], xi[offset + 4] = S, T
        out.append((f"slice{local}_xi", xi))
        q_perp = [F(0)] * N
        q_perp[offset], q_perp[offset + 4] = T, -S
        out.append((f"slice{local}_qperp", q_perp))
        for rest in (1, 2, 3, 5, 6, 7, 8):
            out.append((f"slice{local}_{rest}", coordinate(offset + rest)))
    assert len(out) == 26
    for i, (_, left) in enumerate(out):
        for j, (_, right) in enumerate(out):
            assert sum(x * y for x, y in zip(left, right)) == F(i == j)
    return out


def expected(label):
    if label.startswith("slice0_"):
        return -S * S * T * T / 2 if label == "slice0_8" else F(0)
    if label.endswith("_xi"):
        return F(0)
    if label.endswith("_qperp"):
        return F(-1, 8)
    rest = int(label.rsplit("_", 1)[1])
    if rest in (1, 3, 8):
        return F(-1, 8)
    if rest in (2, 6):
        return -(3 + T * T - S * S) / 16
    if rest in (5, 7):
        return -(3 + S * S - T * T) / 16
    raise AssertionError(label)


def trace_product(*matrices):
    product = matrices[0]
    for matrix in matrices[1:]:
        product = sp_mul(product, matrix)
    return sp_trace(product)


def main():
    z0 = [F(0)] * N
    z0[0], z0[4] = S, T
    d0 = hodge_integer(z0)
    s0 = sp_scale(F(1, 8), sp_mul(sp_transpose(d0), d0))

    # Top projector: e0-perp tensor span{4E00/5+3E11/5,E22}.
    q = [F(0)] * 9
    q[0], q[4] = T, S
    r = [F(0)] * 9
    r[8] = F(1)
    rest_p = sp_add(sp_outer(q, q), sp_outer(r, r))
    projector = {}
    for local in (1, 2):
        projector = sp_add(
            projector,
            {(9 * local + i, 9 * local + j): value
             for (i, j), value in rest_p.items()},
        )
    assert sp_mul(projector, projector) == projector
    assert sp_trace(projector) == 4
    assert sp_mul(s0, projector) == sp_scale(F(1, 8), projector)

    # Exact reduced resolvent Q(1/8-S0)^(-1)Q from product eigenspaces.
    q0 = [F(0)] * 9
    q0[0], q0[4] = S, -T
    rest_r = sp_scale(8, sp_outer(q0, q0))
    for index in (1, 3):
        rest_r[index, index] = F(8)
    for index in (5, 7):
        rest_r[index, index] = F(8) / (T * T)
    for index in (2, 6):
        rest_r[index, index] = F(8) / (S * S)
    resolvent = {(i, i): F(8) for i in range(9)}
    for local in (1, 2):
        resolvent = sp_add(
            resolvent,
            {(9 * local + i, 9 * local + j): value
             for (i, j), value in rest_r.items()},
        )
    assert not sp_mul(projector, resolvent)
    denominator = sp_add(sp_scale(F(1, 8), sp_identity()), sp_scale(-1, s0))
    complement = sp_add(sp_identity(), sp_scale(-1, projector))
    assert sp_mul(denominator, resolvent) == complement

    tangent = tangent_basis()
    images = [hodge_integer(vector) for _, vector in tangent]
    variations = [
        sp_scale(
            F(1, 8),
            sp_add(sp_mul(sp_transpose(d0), image),
                   sp_mul(sp_transpose(image), d0)),
        )
        for image in images
    ]

    hessian = [[F(0) for _ in range(26)] for _ in range(26)]
    for i in range(26):
        for j in range(i, 26):
            # Polarization of
            # q=1/2 Tr(P E*E)-||delta||^2/4+1/2 Tr(P S1 R S1).
            kij = trace_product(projector, sp_transpose(images[i]), images[j]) / 8
            kji = trace_product(projector, sp_transpose(images[j]), images[i]) / 8
            kinetic = (kij + kji) / 4
            normalization = F(-1, 4) if i == j else F(0)
            mij = trace_product(projector, variations[i], resolvent, variations[j])
            mji = trace_product(projector, variations[j], resolvent, variations[i])
            value = kinetic + normalization + (mij + mji) / 4
            hessian[i][j] = hessian[j][i] = value

    for i, (label, _) in enumerate(tangent):
        assert hessian[i][i] == expected(label), (
            label, hessian[i][i], expected(label)
        )
        assert all(not hessian[i][j] for j in range(26) if i != j)

    multiplicities = {}
    for i in range(26):
        value = hessian[i][i]
        multiplicities[value] = multiplicities.get(value, 0) + 1
    assert multiplicities == {
        F(0): 9,
        F(-72, 625): 1,
        F(-1, 8): 8,
        F(-41, 200): 4,
        F(-17, 100): 4,
    }
    print("exact factor-equality Ky-Fan Hessian certificate passed")
    print("complex projective kernel dimension: 9")
    print("negative complex normal dimension: 17")
    print("real-sphere kernel/negative dimensions: 19/34")


if __name__ == "__main__":
    main()
