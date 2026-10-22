#!/usr/bin/env python3
"""Read-only mathematical diagnostics; no author program, network, or file writes."""
from fractions import Fraction as F
from itertools import product
from math import comb, exp, log
import json


def controls():
    # Independent finite enumeration of ten signed frequency choices, not a
    # transcription of the oscillatory estimate. k=0 has constant phase.
    constant = zero = 0
    for choices in product(((0, -1), (0, 1), (1, -1), (1, 1)), repeat=10):
        c0 = c1 = 0
        for k, s in choices:
            if k: c1 += s
            else: c0 += s
        if c1 == 0:
            constant += 1
            if c0 == 0: zero += 1
    assert constant == comb(20, 10) == 184756
    assert zero == comb(10, 5)**2 == 63504
    # A pairing injection gives a uniform upper bound 945 * 2^10 * n^5.
    pairings = 1
    for k in (1, 3, 5, 7, 9): pairings *= k
    assert pairings == 945

    # Exact binomial probabilities at conjugate angles: the two squared
    # moduli are identical; the original two-angle exclusions permit them.
    conjugate = []
    for n in (16, 64, 256):
        m = n//2
        count = sum(comb(m, a)*comb(m, b)
                    for a in range(m+1) for b in range(m+1)
                    if (2*a-m)**2 + (2*b-m)**2 <= n)
        marginal = F(count, 2**n)
        gap = marginal - marginal**2
        assert gap > F(1, 5)
        conjugate.append({'n':n, 'marginal_cdf':float(marginal),
                          'joint_minus_product':float(gap)})
    real_count = sum(comb(256, a) for a in range(257) if (2*a-256)**2 <= 256)
    real_cdf = F(real_count, 2**256)
    assert float(real_cdf) > 1-exp(-1)

    # Exact hinge-function Jensen controls, with repeated boundary roots.
    # Log radii [-1, 0, 0, 1] correspond to a genuine polynomial with
    # |constant coefficient|=1; no numerical root classifier is used.
    radii = (F(-1), F(0), F(0), F(1))
    def J(t): return sum(max(F(0), t-a) for a in radii)
    jensen = []
    for delta in (F(1,5), F(3,2)):
        back = (J(F(0))-J(-delta))/delta
        forward = (J(delta)-J(F(0)))/delta
        assert back <= 1 <= forward
        jensen.append({'delta':str(delta),'back':str(back),
                       'open_count':1,'closed_count':3,'forward':str(forward)})
    assert jensen[0]['back'] == '1' and jensen[0]['forward'] == '3'

    # An explicit signed-measure representation of the BV truncation uses
    # only strict upper tails. This tests the two endpoint values directly.
    v, upper = 0.01, 16.0
    def g(x): return 0.5*log(x) if v < x <= upper else 0.0
    def representation(x):
        continuous = 0.0 if x <= v else 0.5*log(min(x,upper)/v)
        return (0.5*log(v)*(x > v) + continuous
                - 0.5*log(upper)*(x > upper))
    support = (0.0, v, 1.0, upper, upper+1)
    residual = max(abs(g(x)-representation(x)) for x in support)
    assert residual < 1e-14
    assert g(v) == 0 and g(upper) == 0.5*log(upper)
    mass = 0.5*log(v)+0.5*log(upper/v)-0.5*log(upper)
    assert abs(mass) < 1e-14
    # Discrete joint laws with endpoint atoms, one diagonal and one product.
    p = {(a,b):F(int(i==j),5) for i,a in enumerate(support)
         for j,b in enumerate(support)}
    q = {(a,b):F(1,25) for a in support for b in support}
    eps = max(abs(sum(w for (a,b),w in p.items() if a<=s and b<=t)
                  - sum(w for (a,b),w in q.items() if a<=s and b<=t))
              for s in support for t in support)
    lhs = abs(sum(float(p[a,b]-q[a,b])*g(a)*g(b)
                  for a in support for b in support))
    total_variation = log(upper/v)
    assert lhs <= float(eps)*total_variation**2

    # Rational exponent arithmetic catches the strength needed for the
    # fourth-moment tail and the final squared Markov estimate.
    exponents = {
        'turan_measure':-F(120,19),
        'smallball':-F(5),
        'first_tail':F(1)-F(5,2),
        'second_tail':F(2)-F(5,2),
        'jensen_threshold':-F(11,10)+F(9,10),
        'squared_jensen_threshold':2*(-F(11,10)+F(9,10)),
        'final_probability':-F(1,2)-2*(-F(11,10)+F(9,10))
    }
    assert exponents['turan_measure'] < -6
    assert exponents['second_tail'] == -F(1,2)
    assert exponents['final_probability'] == -F(1,10)

    return {
        'diagnostic_only': True,
        'not_a_computer_proof_of_asymptotic_theorem': True,
        'constant_phase_enumeration':{'n':2,'ordered_signed_choices':4**10,
            'constant':constant,'identically_zero':zero,
            'constant_nonzero':constant-zero,
            'universal_pairing_coefficient':pairings*2**10},
        'conjugate_resonance_counterexample_to_original_lemma':conjugate,
        'real_axis_cdf_n256':float(real_cdf),
        'exp1_cdf_at_1':1-exp(-1),
        'jensen_repeated_boundary_root_controls':jensen,
        'bv_endpoint_atoms':{'representation_max_error':residual,
            'lower_endpoint_value':g(v),'upper_endpoint_value':g(upper),
            'signed_measure_total_mass':mass,'joint_cdf_distance':str(eps),
            'product_expectation_difference':lhs,
            'cdf_variation_bound':float(eps)*total_variation**2},
        'rational_exponents':{k:str(v) for k,v in exponents.items()},
        'all_assertions_passed':True
    }


if __name__ == '__main__':
    print(json.dumps(controls(),indent=2,sort_keys=True))
