#!/usr/bin/env python3
"""Independent direct-history replay, not a game or horizon solver."""
from itertools import product

points = sorted(set(product((-1, 0, 1), repeat=2)) - {(0, 0)}) + [(2, 0)]
checks = 0
for lead in range(9, 201):
    for now in range(lead + 1, lead + 82):
        history = [(points[(round_ - 1) % 9],
                    lead + 1 + 9 * ((round_ - 1) // 9), round_)
                   for round_ in range(1, now + 1)]
        if not all(1 <= target - round_ <= lead and site != (0, 0)
                   for site, target, round_ in history):
            raise RuntimeError('Illegal announcement or hit on stationary path')
        pending = [(site, target) for site, target, _ in history if target > now]
        relevant = [(site, target) for site, target in pending
                    if max(map(abs, site)) <= target - now]
        phase = (now - lead - 1) % 9
        expected = lead - 8 + phase if phase < 8 else lead - 1
        if len(pending) != lead - 8 + phase or len(relevant) != expected:
            raise RuntimeError('Pending-count formula mismatch')
        checks += 1
print(f'PASS: direct-history reconstruction of {checks} post-transient states')
