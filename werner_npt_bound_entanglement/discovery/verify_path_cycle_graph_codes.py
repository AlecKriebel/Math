#!/usr/bin/env python3
"""Exact verifier for the constant-syndrome cycle theorem.

Only Python's standard library is used.  Elements of Z[omega],
omega^2 + omega + 1 = 0, are stored as pairs (a,b) representing
a+b*omega.
"""

from fractions import Fraction
from itertools import product


class Eis(tuple):
    def __new__(cls, a=0, b=0):
        return tuple.__new__(cls, (int(a), int(b)))

    @staticmethod
    def coerce(other):
        return other if isinstance(other, Eis) else Eis(other)

    def __add__(self, other):
        other = self.coerce(other)
        return Eis(self[0] + other[0], self[1] + other[1])

    __radd__ = __add__

    def __neg__(self):
        return Eis(-self[0], -self[1])

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) + (-self)

    def __mul__(self, other):
        other = self.coerce(other)
        a, b = self
        c, d = other
        return Eis(a * c - b * d, a * d + b * c - b * d)

    __rmul__ = __mul__

    def conjugate(self):
        return Eis(self[0] - self[1], -self[1])


ZERO = Eis()
ONE = Eis(1)
OMEGA_POWERS = (ONE, Eis(0, 1), Eis(-1, -1))
STATES = tuple((x, y) for x in range(3) for y in range(3))
STATE_INDEX = {state: i for i, state in enumerate(STATES)}


def omega_power(k):
    return OMEGA_POWERS[k % 3]


def transfer(a, psi):
    """The 9-state cycle transfer M_{a,psi} for syndrome s_i=1."""
    matrix = [[ZERO for _ in STATES] for _ in STATES]
    for i, (x, y) in enumerate(STATES):
        for z in range(3):
            j = STATE_INDEX[(y, z)]
            local_weight = -1 if y == 0 and (x + z + a) % 3 == 0 else 2
            matrix[i][j] = local_weight * omega_power(psi * y)
    return matrix


def identity_matrix(n):
    return [[ONE if i == j else ZERO for j in range(n)] for i in range(n)]


def matmul(left, right):
    n = len(left)
    return [
        [
            sum((left[i][k] * right[k][j] for k in range(n)), ZERO)
            for j in range(n)
        ]
        for i in range(n)
    ]


def trace(matrix):
    return sum((matrix[i][i] for i in range(len(matrix))), ZERO)


def characteristic_coefficients(matrix):
    """Return [1,c1,...,cd] for det(lambda I-M).

    Newton identities are exact over Z[omega].  Divisibility by k is
    checked at every step.
    """
    d = len(matrix)
    power = identity_matrix(d)
    power_sums = []
    for _ in range(d):
        power = matmul(power, matrix)
        power_sums.append(trace(power))

    coefficients = [ONE]
    for k in range(1, d + 1):
        numerator = sum(
            (
                coefficients[k - i] * power_sums[i - 1]
                for i in range(1, k + 1)
            ),
            ZERO,
        )
        assert numerator[0] % k == 0 and numerator[1] % k == 0
        coefficients.append(Eis(-numerator[0] // k, -numerator[1] // k))
    return coefficients


def traces_through(matrix, n_max):
    power = identity_matrix(len(matrix))
    values = [trace(power)]
    for _ in range(n_max):
        power = matmul(power, matrix)
        values.append(trace(power))
    return values


def direct_cycle_k(n, a, b):
    """Definition-level evaluation of K for C_n and s=(1,...,1)."""
    total = 0
    for word in product(range(3), repeat=n):
        if sum(word) % 3 != (-b) % 3:
            continue
        weight = 0
        for i, middle in enumerate(word):
            z_label = (word[(i - 1) % n] + word[(i + 1) % n] + a) % 3
            if (middle, z_label) != (0, 0):
                weight += 1
        total += (-1) ** (n - weight) * 2**weight
    return total


def transfer_cycle_k(matrices, n, a, b):
    value = ZERO
    for psi in range(3):
        z_value = traces_through(matrices[(a, psi)], n)[n]
        value += omega_power(psi * b) * z_value
    assert value[0] % 3 == 0 and value[1] == 0
    return value[0] // 3


def twice_real(value):
    """Return 2 Re(a+b*omega)=2a-b."""
    return 2 * value[0] - value[1]


def polynomial_value(coefficients, x):
    value = 0
    for coefficient in coefficients:
        value = value * x + coefficient
    return value


def translate_polynomial(coefficients, shift):
    """Coefficients, low degree first, of p(v+shift)."""
    result = [0] * len(coefficients)
    for degree, coefficient in enumerate(coefficients):
        binomial = 1
        for k in range(degree + 1):
            if k:
                binomial = binomial * (degree - k + 1) // k
            result[k] += coefficient * binomial * shift ** (degree - k)
    return result


def polynomial_add(left, right):
    size = max(len(left), len(right))
    result = [0] * size
    for i in range(size):
        result[i] = (
            (left[i] if i < len(left) else 0)
            + (right[i] if i < len(right) else 0)
        )
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def polynomial_scale(coefficients, scalar):
    return [scalar * coefficient for coefficient in coefficients]


def polynomial_multiply(left, right):
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return result


def main():
    expected_degree_five = {
        (0, 0): [1, -3, -12, 0, 36, 108],
        (0, 1): [1, 3, 6, 36, 36, 108],
        (0, 2): [1, 3, 6, 36, 36, 108],
        (1, 0): [1, -6, 6, -18, 36, 108],
        (1, 1): [1, Eis(0, 0), Eis(0, 6), Eis(-18, -18), 36, 108],
        (1, 2): [1, Eis(0, 0), Eis(-6, -6), Eis(0, 18), 36, 108],
    }

    matrices = {}
    for key, expected in expected_degree_five.items():
        matrices[key] = transfer(*key)
        expected_eis = [Eis.coerce(x) for x in expected] + [ZERO] * 4
        assert characteristic_coefficients(matrices[key]) == expected_eis

    # Definition-level check, independent of the transfer contraction.
    for n in range(3, 7):
        for a in range(2):
            for b in range(3):
                assert direct_cycle_k(n, a, b) == transfer_cycle_k(
                    matrices, n, a, b
                )

    # The four fixed-line endpoint numerators
    # Delta_{a,b}=2K_{0,0}+K_{a,b}.
    z00 = traces_through(matrices[(0, 0)], 15)
    z01 = traces_through(matrices[(0, 1)], 15)
    z10 = traces_through(matrices[(1, 0)], 15)
    z11 = traces_through(matrices[(1, 1)], 15)

    expected_deltas = {
        3: (54, 54, 0, 54),
        4: (882, 882, 1098, 1026),
        5: (2430, 2430, 2430, 2430),
        6: (18738, 19602, 20034, 22302),
        7: (60102, 60102, 64638, 60102),
        8: (396738, 443394, 427842, 440802),
        9: (1614006, 1683990, 1736478, 1736478),
        10: (9464850, 10689570, 10596258, 10417410),
        11: (41329926, 45499806, 45243198, 45756414),
        12: (223985250, 252935298, 255023154, 252468738),
        13: (1031078646, 1169139582, 1160951454, 1162771038),
        14: (5394974706, 6202555074, 6220191042, 6228449154),
        15: (25611873894, 29678381694, 29678381694, 29603428830),
    }

    for n, expected in expected_deltas.items():
        delta_01 = (z00[n] + z01[n])[0]
        delta_1b = []
        for b in range(3):
            rotated = omega_power(b) * z11[n]
            numerator = (
                2 * z00[n][0]
                + 4 * z01[n][0]
                + z10[n][0]
                + twice_real(rotated)
            )
            assert numerator % 3 == 0
            delta_1b.append(numerator // 3)
        assert (delta_01, *delta_1b) == expected

    # Exact endpoint/root-isolation arithmetic used in the proof.
    p00_cubic = [1, -3, -6, -18]
    p10 = [1, -6, 6, -18, 36, 108]
    assert polynomial_value(p00_cubic, Fraction(49, 10)) < 0
    assert polynomial_value(p00_cubic, 5) > 0
    assert polynomial_value(p10, 5) < 0
    assert polynomial_value(p10, Fraction(51, 10)) > 0

    # For p01, the no-root-on-or-outside-|z|=4 calculation reduces to
    # g(16+v), whose coefficients must all be positive.
    g_low_first = [
        55427328,
        -36951552,
        6158592,
        -233280,
        90720,
        -12960,
        180,
        -60,
        5,
    ]
    shifted_g = [
        829776128,
        2044037632,
        808017152,
        143116480,
        14081120,
        828640,
        29300,
        580,
        5,
    ]
    assert translate_polynomial(g_low_first, 16) == shifted_g
    assert all(coefficient > 0 for coefficient in shifted_g)

    # Verify 4AC-B^2 = 12 r^2 g(r^2), coefficient by coefficient.
    a_poly = [0, 0, -15552, 0, 0, 0, 0, 0, 24]
    b_poly = [0, -7776, 0, -2592, 0, 0, 0, 36, 0, 6]
    c_poly = [
        -11664,
        0,
        6480,
        0,
        -1296,
        0,
        36,
        0,
        -3,
        0,
        1,
    ]
    left_side = polynomial_add(
        polynomial_scale(polynomial_multiply(a_poly, c_poly), 4),
        polynomial_scale(polynomial_multiply(b_poly, b_poly), -1),
    )
    g_of_r_squared = [0] * (2 * (len(g_low_first) - 1) + 1)
    for degree, coefficient in enumerate(g_low_first):
        g_of_r_squared[2 * degree] = coefficient
    right_side = polynomial_scale([0, 0] + g_of_r_squared, 12)
    assert left_side == right_side

    # The two Rouche estimates and the two eventual-positivity thresholds.
    assert Fraction(64 + 24 + 52, 1) + Fraction(108, 5) < 256
    assert 384 + 288 + 144 + 108 < 1024
    assert Fraction(49, 10) ** 9 > (
        4 * Fraction(5, 2) ** 9 + 5 * 4**9
    )
    assert Fraction(8, 2**16) + 34 * Fraction(4, 5) ** 16 < 1

    print("verified: direct sums agree with the cycle transfer through n=6")
    print("verified: transfer characteristic polynomials")
    print("verified: exact fixed-line table n=3,...,15")
    print("verified: exact root and eventual-positivity certificates")


if __name__ == "__main__":
    main()
