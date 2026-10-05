#!/usr/bin/env python3
"""Deterministic independent controls; no counterexample witness is bundled.

The oracle expands only small polynomials, uses a gcd to remove multiplicities,
and compares normalized irreducible-factor multiplicities for power equality.
It does not call the verifier's radical helper or reuse its exponent-ratio test.
"""
import itertools
import json
import random
from fractions import Fraction

import sympy as s
from sympy.polys.polyerrors import PolynomialError, CoercionFailed
import verify_factored_witness as subject

z = subject.z


def require(condition, description):
    if not condition:
        raise AssertionError(description)


def gcd_radical(p):
    require(not p.is_zero, "Oracle received zero polynomial")
    return p.exquo(s.gcd(p, p.diff())).monic()


def normalized_factor_multiplicities(p):
    return {tuple(f.monic().all_coeffs()): Fraction(int(n), int(p.degree()))
            for f, n in p.factor_list()[1]}


def check_case(fs, ps, qs):
    r = subject.verify(fs, ps, qs)
    P = s.Poly(s.prod(f**n for f, n in zip(fs, ps)), z, domain=s.QQ)
    Q = s.Poly(s.prod(f**n for f, n in zip(fs, qs)), z, domain=s.QQ)
    Rp, Rq = gcd_radical(P.diff()), gcd_radical(Q.diff())
    derivative_equal = Rp == Rq
    power_equal = normalized_factor_multiplicities(P) == normalized_factor_multiplicities(Q)
    require(P.LC() == Q.LC() == 1, "Oracle monicity")
    require(gcd_radical(P) == gcd_radical(Q), "Oracle root supports")
    require(r["monic_polynomials"] is True and r["equal_zero_sets"] is True,
            "Basic assertions")
    require(r["equal_derivative_zero_sets"] == derivative_equal, "Derivative equality")
    require(r["some_positive_power_equality"] == power_equal, "Power equality")
    require(r["is_counterexample"] == (derivative_equal and not power_equal), "Verdict")
    require(r["degree_P"] == P.degree() and r["degree_Q"] == Q.degree(), "Degrees")
    require(r["distinct_complex_roots"] == gcd_radical(P).degree(), "Distinct roots")
    require(s.Poly(s.sympify(r["derivative_radical_P"]), z, domain=s.QQ) == Rp, "First radical")
    require(s.Poly(s.sympify(r["derivative_radical_Q"]), z, domain=s.QQ) == Rq, "Second radical")
    return r["is_counterexample"]


def run():
    valid = 0
    counterexamples = 0
    banks = [([z], range(1, 4)), ([z, z-1], range(1, 4)),
             ([z**2+1, z-2], range(1, 4)),
             ([z*(z-1), z**2+1], range(1, 4)),
             ([z, z**2+1, z-2], range(1, 3)),
             ([z**3+1], range(1, 4))]
    for fs, exponents in banks:
        vectors = list(itertools.product(exponents, repeat=len(fs)))
        for ps, qs in itertools.product(vectors, repeat=2):
            counterexamples += int(check_case(fs, ps, qs))
            valid += 1
    rng = random.Random(2304029)
    for _ in range(80):
        roots = rng.sample(range(-6, 7), rng.randint(1, 3))
        fs = [z-s.Rational(r, 7) for r in roots]
        ps = [rng.randint(1, 4) for _ in fs]
        qs = [rng.randint(1, 4) for _ in fs]
        counterexamples += int(check_case(fs, ps, qs))
        valid += 1

    invalid = [([], [], []), ([z], [1, 2], [1]), ([z], [1], []),
               ([0], [1], [1]), ([1], [1], [1]), ([2*z], [1], [1]),
               ([z**2], [1], [1]), ([z, z*(z-1)], [1, 1], [1, 1]),
               ([z], [0], [1]), ([z], [-1], [1]), ([z], [True], [1]),
               ([z], [1.0], [1]), ([z], [s.Integer(1)], [1]),
               ([z-s.Float('0.1')], [1], [1]),
               ([z-s.Float('1.000000000000001')], [1], [1]),
               ([s.Poly(z-0.1, z)], [1], [1]),
               ([z+s.sqrt(2)], [1], [1]), ([z+s.Symbol('y')], [1], [1]),
               ([1/z], [1], [1])]
    rejected = 0
    for fs, ps, qs in invalid:
        try:
            subject.verify(fs, ps, qs)
        except (ValueError, PolynomialError, CoercionFailed):
            rejected += 1
        else:
            raise AssertionError("Invalid input accepted: " + repr((fs, ps, qs)))

    for invalid_radical in [0, z-s.Float('0.1')]:
        try:
            subject.monic_radical(invalid_radical)
        except ValueError:
            rejected += 1
        else:
            raise AssertionError("Invalid radical input accepted")

    # Exact rational input remains accepted; no rationalization is required.
    counterexamples += int(check_case([z-s.Rational(1, 10)], [1], [2]))
    valid += 1
    # Very large exponents exercise the non-expanding implementation only.
    big = subject.verify([z, z-1], [10**20, 2*10**20], [3*10**20, 6*10**20])
    require(big['equal_derivative_zero_sets'] and big['some_positive_power_equality']
            and not big['is_counterexample'], 'Large-exponent proportional control')
    require(big['degree_P'] == 3*10**20 and big['degree_Q'] == 9*10**20,
            'Large-exponent degree control')
    require(counterexamples == 0, "Unexpected sample counterexample needs separate audit")
    return {'independent_controls': 'passed', 'expanded_oracle_cases': valid,
            'invalid_inputs_rejected': rejected, 'large_exponent_controls': 1,
            'random_seed': 2304029, 'symbolic_engine': 'SymPy ' + s.__version__,
            'known_counterexample_verified': False,
            'positive_counterexample_fixture_tested': False,
            'limit': 'Same symbolic backend; independent algorithm, not a second CAS.'}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
