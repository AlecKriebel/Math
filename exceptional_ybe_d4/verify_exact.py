#!/usr/bin/env python3
"""Dependency-free exact verification of the exceptional d=4 witness.

The arithmetic field is Q(sqrt(2), sqrt(3), i).  Matrices are stored sparsely
and every comparison is exact.  This checker is independent of SymPy and of
the supplied verifier.
"""

from fractions import Fraction


class Q23:
    """An element a + b*sqrt(2) + c*sqrt(3) + d*sqrt(6)."""

    __slots__ = ("v",)

    def __init__(self, a=0, b=0, c=0, d=0):
        self.v = tuple(Fraction(x) for x in (a, b, c, d))

    def __add__(self, other):
        other = as_q23(other)
        return Q23(*(x + y for x, y in zip(self.v, other.v)))

    __radd__ = __add__

    def __neg__(self):
        return Q23(*(-x for x in self.v))

    def __sub__(self, other):
        return self + (-as_q23(other))

    def __rsub__(self, other):
        return as_q23(other) - self

    def __mul__(self, other):
        other = as_q23(other)
        a, b, c, d = self.v
        e, f, g, h = other.v
        return Q23(
            a * e + 2 * b * f + 3 * c * g + 6 * d * h,
            a * f + b * e + 3 * c * h + 3 * d * g,
            a * g + c * e + 2 * b * h + 2 * d * f,
            a * h + d * e + b * g + c * f,
        )

    __rmul__ = __mul__

    def __truediv__(self, n):
        n = Fraction(n)
        return Q23(*(x / n for x in self.v))

    def __eq__(self, other):
        return self.v == as_q23(other).v

    def __bool__(self):
        return any(self.v)

    def __repr__(self):
        labels = ("", "*sqrt(2)", "*sqrt(3)", "*sqrt(6)")
        terms = [f"{x}{label}" for x, label in zip(self.v, labels) if x]
        return " + ".join(terms) if terms else "0"


def as_q23(value):
    return value if isinstance(value, Q23) else Q23(value)


class CQ23:
    """An element of Q(sqrt(2), sqrt(3), i), as a real/imaginary pair."""

    __slots__ = ("re", "im")

    def __init__(self, re=0, im=0):
        self.re = as_q23(re)
        self.im = as_q23(im)

    def __add__(self, other):
        other = as_cq23(other)
        return CQ23(self.re + other.re, self.im + other.im)

    __radd__ = __add__

    def __neg__(self):
        return CQ23(-self.re, -self.im)

    def __sub__(self, other):
        return self + (-as_cq23(other))

    def __rsub__(self, other):
        return as_cq23(other) - self

    def __mul__(self, other):
        other = as_cq23(other)
        return CQ23(
            self.re * other.re - self.im * other.im,
            self.re * other.im + self.im * other.re,
        )

    __rmul__ = __mul__

    def __truediv__(self, n):
        return CQ23(self.re / n, self.im / n)

    def conjugate(self):
        return CQ23(self.re, -self.im)

    def __eq__(self, other):
        other = as_cq23(other)
        return self.re == other.re and self.im == other.im

    def __bool__(self):
        return bool(self.re) or bool(self.im)

    def __repr__(self):
        if not self.im:
            return repr(self.re)
        return f"({self.re}) + i*({self.im})"


def as_cq23(value):
    if isinstance(value, CQ23):
        return value
    if isinstance(value, Q23):
        return CQ23(value)
    return CQ23(Q23(value))


ZERO = CQ23()
ONE = CQ23(1)


def zero_matrix(n):
    return [dict() for _ in range(n)]


def eye(n):
    out = zero_matrix(n)
    for i in range(n):
        out[i][i] = ONE
    return out


def dense_integer_matrix(rows):
    out = zero_matrix(len(rows))
    for i, row in enumerate(rows):
        for j, value in enumerate(row):
            if value:
                out[i][j] = CQ23(value)
    return out


def matrix_add(a, b):
    assert len(a) == len(b)
    out = zero_matrix(len(a))
    for i, (row_a, row_b) in enumerate(zip(a, b)):
        keys = set(row_a) | set(row_b)
        for j in keys:
            value = row_a.get(j, ZERO) + row_b.get(j, ZERO)
            if value:
                out[i][j] = value
    return out


def matrix_neg(a):
    return [{j: -value for j, value in row.items()} for row in a]


def matrix_sub(a, b):
    return matrix_add(a, matrix_neg(b))


def scalar_mul(scalar, a):
    scalar = as_cq23(scalar)
    if not scalar:
        return zero_matrix(len(a))
    return [
        {j: scalar * value for j, value in row.items() if scalar * value}
        for row in a
    ]


def matmul(a, b):
    assert len(a) == len(b)
    n = len(a)
    out = zero_matrix(n)
    for i, row_a in enumerate(a):
        accum = {}
        for k, value_a in row_a.items():
            for j, value_b in b[k].items():
                accum[j] = accum.get(j, ZERO) + value_a * value_b
        out[i] = {j: value for j, value in accum.items() if value}
    return out


def kron(a, b):
    na, nb = len(a), len(b)
    out = zero_matrix(na * nb)
    for ia, row_a in enumerate(a):
        for ib, row_b in enumerate(b):
            row = out[ia * nb + ib]
            for ja, value_a in row_a.items():
                for jb, value_b in row_b.items():
                    value = value_a * value_b
                    if value:
                        row[ja * nb + jb] = value
    return out


def kron_all(*matrices):
    out = eye(1)
    for matrix in matrices:
        out = kron(out, matrix)
    return out


def adjoint(a):
    n = len(a)
    out = zero_matrix(n)
    for i, row in enumerate(a):
        for j, value in row.items():
            out[j][i] = value.conjugate()
    return out


def trace(a):
    return sum((row.get(i, ZERO) for i, row in enumerate(a)), ZERO)


def assert_equal(label, a, b):
    difference = matrix_sub(a, b)
    for i, row in enumerate(difference):
        if row:
            j, value = next(iter(row.items()))
            raise AssertionError(f"{label}: entry ({i}, {j}) is {value}")
    print(f"[ok] {label}")


def partial_trace_right(a, left_dim, right_dim):
    assert len(a) == left_dim * right_dim
    out = zero_matrix(left_dim)
    for i in range(left_dim):
        for j in range(left_dim):
            value = ZERO
            for r in range(right_dim):
                value += a[i * right_dim + r].get(j * right_dim + r, ZERO)
            if value:
                out[i][j] = value
    return out


def partial_trace_left(a, left_dim, right_dim):
    assert len(a) == left_dim * right_dim
    out = zero_matrix(right_dim)
    for i in range(right_dim):
        for j in range(right_dim):
            value = ZERO
            for r in range(left_dim):
                value += a[r * right_dim + i].get(r * right_dim + j, ZERO)
            if value:
                out[i][j] = value
    return out


I2 = eye(2)
X = dense_integer_matrix([[0, 1], [1, 0]])
Z = dense_integer_matrix([[1, 0], [0, -1]])
J = dense_integer_matrix([[0, -1], [1, 0]])
PAULI = {"I": I2, "X": X, "Z": Z, "J": J}


def tensor_word(word):
    return kron_all(*(PAULI[letter] for letter in word))


def qubit_permutation(output_sources):
    """Matrix sending |b_0...b_{n-1}> to |b_{p_0}...b_{p_{n-1}}>."""

    n_qubits = len(output_sources)
    assert sorted(output_sources) == list(range(n_qubits))
    dimension = 2**n_qubits
    out = zero_matrix(dimension)
    for input_index in range(dimension):
        bits = [
            (input_index >> (n_qubits - 1 - position)) & 1
            for position in range(n_qubits)
        ]
        output_index = 0
        for source in output_sources:
            output_index = 2 * output_index + bits[source]
        out[output_index][input_index] = ONE
    return out


INV_SQRT_6 = Q23(0, 0, 0, Fraction(1, 6))
INV_SQRT_3 = Q23(0, 0, Fraction(1, 3), 0)
TERMS = (
    ("ZIZZ", -INV_SQRT_6),
    ("ZIJJ", -INV_SQRT_6),
    ("JIZJ", -INV_SQRT_6),
    ("JIJZ", INV_SQRT_6),
    ("XIXX", -INV_SQRT_3),
)


def build_h(terms):
    out = zero_matrix(2 ** len(terms[0][0]))
    for word, coefficient in terms:
        out = matrix_add(out, scalar_mul(coefficient, tensor_word(word)))
    return out


def ybe_residual(left, right):
    return matrix_sub(
        matmul(matmul(left, right), left),
        matmul(matmul(right, left), right),
    )


def main():
    i2, i4, i8, i16 = eye(2), eye(4), eye(8), eye(16)
    h = build_h(TERMS)

    assert_equal("H is Hermitian", adjoint(h), h)
    assert_equal("H^2 = I_16", matmul(h, h), i16)
    assert trace(h) == ZERO
    print("[ok] Tr(H) = 0")

    h1, h2 = kron(h, i4), kron(i4, h)
    cubic_left = matrix_sub(
        matmul(matmul(h1, h2), h1),
        matmul(matmul(h2, h1), h2),
    )
    cubic_right = scalar_mul(Fraction(1, 3), matrix_sub(h1, h2))
    assert_equal("cubic reflection identity on 64 dimensions", cubic_left, cubic_right)

    q = CQ23(Q23(Fraction(1, 2)), Q23(0, 0, Fraction(1, 2), 0))
    a = (q - 1) / 2
    b = (q + 1) / 2
    r = matrix_add(scalar_mul(a, i16), scalar_mul(b, h))
    p = scalar_mul(Fraction(1, 2), matrix_sub(i16, h))

    assert_equal("P^2 = P", matmul(p, p), p)
    assert_equal("P is Hermitian", adjoint(p), p)
    assert trace(p) == CQ23(8)
    print("[ok] Tr(P) = rank(P) = 8")

    assert_equal("R is unitary", matmul(adjoint(r), r), i16)
    hecke = matmul(
        matrix_add(r, i16),
        matrix_sub(r, scalar_mul(q, i16)),
    )
    assert_equal("(R + I)(R - qI) = 0", hecke, zero_matrix(16))
    assert trace(r) == 8 * (q - 1)
    print("[ok] Tr(R) = 8(q - 1) = -4 + 4i*sqrt(3)")

    r1, r2 = kron(r, i4), kron(i4, r)
    assert_equal(
        "direct 64x64 Yang--Baxter equation for R",
        ybe_residual(r1, r2),
        zero_matrix(64),
    )

    expected_partial = scalar_mul(2, i4)
    assert_equal(
        "Tr_right(P) = 2 I_4",
        partial_trace_right(p, 4, 4),
        expected_partial,
    )
    assert_equal(
        "Tr_left(P) = 2 I_4",
        partial_trace_left(p, 4, 4),
        expected_partial,
    )

    p1, p2 = kron(p, i4), kron(i4, p)
    tl_obstruction = matrix_sub(
        matmul(matmul(p1, p2), p1),
        scalar_mul(Fraction(1, 3), p1),
    )
    tl_norm = trace(matmul(adjoint(tl_obstruction), tl_obstruction)) / 64
    assert tl_norm == CQ23(Fraction(1, 18))
    print("[ok] exceptional trace norm of the d=3 TL obstruction = 1/18")

    q_projection = matrix_sub(i16, p)
    q1, q2 = kron(q_projection, i4), kron(i4, q_projection)
    complementary_tl_obstruction = matrix_sub(
        matmul(matmul(q1, q2), q1),
        scalar_mul(Fraction(1, 3), q1),
    )
    complementary_tl_norm = (
        trace(
            matmul(
                adjoint(complementary_tl_obstruction),
                complementary_tl_obstruction,
            )
        )
        / 64
    )
    assert complementary_tl_norm == CQ23(Fraction(1, 18))
    print("[ok] exceptional trace norm of the complementary d=3 obstruction = 1/18")

    # Remove the spectator second qubit, then exchange the last two active
    # coordinates.  This gives the standard (3,2)-gYB ordering
    # (a_i, b_{i+1}, a_{i+1}).
    active_terms = []
    for word, coefficient in TERMS:
        assert word[1] == "I"
        active = word[0] + word[2] + word[3]
        standard_order = active[0] + active[2] + active[1]
        active_terms.append((standard_order, coefficient))
    k_h = build_h(tuple(active_terms))
    sitewise_swap = qubit_permutation((1, 0, 3, 2))
    swapped_two_site_h = matmul(matmul(sitewise_swap, h), adjoint(sitewise_swap))
    assert_equal(
        "sitewise-swapped H factors as I_2 tensor K_H",
        swapped_two_site_h,
        kron(i2, k_h),
    )
    k_r = matrix_add(scalar_mul(a, i8), scalar_mul(b, k_h))
    swapped_two_site_r = matmul(matmul(sitewise_swap, r), adjoint(sitewise_swap))
    assert_equal(
        "sitewise-swapped R factors as I_2 tensor K",
        swapped_two_site_r,
        kron(i2, k_r),
    )
    assert_equal("active 8x8 operator is unitary", matmul(adjoint(k_r), k_r), i8)

    k1, k2 = kron(k_r, i4), kron(i4, k_r)
    assert_equal(
        "standard (3,2)-generalized Yang--Baxter equation",
        ybe_residual(k1, k2),
        zero_matrix(32),
    )
    far_left, far_right = kron(k_r, i16), kron(i16, k_r)
    assert_equal(
        "(3,2)-gYB far commutativity",
        matmul(far_left, far_right),
        matmul(far_right, far_left),
    )

    print()
    print("All dependency-free exact checks passed.")
    print("base dimension: 4")
    print("matrix size: 16 x 16")
    print("rank of the (-1)-spectral projection: 8")
    print("normalized spectral trace eta: 1/2")
    print("standard active form: unitary (3,2)-gYB operator on three qubits")


if __name__ == "__main__":
    main()
