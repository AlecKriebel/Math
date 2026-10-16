"""Exact finite-N checks for the inward-funnel density lower bound.

Analytic proof is in QUASILOCALITY_AND_UNBOUNDED_DENSITY.md.
No randomness, truncation approximation, or external packages are used.
"""
from fractions import Fraction
import json


def check(r, max_t=64):
    rho = r/(1-r)
    pi_zero = (1-rho)/2
    d = 1-2*r
    h = {0: Fraction(1)}
    accumulated = Fraction()
    rows = []
    for t in range(max_t+1):
        u = sum(h.values())
        assert u == 1+d*accumulated
        assert u >= 1+d*pi_zero*((t+1)//2)
        assert all(v >= 0 for v in h.values())
        assert all((x+t) % 2 == 0 or v == 0 for x, v in h.items())
        if t % 2 == 0:
            assert h.get(0, Fraction()) >= pi_zero
        if t in (0, 1, 2, 8, 32, max_t):
            rows.append({
                'T': t, 'column_sum_exact': str(u),
                'proved_linear_lower_bound': str(1+d*pi_zero*((t+1)//2)),
                'cone_sites': t*(t+3)//2,
            })
        accumulated += h.get(0, Fraction())+h.get(1, Fraction())
        new_h = {}
        for x in range(-t-1, t+2):
            prob_right = 1-r if x <= 0 else r
            new_h[x] = (prob_right*h.get(x+1, Fraction())
                        +(1-prob_right)*h.get(x-1, Fraction()))
        h = new_h
    return {'r': str(r), 'pi_zero': str(pi_zero), 'controls': rows}


if __name__ == '__main__':
    print(json.dumps({
        'status': 'PASS',
        'exact_rational_controls_T_0_through': 64,
        'cases': [check(r) for r in (Fraction(1, 10), Fraction(1, 4), Fraction(2, 5))],
    }, indent=2))
