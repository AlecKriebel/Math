#!/usr/bin/env python3
"""Independent exact check of the concurrent Galindo--Rowell comparison.

This supported verifier separately encodes the five-word Pauli--Clifford
operator, the literal Family III operator from Galindo--Rowell Section 13,
the four-dimensional site swap, and the displayed local unitary.  Arithmetic
is exact in Q(sqrt(2), sqrt(3), i), using only the Python standard library.
"""

from fractions import Fraction
import sys


if sys.flags.optimize:
    raise RuntimeError("optimized Python is not permitted for scientific verification")


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

    def __truediv__(self, value):
        value = Fraction(value)
        return Q23(*(x / value for x in self.v))

    def __eq__(self, other):
        return self.v == as_q23(other).v

    def __bool__(self):
        return any(self.v)


def as_q23(value):
    return value if isinstance(value, Q23) else Q23(value)


class CQ23:
    """An element of Q(sqrt(2), sqrt(3), i)."""

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

    def __truediv__(self, value):
        return CQ23(self.re / value, self.im / value)

    def conjugate(self):
        return CQ23(self.re, -self.im)

    def __eq__(self, other):
        other = as_cq23(other)
        return self.re == other.re and self.im == other.im

    def __bool__(self):
        return bool(self.re) or bool(self.im)


def as_cq23(value):
    if isinstance(value, CQ23):
        return value
    if isinstance(value, Q23):
        return CQ23(value)
    return CQ23(Q23(value))


ZERO = CQ23()
ONE = CQ23(1)
IUNIT = CQ23(0, 1)
SQRT2 = CQ23(Q23(0, 1))
SQRT3 = CQ23(Q23(0, 0, 1))


def require(condition, label):
    if not condition:
        raise AssertionError(label)


def matrix(rows):
    width = len(rows[0])
    require(all(len(row) == width for row in rows), "ragged matrix")
    return tuple(tuple(as_cq23(value) for value in row) for row in rows)


def zero(rows, columns=None):
    columns = rows if columns is None else columns
    return matrix([[ZERO for _ in range(columns)] for _ in range(rows)])


def eye(n):
    return matrix([[ONE if i == j else ZERO for j in range(n)] for i in range(n)])


def add(*matrices):
    rows, columns = len(matrices[0]), len(matrices[0][0])
    require(all(len(a) == rows and len(a[0]) == columns for a in matrices), "add dimensions")
    return matrix(
        [[sum((a[i][j] for a in matrices), ZERO) for j in range(columns)] for i in range(rows)]
    )


def neg(a):
    return matrix([[-value for value in row] for row in a])


def sub(a, b):
    return add(a, neg(b))


def smul(scalar, a):
    scalar = as_cq23(scalar)
    return matrix([[scalar * value for value in row] for row in a])


def mmul(a, b):
    require(len(a[0]) == len(b), "multiply dimensions")
    return matrix(
        [
            [sum((a[i][k] * b[k][j] for k in range(len(b))), ZERO) for j in range(len(b[0]))]
            for i in range(len(a))
        ]
    )


def kron2(a, b):
    return matrix(
        [
            [a[ia][ja] * b[ib][jb] for ja in range(len(a[0])) for jb in range(len(b[0]))]
            for ia in range(len(a))
            for ib in range(len(b))
        ]
    )


def kron(*matrices):
    out = matrix([[ONE]])
    for factor in matrices:
        out = kron2(out, factor)
    return out


def dagger(a):
    return matrix([[a[j][i].conjugate() for j in range(len(a))] for i in range(len(a[0]))])


def equal(a, b):
    return len(a) == len(b) and len(a[0]) == len(b[0]) and all(
        a[i][j] == b[i][j] for i in range(len(a)) for j in range(len(a[0]))
    )


def pauli_word(word):
    return kron(*(PAULI[letter] for letter in word))


def site_swap():
    out = [[ZERO for _ in range(16)] for _ in range(16)]
    for left in range(4):
        for right in range(4):
            out[4 * right + left][4 * left + right] = ONE
    return matrix(out)


I2 = matrix([[1, 0], [0, 1]])
X = matrix([[0, 1], [1, 0]])
Z = matrix([[1, 0], [0, -1]])
J = matrix([[0, -1], [1, 0]])
PAULI = {"I": I2, "X": X, "Z": Z, "J": J}


def main():
    identity16 = eye(16)

    # Independently encode the five-word Pauli--Clifford representative.
    m = smul(
        Fraction(1, 2),
        add(
            neg(pauli_word("ZIZZ")),
            neg(pauli_word("ZIJJ")),
            neg(pauli_word("JIZJ")),
            pauli_word("JIJZ"),
        ),
    )
    e = pauli_word("XIXX")
    # Encode sqrt(2/3)=sqrt(6)/3 and 1/sqrt(3)=sqrt(3)/3 exactly.
    h = add(smul(CQ23(Q23(0, 0, 0, Fraction(1, 3))), m), smul(-SQRT3 / 3, e))
    q = (ONE + IUNIT * SQRT3) / 2
    r_k = add(smul((q - ONE) / 2, identity16), smul((q + ONE) / 2, h))

    mathsf_a = smul(-IUNIT * SQRT2, m)
    mathsf_b = smul(IUNIT, e)
    u_k = smul(Fraction(1, 2), add(mathsf_a, mmul(mathsf_a, mathsf_b)))
    v_k = smul(Fraction(1, 2), sub(mathsf_a, mmul(mathsf_a, mathsf_b)))
    ukvk = mmul(u_k, v_k)

    require(equal(mmul(u_k, u_k), neg(identity16)), "U_K^2 = -I")
    print("[ok] U_K^2 = -I")
    require(equal(mmul(v_k, v_k), neg(identity16)), "V_K^2 = -I")
    print("[ok] V_K^2 = -I")
    require(equal(ukvk, neg(mmul(v_k, u_k))), "U_K V_K = -V_K U_K")
    print("[ok] U_K V_K = -V_K U_K")
    require(equal(ukvk, mathsf_b), "U_K V_K = mathsf B")
    print("[ok] U_K V_K = mathsf B")
    intrinsic_sum = add(u_k, v_k, ukvk)
    require(
        equal(intrinsic_sum, smul(-IUNIT * SQRT3, h)),
        "U_K + V_K + U_K V_K = -i sqrt(3) H",
    )
    print("[ok] U_K + V_K + U_K V_K = -i sqrt(3) H")

    zeta = (SQRT3 + IUNIT) / 2
    intrinsic_r = smul(IUNIT * zeta / 2, add(identity16, u_k, v_k, ukvk))
    require(equal(r_k, intrinsic_r), "intrinsic Family III formula")
    print("[ok] intrinsic Family III formula for R_K")

    # Literal Galindo--Rowell Section 13 tensor placements.
    p_z = kron(I2, Z, Z, I2)
    p_x = kron(X, I2, X, X)
    u_gr = smul(IUNIT, p_z)
    v_gr = smul(IUNIT, p_x)
    r_gr = smul(IUNIT * zeta / 2, add(identity16, u_gr, v_gr, mmul(u_gr, v_gr)))

    two = CQ23(2)
    s = smul(
        Fraction(1, 4),
        matrix(
            [
                [two + SQRT2, -IUNIT * SQRT2, IUNIT * SQRT2, two - SQRT2],
                [SQRT2, IUNIT * (two + SQRT2), IUNIT * (two - SQRT2), -SQRT2],
                [-(two - SQRT2), -IUNIT * SQRT2, IUNIT * SQRT2, -(two + SQRT2)],
                [-SQRT2, IUNIT * (two - SQRT2), IUNIT * (two + SQRT2), SQRT2],
            ]
        ),
    )
    require(equal(mmul(dagger(s), s), eye(4)), "S^dagger S = I_4")
    print("[ok] S^dagger S = I_4")

    sigma = site_swap()
    opposite = mmul(mmul(sigma, r_gr), sigma)
    local_change = kron(s, s)
    comparison = mmul(mmul(dagger(local_change), opposite), local_change)
    require(equal(r_k, comparison), "R_K local-unitary/site-reversal comparison")
    print("[ok] R_K = (S^dagger tensor S^dagger) Sigma R_GR Sigma (S tensor S)")

    u_opposite = mmul(mmul(sigma, u_gr), sigma)
    v_opposite = mmul(mmul(sigma, v_gr), sigma)
    u_comparison = mmul(mmul(dagger(local_change), u_opposite), local_change)
    v_comparison = mmul(mmul(dagger(local_change), v_opposite), local_change)
    require(equal(u_k, u_comparison), "U generator comparison")
    require(equal(v_k, v_comparison), "V generator comparison")
    print("[ok] quaternionic generators match componentwise after site reversal")

    print("All concurrent-work equivalence checks passed exactly.")


if __name__ == "__main__":
    main()
