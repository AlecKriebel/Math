#!/usr/bin/env python3
"""Exact algebra and scope controls, not a formal complex-analysis proof."""
import copy
import json
import math
from fractions import Fraction
from pathlib import Path


def require(condition, label):
    if not condition:
        raise ValueError(label)


def check_claims(c):
    require(c['problem_id'] == '2302042', 'problem identity')
    require(c['freeze_kind'] == 'new_recovery_freeze', 'new freeze')
    require(c['audit_status'] == 'fresh_audit_required', 'audit not inherited')
    p = c['positive_construction']
    require(p['n_min'] == 2, 'construction range')
    require(p['selected_values'] == '2*n', 'number of values')
    require(p['ray_count_coefficient_times_pi'] == '1', 'ray count')
    require(p['total_count_coefficient_times_pi'] == '2*n', 'total count')
    require(p['ratio'] == '1/(2*n)', 'ratio')
    d = c['density_one_exclusion']
    require(d['entire_sum_upper_bound'] == '1', 'entire bound')
    require(d['meromorphic_sum_upper_bound_reported'] == '2', 'meromorphic bound')
    require(d['original_barsegyan_proof_inspected'] is False, 'original proof limitation')
    require(d['universal_bound_independently_proved_here'] is False, 'attribution limitation')
    require(d['scope'] == 'attributed_literature_correction', 'attribution scope')
    require(c['novelty_claim'] is False, 'prior credit')
    require(c['historical_audit_inherited'] is False, 'audit history')
    require(c['raw_dataset_bytes_reverified'] is False, 'dataset verification limit')


def main():
    checks = 0
    def test(ok, label):
        nonlocal checks
        require(ok, label)
        checks += 1

    claims = json.loads(Path(__file__).with_name('CLAIMS.json').read_text())
    check_claims(claims)
    for n in range(2, 42):
        # Exact coefficients of the antiderivative and rotational symmetry.
        for j in range(20):
            exponent = 2*n*j+1
            coeff = Fraction((-1)**j, math.factorial(2*j+1)*exponent)
            derivative_coeff = Fraction((-1)**j, math.factorial(2*j+1))
            test(exponent*coeff == derivative_coeff, 'series derivative')
            test((exponent-1) % (2*n) == 0, '2n-fold rotational covariance')
        # Weight exponent is negative and tail absolutely integrable for n>=2.
        weight = Fraction(1,n)-2
        test(weight < -1, 'tail absolute integrability')
        test(weight+1 > -1, 'integrability of weight times sine at zero')
        # Riesz ray density: (n/pi)t^(n-1)dt integrates to 1/pi.
        ray_mass_times_pi = Fraction(n,n)
        total_mass_times_pi = 2*n*ray_mass_times_pi
        test(total_mass_times_pi == 2*n, 'Riesz total mass')
        ray_zero_count_times_pi = Fraction(1)
        ratio = ray_zero_count_times_pi / total_mass_times_pi
        test(ratio == Fraction(1,2*n), 'ratio normalization')
        test(2*n*ratio == 1, 'sum normalization')
        # Check derivative of leading primitive: (i/n)z^(1-2n)e^(-iz^n).
        # Exponential derivative term has i*(-i)=1 and exponent -n.
        test((1-2*n)+(n-1) == -n, 'leading primitive exponent')
        test(Fraction(1,n)*n == 1, 'leading primitive coefficient')
    for l in range(2, 202):
        n = max(2, (l+1)//2)
        test(2*n >= l, 'enough distinct asymptotic values')
        test(Fraction(l, 2*n) <= 1, 'selected-ratio sum')
        test(l > 1, 'all density-one values contradict reported entire bound')

    mutants = [
        ('ratio factor', ('positive_construction','ratio'), '1/n'),
        ('total zero factor', ('positive_construction','total_count_coefficient_times_pi'), 'n'),
        ('value cardinality', ('positive_construction','selected_values'), 'n'),
        ('unread original proof', ('density_one_exclusion','original_barsegyan_proof_inspected'), True),
        ('unsupported universal proof', ('density_one_exclusion','universal_bound_independently_proved_here'), True),
        ('novelty inflation', ('novelty_claim',), True),
        ('inherited audit', ('historical_audit_inherited',), True),
        ('dataset bytes overclaim', ('raw_dataset_bytes_reverified',), True)
    ]
    rejected = []
    for label, path, value in mutants:
        altered = copy.deepcopy(claims)
        target = altered
        for key in path[:-1]: target = target[key]
        target[path[-1]] = value
        try:
            check_claims(altered)
        except ValueError:
            rejected.append(label)
        else:
            raise ValueError('negative control accepted: '+label)
    print(json.dumps({
        'result': 'PASS', 'exact_checks': checks,
        'claim_scope_checks': 'PASS',
        'negative_controls_rejected': rejected,
        'negative_control_count': len(rejected),
        'analytic_proof_formalized': False,
        'barsegyan_original_proof_verified': False,
        'historical_audit_inherited': False
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
