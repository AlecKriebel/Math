#!/usr/bin/env python3
"""Finite regression checks, not proofs of asymptotic enumeration or probability."""
from pathlib import Path
from math import log, log1p, fsum
from itertools import combinations
import hashlib
import json
import sys

P = Path(__file__).resolve().parent

def require(condition, data):
    if not condition:
        raise RuntimeError(data)

def e(x, y):
    if not x or not y:
        return 0.0
    return x * log1p(y / x) + y * log1p(x / y)

def compositions(n):
    for mask in range(1 << (n - 1)):
        cuts = [0] + [j for j in range(1, n) if mask & (1 << (j - 1))] + [n]
        yield [cuts[j + 1] - cuts[j] for j in range(len(cuts) - 1)]

entropy_profiles = 0
entropy_center_tests = 0
selection_tests = 0
max_total_boundary_entropy = 0.0
for n in range(1, 11):
    for sizes in compositions(n):
        p = [x / n for x in sizes]
        entropy_profiles += 1
        def at(j):
            return p[j] if 0 <= j < len(p) else 0.0
        for center in range(len(p)):
            entropies = [e(at(center-j-1), at(center-j)) + e(at(center+j), at(center+j+1))
                         for j in range(len(p) + 1)]
            total = fsum(entropies)
            max_total_boundary_entropy = max(max_total_boundary_entropy, total)
            require(total <= 2 * log(2) + 1e-12, ('entropy_sum', sizes, center, total))
            entropy_center_tests += 1
            # A constant artificial gap tests the deterministic selection formula only.
            eps = p[center]
            N = int(2 * log(2) / eps) + 1
            scores = []
            for j in range(N + 1):
                lo = max(0, center - j)
                hi = min(len(p) - 1, center + j)
                mass = fsum(p[lo:hi+1])
                boundary = e(at(lo-1), at(lo)) + e(at(hi), at(hi+1))
                zero_padded = e(at(center-j-1), at(center-j)) + e(at(center+j), at(center+j+1))
                require(abs(boundary - zero_padded) < 1e-12,
                        ('clipped_identity', sizes, center, j, boundary, zero_padded))
                scores.append(mass - boundary)
            margin = (eps * (N+1) - 2 * log(2)) / (N+1)
            require(margin > 0 and max(scores) >= margin - 1e-12,
                    ('selection', sizes, center, N, margin, max(scores)))
            selection_tests += 1

H = e(1, 0.5)
gamma = log(2)  # Largest permitted value, hence the hardest upper envelope here.
require(H > gamma, ('H_half', H, gamma))
mountain_windows = 0
mountain_center_windows = 0
mountain_one_sided_windows = 0
min_ratio_to_certificate = float('inf')
for m in range(2, 61):
    sizes = [2**j for j in range(1, m+1)] + [2**j for j in range(m-1, 0, -1)]
    total = sum(sizes)
    require(total == 3 * 2**m - 4, ('total', m, total))
    require(3 * sizes[m-1] > total, ('heavy_center', m))
    for K in range(1, min(m-1, 30) + 1):
        cap = gamma / (2**K - 1)
        for lo in range(len(sizes) - K + 1):
            hi = lo + K - 1
            mass = sum(sizes[lo:hi+1])
            left = sizes[lo-1] if lo else 0
            right = sizes[hi+1] if hi+1 < len(sizes) else 0
            ratio = (e(sizes[lo], left) + e(sizes[hi], right)) / mass
            require(ratio > cap, ('mountain_obstruction', m, K, lo, ratio, cap))
            min_ratio_to_certificate = min(min_ratio_to_certificate, ratio / cap)
            mountain_windows += 1
            if lo <= m-1 <= hi:
                lower = 2 * H * 2**(-(K-1)/2) / K
                require(ratio >= lower - 1e-12, ('center_lower', m, K, lo, ratio, lower))
                mountain_center_windows += 1
            else:
                require(ratio > H, ('one_side_lower', m, K, lo, ratio, H))
                mountain_one_sided_windows += 1

report = {
    'status': 'passed',
    'scope': 'Finite floating-point regression only. All-size proofs are in the two companion notes; no growth or probability conclusion is inferred from these checks.',
    'entropy_profiles': entropy_profiles,
    'entropy_center_tests': entropy_center_tests,
    'selection_tests': selection_tests,
    'max_total_boundary_entropy': max_total_boundary_entropy,
    'total_boundary_entropy_bound': 2 * log(2),
    'mountains_checked': 59,
    'maximum_mountain_parameter': 60,
    'maximum_window_width_checked': 30,
    'mountain_windows': mountain_windows,
    'center_windows': mountain_center_windows,
    'one_sided_windows': mountain_one_sided_windows,
    'minimum_entropy_to_upper_certificate_ratio': min_ratio_to_certificate,
    'H_half': H,
    'maximum_allowed_gamma': gamma,
    'pins': {name: {'sha256': hashlib.sha256((P/name).read_bytes()).hexdigest(),
                    'bytes': (P/name).stat().st_size}
             for name in ['ADAPTIVE_WINDOW_ENTROPY.md', 'EXACT_CANONICAL_WINDOW_OBSTRUCTION.md',
                          'check_adaptive_windows.py']},
}
out = P / (sys.argv[1] if len(sys.argv) > 1 else 'CHECK_NORMAL.json')
out.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
