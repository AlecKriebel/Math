#!/usr/bin/env python3
"""Small independent exact audit; standard library only, no sampled ODE proof.

The field implementation certifies identities in Q(sqrt(3)). The second
implementation reduces words in C4 *_{C2} C6 with an independent central
additive parameter f_theta, where theta is measured in multiples of pi.
This checks consequences of the analytic commutation lemma, not that lemma
itself. Analytic justification is in REPORT.md.
"""
from fractions import Fraction as F
from dataclasses import dataclass
import json


@dataclass(frozen=True)
class K:
    a: F = F(0)
    b: F = F(0)

    @staticmethod
    def of(x):
        return x if isinstance(x, K) else K(F(x))

    def __add__(self, other):
        o = K.of(other)
        return K(self.a + o.a, self.b + o.b)

    __radd__ = __add__

    def __neg__(self):
        return K(-self.a, -self.b)

    def __sub__(self, other):
        return self + -K.of(other)

    def __rsub__(self, other):
        return K.of(other) + -self

    def __mul__(self, other):
        o = K.of(other)
        return K(self.a * o.a + 3 * self.b * o.b,
                 self.a * o.b + self.b * o.a)

    __rmul__ = __mul__

    def inv(self):
        d = self.a * self.a - 3 * self.b * self.b
        assert d != 0
        return K(self.a / d, -self.b / d)

    def __truediv__(self, other):
        return self * K.of(other).inv()


def mat(rows):
    return tuple(tuple(K.of(x) for x in row) for row in rows)


def mm(a, b):
    return tuple(tuple(sum((a[i][k] * b[k][j] for k in range(2)), K())
                       for j in range(2)) for i in range(2))


def mp(a, n):
    assert n >= 0
    out = I
    for _ in range(n):
        out = mm(out, a)
    return out


def det(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def mi(a):
    d = det(a)
    return tuple(tuple(x / d for x in row) for row in
                 ((a[1][1], -a[0][1]), (-a[1][0], a[0][0])))


def fnorm2(a):
    return sum((x*x for row in a for x in row), K())


I = mat([[1, 0], [0, 1]])
minusI = mat([[-1, 0], [0, -1]])
Q = mat([[0, 1], [-1, 0]])
R = mat([[0, 1], [-1, 1]])
U = mat([[1, 1], [0, 1]])
V = mat([[1, 0], [-1, 1]])
root3 = K(F(0), F(1))
P = mat([[1, F(-1, 2)], [0, root3/2]])
C = mat([[F(1, 2), root3/2], [-root3/2, F(1, 2)]])

assert mm(mm(U, V), U) == Q
assert mm(U, V) == R
assert mp(Q, 2) == mp(R, 3) == minusI
assert mp(Q, 4) == mp(R, 6) == I
assert mm(mi(R), Q) == U
assert mm(mi(Q), mp(R, 2)) == V
assert mm(mm(P, R), mi(P)) == C
assert det(P) == root3/2
assert fnorm2(mi(P)) == K.of(F(8, 3))
assert fnorm2(R) == K.of(3)
# Stronger independent conjugacy-radius check; both inputs have the same bound.
assert fnorm2(mm(R, mi(P))) == K.of(F(8, 3))
assert F(8, 3) < 4 and 3 < 4
assert F(9, 4) < 4
# Manuscript's deliberately loose radius estimates, all rational/exact.
assert F(3, 2) * F(1, 64) < F(1, 32)
assert 2 * F(1, 512) < F(1, 64)
assert 4 * F(1, 512) < F(1, 64)
assert F(1, 4096) < F(1, 2048) < F(1, 1024) < F(1, 512)
assert F(1, 512) < F(1, 64) < F(1, 32) < F(1, 16) < F(1, 4)


@dataclass(frozen=True)
class G:
    angle: F = F(0)  # f_(angle*pi), independent infinite additive parameter
    central: int = 0  # iota power modulo 2
    syllables: tuple = ()  # alternating ('x',1), ('y',1 or 2)

    def __mul__(self, other):
        c = self.central + other.central
        out = list(self.syllables)
        for letter, exponent in other.syllables:
            if out and out[-1][0] == letter:
                exponent += out.pop()[1]
            order = 2 if letter == 'x' else 3
            carry, exponent = divmod(exponent, order)
            c += carry
            if exponent:
                out.append((letter, exponent))
        return G(self.angle + other.angle, c % 2, tuple(out))

    def inverse(self):
        out = G(-self.angle, self.central)
        for letter, exponent in reversed(self.syllables):
            order = 2 if letter == 'x' else 3
            carry, remainder = divmod(-exponent, order)
            out = out * G(F(0), carry % 2,
                          ((letter, remainder),) if remainder else ())
        return out

    def power(self, n):
        g = self if n >= 0 else self.inverse()
        out = G()
        for _ in range(abs(n)):
            out = out * g
        return out


x, y, iota = G(syllables=(('x', 1),)), G(syllables=(('y', 1),)), G(central=1)
X, Y = G(F(1, 2))*x, G(F(1, 3))*y
A, B = Y.inverse()*X, X.inverse()*Y.power(2)
assert x.power(2) == y.power(3) == iota
assert x.power(4) == y.power(6) == G()
assert X.power(2) == Y.power(3) == G(F(1), 1)
assert A*B == Y
assert A*B*A == B*A*B == X
assert (A*B).power(6) == G(F(2))
assert A.inverse()*B.inverse()*A.inverse() == B.inverse()*A.inverse()*B.inverse()
for g in [x, y, X, Y, A, B, A*B*A]:
    assert g*g.inverse() == g.inverse()*g == G()

# Adverse control 1: f_(2*pi) must not be simplified globally to identity.
# A profile value 1/2 produces a half-turn for this parameter; rotations
# inside the transition annulus can therefore be nontrivial.
assert G(F(2)) != G()
assert (F(2)*F(1, 2)) % 2 == 1

# Adverse control 2: the matched cancellation angles are essential.
badY = G(F(1, 2))*y
badA, badB = badY.inverse()*X, X.inverse()*badY.power(2)
assert X.power(2) != badY.power(3)
assert badA*badB*badA != badB*badA*badB

# Adverse control 3: local support alone cannot give global commutation.
# Permutations compose right to left. f is supported in D={0,1}, but g
# sends D elsewhere; outside-D points can enter the support.
def pm(a, b):
    return tuple(a[b[k]] for k in range(len(a)))

f = (1, 0, 2, 3)
g = (2, 3, 0, 1)
assert all(f[k] == k for k in (2, 3))
assert pm(f, g) != pm(g, f)

print(json.dumps({
    'verdict': 'PASS',
    'arithmetic': 'exact rational and Q(sqrt(3)); no floating point',
    'matrix_identities': 'PASS',
    'radii_inequalities': 'PASS',
    'formal_commuting_parameter_group_identities': 'PASS',
    'simultaneous_inverse_braid_identity': 'PASS',
    'adverse_controls': {
        'full_cutoff_turn_not_global_identity': 'detected',
        'wrong_cancellation_angle_breaks_braid': 'detected',
        'missing_disk_preservation_breaks_global_commutation': 'detected'
    },
    'limits': 'Does not certify analytic flow or mapping-class facts; see independent prose proof.'
}, indent=2))
