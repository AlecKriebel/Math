#!/usr/bin/env python3
"""Bounded exact controls for identities used in the factorization audit.

These are reproducibility controls, not a proof of limiting boundary behavior.
No submitted code is imported or executed.
"""
from fractions import Fraction as Q
from collections import Counter
from pathlib import Path
import hashlib
import json

C = Counter()


def check(label, predicate):
    assert predicate, label
    C[label] += 1


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1])


def mul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def abs2(a):
    return a[0] ** 2 + a[1] ** 2


def div(a, b):
    d = abs2(b)
    assert d
    return ((a[0] * b[0] + a[1] * b[1]) / d,
            (a[1] * b[0] - a[0] * b[1]) / d)


ONE = (Q(1), Q(0))
I = (Q(0), Q(1))


def disc(w):
    return div(add(ONE, mul(I, w)), sub(ONE, mul(I, w)))


# The exact disk-to-half-plane Poisson-kernel identity, including normalization.
for x in (Q(j, 3) for j in range(-6, 7)):
    for y in (Q(1, 100), Q(1, 10), Q(1, 3), Q(1), Q(2)):
        z = disc((x, y))
        check('strict_disk_coordinate', abs2(z) < 1)
        for t in (Q(j, 3) for j in range(-15, 16)):
            xi = disc((t, Q(0)))
            check('boundary_coordinate', abs2(xi) == 1)
            lhs = (1 - abs2(z)) / abs2(sub(xi, z))
            rhs = y * (1 + t * t) / ((x - t) ** 2 + y * y)
            check('disk_halfplane_poisson_identity', lhs == rhs)


def cayley(f):
    return div(sub(f, ONE), add(f, ONE))


fs = [(Q(a, 3), Q(b, 5)) for a in range(1, 8) for b in range(-5, 6)]
for f in fs:
    b = cayley(f)
    check('strict_cayley_contraction', abs2(b) < 1)
    check('cayley_defect_identity', 1 - abs2(b) == 4 * f[0] / abs2(add(f, ONE)))
    check('cayley_denominator_bound', abs2(add(f, ONE)) >= 1)
for f in fs[::7]:
    for g in fs[::5]:
        lhs = sub(cayley(f), cayley(g))
        rhs = div(mul((Q(2), Q(0)), sub(f, g)), mul(add(f, ONE), add(g, ONE)))
        check('cayley_difference_identity', lhs == rhs)


# A rational upper bound 13*r/(1-r)^2 exceeds the candidate's 4*pi constant.
for r in (Q(1, 4), Q(1, 2), Q(9, 10), Q(99, 100)):
    for epsilon in (Q(1, 2 ** k) for k in (1, 5, 10, 20)):
        majorant = 13 * r / (1 - r) ** 2
        n = 0
        while majorant / 4 ** n > epsilon / 2:
            n += 1
        check('deterministic_precision_stage', majorant / 4 ** n <= epsilon / 2)
        check('minimal_precision_stage', n == 0 or majorant / 4 ** (n - 1) > epsilon / 2)


receipt = {
    'status': 'PASS',
    'exact_assertions': sum(C.values()),
    'by_category': dict(sorted(C.items())),
    'scope': 'Bounded exact rational identity and precision-stage controls. '
             'No universal factorization, density, or boundary theorem is inferred from them.',
    'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
}
out = Path(__file__).with_name('EXACT_CONTROL_RESULTS.json')
out.write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
