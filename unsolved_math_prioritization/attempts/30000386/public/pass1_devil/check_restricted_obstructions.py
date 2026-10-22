#!/usr/bin/env python3
"""Finite algebra/arithmetic checks; the universal proofs are in THEOREMS.md."""
from fractions import Fraction
from itertools import product
from math import floor, pi
import json
from pathlib import Path

# Check negative as well as positive velocities. This grid is a test, not the proof.
velocities = [Fraction(j, 24) for j in range(-24, 24)]
ballistic_cases = 0
for u, v in product(velocities, repeat=2):
    path = [(floor(n*u), floor(n*v)) for n in range(9)]
    for p, q in zip(path, path[1:]):
        if max(abs(p[i]-q[i]) for i in (0, 1)) > 1:
            raise RuntimeError("Illegal ballistic move")
    x, y = path[4]
    targets = {(2*x+dx, 2*y+dy) for dx, dy in product((0, 1), repeat=2)}
    if path[8] not in targets:
        raise RuntimeError("Four-cell certificate failed")
    ballistic_cases += 1

horizon_checks = []
for H in range(101):
    K = (2*H+3)**2
    T = K+H+1
    R = T-K
    if not (K+H < T and K < T and R == H+1 and (2*R+1)**2 == K):
        raise RuntimeError("Lookahead arithmetic failed")
    horizon_checks.append({"H": H, "announcements": K, "death_move": T})

result = {
    "status": "passed",
    "scope": "finite implementation checks accompanying, not replacing, the proofs",
    "ballistic_parameter_pairs_tested": ballistic_cases,
    "negative_velocities_included": True,
    "ballistic_adaptive_trap_time": 8,
    "ballistic_announcement_rounds": [4, 5, 6, 7],
    "fixed_schedule_survival_measure_lower_bound": (5-pi*pi/6)/4,
    "bounded_lookahead_cases_tested": len(horizon_checks),
    "initial_lookahead_cases": horizon_checks[:5],
}
path = Path(__file__).with_name("restricted_obstructions_replay.json")
path.write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps(result, indent=2))
