#!/usr/bin/env python3
"""Independent exact rational checks for the flow01 derivation.

Uses only the standard library. Variables are (p,x,R), where R=e^(-2t).
This validates algebra and sign certificates, not parabolic existence.
"""
from fractions import Fraction as F
import json
from pathlib import Path


class P:
    """Small sparse polynomial ring Q[p,x,R]."""
    def __init__(self, terms=0):
        if isinstance(terms, P):
            self.c = dict(terms.c)
        elif isinstance(terms, dict):
            self.c = {k: F(v) for k, v in terms.items() if v}
        else:
            self.c = {(0, 0, 0): F(terms)} if terms else {}

    def __add__(self, other):
        other = P(other)
        out = dict(self.c)
        for k, v in other.c.items():
            out[k] = out.get(k, F(0)) + v
        return P(out)

    __radd__ = __add__

    def __neg__(self):
        return P({k: -v for k, v in self.c.items()})

    def __sub__(self, other):
        return self + (-P(other))

    def __rsub__(self, other):
        return P(other) + (-self)

    def __mul__(self, other):
        other = P(other)
        out = {}
        for ka, va in self.c.items():
            for kb, vb in other.c.items():
                k = tuple(a + b for a, b in zip(ka, kb))
                out[k] = out.get(k, F(0)) + va * vb
        return P(out)

    __rmul__ = __mul__

    def __pow__(self, n):
        out = P(1)
        for _ in range(n):
            out = out * self
        return out

    def d(self, j):
        out = {}
        for k, v in self.c.items():
            if k[j]:
                kk = list(k)
                kk[j] -= 1
                out[tuple(kk)] = v * k[j]
        return P(out)

    def mean_x(self):
        out = {}
        for k, v in self.c.items():
            kk = (k[0], 0, k[2])
            out[kk] = out.get(kk, F(0)) + v / (k[1] + 1)
        return P(out)

    def at(self, **values):
        indexes = {"p": 0, "x": 1, "R": 2}
        out = {}
        for k, v in self.c.items():
            kk = list(k)
            for name, value in values.items():
                j = indexes[name]
                v *= F(value) ** k[j]
                kk[j] = 0
            out[tuple(kk)] = out.get(tuple(kk), F(0)) + v
        return P(out)

    def scalar(self):
        assert all(k == (0, 0, 0) for k in self.c)
        return self.c.get((0, 0, 0), F(0))


p = P({(1, 0, 0): 1})
x = P({(0, 1, 0): 1})
R = P({(0, 0, 1): 1})
eps, delta = F(1, 96), F(1, 4)
checks = []


def zero(name, q):
    assert not q.c, (name, q.c)
    checks.append(name)


def lap(q):
    return F(1, 2) * (x * (1 - x) * q.d(1).d(1) + (1 - 2*x) * q.d(1))


def generator(q):
    return lap(q) + q - q.mean_x()


# Solve in monomials rather than in the proof's spectral basis.
zero("generator on constant", generator(P(1)))
zero("generator on x", generator(x))
zero("generator on x^2", generator(x*x) - (-F(1, 3) + 2*x - 2*x*x))
a = -(1 - R) * F(1, 6) + (1 - R)*x + R*x*x
zero("true parameter-derivative initial data", a.at(R=1) - x*x)
zero("exact closed evolution residual", -2*R*a.d(2) - generator(a))
zero("conserved fiber mean", a.mean_x() - F(1, 3))
w = eps + delta*a
zero("horizontal initial data", w.at(R=1) - (eps + delta*x*x))
zero("horizontal evolution residual", -2*R*w.d(2) - generator(w))
zero("pole formula", w.at(x=0) - (eps - delta*F(1, 6)*(1 - R)))
zero("initial pole time derivative", (-2*R*w.d(2)).at(x=0, R=1) + F(1, 12))
pole = w.at(x=0, R=F(1, 2)).scalar()
assert pole == -F(1, 96)
zero("exact threshold", w.at(x=0, R=F(3, 4)))

# Initial global positivity, with a nonnegative-factor certificate on [0,1]^2.
A = 4*p + (eps + delta*x*x)*(1 - 2*p)
B = 2 + 2*delta*p*x*(2 - 3*x)
Q = 4*delta*delta*p*(1 - p)*(x**3)*(1 - x)
alo = eps + (4 - 2*eps - 2*delta)*p
blo = 2 - 2*delta
qup = 4*delta*delta*p
zero("A bound factorization", A - alo - delta*(x*x + 2*p*(1 - x*x)))
zero("B bound factorization", B - blo - 2*delta*((1 - p) + p*(1 - x)*(1 + 3*x)))
zero("Q bound factorization", qup - Q - 4*delta*delta*p*((1 - x)*(1 + x + x*x) + x**4 + p*x**3*(1 - x)))
zero("strict determinant lower bound", alo*blo - qup - (F(1, 64) + F(159, 32)*p))

# Frame/gauge diagnostic: a pure-base stationary weight has constant w.
zero("probability-flow pure-base gauge diagnostic", generator(P(1)))
rank = 2
printed_literal = lap(P(1)) + rank*P(1) - P(1).mean_x()
assert printed_literal.scalar() == 1
checks.append("literal printed +r*c disagrees with pure-base stationarity at rank two")

result = {
    "verdict": "all exact algebraic checks passed",
    "checks": checks,
    "number_of_checks": len(checks),
    "negative_horizontal_coefficient_at_t_log2_over2": str(pole),
    "initial_pole_derivative": "-1/12",
    "zero_threshold_exp_minus2t": "3/4",
    "strict_initial_determinant_bound": "1/64 + (159/32)*p",
    "limitations": [
        "The proof of scalar-flow frame invariance is mathematical, not machine-certified here.",
        "Parabolic existence and finite-time parameter regularity are classical analytic inputs.",
        "The nonlinear-family chain rule and measure derivative require smoothness and are justified in the review.",
        "No numerical simulation or numerical approximation is used."
    ]
}
Path(__file__).with_name("exact_results.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
