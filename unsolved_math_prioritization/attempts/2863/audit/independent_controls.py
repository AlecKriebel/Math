#!/usr/bin/env python3
"""Independent exact reimplementation of the 860 published finite controls.

Requires SymPy. Does not import or execute the author's verify.py. Uses SymPy
polynomial arithmetic and gcd degrees for cokernel dimensions rather than the
author's hand-written polynomial arithmetic and rational matrix elimination.
These finite controls do not establish a universal theorem or a manifold rank.
"""
import json
from collections import Counter
from itertools import combinations, product
from math import gcd, prod

import sympy as s

A = s.Symbol("A")
sections = Counter()


def P(expr):
    return s.Poly(expr, A, domain=s.QQ)


def check(condition, section):
    if not condition:
        raise AssertionError(section)
    sections[section] += 1


phi = {n: P(s.cyclotomic_poly(n, A)) for n in range(1, 31)}
for n in range(1, 31):
    remainder_poly = P(A**n - 1)
    for d in s.divisors(n)[:-1]:
        remainder_poly, remainder = remainder_poly.div(phi[d])
        check(remainder.is_zero, "cyclotomic_divisions")
    check(remainder_poly == phi[n] and phi[n].LC() == 1
          and all(c.q == 1 for c in phi[n].all_coeffs()),
          "cyclotomic_integrality")
    check(P(prod(phi[d].as_expr() for d in s.divisors(n))) == P(A**n - 1),
          "cyclotomic_product_identities")

half_orders = tuple(range(1, 16, 2))
primes = [phi[2*n] for n in half_orders]
for p, q in combinations(primes, 2):
    u, v, g = s.gcdex(p, q)
    check(g == P(1) and u*p + v*q == P(1), "pairwise_bezout")


def cokernel_q_dimension(f, modulus):
    # Q[A]/(modulus, f) has dimension deg gcd(modulus, f).
    return s.gcd(f, modulus).degree()


for i, p in enumerate(primes):
    for j, q in enumerate(primes):
        for exponent in (1, 2, 3):
            check(cokernel_q_dimension(q**exponent, p)
                  == (p.degree() if i == j else 0), "cyclic_fibers")

for i, j in combinations(range(len(primes)), 2):
    f = primes[i]**2 * primes[j]
    for index, p in enumerate(primes):
        check(cokernel_q_dimension(f, p)
              == (p.degree() if index in (i, j) else 0),
              "mixed_annihilator_fibers")

for p in primes[:5]:
    for exponent in (1, 2, 3):
        check(cokernel_q_dimension(p, p**exponent) == p.degree(),
              "primary_length_not_fiber_dimension")
        check((p**exponent).degree() == exponent*p.degree(), "primary_length")

for p in primes:
    torsion_q_dimension = sum(cokernel_q_dimension(q, p) for q in primes)
    check(torsion_q_dimension == p.degree(), "rank_one_all_selected_orders_model")
    check(s.Rational(p.degree() + torsion_q_dimension, p.degree()) == 2,
          "rank_one_specialization_jump")

groups = [()] + [(n,) for n in range(2, 13)]
groups += list(product(range(2, 7), repeat=2))
groups += list(product(range(2, 5), repeat=3))
abelian_examples = []
for invariants in groups:
    elements = set(product(*(range(n) for n in invariants)))
    remaining = set(elements)
    orbits = []
    while remaining:
        x = min(remaining)
        orbit = {x, tuple((-value) % n for value, n in zip(x, invariants))}
        remaining.difference_update(orbit)
        orbits.append(orbit)
    fixed = sum(all((2*x) % n == 0 for x, n in zip(v, invariants))
                for v in elements)
    check(2*len(orbits) == len(elements) + fixed, "abelian_character_orbits")
    check(fixed == prod(gcd(2, n) for n in invariants), "abelian_two_torsion")
    if invariants in [(), (2,), (3,), (4,), (2, 2), (2, 3)]:
        abelian_examples.append({"cyclic_factors": list(invariants),
                                 "diagonal_characters": len(orbits),
                                 "order": len(elements), "two_torsion_order": fixed})

crt_examples = []
for count in (2, 4, 6, 8):
    moduli = primes[:count]
    residues = [P(i + 1 + A + (i*i + 1)*A**2).rem(p)
                for i, p in enumerate(moduli)]
    total = prod(moduli)
    answer = P(0)
    for p, residue in zip(moduli, residues):
        other, rem = total.div(p)
        check(rem.is_zero, "crt_exact_quotients")
        check(s.gcd(other, p) == P(1), "crt_coprime")
        inverse = s.invert(other, p)
        answer += other * inverse * residue
    answer = answer.rem(total)
    for p, residue in zip(moduli, residues):
        check(answer.rem(p) == residue, "finite_root_interpolation")
    crt_examples.append({"orders": [2*n for n in half_orders[:count]],
                         "polynomial_degree": answer.degree()})

for half_order in range(5, 46):
    # Substitute k=3,q=2 and p=0,1 in Kitaeff's displayed coefficient.
    # The exponent 3*((q/2)**2 - 1) is zero, so no root arithmetic is needed.
    q = s.Integer(2)
    exponent = 3*((q/2)**2 - 1)
    multiplicity = 1 + int(half_order % 2 == 0)
    coefficient_sum = sum((-1)**(p + 1)*multiplicity*A**exponent for p in (0, 1))
    check(s.expand(coefficient_sum) == 0, "evaluation_kernel_scalar_cancellation")

assert sum(sections.values()) == 860
print(json.dumps({
    "result": "PASS",
    "total_assertions": sum(sections.values()),
    "sections": dict(sections),
    "abelian_examples": abelian_examples,
    "crt_examples": crt_examples,
    "engine": "Independent reimplementation with SymPy " + s.__version__,
    "scope": "Finite exact controls only. No universal module theorem, imported topology theorem, or manifold skein rank is certified."
}, indent=2, sort_keys=True))
