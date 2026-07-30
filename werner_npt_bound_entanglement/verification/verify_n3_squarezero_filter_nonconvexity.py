#!/usr/bin/env python3
"""Exact checker for the flag--Bell reciprocal-filter obstruction.

Only Python's standard library is used.  The physical contraction is
performed in Q(omega)[x,y], where omega^2 + omega + 1 = 0.
"""

from fractions import Fraction as F
from itertools import combinations, permutations


class O:
    """An element a + b*omega of Q(omega)."""

    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a = a if isinstance(a, F) else F(a)
        self.b = b if isinstance(b, F) else F(b)

    @staticmethod
    def make(value):
        return value if isinstance(value, O) else O(value)

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

    def conjugate(self):
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


def omega_power(power):
    return (ONE, OMEGA, -ONE - OMEGA)[power % 3]


# A polynomial is a sparse dictionary (x-degree,y-degree) -> Q(omega).
def pc(value):
    value = O.make(value)
    return {} if not value else {(0, 0): value}


X = {(1, 0): ONE}
Y = {(0, 1): ONE}


def padd(*polynomials):
    out = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            out[monomial] = out.get(monomial, ZERO) + coefficient
            if not out[monomial]:
                del out[monomial]
    return out


def pneg(polynomial):
    return {monomial: -coefficient for monomial, coefficient in polynomial.items()}


def psub(left, right):
    return padd(left, pneg(right))


def pmul(left, right):
    out = {}
    for (i, j), a in left.items():
        for (k, ell), b in right.items():
            monomial = (i + k, j + ell)
            out[monomial] = out.get(monomial, ZERO) + a * b
            if not out[monomial]:
                del out[monomial]
    return out


def pscale(coefficient, polynomial):
    return pmul(pc(coefficient), polynomial)


def pconjugate(polynomial):
    return {
        monomial: coefficient.conjugate()
        for monomial, coefficient in polynomial.items()
    }


def ppow(polynomial, exponent):
    out = pc(1)
    for _ in range(exponent):
        out = pmul(out, polynomial)
    return out


def index(word):
    return 9 * word[0] + 3 * word[1] + word[2]


def digits(integer):
    return (integer // 9, (integer // 3) % 3, integer % 3)


def bell_flag(flag, r, phase, coefficient=None):
    """Unnormalized |flag> tensor sum_j omega^(phase*j)|j,j+r>."""
    coefficient = pc(1) if coefficient is None else coefficient
    return {
        index((j, flag, (j + r) % 3)): pscale(
            omega_power(phase * j), coefficient
        )
        for j in range(3)
    }


def add_vectors(*vectors):
    out = {}
    for vector in vectors:
        for position, value in vector.items():
            out[position] = padd(out.get(position, {}), value)
            if not out[position]:
                del out[position]
    return out


def outer(left, right):
    return {
        (i, j): pmul(a, pconjugate(b))
        for i, a in left.items()
        for j, b in right.items()
    }


def partial_trace(matrix, traced):
    traced = set(traced)
    remaining = [site for site in range(3) if site not in traced]
    out = {}
    for (row, column), value in matrix.items():
        row_digits = digits(row)
        column_digits = digits(column)
        if any(row_digits[site] != column_digits[site] for site in traced):
            continue
        new_row = 0
        new_column = 0
        for site in remaining:
            new_row = 3 * new_row + row_digits[site]
            new_column = 3 * new_column + column_digits[site]
        key = (new_row, new_column)
        out[key] = padd(out.get(key, {}), value)
        if not out[key]:
            del out[key]
    return out


def hs_inner(left, right):
    return padd(
        *(
            pmul(pconjugate(value), right.get(key, {}))
            for key, value in left.items()
        )
    )


def endpoint_bilinear(left, right):
    out = {}
    for size in range(4):
        for sites in combinations(range(3), size):
            out = padd(
                out,
                pscale(
                    F(-1, 2) ** size,
                    hs_inner(
                        partial_trace(left, sites),
                        partial_trace(right, sites),
                    ),
                ),
            )
    return out


def permutation_sign(permutation):
    inversions = sum(
        permutation[i] > permutation[j]
        for i in range(len(permutation))
        for j in range(i + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def determinant(matrix):
    out = {}
    for permutation in permutations(range(len(matrix))):
        term = pc(permutation_sign(permutation))
        for row, column in enumerate(permutation):
            term = pmul(term, matrix[row][column])
        out = padd(out, term)
    return out


# The four unnormalized columns.  Each Bell vector has squared norm 3.
u0 = bell_flag(0, 0, 0)
u1 = add_vectors(
    bell_flag(1, 2, 1, X),
    bell_flag(2, 0, 0),
)
w0 = bell_flag(0, 1, 1)
w1 = add_vectors(
    bell_flag(1, 0, 2, Y),
    bell_flag(2, 1, 1),
)

units = [outer(u, w) for u in (u0, u1) for w in (w0, w1)]
raw_gram = [
    [endpoint_bilinear(left, right) for right in units]
    for left in units
]

x2 = ppow(X, 2)
y2 = ppow(Y, 2)
xy = pmul(X, Y)
x2y2 = pmul(x2, y2)

# Raw Bell vectors are sqrt(3) times the normalized Bell vectors, so
# this matrix is nine times the unnormalized-logical Gram in the note.
expected_raw_gram = [
    [pc(3), {}, {}, pscale(F(-3, 4), padd(xy, pc(4)))],
    [{}, pscale(6, padd(y2, pc(1))), {}, {}],
    [{}, {}, pscale(6, padd(x2, pc(1))), {}],
    [
        pscale(F(-3, 4), padd(xy, pc(4))),
        {},
        {},
        pscale(
            F(3, 2),
            padd(
                pscale(2, x2y2),
                pscale(4, x2),
                pscale(-1, xy),
                pscale(4, y2),
                pc(2),
            ),
        ),
    ],
]
assert raw_gram == expected_raw_gram

one_plus_x2 = padd(pc(1), x2)
one_plus_y2 = padd(pc(1), y2)
p_polynomial = padd(
    pscale(15, x2y2),
    pscale(32, x2),
    pscale(-16, xy),
    pscale(32, y2),
)
expected_raw_determinant = pscale(
    F(81, 4),
    pmul(pmul(one_plus_x2, one_plus_y2), p_polynomial),
)
assert determinant(raw_gram) == expected_raw_determinant


# Verify the one-site plane marginals before using their determinant
# product.  If N=1+x^2, then
#
#   N*3*rho_i^U = N*Tr_hat{i}|u0_raw><u0_raw|
#                 + Tr_hat{i}|u1_raw><u1_raw|.
def dense_reduction(vector, site):
    reduced = partial_trace(outer(vector, vector), tuple(i for i in range(3) if i != site))
    return [
        [reduced.get((row, column), {}) for column in range(3)]
        for row in range(3)
    ]


def dense_padd(left, right):
    return [
        [padd(left[i][j], right[i][j]) for j in range(len(left[0]))]
        for i in range(len(left))
    ]


def dense_pscale(polynomial, matrix):
    return [
        [pmul(polynomial, matrix[i][j]) for j in range(len(matrix[0]))]
        for i in range(len(matrix))
    ]


def diagonal_polynomials(entries):
    return [
        [entries[i] if i == j else {} for j in range(3)]
        for i in range(3)
    ]


u_scaled_marginals = [
    dense_padd(
        dense_pscale(one_plus_x2, dense_reduction(u0, site)),
        dense_reduction(u1, site),
    )
    for site in range(3)
]
w_scaled_marginals = [
    dense_padd(
        dense_pscale(one_plus_y2, dense_reduction(w0, site)),
        dense_reduction(w1, site),
    )
    for site in range(3)
]
expected_u_balanced = diagonal_polynomials([pscale(2, one_plus_x2)] * 3)
expected_w_balanced = diagonal_polynomials([pscale(2, one_plus_y2)] * 3)
expected_u_flag = diagonal_polynomials(
    [pscale(3, one_plus_x2), pscale(3, x2), pc(3)]
)
expected_w_flag = diagonal_polynomials(
    [pscale(3, one_plus_y2), pscale(3, y2), pc(3)]
)
assert u_scaled_marginals == [
    expected_u_balanced,
    expected_u_flag,
    expected_u_balanced,
]
assert w_scaled_marginals == [
    expected_w_balanced,
    expected_w_flag,
    expected_w_balanced,
]


# The scalar certificate for the product-determinant inequality.
# F(z)=256(15z+48)(1+z)^2-59049z.
def f_polynomial(z):
    return 3840 * z**3 + 19968 * z**2 - 30633 * z + 12288


r = F(13, 20)
# Exact expansions on the two sides of r.
# z=r+t:
assert f_polynomial(r) == F(186759, 100)
assert 11520 * r * r + 39936 * r - 30633 == F(963, 5)
assert 11520 * r + 19968 == 27456

# On 0<=z<=r put s=r-z.  Both displayed lower-bound terms are positive.
assert 27456 - 3840 * r > 0
assert F(186759, 100) - F(963, 5) * r == F(8712, 5)


# Exact reciprocal-filter curvature at x=1/10, y=1/100.
x = F(1, 10)
y = F(1, 100)
z = x * y
s0 = x * x + y * y
s1 = 4 * (x * x - y * y)
s2 = 16 * s0
p0 = 15 * z * z - 16 * z + 32 * s0
q0 = 1 + z * z + s0

assert p0 == F(61443, 200000)
assert q0 == F(1010101, 1000000)

log_second = (
    32 * (s2 * p0 - 32 * s1 * s1) / (p0 * p0)
    + (s2 * q0 - s1 * s1) / (q0 * q0)
)
expected_log_second = F(
    -9845853439120560320,
    427988320182198573561,
)
assert log_second == expected_log_second
assert log_second < 0

ratio = F(256, 59049) * p0 * q0 / (z * z)
assert ratio == F(27583838108, 20503125)
assert ratio > 1

ratio_second = (
    F(256, 59049)
    / (z * z)
    * (64 * s1 * s1 + (32 * q0 + p0) * s2)
)
assert ratio_second == F(859750796032, 36905625)
assert ratio_second > 0


# A length-three Taylor-series check for the normalized determinant
# defect itself.  Entries are coefficients of 1,t,t^2.
def sadd(left, right):
    return tuple(left[i] + right[i] for i in range(3))


def sscale(coefficient, series):
    return tuple(coefficient * value for value in series)


def smul(left, right):
    return tuple(
        sum(left[j] * right[i - j] for j in range(i + 1))
        for i in range(3)
    )


def sinv(series):
    a, b, c = series
    return (1 / a, -b / (a * a), b * b / (a**3) - c / (a * a))


x2_series = (x * x, 4 * x * x, 8 * x * x)
y2_series = (y * y, -4 * y * y, 8 * y * y)
s_series = sadd(x2_series, y2_series)
a_series = sadd((F(1), F(0), F(0)), x2_series)
b_series = sadd((F(1), F(0), F(0)), y2_series)
p_series = sadd((15 * z * z - 16 * z, F(0), F(0)), sscale(32, s_series))
ab_inverse = sinv(smul(a_series, b_series))
det_series = sscale(F(1, 324), smul(p_series, ab_inverse))
rhs_series = sscale(
    F(729, 1024) * z * z,
    smul(ab_inverse, ab_inverse),
)
defect_series = sadd(det_series, sscale(-1, rhs_series))
defect_second = 2 * defect_series[2]
expected_defect_second = F(
    1294370873331706238711800,
    84322645437596652728132481,
)
assert defect_second == expected_defect_second
assert defect_second > 0

print("verified: exact flag--Bell endpoint Gram and determinant")
print("verified: full-rank marginal product formula and strict scalar certificate")
print("verified: exact negative reciprocal-filter log curvature")
print("verified: unlogged ratio and determinant defect retain positive curvature")
