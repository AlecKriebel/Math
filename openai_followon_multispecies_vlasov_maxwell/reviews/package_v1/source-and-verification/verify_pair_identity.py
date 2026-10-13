#!/usr/bin/env python3
"""Exact cleared-denominator check of the generic pair cancellation.

No external packages are required. Polynomials are sparse dictionaries in
(a1,a2,a3,u1,u2,u3), with integer coefficients. Rotation covariance allows
n=(0,0,1); all polynomial identities are verified for generic a,u. Source
and receiver accelerations cancel separately by linearity before this check.
This checks a local algebraic identity, not the global PDE theorem.
"""
from __future__ import annotations

import hashlib
import json
import platform
from pathlib import Path

DIM = 6
ZERO_MONOMIAL = (0,) * DIM


class Poly:
    def __init__(self, terms=None):
        if isinstance(terms, int):
            self.terms = {} if not terms else {ZERO_MONOMIAL: terms}
        else:
            self.terms = {k: v for k, v in (terms or {}).items() if v}

    @staticmethod
    def variable(index):
        exponent = [0] * DIM
        exponent[index] = 1
        return Poly({tuple(exponent): 1})

    def __add__(self, other):
        if isinstance(other, int):
            other = Poly(other)
        terms = self.terms.copy()
        for key, value in other.terms.items():
            terms[key] = terms.get(key, 0) + value
        return Poly(terms)

    __radd__ = __add__

    def __neg__(self):
        return Poly({key: -value for key, value in self.terms.items()})

    def __sub__(self, other):
        return self + (-other if isinstance(other, Poly) else -Poly(other))

    def __rsub__(self, other):
        return Poly(other) + (-self)

    def __mul__(self, other):
        if isinstance(other, int):
            other = Poly(other)
        terms = {}
        for key1, value1 in self.terms.items():
            for key2, value2 in other.terms.items():
                key = tuple(x + y for x, y in zip(key1, key2))
                terms[key] = terms.get(key, 0) + value1 * value2
        return Poly(terms)

    __rmul__ = __mul__


def dot(left, right):
    return sum((x * y for x, y in zip(left, right)), Poly())


def scale(scalar, vector):
    return [scalar * x for x in vector]


def add(*vectors):
    return [sum((vector[i] for vector in vectors), Poly()) for i in range(3)]


def check_zero(name, vector, results):
    residual_sizes = [len(entry.terms) for entry in vector]
    if residual_sizes != [0, 0, 0]:
        raise AssertionError((name, residual_sizes))
    results[name] = residual_sizes


def main():
    # Basic engine checks independent of the target identity.
    x, y = Poly.variable(0), Poly.variable(1)
    assert not ((x + y) * (x - y) - x * x + y * y).terms
    assert not ((1 - x) + x - 1).terms

    a = [Poly.variable(i) for i in range(3)]
    u = [Poly.variable(i + 3) for i in range(3)]
    n = [Poly(0), Poly(0), Poly(1)]
    d = 1 - dot(n, u)
    D = 1 - dot(n, a)
    e = 1 - dot(a, u)
    qinv = 1 - dot(u, u)
    qXinv = 1 - dot(a, a)
    # k=kappa/D and N_0=M/D.
    kappa = add(scale(D, u), scale(-e, n))
    M = add(scale(d, a), scale(-D, u), scale(D - d, n))
    results = {}

    # n dot N_0=0, and the first displayed geometric identity.
    assert not dot(n, M).terms
    scalar_residual = dot(M, u) - d * (d - D) - D * qinv + e * d
    assert not scalar_residual.terms
    results["geometric_scalar_identity"] = 0

    # N_0+n(N_0 dot a)/D+k = (d/D)(a-n qXinv/D),
    # cleared by D^2.
    geometric_vector = add(
        scale(D, M),
        scale(dot(M, a), n),
        scale(D, kappa),
        scale(-d * D, a),
        scale(d * qXinv, n),
    )
    check_zero("geometric_vector_identity", geometric_vector, results)

    # Remaining identity after source and receiver accelerations cancel:
    # both sides are multiplied by r^2 d^2 D^3.
    lhs = scale(-D * D * qinv, kappa)
    rhs = add(
        scale(e * d * D, M),
        scale(e * d * dot(M, a), n),
        scale(d * D * (d - D), kappa),
        scale(-D * dot(M, u), kappa),
        scale(e * d * d * qXinv, n),
        scale(-e * d * d * D, a),
    )
    check_zero("signed_pair_identity", add(lhs, scale(Poly(-1), rhs)), results)

    # Receiver acceleration coefficients cancel identically, componentwise,
    # because kappa = D u-e n. This is the coefficient vector multiplying
    # the arbitrary scalar product with alpha_t.
    check_zero(
        "receiver_acceleration_cancellation",
        add(scale(-D, u), scale(e, n), kappa),
        results,
    )
    # Source acceleration terms are the identical three terms on both sides:
    # -b/(r d), -n(a dot b)/(r d D), -k(n dot b)/(r d^2).
    results["source_acceleration_cancellation"] = "identical linear terms"

    output = {
        "scope": "Generic algebraic source/receiver signed identity only",
        "arithmetic": "exact sparse integer polynomials; no tolerance",
        "rotation_reduction": "n=(0,0,1), generic a,u",
        "python": platform.python_version(),
        "checks": results,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
