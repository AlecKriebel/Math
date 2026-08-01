#!/usr/bin/env python3
"""Dependency-free exact checks for the corrected mixed DTH lift.

All scalar arithmetic is in Q(i).  A four-dimensional one-site model is
enough to audit the tensor/partial-transpose identities, which are independent
of the dimension and of the special triple-qutrit Omega form.
"""

from dataclasses import dataclass
from fractions import Fraction as F


@dataclass(frozen=True)
class QI:
    re: F = F(0)
    im: F = F(0)

    @staticmethod
    def make(value):
        if isinstance(value, QI):
            return value
        return QI(F(value), F(0))

    def __add__(self, other):
        other = QI.make(other)
        return QI(self.re + other.re, self.im + other.im)

    __radd__ = __add__

    def __neg__(self):
        return QI(-self.re, -self.im)

    def __sub__(self, other):
        return self + (-QI.make(other))

    def __rsub__(self, other):
        return QI.make(other) - self

    def __mul__(self, other):
        other = QI.make(other)
        return QI(
            self.re * other.re - self.im * other.im,
            self.re * other.im + self.im * other.re,
        )

    __rmul__ = __mul__

    def conj(self):
        return QI(self.re, -self.im)

    def __bool__(self):
        return bool(self.re or self.im)

    def __lt__(self, other):
        other = QI.make(other)
        assert self.im == other.im == 0
        return self.re < other.re


ZERO = QI()
ONE = QI(F(1))
I = QI(F(0), F(1))


def clean(vector):
    return {key: value for key, value in vector.items() if value}


def add(left, right, scale=ONE):
    scale = QI.make(scale)
    out = dict(left)
    for key, value in right.items():
        out[key] = out.get(key, ZERO) + scale * value
    return clean(out)


def tensor(*vectors):
    out = {(): ONE}
    for vector in vectors:
        new = {}
        for prefix, x in out.items():
            for suffix, y in vector.items():
                suffix = suffix if isinstance(suffix, tuple) else (suffix,)
                key = prefix + suffix
                new[key] = new.get(key, ZERO) + x * y
        out = clean(new)
    return out


def conjugate(vector):
    return {key: value.conj() for key, value in vector.items()}


def dot(left, right):
    result = ZERO
    for key, value in left.items():
        result += value.conj() * right.get(key, ZERO)
    return result


def outer(vector):
    return {
        (ket, bra): x * y.conj()
        for ket, x in vector.items()
        for bra, y in vector.items()
        if x and y
    }


def op_expectation(vector, operator):
    result = ZERO
    for (ket, bra), value in operator.items():
        result += vector.get(ket, ZERO).conj() * value * vector.get(bra, ZERO)
    return result


def partial_transpose_first_bivector(operator):
    """Transpose tensor positions 0,1 between ket and bra."""
    out = {}
    for (ket, bra), value in operator.items():
        new_ket = bra[:2] + ket[2:]
        new_bra = ket[:2] + bra[2:]
        key = (new_ket, new_bra)
        out[key] = out.get(key, ZERO) + value
    return clean(out)


def basis(index):
    return {(index,): ONE}


def wedge(u, v):
    return add(tensor(u, v), tensor(v, u), -ONE)


def swap_position(vector, first, second):
    out = {}
    for word, value in vector.items():
        word = list(word)
        word[first], word[second] = word[second], word[first]
        word = tuple(word)
        out[word] = out.get(word, ZERO) + value
    return clean(out)


def jucys(vector):
    out = {}
    for first in range(4):
        out = add(out, swap_position(vector, first, 4))
    return out


def mixed_support(vector):
    """C_s on slots bar(V),bar(V),V,V,V -> V,V,bar(V)."""
    out = {}
    for (i, j, a, b, k), value in vector.items():
        if i == k:
            key = (a, b, j)
            out[key] = out.get(key, ZERO) + value
    return clean(out)


def matrix_dagger_times(W, z, dimension):
    out = {}
    for j in range(dimension):
        value = ZERO
        for i in range(dimension):
            value += W.get((i, j), ZERO).conj() * z.get((i,), ZERO)
        if value:
            out[(j,)] = value
    return out


def pair_exchange(vector):
    out = {}
    for (i, j, a, b, k), value in vector.items():
        key = (a, b, i, j, k)
        out[key] = out.get(key, ZERO) + value
    return clean(out)


# -------------------------------------------------------------------------
# Exact mixed density consistency and support evaluation.

dimension = 4
u = add(basis(0), basis(1), I)
v = basis(2)
w = wedge(u, v)  # A genuinely complex decomposable bivector.
z_support = basis(3)

h = tensor(w, w, z_support)
m = tensor(conjugate(w), w, z_support)
rho = outer(h)
sigma = partial_transpose_first_bivector(rho)

assert sigma == outer(m)
assert pair_exchange(h) == h
assert mixed_support(m) == {}

# Non-support case: C_s(bar(w) tensor w tensor z)
# equals w tensor (W^dagger z), with normalization one.
z_nonsupport = basis(0)
m_non = tensor(conjugate(w), w, z_nonsupport)
wdz = matrix_dagger_times(w, z_nonsupport, dimension)
assert mixed_support(m_non) == tensor(w, wdz)

norm_w = dot(w, w)
norm_wdz = dot(wdz, wdz)
support_norm = dot(mixed_support(m_non), mixed_support(m_non))
assert support_norm == norm_w * norm_wdz

# The positive mixed localizer pulls back to one quarter of J_5 on a
# Veronese ket.
h_non = tensor(w, w, z_nonsupport)
assert dot(h_non, jucys(h_non)) == QI.make(4) * support_norm


# -------------------------------------------------------------------------
# A symmetric first-Pluecker ket can still fail the PPT consistency.
# Take two bivectors sharing e0, so their wedge is zero.

a = wedge(basis(0), basis(1))
b = wedge(basis(0), basis(2))
z = basis(3)
entangled_h = add(tensor(a, b, z), tensor(b, a, z))
assert pair_exchange(entangled_h) == entangled_h

entangled_sigma = partial_transpose_first_bivector(outer(entangled_h))
negative_test = add(
    tensor(conjugate(b), b, z),
    tensor(conjugate(a), a, z),
    -ONE,
)
negative_value = op_expectation(negative_test, entangled_sigma)
assert negative_value < ZERO


# -------------------------------------------------------------------------
# Audit the local mixed SU(3) representation dimensions supplied for the
# future block calculation.  dim(p,q)=(p+1)(q+1)(p+q+2)/2.

def su3_dimension(p, q):
    return (p + 1) * (q + 1) * (p + q + 2) // 2


mixed_multiplicities = {
    (3, 2): 1,
    (2, 1): 6,
    (1, 0): 6,
    (1, 3): 2,
    (0, 2): 5,
    (4, 0): 1,
}
assert sum(
    multiplicity * su3_dimension(*weight)
    for weight, multiplicity in mixed_multiplicities.items()
) == 3**5
assert sum(m * m for m in mixed_multiplicities.values()) == 103


print("verified exact corrected mixed DTH module")
print("rho^Gamma_1 = |bar(w),w,z><bar(w),w,z|")
print("C_s(bar(w),w,z) = w tensor W^dagger z")
print("<h,J5 h> = 4 ||C_s m||^2")
print("symmetric Pluecker source need not satisfy PPT:", negative_value.re)
print("local mixed commutant dimension: 103")
