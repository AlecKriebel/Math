#!/usr/bin/env python3
"""Independent exact, continuous certificate. Standard library; no writes.

The Bernstein positivity checks certify whole intervals, not sampled points.
Finite rank-one and rational corner controls are separately labelled evidence.
"""
from fractions import Fraction as Q
from math import comb, isqrt
import argparse, csv, json
from pathlib import Path

def bernstein_on_interval(coefficients, lo, hi):
    """Convert p(lo+(hi-lo)t) to Bernstein basis of unchanged degree."""
    n = len(coefficients) - 1
    local = [sum(coefficients[j] * comb(j, i) * lo**(j-i) * (hi-lo)**i
                 for j in range(i, n+1)) for i in range(n+1)]
    return [sum(local[i] * Q(comb(k, i), comb(n, i)) for i in range(k+1))
            for k in range(n+1)]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--candidate-csv', type=Path)
    a = ap.parse_args()
    # C=91/(100*factor)-1-beta/4.
    # C=R/[25(2-a)(2+a)^2], and 9 C^2-beta=P/[625(2-a)^2(2+a)^4].
    R = list(map(Q, [328, -1292, 1846, 559]))
    P = list(map(Q, [808256, -7787968, 26922160, -38590240,
                    17679340, 18324452, 2749829]))
    r_coeff = bernstein_on_interval(R, Q(0), Q(2,5))
    assert min(r_coeff) > 0
    intervals = [(Q(0), Q(1,5)), (Q(1,5), Q(2,5))]
    p_coeff = [bernstein_on_interval(P, lo, hi) for lo, hi in intervals]
    assert all(min(row) > 0 for row in p_coeff)
    # Positive denominators, C>0 and 9C^2>beta yield sqrt(beta)/3<C.
    assert Q(2,5) < 2 and Q(91,100) < Q(24,25)**2
    # Direct algebraic feedback elimination controls, including both extremes.
    feedback_cases = 0
    for amplitude in [Q(1,10**12), Q(1,100), Q(1,5), Q(2,5)]:
        for strength in [6+Q(1,10**12), Q(601,100), Q(10), Q(16)]:
            for saturation in [Q(0), Q(1,10**12), Q(1,2), 1-Q(1,10**12), Q(1)]:
                radius = amplitude * saturation
                g = strength * (1-saturation*saturation)
                assert 0 <= g <= 16-100*radius*radius
                assert 0 <= g/(4-radius*radius) <= (16-100*radius*radius)/(4-radius*radius)
                feedback_cases += 1
    # Verify the original covering table independently, including adjacency.
    table_rows = 0
    maximum_original = None
    if a.candidate_csv:
        rows = list(csv.DictReader(a.candidate_csv.read_text().splitlines()))
        assert len(rows) == 40
        last = Q(0)
        for j, row in enumerate(rows):
            lo, hi = Q(row['lower']), Q(row['upper'])
            assert int(row['interval']) == j and lo == last and hi-lo == Q(1,100)
            beta = (16-100*lo*lo)/(4-lo*lo)
            k = int(row['sqrt_upper_times_1000'])
            assert Q(row['beta_upper']) == beta
            assert Q(k*k,10**6) >= beta
            assert not k or Q((k-1)**2,10**6) < beta
            envelope = (2+hi)**2/(4*(2-hi)**2)*(1+Q(k,3000)+beta/4)
            assert Q(row['norm_squared_upper']) == envelope <= Q(91,100)
            maximum_original = envelope if maximum_original is None else max(maximum_original,envelope)
            last, table_rows = hi, table_rows+1
        assert last == Q(2,5)
    # Constants require no regularity or n-dependent input.
    kappa = Q(24,25)
    delta = 16*kappa/(1-kappa)
    dsum = 3+Q(25,24)*delta
    distortion = dsum+Q(35,24)*delta
    assert (delta,dsum,distortion) == (384,403,963)
    assert 1+Q(25,96)*delta == 101
    # Distinct exact Gram-matrix test for the rank-one norm bound.
    # On span{1,q}, norm<=C iff C-I transformed Gram matrix is PSD.
    gram_cases = 0
    for beta, root in [(Q(0),Q(0)),(Q(1,9),Q(1,3)),(Q(1),Q(1)),(Q(4),Q(2))]:
        C = 1+root/3+beta/4
        for m in [Q(j,20) for j in range(21)]:
            for v in [m*m+(m-m*m)*Q(j,20) for j in range(21)]:
                den = 1+beta*m
                t11 = (1+beta*beta*(v-m*m))/(den*den)
                t22 = Q(1)
                cross_squared = beta*beta*(v-m*m)/(den*den)
                assert C-t11 >= 0 and C-t22 >= 0
                assert (C-t11)*(C-t22)-cross_squared >= 0
                gram_cases += 1
    print(json.dumps(dict(
        status='PASS', mechanism='Exact Bernstein positivity of transformed continuous inequality',
        continuous_domain='0<=a<=2/5; beta=(16-100a^2)/(4-a^2)',
        continuous_conclusion='U(a)<91/100<(24/25)^2',
        R_bernstein=[str(v) for v in r_coeff],
        P_bernstein_intervals=[dict(lower=str(lo),upper=str(hi),coefficients=[str(v) for v in row])
                               for (lo,hi),row in zip(intervals,p_coeff)],
        original_table_rows=table_rows,
        original_table_maximum=str(maximum_original) if maximum_original is not None else None,
        feedback_boundary_controls=feedback_cases, finite_gram_controls=gram_cases,
        delta_sum=str(delta), displacement_sum=str(dsum), log_distortion=str(distortion),
        limitations='The continuous polynomial certificate is a proof of its inequality. Finite feedback/Gram controls do not prove the infinite-dimensional theorem.'
    ), indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
