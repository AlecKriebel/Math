#!/usr/bin/env python3
"""Exact arithmetic controls, not a theorem prover or independent audit."""
from fractions import Fraction as F
import json

checks = {}
def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks[name] = checks.get(name, 0) + 1

# Polynomial coefficients in ascending order.
def add(a, b):
    n = max(len(a), len(b))
    return [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
            for i in range(n)]
def scale(a, c):
    return [c*x for x in a]

# Universal identity after multiplying the positive denominators:
# 27(t-2)-18(t-1)=9(t-4).
check('budget_margin_polynomial_identity',
      add(scale([-2, 1], 27), scale([-1, 1], -18)) == scale([-4, 1], 9))
# 2+18*((t-2)/18)=t.
check('outside_bound_polynomial_identity',
      add([2, 0], [-2, 1]) == [0, 1])
# t>28 implies t-2>26>18, and hence P>1.
check('parameter_threshold_certificate', 28-2 > 18)
check('margin_sign_threshold_certificate', 28 > 4 and 28 > 2 and 28 > 1)

thresholds = [F(28)+F(1,10**k) for k in range(1,16)]
thresholds += [F(n) for n in range(29,1029)]
thresholds += [F(10**k) for k in range(2,15)]
for t in thresholds:
    p = (t-2)/18
    b = 1/p
    g = 27/(t-1)
    delta = (g-b)/2
    check('sample_parameter_gt_one', p > 1)
    check('sample_outside_bound', 2+18*p == t)
    check('sample_strict_budget_margin', b < g)
    check('sample_margin_identity', g-b == 9*(t-4)/((t-1)*(t-2)))
    check('sample_enlargement_budget', b+delta < g)
    for m in (F(1), F(3,2), F(2)):
        check('sample_actual_supremum_bound', 2+9*p*m <= t)
    # Finite examples plus a separately explicit infinity case.
    for u in (F(0), F(1), t-F(1,10), t, t+F(1,10), t+1, t+2):
        check('sample_exact_superlevel_truncation', (min(u,t+1)>t) == (u>t))
    check('sample_infinity_truncation', t+1 > t)

report = {
    'status': 'PASS_ARITHMETIC_ONLY',
    'independent_mathematical_audit': 'NOT_ASSESSED_BY_ARITHMETIC_PROGRAM',
    'scope': 'Exact algebra and finite rational controls only; imported covering theorem and potential-theory facts are not formally verified.',
    'sample_threshold_count': len(thresholds),
    'checks_by_name': checks,
    'total_assertions': sum(checks.values()),
    'limitations': ['No numerical search proves the imported theorem.', 'Polynomial identities have separate sign arguments in PROOF.md.', 'No original-paper proof audit was performed.']
}
print(json.dumps(report, indent=2, sort_keys=True))
