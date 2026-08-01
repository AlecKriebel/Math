#!/usr/bin/env python3
"""Dependency-free exact audit for the product-corner second blow-up.

The Hodge matrices are cleared of their fixed factor ``2 sqrt(2)``.  For

    z(t) = |000> + t delta + t^2 eta

the script constructs the Feshbach expansion of the eight eigenvalues that
converge to one.  It audits the real quartic Gram form for three canonical
zero-Hessian directions: a rank-one single edge, two compatible Bell edges,
and three compatible Bell edges.  All scalars lie in Q(i), represented below
as pairs of ``Fraction`` objects.
"""

from fractions import Fraction as F
from itertools import product


N = 27
PIND = [9 * i + 3 * j + k for i, j, k in product((1, 2), repeat=3)]
QIND = [i for i in range(N) if i not in PIND]
ZERO = (F(0), F(0))
ONE = (F(1), F(0))
IUNIT = (F(0), F(1))


def g(value=0, imag=0):
    return (F(value), F(imag))


def ga(x, y):
    return (x[0] + y[0], x[1] + y[1])


def gn(x):
    return (-x[0], -x[1])


def gm(x, y):
    return (x[0] * y[0] - x[1] * y[1],
            x[0] * y[1] + x[1] * y[0])


def gc(x):
    return (x[0], -x[1])


def gs(q, x):
    return (q * x[0], q * x[1])


def epsilon(p, a, i):
    positive = ((0, 1, 2), (1, 2, 0), (2, 0, 1))
    negative = ((0, 2, 1), (2, 1, 0), (1, 0, 2))
    return int((p, a, i) in positive) - int((p, a, i) in negative)


def sp_clean(a):
    return {key: value for key, value in a.items() if value != ZERO}


def sp_add(*matrices):
    out = {}
    for matrix in matrices:
        for key, value in matrix.items():
            out[key] = ga(out.get(key, ZERO), value)
    return sp_clean(out)


def sp_scale(q, a):
    return sp_clean({key: gs(q, value) for key, value in a.items()})


def sp_adj(a):
    return {(j, i): gc(value) for (i, j), value in a.items()}


def sp_mul(a, b):
    by_row = {}
    for (k, j), value in b.items():
        by_row.setdefault(k, []).append((j, value))
    out = {}
    for (i, k), x in a.items():
        for j, y in by_row.get(k, ()):
            key = (i, j)
            out[key] = ga(out.get(key, ZERO), gm(x, y))
    return sp_clean(out)


def sp_trace(a, n):
    out = ZERO
    for i in range(n):
        out = ga(out, a.get((i, i), ZERO))
    return out


def sp_eye(n):
    return {(i, i): ONE for i in range(n)}


def sp_block(a, rows, columns):
    row_index = {old: new for new, old in enumerate(rows)}
    col_index = {old: new for new, old in enumerate(columns)}
    return {(row_index[i], col_index[j]): value
            for (i, j), value in a.items()
            if i in row_index and j in col_index}


def dense_real(a, n):
    out = [[F(0) for _ in range(n)] for _ in range(n)]
    for (i, j), value in a.items():
        assert value[1] == 0
        out[i][j] = value[0]
    return out


def hodge(index, coefficient=ONE):
    p, q, r = index
    out = {}
    for aa, bb, cc, ii, jj, kk in product(range(3), repeat=6):
        value = (epsilon(p, aa, ii) * epsilon(q, bb, jj)
                 * epsilon(r, cc, kk))
        if value:
            out[9 * aa + 3 * bb + cc, 9 * ii + 3 * jj + kk] = (
                gs(F(value), coefficient)
            )
    return out


DBASIS = [hodge(idx) for idx in product(range(3), repeat=3)]


def dmat(vector):
    terms = []
    for index, coefficient in vector.items():
        if coefficient != ZERO:
            terms.append({key: gm(coefficient, value)
                          for key, value in DBASIS[index].items()})
    return sp_add(*terms) if terms else {}


def vector(entries, imaginary=False):
    unit = IUNIT if imaginary else ONE
    return {9 * i + 3 * j + k: gs(F(value), unit)
            for (i, j, k), value in entries.items() if value}


def vadd(left, right, sign=1):
    out = dict(left)
    for key, value in right.items():
        out[key] = ga(out.get(key, ZERO), gs(F(sign), value))
        if out[key] == ZERO:
            del out[key]
    return out


def vnorm2(vector_):
    return sum(x[0] * x[0] + x[1] * x[1] for x in vector_.values())


def matrix_poly(a, coefficients, n):
    """Evaluate sum coefficients[k] a^k for real sparse ``a``."""
    out = {}
    power_a = sp_eye(n)
    for coefficient in coefficients:
        out = sp_add(out, sp_scale(coefficient, power_a))
        power_a = sp_mul(power_a, a)
    return out


def fixed_data(delta, case):
    d0 = DBASIS[0]
    d1 = dmat(delta)
    s1 = sp_add(sp_mul(sp_adj(d0), d1), sp_mul(sp_adj(d1), d0))
    s2 = sp_mul(sp_adj(d1), d1)
    b1 = sp_block(s1, PIND, QIND)
    b2_straight = sp_block(s2, PIND, QIND)
    assert sp_mul(b1, sp_adj(b2_straight)) == {}
    assert sp_mul(b2_straight, sp_adj(b1)) == {}
    h2 = sp_add(sp_block(s2, PIND, PIND), sp_mul(b1, sp_adj(b1)))

    # In every smooth zero-cone chart audited here, h2 has rank four and
    # spectrum {0^4,x^2,y^2}, allowing x=y.  Its range projector and
    # Moore--Penrose inverse are rational polynomials in h2.  This avoids
    # eigenvectors and square roots, even for unequal edge amplitudes.
    trace_h = sp_trace(h2, 8)
    trace_h2 = sp_trace(sp_mul(h2, h2), 8)
    assert trace_h[1] == trace_h2[1] == 0
    sigma = trace_h[0] / 2
    product_xy = (sigma * sigma - trace_h2[0] / 2) / 2
    assert product_xy > 0
    projector = sp_scale(F(1, 1) / product_xy, sp_mul(
        h2, sp_add(sp_scale(sigma, sp_eye(8)), sp_scale(F(-1), h2))))
    inverse = sp_scale(F(1, 1) / product_xy,
                       sp_add(sp_scale(sigma, projector), sp_scale(F(-1), h2)))

    complement = sp_add(sp_eye(8), sp_scale(F(-1), projector))
    assert sp_mul(projector, projector) == projector
    assert sp_mul(projector, complement) == {}
    return d0, d1, b1, h2, projector, complement, inverse


def audit_straight_cubic_zero(delta):
    d0 = DBASIS[0]
    d1 = dmat(delta)
    s1 = sp_add(sp_mul(sp_adj(d0), d1), sp_mul(sp_adj(d1), d0))
    s2 = sp_mul(sp_adj(d1), d1)
    b1 = sp_block(s1, PIND, QIND)
    b2 = sp_block(s2, PIND, QIND)
    assert sp_mul(b1, sp_adj(b2)) == {}
    assert sp_mul(b2, sp_adj(b1)) == {}


def audit_scaled_single_tie(delta):
    """Audit all two-plane choices in the sixfold tied H2 space."""
    d0 = DBASIS[0]
    d1 = dmat(delta)
    s1 = sp_add(sp_mul(sp_adj(d0), d1), sp_mul(sp_adj(d1), d0))
    s2 = sp_mul(sp_adj(d1), d1)
    b1 = sp_block(s1, PIND, QIND)
    b2 = sp_block(s2, PIND, QIND)
    c2 = sp_block(s2, QIND, QIND)
    h2 = sp_add(sp_block(s2, PIND, PIND), sp_mul(b1, sp_adj(b1)))
    assert sp_mul(h2, h2) == sp_scale(F(4), h2)
    assert rank_rational(dense_real(h2, 8)) == 2
    positive = sp_scale(F(1, 4), h2)
    tied = sp_add(sp_eye(8), sp_scale(F(-1), positive))
    h40 = sp_add(sp_mul(b2, sp_adj(b2)),
                 sp_mul(sp_mul(b1, c2), sp_adj(b1)))
    # The fourth operator is zero on all six tied directions, so every
    # possible extra two-plane gives the same quartic trace.
    assert sp_mul(tied, sp_mul(h40, tied)) == {}
    bgram = sp_mul(b1, sp_adj(b1))
    value = sp_trace(sp_mul(positive, sp_add(
        h40, sp_scale(F(-1), sp_mul(h2, bgram)))), 8)
    assert value == g(-8)


def quartic_value(delta, eta, case, data=None):
    if data is None:
        data = fixed_data(delta, case)
    d0, d1, b1, h2, projector, complement, inverse = data
    d2 = dmat(eta)
    s2 = sp_add(sp_mul(sp_adj(d1), d1),
                sp_mul(sp_adj(d0), d2), sp_mul(sp_adj(d2), d0))
    s3 = sp_add(sp_mul(sp_adj(d1), d2), sp_mul(sp_adj(d2), d1))
    s4 = sp_mul(sp_adj(d2), d2)
    a3 = sp_block(s3, PIND, PIND)
    a4 = sp_block(s4, PIND, PIND)
    b2 = sp_block(s2, PIND, QIND)
    b3 = sp_block(s3, PIND, QIND)
    c2 = sp_block(s2, QIND, QIND)
    h3 = sp_add(a3, sp_mul(b1, sp_adj(b2)), sp_mul(b2, sp_adj(b1)))
    h40 = sp_add(
        a4, sp_mul(b2, sp_adj(b2)), sp_mul(b1, sp_adj(b3)),
        sp_mul(b3, sp_adj(b1)), sp_mul(sp_mul(b1, c2), sp_adj(b1)),
    )
    bgram = sp_mul(b1, sp_adj(b1))
    eigenvalue_term = sp_mul(h2, bgram)
    direct = sp_trace(sp_mul(projector,
                             sp_add(h40, sp_scale(F(-1), eigenvalue_term))), 8)
    mixing = sp_trace(sp_mul(inverse, sp_mul(h3, sp_mul(
        complement, sp_mul(h3, projector)))), 8)
    coefficient = ga(direct, mixing)
    assert coefficient[1] == 0
    return 4 * vnorm2(eta) - coefficient[0]


def real_basis():
    coordinates = [9 * i + 3 * j + k
                   for i, j, k in product(range(3), repeat=3)
                   if sum(x != 0 for x in (i, j, k)) >= 2]
    out = []
    for coordinate in coordinates:
        out.append({coordinate: ONE})
        out.append({coordinate: IUNIT})
    assert len(out) == 40
    return out


def gram_matrix(delta, case):
    basis = real_basis()
    data = fixed_data(delta, case)
    q0 = quartic_value(delta, {}, case, data)
    diagonal = []
    for v in basis:
        qp = quartic_value(delta, v, case, data)
        qm = quartic_value(delta, vadd({}, v, -1), case, data)
        assert qp == qm
        diagonal.append(qp - q0)
    matrix = [[F(0) for _ in basis] for _ in basis]
    for i in range(len(basis)):
        matrix[i][i] = diagonal[i]
        for j in range(i):
            qsum = quartic_value(delta, vadd(basis[i], basis[j]), case, data)
            value = (qsum - q0 - diagonal[i] - diagonal[j]) / 2
            matrix[i][j] = matrix[j][i] = value
    return q0, matrix


def dense_mul(a, b):
    bt = list(zip(*b))
    return [[sum(x * y for x, y in zip(row, column))
             for column in bt] for row in a]


def dense_add(a, b, factor=F(1)):
    return [[x + factor * y for x, y in zip(ra, rb)]
            for ra, rb in zip(a, b)]


def dense_eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def dense_poly_zero(matrix, roots):
    n = len(matrix)
    value = dense_eye(n)
    identity = dense_eye(n)
    for root in roots:
        value = dense_mul(value, dense_add(matrix, identity, -root))
    return all(not x for row in value for x in row)


def rank_rational(matrix):
    a = [row[:] for row in matrix]
    pivot = 0
    for column in range(len(a[0])):
        row = next((i for i in range(pivot, len(a)) if a[i][column]), None)
        if row is None:
            continue
        a[pivot], a[row] = a[row], a[pivot]
        scale = a[pivot][column]
        a[pivot] = [x / scale for x in a[pivot]]
        for i in range(len(a)):
            if i != pivot and a[i][column]:
                scale = a[i][column]
                a[i] = [x - scale * y for x, y in zip(a[i], a[pivot])]
        pivot += 1
    return pivot


def audit_case(label, delta, expected_q0, roots, multiplicities,
               same_edge_kernel=False):
    q0, gram = gram_matrix(delta, label)
    assert q0 == F(expected_q0)
    assert gram == [list(row) for row in zip(*gram)]
    assert dense_poly_zero(gram, tuple(F(x) for x in roots))
    identity = dense_eye(len(gram))
    actual = tuple(len(gram) - rank_rational(dense_add(
        gram, identity, -F(root))) for root in roots)
    assert actual == multiplicities
    if same_edge_kernel:
        # The eight real kernel coordinates are precisely the four complex
        # coefficients eta_{ij0}, i,j in {1,2}, on the same edge as delta.
        basis_coordinates = [9 * i + 3 * j + k
                             for i, j, k in product(range(3), repeat=3)
                             if sum(x != 0 for x in (i, j, k)) >= 2
                             for _ in (0, 1)]
        same_edge = {9 * i + 3 * j for i, j in product((1, 2), repeat=2)}
        for index, coordinate in enumerate(basis_coordinates):
            zero_row = all(not x for x in gram[index])
            assert zero_row == (coordinate in same_edge)
    print(label, "straight quartic", q0, "multiplicities", actual,
          "at Gram roots", roots)


def expected_single_gram():
    coordinates = [(i, j, k)
                   for i, j, k in product(range(3), repeat=3)
                   if sum(x != 0 for x in (i, j, k)) >= 2
                   for _ in (0, 1)]
    diagonal = []
    for i, j, k in coordinates:
        if k == 0:
            value = F(0)               # the same 12 edge
        elif i == 0 or j == 0:
            value = F(2)               # the 13 and 23 edges
        else:
            value = F(2 if i == j else 4)
        diagonal.append(value)
    return [[diagonal[i] if i == j else F(0)
             for j in range(40)] for i in range(40)]


def audit_single_amplitude_interpolation():
    """Prove the universal single-edge Gram by exact interpolation.

    Put the singular values at (a,1).  After clearing the fourth power of
    pi=(a^2-1)^2 from the rational projector formula, every difference
    between an actual Gram entry and the claimed constant has degree at
    most 20 in a.  Twenty-one exact nonsingular values therefore prove the
    polynomial identity.  The degree accounting is recorded in the note.
    """
    expected = expected_single_gram()
    values = [0] + list(range(2, 22))
    assert len(values) == 21
    for amplitude in values:
        delta = vector({(1, 1, 0): amplitude, (2, 2, 0): 1})
        q0, gram = gram_matrix(delta, "single_interpolation")
        assert q0 == 8 * amplitude * amplitude
        assert gram == expected
    print("single-edge rational identity interpolated at 21 exact values")


def main():
    rank_one = vector({(1, 1, 0): 1})
    two_edges = vector({(1, 1, 0): 1, (2, 2, 0): 1,
                        (1, 0, 1): 1, (2, 0, 2): 1})
    three_edges = vector({(1, 1, 0): 1, (2, 2, 0): 1,
                          (1, 0, 1): 1, (2, 0, 2): 1,
                          (0, 1, 2): 1, (0, 2, 1): -1})
    single_generic = vector({(1, 1, 0): 2, (2, 2, 0): 1})
    two_unequal = vector({(1, 1, 0): 2, (2, 2, 0): 2,
                          (1, 0, 1): 1, (2, 0, 2): 1})
    three_unequal = vector({(1, 1, 0): 3, (2, 2, 0): 3,
                            (1, 0, 1): 1, (2, 0, 2): 1,
                            (0, 1, 2): 2, (0, 2, 1): -2})
    # One dense complex slice vector audits the support-parity H3=0 identity
    # without imposing any zero-cone relations.
    dense = {}
    for serial, (i, j, k) in enumerate(product(range(3), repeat=3)):
        if sum(x != 0 for x in (i, j, k)) >= 2:
            dense[9 * i + 3 * j + k] = g(serial + 1, 2 * serial - 3)
    audit_straight_cubic_zero(dense)
    scaled_tie = vector({(1, 1, 0): 1, (2, 2, 0): 1})
    audit_scaled_single_tie(scaled_tie)
    audit_single_amplitude_interpolation()
    audit_case("rank_one", rank_one, 0, (0, 2, 4), (8, 24, 8), True)
    audit_case("single_generic", single_generic, 32,
               (0, 2, 4), (8, 24, 8))
    audit_case("two_edges", two_edges, 20,
               (0, 2, F(8, 3), 4), (12, 8, 12, 8))
    audit_case("two_unequal", two_unequal, 152,
               (0, 2, F(8, 3), 4), (12, 8, 12, 8))
    audit_case("three_edges", three_edges, 36,
               (0, 2, F(8, 3), 4), (12, 8, 12, 8))
    audit_case("three_unequal", three_unequal, 980,
               (0, 2, F(8, 3), 4), (12, 8, 12, 8))
    print("exact curved product-corner Feshbach audit passed")


if __name__ == "__main__":
    main()
