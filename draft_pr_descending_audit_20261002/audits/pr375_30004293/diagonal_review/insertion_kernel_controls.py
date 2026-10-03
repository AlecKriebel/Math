"""Exact one-pivot enumeration of the entire deletion/reinsertion union.

Created after the independent seal. This is an additional finite control,
not a proof of the asymptotic result. No candidate code is imported.
"""
from fractions import Fraction
from itertools import product
from collections import Counter
from datetime import datetime, timezone
import json

ground = tuple(range(2, 9))
laws = {}
for mask in range(1 << len(ground)):
    s = frozenset(a for i, a in enumerate(ground) if mask >> i & 1)
    laws[s] = Fraction(1)
    for a in ground:
        laws[s] *= Fraction(1, a) if a in s else Fraction(a-1, a)

collision_sets = set()
for s in laws:
    coefficients = Counter({0:1})
    for a in sorted(s):
        old = coefficients.copy()
        for x, n in old.items():
            coefficients[x+a] += n
    if max(coefficients.values()) >= 2:
        collision_sets.add(s)

covered = set()
kernel = Fraction(0)
valid_roots = ghost_assignments = with_unselected_roots = 0
for b, prob in laws.items():
    entries = tuple(sorted(b))
    # The two independent quotient pivot classes in Q^2/<1>.
    for pivot_class in (-1, 1):
        for choices in product((-1, 0, 1), repeat=len(entries)):
            ghost_assignments += 1
            root = -sum(a*c for a, c in zip(entries, choices))*pivot_class
            if root not in ground or root in b:
                continue
            if any(a > root and c for a, c in zip(entries, choices)):
                continue
            s = b | {root}
            assert s in collision_sets
            assert laws[s] == prob/Fraction(root-1)
            covered.add(s)
            kernel += prob/Fraction(root-1)
            valid_roots += 1
            with_unselected_roots += int(root not in b)
assert covered == collision_sets
event_prob = sum((laws[s] for s in collision_sets), Fraction(0))
assert event_prob <= kernel
# Rational certificate for (21/20)*log(7/3)<1:
# exp(20/21) exceeds its first five nonnegative Taylor terms.
x = Fraction(20, 21)
exp_lower = Fraction(1)
term = Fraction(1)
for j in range(1, 5):
    term *= x/j
    exp_lower += term
assert exp_lower > Fraction(7, 3)
print(json.dumps({
    'utc':datetime.now(timezone.utc).isoformat(),
    'all_checks_passed':True,
    'ghost_assignments':ghost_assignments,
    'collision_realizations':len(collision_sets),
    'covered_collision_realizations':len(covered),
    'valid_roots':valid_roots,
    'unselected_distinct_root_checks':with_unselected_roots,
    'exact_collision_probability':str(event_prob),
    'exact_reinsertion_union_weight':str(kernel),
    'strict_log_increment_certificate_exp_lower':str(exp_lower),
    'infinite_probability_statement_tested':False,
}, indent=2, sort_keys=True))
