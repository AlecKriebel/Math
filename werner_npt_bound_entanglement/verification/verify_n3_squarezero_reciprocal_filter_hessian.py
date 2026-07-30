#!/usr/bin/env python3
"""Exact verifier for the sharp reciprocal-filter Hessian.

The program uses only Python's standard library.  Arithmetic is
performed in Q(omega), omega^2 + omega + 1 = 0.
"""

from fractions import Fraction as F
from itertools import combinations


class O:
    """An element a + b*omega of Q(omega)."""

    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a = a if isinstance(a, F) else F(a)
        self.b = b if isinstance(b, F) else F(b)

    @staticmethod
    def make(x):
        return x if isinstance(x, O) else O(x)

    def __add__(self, other):
        other = O.make(other)
        return O(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return O(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-O.make(other))

    def __rsub__(self, other):
        return O.make(other) - self

    def __mul__(self, other):
        other = O.make(other)
        return O(
            self.a * other.a - self.b * other.b,
            self.a * other.b + self.b * other.a - self.b * other.b,
        )

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, O):
            # (a+bw)^-1 = ((a-b)-b w)/(a^2-ab+b^2).
            norm = other.a * other.a - other.a * other.b + other.b * other.b
            return self * O(other.a - other.b, -other.b) / norm
        return O(self.a / other, self.b / other)

    def conjugate(self):
        # conjugate(omega) = omega^2 = -1-omega.
        return O(self.a - self.b, -self.b)

    def __eq__(self, other):
        other = O.make(other)
        return self.a == other.a and self.b == other.b

    def __bool__(self):
        return bool(self.a or self.b)

    def __repr__(self):
        return f"O({self.a},{self.b})"


ZERO = O()
ONE = O(1)
OMEGA = O(0, 1)
D = 27


def digits(k):
    return (k // 9, (k // 3) % 3, k % 3)


def index(word):
    return 9 * word[0] + 3 * word[1] + word[2]


def omega_power(k):
    return (ONE, OMEGA, -ONE - OMEGA)[k % 3]


def add_sparse(*terms):
    out = {}
    for coefficient, matrix in terms:
        coefficient = O.make(coefficient)
        for key, value in matrix.items():
            out[key] = out.get(key, ZERO) + coefficient * value
            if not out[key]:
                del out[key]
    return out


def scale_vector(coefficient, vector):
    coefficient = O.make(coefficient)
    return {i: coefficient * value for i, value in vector.items() if coefficient * value}


def add_vectors(*terms):
    out = {}
    for coefficient, vector in terms:
        coefficient = O.make(coefficient)
        for i, value in vector.items():
            out[i] = out.get(i, ZERO) + coefficient * value
            if not out[i]:
                del out[i]
    return out


def inner_vector(u, v):
    return sum((value.conjugate() * v.get(i, ZERO) for i, value in u.items()), ZERO)


def outer(u, v, coefficient=ONE):
    coefficient = O.make(coefficient)
    return {
        (i, j): coefficient * x * y.conjugate()
        for i, x in u.items()
        for j, y in v.items()
        if coefficient * x * y.conjugate()
    }


def partial_trace(matrix, traced):
    traced = set(traced)
    remaining = [i for i in range(3) if i not in traced]
    out = {}
    for (row, col), value in matrix.items():
        rr = digits(row)
        cc = digits(col)
        if any(rr[i] != cc[i] for i in traced):
            continue
        new_row = 0
        new_col = 0
        for site in remaining:
            new_row = 3 * new_row + rr[site]
            new_col = 3 * new_col + cc[site]
        key = (new_row, new_col)
        out[key] = out.get(key, ZERO) + value
        if not out[key]:
            del out[key]
    return out


def hs_inner(a, b):
    return sum(
        (value.conjugate() * b.get(key, ZERO) for key, value in a.items()),
        ZERO,
    )


def endpoint_bilinear(a, b):
    value = ZERO
    for size in range(4):
        for sites in combinations(range(3), size):
            value += F(-1, 2) ** size * hs_inner(
                partial_trace(a, sites), partial_trace(b, sites)
            )
    return value


def dense_zero(rows, cols):
    return [[ZERO for _ in range(cols)] for _ in range(rows)]


def dense_add(a, b):
    return [
        [a[i][j] + b[i][j] for j in range(len(a[0]))]
        for i in range(len(a))
    ]


def dense_scale(coefficient, a):
    return [
        [O.make(coefficient) * a[i][j] for j in range(len(a[0]))]
        for i in range(len(a))
    ]


def dense_mul(a, b):
    return [
        [
            sum((a[i][k] * b[k][j] for k in range(len(b))), ZERO)
            for j in range(len(b[0]))
        ]
        for i in range(len(a))
    ]


def dense_dagger(a):
    return [
        [a[j][i].conjugate() for j in range(len(a))]
        for i in range(len(a[0]))
    ]


def dense_trace(a):
    return sum((a[i][i] for i in range(len(a))), ZERO)


def columns_gram(left, operator, right, site):
    out = dense_zero(len(left), len(right))
    images = [apply_local(operator, vector, site) for vector in right]
    for i, u in enumerate(left):
        for j, v in enumerate(images):
            out[i][j] = inner_vector(u, v)
    return out


def apply_local(operator, vector, site=0):
    out = {}
    for old_index, value in vector.items():
        old = list(digits(old_index))
        for new_symbol in range(3):
            coefficient = operator[new_symbol][old[site]]
            if not coefficient:
                continue
            new = old[:]
            new[site] = new_symbol
            new_index = index(new)
            out[new_index] = out.get(new_index, ZERO) + coefficient * value
            if not out[new_index]:
                del out[new_index]
    return out


def columns_right_multiply(columns, matrix):
    return [
        add_vectors(*((matrix[k][j], columns[k]) for k in range(len(columns))))
        for j in range(len(matrix[0]))
    ]


def ghz(a, b, k):
    # This is sqrt(3) times the normalized vector.
    return {
        index((j, (j + a) % 3, (j + b) % 3)): omega_power(k * j)
        for j in range(3)
    }


U = [ghz(0, 0, 0), ghz(0, 0, 1)]
W = [ghz(1, 2, 2), ghz(2, 1, 2)]


def frame_derivatives(frame, operator, sign, site):
    """Return sqrt(3) times F, Fdot, Fddot."""
    operator2 = dense_mul(operator, operator)
    a = dense_scale(F(1, 3), columns_gram(frame, operator, frame, site))
    b = dense_scale(F(1, 3), columns_gram(frame, operator2, frame, site))
    af = [apply_local(operator, vector, site) for vector in frame]
    a2f = [apply_local(operator2, vector, site) for vector in frame]
    fa = columns_right_multiply(frame, a)
    first = [
        add_vectors((sign, af[j]), (-sign, fa[j]))
        for j in range(2)
    ]
    a_squared = dense_mul(a, a)
    correction = dense_add(dense_scale(3, a_squared), dense_scale(-2, b))
    afa = columns_right_multiply(af, a)
    fcorr = columns_right_multiply(frame, correction)
    second = [
        add_vectors((1, a2f[j]), (-2, afa[j]), (1, fcorr[j]))
        for j in range(2)
    ]
    return frame, first, second


def endpoint_units(operator, site):
    u0, u1, u2 = frame_derivatives(U, operator, 1, site)
    w0, w1, w2 = frame_derivatives(W, operator, -1, site)
    levels = ([], [], [])
    for a in range(2):
        for b in range(2):
            e0 = outer(u0[a], w0[b], F(1, 3))
            e1 = add_sparse(
                (F(1, 3), outer(u1[a], w0[b])),
                (F(1, 3), outer(u0[a], w1[b])),
            )
            e2 = add_sparse(
                (F(1, 3), outer(u2[a], w0[b])),
                (F(2, 3), outer(u1[a], w1[b])),
                (F(1, 3), outer(u0[a], w2[b])),
            )
            levels[0].append(e0)
            levels[1].append(e1)
            levels[2].append(e2)
    return levels, (u0, u1, u2), (w0, w1, w2)


def endpoint_derivatives(levels):
    e0, e1, e2 = levels
    h0 = dense_zero(4, 4)
    h1 = dense_zero(4, 4)
    h2 = dense_zero(4, 4)
    for i in range(4):
        for j in range(4):
            h0[i][j] = endpoint_bilinear(e0[i], e0[j])
            h1[i][j] = (
                endpoint_bilinear(e1[i], e0[j])
                + endpoint_bilinear(e0[i], e1[j])
            )
            h2[i][j] = (
                endpoint_bilinear(e2[i], e0[j])
                + 2 * endpoint_bilinear(e1[i], e1[j])
                + endpoint_bilinear(e0[i], e2[j])
            )
    return h0, h1, h2


def projector_derivatives(levels):
    f0, f1, f2 = levels
    p0 = {}
    p1 = {}
    p2 = {}
    for j in range(2):
        p0 = add_sparse((1, p0), (F(1, 3), outer(f0[j], f0[j])))
        p1 = add_sparse(
            (1, p1),
            (F(1, 3), outer(f1[j], f0[j])),
            (F(1, 3), outer(f0[j], f1[j])),
        )
        p2 = add_sparse(
            (1, p2),
            (F(1, 3), outer(f2[j], f0[j])),
            (F(2, 3), outer(f1[j], f1[j])),
            (F(1, 3), outer(f0[j], f2[j])),
        )
    return p0, p1, p2


def sparse_trace_square(a):
    dimension = 1 + max((max(key) for key in a), default=-1)
    return sum(
        (
            a.get((i, j), ZERO) * a.get((j, i), ZERO)
            for i in range(dimension)
            for j in range(dimension)
        ),
        ZERO,
    )


def sparse_trace(a):
    dimension = 1 + max((max(key) for key in a), default=-1)
    return sum((a.get((i, i), ZERO) for i in range(dimension)), ZERO)


def directional_hessian(operator, site, check_base=False):
    levels, u_levels, w_levels = endpoint_units(operator, site)
    h0, h1, h2 = endpoint_derivatives(levels)
    if check_base:
        expected = [
            [O(F(1, 2)) if i == j else ZERO for j in range(4)]
            for i in range(4)
        ]
        assert h0 == expected
    assert h1 == dense_zero(4, 4)
    # H0 = I/2, so the log-determinant contribution is
    # 2 tr(H2) - 4 tr(H1^2).
    answer = 2 * dense_trace(h2) - 4 * dense_trace(dense_mul(h1, h1))
    for frame_levels in (u_levels, w_levels):
        p0, p1, p2 = projector_derivatives(frame_levels)
        for kept_site in range(3):
            traced = tuple(i for i in range(3) if i != kept_site)
            if check_base:
                rho0 = partial_trace(p0, traced)
                expected_rho0 = {
                    (i, i): O(F(2, 3)) for i in range(3)
                }
                assert rho0 == expected_rho0
            rho1 = partial_trace(p1, traced)
            rho2 = partial_trace(p2, traced)
            assert sparse_trace(rho1) == ZERO
            answer -= (
                F(3, 2) * sparse_trace(rho2)
                - F(9, 4) * sparse_trace_square(rho1)
            )
    assert answer.b == 0
    return answer.a


def hermitian_off_diagonal(r, s, phase):
    out = dense_zero(3, 3)
    out[r][s] = phase
    out[s][r] = phase.conjugate()
    return out


def diagonal(entries):
    out = dense_zero(3, 3)
    for i, value in enumerate(entries):
        out[i][i] = O(value)
    return out


generators = []
for r, s in combinations(range(3), 2):
    generators.append(hermitian_off_diagonal(r, s, ONE))
    generators.append(hermitian_off_diagonal(r, s, OMEGA))
generators.append(diagonal((1, -1, 0)))
generators.append(diagonal((1, 1, -2)))

expected_diagonal = [F(208, 9)] * 6 + [F(18), F(54)]
expected = [[F(0) for _ in range(8)] for _ in range(8)]
for pair in range(3):
    i = 2 * pair
    expected[i][i] = expected[i + 1][i + 1] = F(208, 9)
    expected[i][i + 1] = expected[i + 1][i] = F(-104, 9)
expected[6][6] = F(18)
expected[7][7] = F(54)

for physical_site in range(3):
    diagonal_values = [
        directional_hessian(
            generator,
            physical_site,
            check_base=(physical_site == 0 and i == 0),
        )
        for i, generator in enumerate(generators)
    ]
    assert diagonal_values == expected_diagonal

    hessian = [[F(0) for _ in range(8)] for _ in range(8)]
    for i in range(8):
        hessian[i][i] = diagonal_values[i]
        for j in range(i):
            summed = dense_add(generators[i], generators[j])
            mixed = (
                directional_hessian(summed, physical_site)
                - diagonal_values[i]
                - diagonal_values[j]
            ) / 2
            hessian[i][j] = hessian[j][i] = mixed
    assert hessian == expected

    # Each off-diagonal 2x2 block has positive determinant and
    # diagonal; the final two entries are positive.
    for pair in range(3):
        i = 2 * pair
        assert hessian[i][i] > 0
        assert (
            hessian[i][i] * hessian[i + 1][i + 1]
            - hessian[i][i + 1] ** 2
            > 0
        )
    assert hessian[6][6] > 0 and hessian[7][7] > 0

print("verified: exact sharp GHZ endpoint Gram H = I_4/2")
print("verified: full 8x8 reciprocal-filter Hessian at all three sites")
print("verified: Hessian is strictly positive on traceless Hermitian filters")
