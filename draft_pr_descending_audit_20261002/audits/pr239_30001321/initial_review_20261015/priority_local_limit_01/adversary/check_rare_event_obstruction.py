"""Exact finite-N controls for the analytic inference obstruction.

This is NOT a construction of a space-time i.i.d. RWRE.
Run with Python 3; no packages required. Output is deterministic.
"""
from fractions import Fraction
from math import comb, ceil, log
import json


def check(n):
    alpha = {2*k-n: Fraction(comb(n, k), 2**n) for k in range(n+1)}
    c = Fraction(1, 2)
    p = Fraction(1, n*n)
    support = {x: (x > 0)-(x < 0) for x in alpha}
    states = []
    for bernoulli, sign, probability in (
        (0, 1, 1-p), (1, 1, p/2), (1, -1, p/2)
    ):
        mu = {x: a*(1+c*bernoulli*sign*support[x]) for x, a in alpha.items()}
        assert sum(mu.values()) == 1
        assert all(a > 0 for a in mu.values())
        states.append((probability, mu, bernoulli))
    for x, a in alpha.items():
        assert sum(prob*mu[x] for prob, mu, _ in states) == a
        second_moment = sum(prob*(mu[x]-a)**2 for prob, mu, _ in states)
        assert second_moment == c*c*p*a*a*support[x]**2
    zero = alpha.get(0, Fraction())
    widths = sorted({1, 2, 3, n+1, ceil(log(n+1))})
    for width in widths:
        for _, mu, bernoulli in states:
            coarse = {}
            for x in alpha:
                cell = x//width
                coarse[cell] = coarse.get(cell, Fraction())+mu[x]-alpha[x]
            distance = sum(abs(value) for value in coarse.values())
            assert distance == c*bernoulli*(1-zero)
        epsilon = Fraction(1, 8)
        tail = sum(prob for prob, _, b in states if c*b*(1-zero)>epsilon)
        assert tail == p
    return {
        "N": n,
        "partition_widths": widths,
        "exact_coarse_tail_at_epsilon_1_over_8": str(p),
        "max_local_L2_error_times_N_cubed": float(
            max(c*c*p*a*a*support[x]**2 for x, a in alpha.items())*n**3
        ),
    }


if __name__ == "__main__":
    rows = [check(n) for n in range(1, 129)]
    print(json.dumps({
        "status": "PASS",
        "exact_rational_checks_N_1_through": 128,
        "not_a_target_model_counterexample": True,
        "controls": [row for row in rows if row['N'] in (1, 2, 8, 32, 128)],
    }, indent=2))
