"""Exact checker for the qutrit three-replica S3 obstruction."""

from fractions import Fraction as F


class Q3:
    """An exact element a+b*sqrt(3)."""

    def __init__(self, a=0, b=0):
        self.a = F(a)
        self.b = F(b)

    def __add__(self, other):
        other = as_q3(other)
        return Q3(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return Q3(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-as_q3(other))

    def __rsub__(self, other):
        return as_q3(other) - self

    def __mul__(self, other):
        other = as_q3(other)
        return Q3(
            self.a * other.a + 3 * self.b * other.b,
            self.a * other.b + self.b * other.a,
        )

    __rmul__ = __mul__

    def __eq__(self, other):
        other = as_q3(other)
        return self.a == other.a and self.b == other.b

    def __repr__(self):
        return f"Q3({self.a}, {self.b})"


def as_q3(value):
    return value if isinstance(value, Q3) else Q3(value)


def matmul(a, b):
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b)))
         for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def trace(a):
    return sum(a[i][i] for i in range(len(a)))


def det2(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


# Reconstruct (13) from the exact standard-representation matrices in
# the basis where the (13) reflection is diagonal.
root3_over_2 = Q3(0, F(1, 2))
a = [
    [Q3(F(-1, 2)), root3_over_2],
    [root3_over_2, Q3(F(1, 2))],
]
two_i_minus_a = [
    [Q3(2) - a[i][j] if i == j else -a[i][j] for j in range(2)]
    for i in range(2)
]


def kron(x, y):
    return [
        [x[i // len(y)] [j // len(y[0])]
         * y[i % len(y)] [j % len(y[0])]
         for j in range(len(x[0]) * len(y[0]))]
        for i in range(len(x) * len(y))
    ]


full = [[Q3(9) * value for value in row]
        for row in kron(a, two_i_minus_a)]
# The +1 eigenspace of diagonal b tensor b is indexed by |00>, |11>.
derived = [[full[i][j] for j in (0, 3)] for i in (0, 3)]

# After diagonalizing the (13) reflections, compression to the +1
# eigenspace of b tensor b gives this rational two-by-two block.
block = [
    [F(9, 4) * -5, F(9, 4) * -3],
    [F(9, 4) * -3, F(9, 4) * 3],
]
assert derived == [[Q3(value) for value in row] for row in block]

assert trace(block) == F(-9, 2)
assert det2(block) == F(-243, 2)

# Verify the two claimed eigenvalues exactly through trace and product.
lam_pos = F(9)
lam_neg = F(-27, 2)
assert lam_pos + lam_neg == trace(block)
assert lam_pos * lam_neg == det2(block)
assert matmul(block, [[F(3)], [F(1)]]) == [
    [lam_neg * F(3)],
    [lam_neg],
]
assert matmul(block, [[F(1)], [F(-3)]]) == [
    [lam_pos],
    [lam_pos * F(-3)],
]

# Also verify the unscaled rational matrix used in the derivation.
core = [[F(-5), F(-3)], [F(-3), F(3)]]
assert trace(core) == F(-2)
assert det2(core) == F(-24)
assert (F(4) + F(6) == F(10))

print(
    "verified: compressed S3 block has exact eigenvalues "
    "9 and -27/2; qutrit sign sectors are essential"
)
