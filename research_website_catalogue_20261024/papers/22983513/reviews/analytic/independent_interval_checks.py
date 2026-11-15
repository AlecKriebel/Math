#!/usr/bin/env python3
"""Bounded exact checks of actual infinite interval coordinate remainder.

Finite sums are enclosed by a proved tail bound. This does not prove the
arbitrary-domain theorem. Uses no published verifier imports or outputs.
"""
from fractions import Fraction as F
from pathlib import Path
import json


def need(condition, label):
    if not condition:
        raise RuntimeError(label)


def atan_bounds(x, terms=24):
    s = sum((F((-1) ** h, 2 * h + 1) * x ** (2 * h + 1)
             for h in range(terms)), F(0))
    nxt = F((-1) ** terms, 2 * terms + 1) * x ** (2 * terms + 1)
    return min(s, s + nxt), max(s, s + nxt)


def main():
    # Machin: tan(4 atan(1/5)-atan(1/239))=1 and angle lies in (0,pi/2).
    a, b = atan_bounds(F(1, 5))
    c, d = atan_bounds(F(1, 239))
    pi_lo, pi_hi = 16 * a - 4 * d, 16 * b - 4 * c
    need(F(3) < pi_lo < pi_hi < F(22, 7), 'Machin interval orientation')
    need(pi_hi - pi_lo < F(1, 10**34), 'Machin enclosure width')
    rows = []
    cutoff = 512
    for z in map(F, ['3/2', '4', '9/2', '9', '10', '25', '65/4']):
        low = [j for j in range(1, 7) if j * j < z]
        need(all(j * j >= z for j in range(7, 10)), 'complete low block')
        p = max(low)
        need(cutoff >= 2 * p, 'tail denominator condition')
        exact = sum((4 * (z-j*j) * j*j - (z-j*j)**2 for j in low), F(0))
        numerator = F(0)
        for j in low:
            for k in range(1, cutoff + 1):
                if k*k > z and (k+j) % 2:
                    # L=pi, E_j=j^2; coordinate matrix from sine integration.
                    numerator += (64*j*j*(z-j*j)*k*k*(k*k-z)
                                  / F((k*k-j*j)**3))
        lower, upper_partial = numerator/pi_hi**2, numerator/pi_lo**2
        ratio = 1 - F(p*p, (cutoff+1)**2)
        # All k>K: (k^2-z)<=k^2, (k^2-j^2)>=ratio*k^2,
        # and sum_{k>K}1/k^2 <= integral_K^infty x^-2 dx = 1/K.
        tail = (64 * sum((j*j*(z-j*j) for j in low), F(0))
                / (pi_lo**2 * ratio**3 * cutoff))
        need(F(0) < lower <= upper_partial < exact, 'positive strict omitted tail')
        need(exact < upper_partial + tail, 'analytic infinite remainder enclosure')
        need(upper_partial/64 + tail/64 < exact, 'missing coefficient mutant rejected')
        need(-upper_partial - tail < 0 < exact, 'wrong sign mutant rejected')
        rows.append(dict(z=str(z),low=low,K=cutoff,
                         exact_F=str(exact),partial_lower_float=float(lower),
                         partial_upper_float=float(upper_partial),
                         tail_upper_float=float(tail),
                         exact_partial_lower=str(lower),exact_partial_upper=str(upper_partial),
                         exact_tail_bound=str(tail)))
    # Closed interval formulas are compared to independent exact finite moments.
    for J in range(1, 129):
        energies = [F(j*j) for j in range(1, J+1)]
        A = sum(energies)/J
        B = sum((e*e for e in energies))/J
        D = 9*A*A - 5*B
        gap = 2*J+1
        margin = D-F(gap*gap, 4)
        need(D == F((J+1)*(2*J+1)*(3*J+5), 12), 'interval D formula')
        need(margin == F((2*J+1)*(3*J*J+2*J+2), 12) > 0, 'interval margin formula')
    need(sum((4*(1-j*j)*j*j-(1-j*j)**2 for j in []), F(0)) == 0,
         'z=E1 is equality and must be excluded')
    # No synthetic finite-dimensional matrix can satisfy every coordinate row
    # first-moment identity: antisymmetric energy factors have zero total trace.
    e = [F(1), F(1), F(4), F(9)]
    total = sum(((ek-ej)*F((j+1)*(k+1), j+k+3)**2
                 for j, ej in enumerate(e) for k, ek in enumerate(e)), F(0))
    need(total == 0 and total != len(e), 'finite-trace obstruction')
    result = dict(status='PASS_BOUNDED_EXACT_INTERVAL_REMAINDER_ENCLOSURES',
                  arithmetic='fractions.Fraction; displayed floats are convenience only',
                  pi_enclosure_method='Machin identity and 24-term alternating rational arctan bounds',
                  pi_lower=str(pi_lo),pi_upper=str(pi_hi),
                  threshold_cases=rows,closed_form_J_cases=128,
                  negative_control_families=['missing coefficient64','wrong sign','finite truncation as exact',
                                             'strictness at z=E1','finite row sum-rule realization'],
                  scope='Actual interval infinite series enclosed by analytic tail; not arbitrary-domain proof.')
    Path(__file__).with_name('INDEPENDENT_CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'], len(rows), 'thresholds;', 128, 'closed-form J cases')


if __name__ == '__main__':
    main()
