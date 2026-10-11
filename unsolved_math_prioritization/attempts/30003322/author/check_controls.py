#!/usr/bin/env python3
"""Exact finite controls for RESULTS.md. No claim of formal proof verification."""
from fractions import Fraction as Q
from itertools import product
import json
import random
from pathlib import Path

class EventuallyConstant:
    def __init__(self, prefix=(), tail=0):
        self.tail = Q(tail)
        p = [Q(x) for x in prefix]
        while p and p[-1] == self.tail:
            p.pop()
        self.prefix = tuple(p)
    def coefficient(self, n):
        return self.prefix[n] if n < len(self.prefix) else self.tail
    def __add__(self, other):
        m = max(len(self.prefix), len(other.prefix))
        return EventuallyConstant(
            [self.coefficient(i) + other.coefficient(i) for i in range(m)],
            self.tail + other.tail)
    def scale(self, q):
        return EventuallyConstant([q*x for x in self.prefix], q*self.tail)
    def truncate(self, n):
        return EventuallyConstant([self.coefficient(i) for i in range(n)], 0)
    def __eq__(self, other):
        return self.prefix == other.prefix and self.tail == other.tail

def is_dyadic(q):
    d = Q(q).denominator
    return d & (d-1) == 0

def trim(a):
    a = [Q(x) for x in a]
    while a and not a[-1]:
        a.pop()
    return a

def divrem(a, b):
    a, b = trim(a), trim(b)
    assert b
    while len(a) >= len(b):
        k, c = len(a)-len(b), a[-1]/b[-1]
        for j, v in enumerate(b):
            a[k+j] -= c*v
        a = trim(a)
    return a

def gcd(a, b):
    a, b = trim(a), trim(b)
    while b:
        a, b = b, divrem(a, b)
    return [x/a[-1] for x in a] if a else []

def run():
    results = {}
    # Finite tree checks only: prefix closure is compatible with a missing next level.
    counts = []
    for d in range(0, 11):
        tree = {s for n in range(d+1) for s in product((-1, 1), repeat=n)}
        assert len(tree) == 2**(d+1)-1
        assert all(s[:j] in tree for s in tree for j in range(len(s)+1))
        assert (1,)*(d+1) not in tree
        counts.append(len(tree))
    results["finite_tree_node_counts_depth_0_to_10"] = counts

    # Odd localization obstruction: enough powers of 2 never divide a fixed nonzero numerator.
    localization_cases = 0
    for p in [3, 5, 7, 11, 13]:
        for m in range(1, 101):
            for r in range(6):
                a = Q(m, p**r)
                b = a / 2**8
                # m<=100, so after division by 256 a factor of 2 must remain in denominator.
                assert b.denominator % 2 == 0
                localization_cases += 1
    results["odd_localization_cases"] = localization_cases

    x = EventuallyConstant([], 1)
    assert x.scale(Q(1, 2)).tail.denominator == 2
    assert not is_dyadic(x.scale(Q(1, 3)).tail)
    for n in range(101):
        assert x.scale(Q(1, 3)).truncate(n).tail == 0
    rng = random.Random(30003322)
    for _ in range(1000):
        def sample():
            return EventuallyConstant(
                [Q(rng.randint(-8, 8), rng.randint(1, 8)) for _ in range(rng.randrange(8))],
                rng.randint(-5, 5))
        a, b_, c = sample(), sample(), sample()
        assert (a+b_)+c == a+(b_+c)
        assert a+b_ == b_+a
        assert a + a.scale(-1) == EventuallyConstant()
        assert (a+b_).tail.denominator == 1
        # Dividing twice and multiplying back works ambiently; membership is separate.
        assert a.scale(Q(1, 2)).scale(2) == a
    results["eventually_constant_group_exact_trials"] = 1000
    results["infinite_series_membership_controls"] = {
        "x_in_G_Z": True, "x_over_2_in_G_Z": False,
        "x_in_G_D": True, "x_over_3_in_G_D": False,
        "truncations_of_x_over_3_in_H_checked_through_length": 100}

    for n in range(1, 65):
        f = [1] + [0]*(n-1) + [1]
        derivative = [0]*(n-1) + [n]
        assert gcd(f, derivative) == [Q(1)]
    results["squarefree_one_plus_u_power_n_checked_n"] = [1, 64]
    results["status"] = "PASS"
    results["limits"] = [
        "Finite rational and polynomial controls; not a formal verification of surreal arithmetic.",
        "No computation establishes NBG independence or either universal set-model converse.",
        "Real-coefficient and infinite-support assertions are proved in RESULTS.md, not exhaustively tested here."
    ]
    return results

if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2))

