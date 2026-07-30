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

    def __truediv__(self, other):
        other = O.make(other)
        norm = (
            other.a * other.a
            - other.a * other.b
            + other.b * other.b
        )
        if not norm:
            raise ZeroDivisionError
        numerator = self * O(other.a - other.b, -other.b)
        return O(numerator.a / norm, numerator.b / norm)

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


# Raw-defect convexity fails even along a diagonal reciprocal filter,
# although the unlogged normalized ratio is convex there.  Here
# x=10, y=1/10 and x_t=x exp(2t), y_t=y exp(-2t).
x_defect = F(10)
y_defect = F(1, 10)
z_defect = x_defect * y_defect
x2_defect_series = (
    x_defect * x_defect,
    4 * x_defect * x_defect,
    8 * x_defect * x_defect,
)
y2_defect_series = (
    y_defect * y_defect,
    -4 * y_defect * y_defect,
    8 * y_defect * y_defect,
)
s_defect_series = sadd(x2_defect_series, y2_defect_series)
a_defect_series = sadd((F(1), F(0), F(0)), x2_defect_series)
b_defect_series = sadd((F(1), F(0), F(0)), y2_defect_series)
p_defect_series = sadd(
    (
        15 * z_defect * z_defect - 16 * z_defect,
        F(0),
        F(0),
    ),
    sscale(32, s_defect_series),
)
ab_defect_inverse = sinv(smul(a_defect_series, b_defect_series))
det_defect_series = sscale(
    F(1, 324),
    smul(p_defect_series, ab_defect_inverse),
)
rhs_defect_series = sscale(
    F(729, 1024) * z_defect * z_defect,
    smul(ab_defect_inverse, ab_defect_inverse),
)
raw_defect_series = sadd(
    det_defect_series,
    sscale(-1, rhs_defect_series),
)
assert raw_defect_series[0] == F(5797901743, 59938790976)
assert raw_defect_series[0] > 0
raw_defect_second = 2 * raw_defect_series[2]
assert raw_defect_second == F(
    -2904456294125,
    85983132198681,
)
assert raw_defect_second < 0

s0_defect = x_defect * x_defect + y_defect * y_defect
s1_defect = 4 * (x_defect * x_defect - y_defect * y_defect)
s2_defect = 16 * (x_defect * x_defect + y_defect * y_defect)
p0_defect = 15 * z_defect * z_defect - 16 * z_defect + 32 * s0_defect
q0_defect = 1 + z_defect * z_defect + s0_defect
ratio_defect_second = (
    F(256, 59049)
    / (z_defect * z_defect)
    * (
        64 * s1_defect * s1_defect
        + (32 * q0_defect + p0_defect) * s2_defect
    )
)
assert ratio_defect_second == F(3292929645568, 36905625)
assert ratio_defect_second > 0


# A transverse reciprocal filter leaves the displayed two-parameter
# pencil, and it also destroys convexity of the unlogged ratio.  The
# following Pythagorean parameters keep the normalized frame inside
# Q(omega):
#
#   x=40/399, sqrt(1+x^2)=401/399,
#   y=400/39999, sqrt(1+y^2)=40001/39999.
def pevaluate(polynomial, x_value, y_value):
    return sum(
        (
            coefficient * x_value**i * y_value**j
            for (i, j), coefficient in polynomial.items()
        ),
        ZERO,
    )


def oevaluate_vector(vector, x_value, y_value):
    return {
        position: pevaluate(value, x_value, y_value)
        for position, value in vector.items()
    }


def oscale_vector(coefficient, vector):
    coefficient = O.make(coefficient)
    return {
        position: coefficient * value
        for position, value in vector.items()
        if coefficient * value
    }


def oadd_vectors(*terms):
    out = {}
    for coefficient, vector in terms:
        coefficient = O.make(coefficient)
        for position, value in vector.items():
            out[position] = out.get(position, ZERO) + coefficient * value
            if not out[position]:
                del out[position]
    return out


def oinner_vector(left, right):
    return sum(
        (
            value.conjugate() * right.get(position, ZERO)
            for position, value in left.items()
        ),
        ZERO,
    )


def oouter(left, right, coefficient=ONE):
    coefficient = O.make(coefficient)
    return {
        (i, j): coefficient * a * b.conjugate()
        for i, a in left.items()
        for j, b in right.items()
        if coefficient * a * b.conjugate()
    }


def oadd_sparse(*terms):
    out = {}
    for coefficient, matrix in terms:
        coefficient = O.make(coefficient)
        for key, value in matrix.items():
            out[key] = out.get(key, ZERO) + coefficient * value
            if not out[key]:
                del out[key]
    return out


def opartial_trace(matrix, traced):
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
        out[key] = out.get(key, ZERO) + value
        if not out[key]:
            del out[key]
    return out


def ohs_inner(left, right):
    return sum(
        (
            value.conjugate() * right.get(key, ZERO)
            for key, value in left.items()
        ),
        ZERO,
    )


def oendpoint_bilinear(left, right):
    out = ZERO
    for size in range(4):
        for sites in combinations(range(3), size):
            out += F(-1, 2) ** size * ohs_inner(
                opartial_trace(left, sites),
                opartial_trace(right, sites),
            )
    return out


def odense_mul(left, right):
    return [
        [
            sum(
                (left[i][k] * right[k][j] for k in range(len(right))),
                ZERO,
            )
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def odense_scale(coefficient, matrix):
    coefficient = O.make(coefficient)
    return [
        [coefficient * value for value in row]
        for row in matrix
    ]


def oapply_local(operator, vector, site):
    out = {}
    for old_index, value in vector.items():
        old_digits = list(digits(old_index))
        for new_symbol in range(3):
            coefficient = operator[new_symbol][old_digits[site]]
            if not coefficient:
                continue
            new_digits = old_digits[:]
            new_digits[site] = new_symbol
            new_index = index(new_digits)
            out[new_index] = (
                out.get(new_index, ZERO) + coefficient * value
            )
            if not out[new_index]:
                del out[new_index]
    return out


def ocolumns_gram(frame, operator, site):
    images = [oapply_local(operator, vector, site) for vector in frame]
    return [
        [oinner_vector(left, right) for right in images]
        for left in frame
    ]


def ocolumns_right_multiply(frame, matrix):
    return [
        oadd_vectors(
            *((matrix[k][j], frame[k]) for k in range(len(frame)))
        )
        for j in range(len(matrix[0]))
    ]


def oframe_derivatives(frame, operator, sign, site):
    operator_squared = odense_mul(operator, operator)
    a = odense_scale(F(1, 3), ocolumns_gram(frame, operator, site))
    b = odense_scale(
        F(1, 3), ocolumns_gram(frame, operator_squared, site)
    )
    acted = [oapply_local(operator, vector, site) for vector in frame]
    acted_twice = [
        oapply_local(operator_squared, vector, site) for vector in frame
    ]
    frame_a = ocolumns_right_multiply(frame, a)
    first = [
        oadd_vectors((sign, acted[j]), (-sign, frame_a[j]))
        for j in range(2)
    ]
    a_squared = odense_mul(a, a)
    correction = [
        [3 * a_squared[i][j] - 2 * b[i][j] for j in range(2)]
        for i in range(2)
    ]
    acted_a = ocolumns_right_multiply(acted, a)
    frame_correction = ocolumns_right_multiply(frame, correction)
    second = [
        oadd_vectors(
            (1, acted_twice[j]),
            (-2, acted_a[j]),
            (1, frame_correction[j]),
        )
        for j in range(2)
    ]
    return frame, first, second


def osadd(left, right):
    return tuple(left[i] + right[i] for i in range(3))


def osscale(coefficient, series):
    coefficient = O.make(coefficient)
    return tuple(coefficient * value for value in series)


def osmul(left, right):
    return tuple(
        sum(
            (left[j] * right[i - j] for j in range(i + 1)),
            ZERO,
        )
        for i in range(3)
    )


def osinv(series):
    a, b, c = series
    return (
        ONE / a,
        -b / (a * a),
        b * b / (a * a * a) - c / (a * a),
    )


def oseries_matrix(value, first, second):
    return [
        [
            (value[i][j], first[i][j], second[i][j] * F(1, 2))
            for j in range(len(value[0]))
        ]
        for i in range(len(value))
    ]


def odeterminant_series(matrix):
    size = len(matrix)
    out = (ZERO, ZERO, ZERO)
    for permutation in permutations(range(size)):
        term = (ONE, ZERO, ZERO)
        for row, column in enumerate(permutation):
            term = osmul(term, matrix[row][column])
        out = osadd(
            out,
            osscale(permutation_sign(permutation), term),
        )
    return out


def oendpoint_derivative_matrices(u_levels, w_levels):
    endpoint_levels = ([], [], [])
    for a in range(2):
        for b in range(2):
            u0_level, u1_level, u2_level = (
                levels[a] for levels in u_levels
            )
            w0_level, w1_level, w2_level = (
                levels[b] for levels in w_levels
            )
            endpoint_levels[0].append(
                oouter(u0_level, w0_level, F(1, 3))
            )
            endpoint_levels[1].append(
                oadd_sparse(
                    (F(1, 3), oouter(u1_level, w0_level)),
                    (F(1, 3), oouter(u0_level, w1_level)),
                )
            )
            endpoint_levels[2].append(
                oadd_sparse(
                    (F(1, 3), oouter(u2_level, w0_level)),
                    (F(2, 3), oouter(u1_level, w1_level)),
                    (F(1, 3), oouter(u0_level, w2_level)),
                )
            )
    e0, e1, e2 = endpoint_levels
    h0 = [[ZERO for _ in range(4)] for _ in range(4)]
    h1 = [[ZERO for _ in range(4)] for _ in range(4)]
    h2 = [[ZERO for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            h0[i][j] = oendpoint_bilinear(e0[i], e0[j])
            h1[i][j] = (
                oendpoint_bilinear(e1[i], e0[j])
                + oendpoint_bilinear(e0[i], e1[j])
            )
            h2[i][j] = (
                oendpoint_bilinear(e2[i], e0[j])
                + 2 * oendpoint_bilinear(e1[i], e1[j])
                + oendpoint_bilinear(e0[i], e2[j])
            )
    return h0, h1, h2


def omarginal_derivative_series(levels):
    f0, f1, f2 = levels
    p0 = {}
    p1 = {}
    p2 = {}
    for column in range(2):
        p0 = oadd_sparse(
            (1, p0), (F(1, 3), oouter(f0[column], f0[column]))
        )
        p1 = oadd_sparse(
            (1, p1),
            (F(1, 3), oouter(f1[column], f0[column])),
            (F(1, 3), oouter(f0[column], f1[column])),
        )
        p2 = oadd_sparse(
            (1, p2),
            (F(1, 3), oouter(f2[column], f0[column])),
            (F(2, 3), oouter(f1[column], f1[column])),
            (F(1, 3), oouter(f0[column], f2[column])),
        )
    out = []
    for site in range(3):
        traced = tuple(i for i in range(3) if i != site)
        reduced = [
            opartial_trace(projector, traced)
            for projector in (p0, p1, p2)
        ]
        dense = [
            [
                [
                    reduced[level].get((i, j), ZERO)
                    for j in range(3)
                ]
                for i in range(3)
            ]
            for level in range(3)
        ]
        out.append(oseries_matrix(*dense))
    return out


x_exact = F(40, 399)
y_exact = F(400, 39999)
u_exact = [
    oevaluate_vector(u0, x_exact, y_exact),
    oscale_vector(
        F(399, 401), oevaluate_vector(u1, x_exact, y_exact)
    ),
]
w_exact = [
    oevaluate_vector(w0, x_exact, y_exact),
    oscale_vector(
        F(39999, 40001), oevaluate_vector(w1, x_exact, y_exact)
    ),
]
assert all(
    oinner_vector(u_exact[i], u_exact[j])
    == (O(3) if i == j else ZERO)
    for i in range(2)
    for j in range(2)
)
assert all(
    oinner_vector(w_exact[i], w_exact[j])
    == (O(3) if i == j else ZERO)
    for i in range(2)
    for j in range(2)
)
assert all(
    oinner_vector(left, right) == ZERO
    for left in u_exact
    for right in w_exact
)

off_diagonal_02 = [
    [ZERO, ZERO, ONE],
    [ZERO, ZERO, ZERO],
    [ONE, ZERO, ZERO],
]
u_derivatives = oframe_derivatives(
    u_exact, off_diagonal_02, 1, 1
)
w_derivatives = oframe_derivatives(
    w_exact, off_diagonal_02, -1, 1
)
h_derivatives = oendpoint_derivative_matrices(
    u_derivatives, w_derivatives
)
h_series = odeterminant_series(oseries_matrix(*h_derivatives))
marginal_series = (
    omarginal_derivative_series(u_derivatives)
    + omarginal_derivative_series(w_derivatives)
)
marginal_product_series = (ONE, ZERO, ZERO)
for matrix_series in marginal_series:
    marginal_product_series = osmul(
        marginal_product_series,
        odeterminant_series(matrix_series),
    )

unscaled_ratio_series = osmul(
    h_series, osinv(marginal_product_series)
)
normalized_ratio_series = osscale(
    F(2**22, 3**18), unscaled_ratio_series
)
transverse_ratio_second = 2 * normalized_ratio_series[2]
assert transverse_ratio_second.b == 0
assert transverse_ratio_second.a < 0

print("verified: exact flag--Bell endpoint Gram and determinant")
print("verified: full-rank marginal product formula and strict scalar certificate")
print("verified: exact negative reciprocal-filter log curvature")
print("verified: positive diagonal-path ratio and defect curvature")
print("verified: exact negative diagonal raw-defect curvature")
print(
    "verified: exact negative transverse unlogged-ratio curvature",
    transverse_ratio_second.a,
)
