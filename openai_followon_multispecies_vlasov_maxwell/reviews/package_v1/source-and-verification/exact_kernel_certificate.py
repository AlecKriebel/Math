#!/usr/bin/env python3
"""Exact polynomial and rational certificates for the signed VM kernel.

No third-party packages. Polynomial zero certificates are universal; random
rational tests below are supplementary checks of the assembled identity.
The proof uses rotation covariance to take the cone direction n=(0,0,1).
"""
from fractions import Fraction as F
from itertools import product
from random import Random
import json

NVAR = 6  # a1,a2,a3,u1,u2,u3
ZERO = (0,) * NVAR


class Poly:
    def __init__(self, v=0):
        self.c = v if isinstance(v, dict) else ({ZERO: F(v)} if v else {})
        self.c = {m: q for m, q in self.c.items() if q}

    def __add__(self, v):
        v = v if isinstance(v, Poly) else Poly(v)
        out = dict(self.c)
        for m, q in v.c.items():
            out[m] = out.get(m, F(0)) + q
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({m: -q for m, q in self.c.items()})

    def __sub__(self, v):
        return self + -Poly(v) if not isinstance(v, Poly) else self + -v

    def __rsub__(self, v):
        return Poly(v) + -self

    def __mul__(self, v):
        v = v if isinstance(v, Poly) else Poly(v)
        out = {}
        for m, p in self.c.items():
            for n, q in v.c.items():
                k = tuple(x + y for x, y in zip(m, n))
                out[k] = out.get(k, F(0)) + p * q
        return Poly(out)

    __rmul__ = __mul__

    def iszero(self):
        return not self.c


def variable(i):
    m = tuple(int(i == j) for j in range(NVAR))
    return Poly({m: F(1)})


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), 0)


def scale(q, v):
    return [q * x for x in v]


def add(*vs):
    return [sum(z) for z in zip(*vs)]


a = [variable(i) for i in range(3)]
u = [variable(i) for i in range(3, 6)]
n = [Poly(0), Poly(0), Poly(1)]
d, D, e = 1 - u[2], 1 - a[2], 1 - dot(a, u)
qs_inv2, qr_inv2 = 1 - dot(u, u), 1 - dot(a, a)
Nbar = add(scale(d, add(a, scale(-1, n))), scale(D, add(n, scale(-1, u))))

# cancellation.tex 89: denominator-cleared scalar identity.
scalar = dot(Nbar, u) - d * (d - D) - qs_inv2 * D + e * d
assert scalar.iszero()

# cancellation.tex 96-98: denominator-cleared vector identity.
vector = add(scale(D, Nbar), scale(dot(Nbar, a), n), scale(D * D, u),
             scale(-e * D, n), scale(-d * D, a), scale(d * qr_inv2, n))
assert all(v.iszero() for v in vector)

# Geometry requires n dot Nbar=0, for every a,u.
assert dot(n, Nbar).iszero()


def test_combined(a, u, A, b, r):
    """Direct first derivative of k0/(rd), all numbers exact rationals."""
    n = [F(0), F(0), F(1)]
    d, D, e = 1 - u[2], 1 - a[2], 1 - dot(a, u)
    tprime = d / D
    rprime = tprime - 1
    nprime = scale(1 / r, add(scale(tprime, add(a, scale(-1, n))),
                                    add(n, scale(-1, u))))
    aprime = scale(tprime, A)
    dprime = -dot(nprime, u) - dot(n, b)
    Dprime = -dot(nprime, a) - dot(n, aprime)
    eprime = -dot(aprime, u) - dot(a, b)
    k0 = add(u, scale(-e / D, n))
    k0prime = add(b, scale(-eprime / D + e * Dprime / (D * D), n),
                  scale(-e / D, nprime))
    primitive_prime = add(scale(1 / (r * d), k0prime),
                          scale(-rprime / (r * r * d) - dprime / (r * d * d), k0))

    def H(v):
        return add(v, scale(dot(a, v) / D, n))

    g = scale(1 / d, add(u, scale(-1, n)))
    guprime = add(scale(1 / d, b), scale(b[2] / (d * d), add(u, scale(-1, n))))
    source = add(scale(-1 / r, H(guprime)),
                 scale(-(1 - dot(u, u)) / (r * r * d), H(g)))
    rhs = add(scale(-1, primitive_prime),
              scale(e / (r * r * D * D), add(scale((1 - dot(a, a)) / D, n), scale(-1, a))),
              scale(dot(A, k0) / (r * D * D), n))
    assert source == rhs, (a, u, A, b, r, source, rhs)
    # Source electric kernel and force-to-branch conversion.
    electric = add(scale((1 - dot(u, u)) / (r*r*d*d*d), add(n, scale(-1, u))),
                   scale(1 / (r*d*d*d), add(scale(b[2], add(n, scale(-1, u))), scale(-d, b))))
    assert source == scale(1 / D, H(scale(D*d, electric)))


random = Random(362)
cases = 0
# Includes zero velocities, nearly null directions, identical source/receiver,
# opposite directions, and general independent signed accelerations.
velocities = [[F(0),F(0),F(0)], [F(0),F(0),F(999,1000)],
              [F(0),F(0),F(-999,1000)], [F(3,5),F(0),F(3,5)]]
for a,u in product(velocities, repeat=2):
    for A,b in product([[F(0)]*3,[F(1),F(-2),F(3)]], repeat=2):
        for r in [F(1,1000000), F(1), F(1000000)]:
            test_combined(a,u,A,b,r)
            cases += 1
for _ in range(100):
    a = [F(random.randrange(-3,4),10) for _ in range(3)]
    u = [F(random.randrange(-3,4),10) for _ in range(3)]
    A = [F(random.randrange(-10,11),7) for _ in range(3)]
    b = [F(random.randrange(-10,11),7) for _ in range(3)]
    r = F(random.randrange(1,100),11)
    test_combined(a,u,A,b,r)
    cases += 1
print(json.dumps({"universal_polynomial_residuals": [len(scalar.c)] + [len(v.c) for v in vector],
                  "exact_rational_combined_checks": cases,
                  "result": "PASS", "scope": "kinematic signed identity; not impulse estimates"}, indent=2))
