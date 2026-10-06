#!/usr/bin/env python3
"""Finite algebra/numerical diagnostics only, never a proof of FRW Theorem 2."""
import json
import math
import sys


def need(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    need(sys.flags.isolated and sys.flags.no_site, 'run with -I -S')
    need(len(sys.argv) == 1, 'no arguments')
    rows = []
    for d in [0.0, 0.125, 0.5, 1.0, math.sqrt(2), 1.75, 2.0]:
        theta = math.asin(d / 2)
        endpoint_distance = 2 * math.sin(theta)
        omega = 2 * theta / (2 * math.pi)
        need(abs(endpoint_distance - d) < 1e-14, 'arc diameter identity')
        need(abs(omega - math.asin(d / 2) / math.pi) < 1e-14, 'arc measure identity')
        need(0 <= theta <= math.pi / 2 and 0 <= omega <= 0.5, 'ranges')
        for j in range(31):
            s = -theta + 2 * theta * j / 30
            for k in range(31):
                t = -theta + 2 * theta * k / 30
                need(2 * abs(math.sin((s - t) / 2)) <= d + 1e-14, 'sampled chord maximum')
        rows.append({'diameter': d, 'theta': theta, 'endpoint_distance': endpoint_distance, 'omega': omega})
    bounds = [math.asin(i / 1000) / math.pi for i in range(1001)]
    need(all(a <= b for a, b in zip(bounds, bounds[1:])), 'sampled monotonicity')
    need(bounds[0] == 0 and bounds[-1] == 0.5, 'bound endpoints')
    need(0.75 > math.asin(1) / math.pi, 'major arc is not sharp at diameter two')
    print(json.dumps({'problem_id': 2303021, 'result': 'PASS', 'arc_checks': rows,
        'sampled_chord_pairs': 7 * 31 * 31, 'bound_grid_points': len(bounds),
        'general_continuum_theorem_proved': False,
        'analytic_proofs_location': 'MATHEMATICAL_AUDIT.md',
        'disconnected_counterexample': {'diameter': 2, 'finite_boundary_set_harmonic_measure': 0, 'proposed_lower_bound': 0.5},
        'absorbing_extension': {'value': 1, 'maximum_bound': 0.5, 'classical_interior_harmonic_measure_claimed': False}}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
