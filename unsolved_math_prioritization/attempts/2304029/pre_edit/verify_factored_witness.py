#!/usr/bin/env python3
"""Exact test of a rational-factor witness for Function Theory 4.29.

No counterexample is bundled. This verifier avoids expanding large powers.
Requires SymPy. A user may call verify(factors, p_exponents, q_exponents).
Each factor must be monic, nonconstant, squarefree and pairwise coprime in Q[z].
"""
import json
import sympy as s

z = s.Symbol("z")


def monic_radical(expr):
    p = s.Poly(expr, z, domain=s.QQ)
    if p.is_zero:
        raise ValueError("Zero polynomial has no finite squarefree radical.")
    return p.sqf_part().monic()


def verify(factors, p_exponents, q_exponents):
    fs = [s.Poly(f, z, domain=s.QQ) for f in factors]
    if not fs or not (len(fs) == len(p_exponents) == len(q_exponents)):
        raise ValueError("Provide matching nonempty factor and exponent lists.")
    for exponents in [p_exponents, q_exponents]:
        if any(not isinstance(n, int) or isinstance(n, bool) or n < 1 for n in exponents):
            raise ValueError("Exponents must be positive Python integers.")
    for i, f in enumerate(fs):
        if f.degree() < 1 or f.LC() != 1 or s.gcd(f, f.diff()).degree() != 0:
            raise ValueError("Factors must be monic, nonconstant and squarefree.")
        if any(s.gcd(f, g).degree() != 0 for g in fs[:i]):
            raise ValueError("Factors must be pairwise coprime.")
    S = s.Poly(s.prod(f.as_expr() for f in fs), z, domain=s.QQ)

    def derivative_radical(exponents):
        numerator = s.Poly(0, z, domain=s.QQ)
        repeated_support = s.Integer(1)
        for f, n in zip(fs, exponents):
            numerator += n * f.diff() * S.exquo(f)
            if n > 1:
                repeated_support *= f.as_expr()
        return monic_radical(repeated_support * numerator.as_expr())

    Rp = derivative_radical(p_exponents)
    Rq = derivative_radical(q_exponents)
    proportional = all(p_exponents[0] * q == q_exponents[0] * p
                       for p, q in zip(p_exponents, q_exponents))
    result = {
        "monic_polynomials": True,
        "equal_zero_sets": True,
        "equal_derivative_zero_sets": Rp == Rq,
        "some_positive_power_equality": proportional,
        "is_counterexample": (Rp == Rq and not proportional),
        "degree_P": sum(f.degree() * n for f, n in zip(fs, p_exponents)),
        "degree_Q": sum(f.degree() * n for f, n in zip(fs, q_exponents)),
        "distinct_complex_roots": S.degree(),
        "derivative_radical_P": str(Rp.as_expr()),
        "derivative_radical_Q": str(Rq.as_expr()),
    }
    return result


def self_test():
    # Both polynomials have multiple roots at 0 and 1; powers are proportional.
    a = verify([z, z - 1], [2, 2], [4, 4])
    assert a["equal_derivative_zero_sets"] and a["some_positive_power_equality"]
    assert not a["is_counterexample"]
    # Equal polynomial roots do not force equal derivative roots.
    b = verify([z, z - 1], [2, 3], [3, 2])
    assert not b["equal_derivative_zero_sets"] and not b["some_positive_power_equality"]
    # Simple roots must not be silently included among derivative roots.
    c = verify([z, z - 1], [1, 1], [2, 2])
    assert not c["equal_derivative_zero_sets"] and c["some_positive_power_equality"]
    # Check a quadratic factor and direct expansion on small examples.
    fs = [z**2 + 1, z - 2]
    for ps, qs in [([2, 3], [4, 6]), ([1, 3], [2, 1])]:
        r = verify(fs, ps, qs)
        P = s.prod(f**n for f, n in zip(fs, ps))
        Q = s.prod(f**n for f, n in zip(fs, qs))
        assert r["equal_derivative_zero_sets"] == (
            monic_radical(s.diff(P, z)) == monic_radical(s.diff(Q, z)))
    rejected = 0
    for fs, ps, qs in [([2*z], [1], [1]), ([z*z], [1], [1]),
                        ([z, z], [1,1], [1,1]), ([z], [0], [1])]:
        try:
            verify(fs, ps, qs)
        except ValueError:
            rejected += 1
    assert rejected == 4
    print(json.dumps({"self_tests": "passed", "known_counterexample_verified": False,
                      "symbolic_engine": "SymPy " + s.__version__}, indent=2))


if __name__ == "__main__":
    self_test()
