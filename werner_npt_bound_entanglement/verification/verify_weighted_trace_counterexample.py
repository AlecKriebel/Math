#!/usr/bin/env python3
"""Exact audit of the positive weighted-kernel-trace example.

Only the standard library and arithmetic in Q(sqrt(5),sqrt(6)) are
used.  The code reconstructs the whitened rank-two operator from the
three columns of the row isometry, checks its compression kernel, and
contracts the four-copy endpoint Hessian directly.
"""

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations


@dataclass(frozen=True)
class Q:
    """a + b sqrt(5) + c sqrt(6) + d sqrt(30)."""

    a: Fraction = Fraction(0)
    b: Fraction = Fraction(0)
    c: Fraction = Fraction(0)
    d: Fraction = Fraction(0)

    def __add__(self, other):
        other = q(other)
        return Q(
            self.a + other.a,
            self.b + other.b,
            self.c + other.c,
            self.d + other.d,
        )

    __radd__ = __add__

    def __neg__(self):
        return Q(-self.a, -self.b, -self.c, -self.d)

    def __sub__(self, other):
        return self + (-q(other))

    def __rsub__(self, other):
        return q(other) - self

    def __mul__(self, other):
        other = q(other)
        a, b, c, d = self.a, self.b, self.c, self.d
        e, f, g, h = other.a, other.b, other.c, other.d
        return Q(
            a * e + 5 * b * f + 6 * c * g + 30 * d * h,
            a * f + b * e + 6 * c * h + 6 * d * g,
            a * g + c * e + 5 * b * h + 5 * d * f,
            a * h + d * e + b * g + c * f,
        )

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        scalar = Fraction(scalar)
        return Q(
            self.a / scalar,
            self.b / scalar,
            self.c / scalar,
            self.d / scalar,
        )


def q(value):
    if isinstance(value, Q):
        return value
    return Q(Fraction(value))


@dataclass(frozen=True)
class QC:
    re: Q = Q()
    im: Q = Q()

    def __add__(self, other):
        other = qc(other)
        return QC(self.re + other.re, self.im + other.im)

    __radd__ = __add__

    def __neg__(self):
        return QC(-self.re, -self.im)

    def __sub__(self, other):
        return self + (-qc(other))

    def __rsub__(self, other):
        return qc(other) - self

    def __mul__(self, other):
        other = qc(other)
        return QC(
            self.re * other.re - self.im * other.im,
            self.re * other.im + self.im * other.re,
        )

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        return QC(self.re / scalar, self.im / scalar)

    def conj(self):
        return QC(self.re, -self.im)


def qc(value):
    if isinstance(value, QC):
        return value
    return QC(q(value))


ZERO = QC()
ONE = QC(q(1))
I = QC(Q(), q(1))
SQRT5 = Q(b=Fraction(1))
SQRT6 = Q(c=Fraction(1))
SQRT30 = Q(d=Fraction(1))


def add_entry(matrix, key, value):
    value = qc(value)
    if value == ZERO:
        return
    new_value = matrix.get(key, ZERO) + value
    if new_value == ZERO:
        matrix.pop(key, None)
    else:
        matrix[key] = new_value


def outer(left, right):
    out = {}
    for row, a in left.items():
        for col, b in right.items():
            add_entry(out, (row, col), a * b.conj())
    return out


def add_matrix(left, right):
    out = dict(left)
    for key, value in right.items():
        add_entry(out, key, value)
    return out


def partial_trace(matrix, kept):
    kept = tuple(kept)
    traced = tuple(site for site in range(4) if site not in kept)
    out = {}
    for (row, col), value in matrix.items():
        if all(row[site] == col[site] for site in traced):
            r = tuple(row[site] for site in kept)
            c = tuple(col[site] for site in kept)
            add_entry(out, (r, c), value)
    return out


def partial_trace_n(matrix, kept, party_count):
    kept = tuple(kept)
    traced = tuple(site for site in range(party_count) if site not in kept)
    out = {}
    for (row, col), value in matrix.items():
        if all(row[site] == col[site] for site in traced):
            r = tuple(row[site] for site in kept)
            c = tuple(col[site] for site in kept)
            add_entry(out, (r, c), value)
    return out


def trace_product(left, right):
    return sum(
        (
            value * right.get((col, row), ZERO)
            for (row, col), value in left.items()
        ),
        ZERO,
    )


def right_local_multiply(matrix, local):
    out = {}
    for (row, middle), value in matrix.items():
        for (source, target), coefficient in local.items():
            if source != middle[0]:
                continue
            col = list(middle)
            col[0] = target
            add_entry(out, (row, tuple(col)), value * coefficient)
    return out


def hessian(left, right):
    p_left = right_local_multiply(P_HAT, left)
    p_right = right_local_multiply(P_HAT, right)
    value = ZERO
    for size in range(5):
        coefficient = Fraction(-1, 2) ** (4 - size)
        for kept in combinations(range(4), size):
            value += coefficient * trace_product(
                partial_trace(p_left, kept),
                partial_trace(p_right, kept),
            )
    return value


def local_matrix(diagonal=(), entries=()):
    out = {}
    for index, value in enumerate(diagonal):
        add_entry(out, (index, index), value)
    for row, col, value in entries:
        add_entry(out, (row, col), value)
    return out


def compression(local):
    out = [[ZERO, ZERO], [ZERO, ZERO]]
    for a, left in enumerate((U0, U1)):
        for b, right in enumerate((U0, U1)):
            value = ZERO
            for row, x in left.items():
                for col, y in right.items():
                    if row[1:] == col[1:]:
                        value += (
                            x.conj()
                            * local.get((row[0], col[0]), ZERO)
                            * y
                        )
            out[a][b] = value
    return out


def map_product(left, right):
    """Return left right^* for sparse maps with two columns."""

    out = {}
    for column in range(2):
        for row, value in left.items():
            if row[1] != column:
                continue
            for col, coefficient in right.items():
                if col[1] == column:
                    add_entry(
                        out,
                        (row[0], col[0]),
                        value * coefficient.conj(),
                    )
    return out


def phi3_pairing(left, right):
    value = ZERO
    for size in range(4):
        coefficient = Fraction(-1, 2) ** (3 - size)
        for kept in combinations(range(3), size):
            value += coefficient * trace_product(
                partial_trace_n(left, kept, 3),
                partial_trace_n(right, kept, 3),
            )
    return value


# The row isometry W has columns
# (2,-1,0,0)/sqrt(5), (1,2,-5,0)/sqrt(30), (0,0,0,1)
# on output basis (122,1), (220,0), (220,1), (212,0).
# Reshaping its qubit index gives the two columns below.
U0 = {
    (0, 2, 2, 0): QC(-SQRT5 / 5),
    (1, 2, 2, 0): QC(SQRT30 / 15),
    (2, 2, 1, 2): ONE,
}
U1 = {
    (0, 1, 2, 2): QC(2 * SQRT5 / 5),
    (1, 1, 2, 2): QC(SQRT30 / 30),
    (1, 2, 2, 0): QC(-SQRT30 / 6),
}
P_HAT = add_matrix(outer(U0, U0), outer(U1, U1))

A0 = local_matrix(
    diagonal=(-17, 12, 5),
    entries=((0, 1, 4 * SQRT6), (1, 0, 4 * SQRT6)),
)
X02 = local_matrix(entries=((0, 2, 1), (2, 0, 1)))
Y02 = local_matrix(entries=((0, 2, -I), (2, 0, I)))
X12 = local_matrix(entries=((1, 2, 1), (2, 1, 1)))
Y12 = local_matrix(entries=((1, 2, -I), (2, 1, I)))
KERNEL = (A0, X02, Y02, X12, Y12)

R = local_matrix(
    diagonal=(Fraction(13, 24), Fraction(1, 2), Fraction(23, 24)),
    entries=((0, 1, SQRT6 / 6), (1, 0, SQRT6 / 6)),
)
R_CRIT = local_matrix(
    diagonal=(Fraction(29, 30), Fraction(1, 5), Fraction(5, 6)),
    entries=((0, 1, SQRT6 / 15), (1, 0, SQRT6 / 15)),
)

# Exact counterexample to the tempting pointwise rank-one-kernel sign.
# Sparse map keys are ((physical triple), logical column).
PHYSICAL_BASIS = (
    (2, 1, 2),
    (2, 0, 2),
    (2, 2, 1),
    (0, 1, 1),
)
V_MAP = {
    (PHYSICAL_BASIS[row], column): qc(value)
    for row, values in enumerate(((-2, 1), (1, 0), (-4, 2), (-4, 2)))
    for column, value in enumerate(values)
    if value
}
W_MAP = {
    (PHYSICAL_BASIS[row], column): qc(value)
    for row, values in enumerate(((4, 6), (0, 0), (0, -2), (-2, -1)))
    for column, value in enumerate(values)
    if value
}


def main():
    # V^*W=0 entry by entry.
    for left_column in range(2):
        for right_column in range(2):
            overlap = sum(
                (
                    V_MAP.get((basis, left_column), ZERO).conj()
                    * W_MAP.get((basis, right_column), ZERO)
                    for basis in PHYSICAL_BASIS
                ),
                ZERO,
            )
            assert overlap == ZERO

    h_v = map_product(V_MAP, V_MAP)
    h_w = map_product(W_MAP, W_MAP)
    b_wv = map_product(W_MAP, V_MAP)
    b_vw = map_product(V_MAP, W_MAP)
    cross_positive = phi3_pairing(h_v, h_w)
    coherent = phi3_pairing(b_wv, b_vw)
    assert cross_positive == qc(Fraction(233, 2))
    assert coherent == qc(Fraction(113, 2))
    assert (
        (cross_positive - coherent / 2) / (46 * 61)
        == qc(Fraction(353, 11224))
    )

    for basis_element in KERNEL:
        assert compression(basis_element) == [
            [ZERO, ZERO],
            [ZERO, ZERO],
        ]

    assert compression(R) == [[ONE, ZERO], [ZERO, ONE]]
    assert Fraction(13, 24) * Fraction(1, 2) - Fraction(1, 6) == Fraction(5, 48)

    expected_diagonal = (
        Fraction(-375, 4),
        Fraction(3, 20),
        Fraction(3, 20),
        Fraction(11, 60),
        Fraction(11, 60),
    )
    norms = (650, 2, 2, 2, 2)
    for basis_element, expected in zip(KERNEL, expected_diagonal):
        assert hessian(basis_element, basis_element) == qc(expected)

    assert hessian(X02, X12) == QC(SQRT6 / 30)
    assert hessian(Y02, Y12) == QC(SQRT6 / 30)
    assert hessian(A0, X02) == ZERO
    assert hessian(A0, Y02) == ZERO
    assert hessian(A0, X12) == ZERO
    assert hessian(A0, Y12) == ZERO

    weighted_trace = sum(
        (
            hessian(basis_element, basis_element) / norm
            for basis_element, norm in zip(KERNEL, norms)
        ),
        ZERO,
    )
    assert weighted_trace == qc(Fraction(59, 312))

    assert compression(R_CRIT) == [[ONE, ZERO], [ZERO, ONE]]
    assert Fraction(29, 30) * Fraction(1, 5) - Fraction(6, 225) == Fraction(1, 6)
    for basis_element in KERNEL:
        assert hessian(R_CRIT, basis_element) == ZERO
    assert hessian(R, A0) == qc(Fraction(-75, 32))
    assert hessian(R_CRIT, R_CRIT) == qc(Fraction(11, 48))

    print(
        "verified: paired value 353/11224 > 0; "
        "stationary projection-origin trace 59/312 > 0"
    )


if __name__ == "__main__":
    main()
