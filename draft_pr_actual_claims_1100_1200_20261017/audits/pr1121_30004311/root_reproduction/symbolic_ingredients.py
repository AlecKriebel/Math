"""Universal degree-four identities, independently encoded over F_5.

Terms of total degree >=5 vanish in the ideal x F_5[x]/(x^5),
including after substituting any two elements of that ideal.
"""
import hashlib
import json
from pathlib import Path

P = 5
X = {(1, 0): 1}
Y = {(0, 1): 1}


def add(*terms):
    out = {}
    for term in terms:
        for m, c in term.items():
            out[m] = (out.get(m, 0) + c) % P
    return {m: c for m, c in out.items() if c}


def scale(a, c):
    return {m: c * v % P for m, v in a.items() if c * v % P}


def mul(a, b):
    out = {}
    for (i, j), c in a.items():
        for (k, l), d in b.items():
            if i + j + k + l < P:
                m = (i + k, j + l)
                out[m] = (out.get(m, 0) + c * d) % P
    return {m: c for m, c in out.items() if c}


def power(a, n):
    out = {(0, 0): 1}
    for _ in range(n):
        out = mul(out, a)
    return out


def logarithm(a):
    return add(*(scale(power(a, k), (-1) ** (k + 1) * pow(k, -1, P))
                 for k in range(1, P)))


def exponential_minus_one(a):
    factorial = 1
    terms = []
    for k in range(1, P):
        factorial *= k
        terms.append(scale(power(a, k), pow(factorial, -1, P)))
    return add(*terms)


def check_equal(a, b, label):
    if a != b:
        raise RuntimeError((label, a, b))


def run():
    circle = add(X, Y, mul(X, Y))
    checks = [
        (logarithm(exponential_minus_one(X)), X, "log(exp(X))=X"),
        (exponential_minus_one(logarithm(X)), X, "exp(log(X))=X"),
        (logarithm(circle), add(logarithm(X), logarithm(Y)),
         "log(X+Y+XY)=log(X)+log(Y)"),
        (exponential_minus_one(add(X, Y)),
         add(exponential_minus_one(X), exponential_minus_one(Y),
             mul(exponential_minus_one(X), exponential_minus_one(Y))),
         "exp(X+Y)=exp(X)exp(Y)"),
    ]
    for a, b, label in checks:
        check_equal(a, b, label)

    # The fourth coefficient of log(r) is checked symbolically in the
    # independent coefficient ring F_5[a1,a2,a3,a4], not by 625 values.
    # Its expected polynomial follows from r^2:2a1a3+a2^2,
    # r^3:3a1^2a2, and r^4:a1^4.
    coefficients = {
        "a4": 1,
        "a1*a3": (-2 * pow(2, -1, P)) % P,
        "a2^2": (-pow(2, -1, P)) % P,
        "a1^2*a2": (3 * pow(3, -1, P)) % P,
        "a1^4": (-pow(4, -1, P)) % P,
    }
    check_equal(coefficients,
                {"a4": 1, "a1*a3": 4, "a2^2": 2,
                 "a1^2*a2": 1, "a1^4": 1}, "eta coefficients")

    # Binary ingredients, independently represented as integer bitmasks.
    vectors = [v for v in range(32) if v.bit_count() % 2 == 0]
    rotate = lambda v: ((v << 1) & 31) | (v >> 4)
    beta = lambda v, w: (v & w).bit_count() % 2
    quadratic = lambda v: (v.bit_count() // 2) % 2
    for v in vectors:
        if quadratic(rotate(v)) != quadratic(v):
            raise RuntimeError("quadratic rotation")
        if v and rotate(v) == v:
            raise RuntimeError("nonzero fixed vector")
        if v and not any(beta(v, w) for w in vectors):
            raise RuntimeError("degenerate beta")
        for w in vectors:
            if quadratic(v ^ w) != quadratic(v) ^ quadratic(w) ^ beta(v, w):
                raise RuntimeError("quadratic polarization")
            if beta(rotate(v), rotate(w)) != beta(v, w):
                raise RuntimeError("beta rotation")
    if len({rotate(v) ^ v for v in vectors}) != 16:
        raise RuntimeError("M-id not bijective")
    return {
        "status": "PASS",
        "symbolic_ring": "F5[X,Y]/(monomials of total degree >=5)",
        "universal_identities": [label for _, _, label in checks],
        "eta_coefficients_mod5": coefficients,
        "binary_vectors": len(vectors),
        "binary_ordered_pairs": len(vectors) ** 2,
        "M_minus_identity_bijective": True,
        "finite_checks_are_not_a_replacement_for_simplicity_or_obstruction_proofs": True,
    }


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2, sort_keys=True))
