#!/usr/bin/env python3
"""Exact audit witnesses; these checks do not certify literature completeness."""
from fractions import Fraction as Q
from pathlib import Path
import datetime
import json


def scalar_pushforward(kernel, scale):
    out = {}
    for mark, mass in kernel.items():
        out[mark * scale] = out.get(mark * scale, Q(0)) + mass
    return out


def main():
    before = {Q(-2): Q(1, 2), Q(-1): Q(1, 2), Q(1): Q(1, 2), Q(2): Q(1, 2)}
    after = {Q(-2): Q(1, 2), Q(-1): Q(1), Q(1): Q(1), Q(2): Q(1, 2)}
    # Any scale sending finite support S to itself must send one point of S
    # to another; this exhaustive finite set therefore includes every candidate.
    scales = {a / b for a in before for b in before}
    support_preserving = [a for a in scales if set(scalar_pushforward(before, a)) == set(before)]
    exact_matching = [a for a in scales if scalar_pushforward(before, a) == after]
    assert sorted(support_preserving) == [Q(-1), Q(1)]
    assert exact_matching == []
    rate_before = sum(z*z*m for z, m in before.items())
    rate_after = sum(z*z*m for z, m in after.items())
    assert rate_before == 5 and rate_after == 6

    cases = []
    for a in [Q(1, 100), Q(1, 4), Q(49, 100)]:
        for beta in [Q(0), Q(1), Q(1999, 1000)]:
            lower = max(beta, 1 / (1-a))
            p = (lower + 2) / 2
            assert 1 < p < 2 and p > beta and p > 1/(1-a)
            cases.append({'alpha': str(a), 'beta': str(beta), 'auxiliary_p': str(p)})
    # Analytic beta=2 witness after z=exp(-u): quadratic mass is
    # 2 int_1^infinity u^-2 du = 2. For r<2, the r-moment is
    # 2 int_1^infinity exp((2-r)u)u^-2 du = infinity.
    # The small-jump quadratic tail at epsilon=exp(-m) is exactly 2/m.
    tails = {str(m): str(Q(2, m)) for m in [1, 2, 10, 100]}
    assert all(Q(v) > 0 for v in tails.values())

    result = {
        'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'status': 'pass',
        'scope': 'Exact rational support and parameter checks plus explicit analytic integral reductions',
        'scalar_kernel_witness': {
            'quadratic_rate_before': str(rate_before),
            'quadratic_rate_after': str(rate_after),
            'support_preserving_scales': [str(a) for a in sorted(support_preserving)],
            'matching_scales': exact_matching,
        },
        'nonsymmetric_levy_functionals_specialization': cases,
        'BG2_quadratic_mass': '2',
        'BG2_small_jump_quadratic_tails_at_exp_minus_m': tails,
        'limitations': [
            'Does not infer novelty from absence of search results.',
            'Does not claim the scalar-kernel example excludes all multidimensional representations.',
            'No simulation or floating-point asymptotics used.',
        ],
    }
    Path('SCOPE_CHECK_RECEIPT.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
