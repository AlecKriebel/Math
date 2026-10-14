#!/usr/bin/env python3
"""Exact arithmetic checks accompanying REPORT.md; not a strategy-search proof."""
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import json


def parameters(r):
    assert r >= 1
    L = 1
    while 3 * L <= 2 * r + 1:
        L *= 3
    R = (L - 1) // 2
    w = r - R
    C = (L * L + 3 * L) // 2
    D = C - w - 1
    return L, R, w, C, D


checks = 0
for r in range(1, 20001):
    L, R, w, C, D = parameters(r)
    assert L >= 3 and L <= 2*r+1 < 3*L
    assert 0 <= w <= L-1
    geometric = Q(0)
    side = L
    elapsed = w
    while side > 3:
        q = side // 3
        assert (side-1)//2 - q == (q-1)//2
        elapsed += q
        geometric += Q(1, q)
        side = q
    assert elapsed == r-1
    assert geometric == Q(1, 2) - Q(3, 2*L)
    coefficient = Q(w, L*L) + geometric
    assert 2*coefficient <= 1-Q(L+2, L*L) < 1
    assert D >= (L*L+L)//2 > Q(L*L, 2)
    assert Q(L*L, D) < 2
    assert D+w == C-1
    assert Q(C-w) > Q((2*r+1)*(r+2), 9)
    # The smallest and largest allowed preloaded integer counts have
    # precisely the claimed strict terminal-density boundary.
    max_m = C-w-1
    assert Q(max_m+w, L*L) + geometric < 1
    assert Q(max_m+1+w, L*L) + geometric == 1
    checks += 1

for j in range(1, 10001):
    s, r = 2*(j-1)**2, 4*j-2
    L, R, w, C, D = parameters(r)
    assert s+w < C
    difference = Q((2*r+1)*(r+2), 9)-s
    assert difference == Q(14*j*j+24*j-18, 9) > 0
    checks += 1

L, R, w, C, D = parameters(4)
assert (L, R, w, C, D) == (9, 4, 0, 54, 53)
A = w+1+(L*L-3*L)//2
assert A == 28
beta = Q(1)
betas = []
for _ in range(2):
    denominator = L*L-beta*A
    assert denominator > 0
    next_beta = beta*L*L/denominator
    assert 1/next_beta == 1/beta-Q(A, L*L)
    beta = next_beta
    betas.append(beta)
assert betas == [Q(81, 53), Q(81, 25)]
L13, _, w13, _, _ = parameters(13)
assert L13 == 27 and w13 == 0
coefficient13 = Q(w13, L13*L13)+Q(1, 2)-Q(3, 2*L13)
assert coefficient13 == Q(4, 9)
assert beta*coefficient13 == Q(36, 25) > 1

report = Path(__file__).with_name('REPORT.md')
receipt = {
    'status': 'PASS',
    'kind': 'Exact rational arithmetic checks; not exhaustive game solving',
    'remaining_time_cases': 20000,
    'sparse_sequence_cases': 10000,
    'total_parameter_cases': checks,
    'three_time_composition_obstruction': {
        'allowed_times': [13, 17, 21],
        'successive_effective_budgets': [str(x) for x in betas],
        'terminal_upper_bound': str(beta*coefficient13),
        'meaning': 'The stated sufficient bound fails; no losing-game assertion.'
    },
    'report_sha256': sha256(report.read_bytes()).hexdigest(),
}
print(json.dumps(receipt, indent=2))
Path(__file__).with_name('BOUNDS_CHECK.json').write_text(json.dumps(receipt, indent=2)+'\n')
