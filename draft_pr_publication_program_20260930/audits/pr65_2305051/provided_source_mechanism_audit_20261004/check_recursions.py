#!/usr/bin/env python3
"""Bounded diagnostics, not proofs of infinite-stage or historical claims."""
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

def fixed_children(a):
    return [a - 1, a + 1, a + 1, a - 1] if a else [0] * 4

def submitted_children(left, a, right):
    if not a:
        return [0] * 4
    e1 = 1 if left >= a else -1
    e4 = 1 if right > a else -1
    pairs = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    e2, e3 = next(p for p in pairs if e1 + sum(p) + e4 == 0)
    return [a + e for e in [e1, e2, e3, e4]]

def grow(values, family):
    out = []
    for j, a in enumerate(values):
        children = fixed_children(a) if family == 'fixed1966' else submitted_children(values[j - 1], a, values[(j + 1) % len(values)])
        assert sum(children) == 4 * a
        assert min(children) >= 0
        assert children == [0] * 4 if not a else sorted(c - a for c in children) == [-1, -1, 1, 1]
        out.extend(children)
    return out

def digest(values):
    return hashlib.sha256(json.dumps(values, separators=(',', ':')).encode()).hexdigest()

def main():
    cases = 0
    # All bounded local configurations obeying the inductive neighbor bound.
    for left in range(11):
        for a in range(11):
            for right in range(11):
                if abs(left-a) <= 2 and abs(right-a) <= 2:
                    cs = submitted_children(left, a, right)
                    assert min(cs) >= 0 and sum(cs) == 4*a
                    assert max(abs(cs[j+1]-cs[j]) for j in range(3)) <= 2
                    cases += 1
    edges = 0
    for far_left in range(9):
        for a in range(9):
            for b in range(9):
                for far_right in range(9):
                    if max(abs(far_left-a), abs(a-b), abs(b-far_right)) <= 2:
                        for family in ['fixed1966', 'submitted']:
                            ca = fixed_children(a) if family == 'fixed1966' else submitted_children(far_left, a, b)
                            cb = fixed_children(b) if family == 'fixed1966' else submitted_children(a, b, far_right)
                            assert abs(ca[-1]-cb[0]) <= 2
                            edges += 1
    all_stages = {}
    distributions = {}
    for family in ['fixed1966', 'submitted']:
        values = [1]
        stages = []
        for n in range(10):
            assert len(values) == 4**n and sum(values) == 4**n
            assert 0 <= min(values) and max(values) <= n+1
            max_jump = max(abs(values[(j+1) % len(values)]-a) for j, a in enumerate(values))
            assert max_jump <= 2
            if family == 'fixed1966' and n:
                assert all(a == 0 for a in values[:4**(n-1)])
                assert all(a == 0 for a in values[-4**(n-1):])
            distribution = dict(sorted(Counter(values).items()))
            distributions[(family, n)] = distribution
            stages.append({'n': n, 'cells': len(values), 'mass': '1', 'max_height': max(values),
                           'max_circular_neighbor_jump': max_jump, 'height_counts': distribution,
                           'zero_cell_fraction': str(Fraction(distribution.get(0,0), len(values))),
                           'array_sha256': digest(values),
                           'first_cells': values[:min(16,len(values))]})
            if n < 9:
                values = grow(values, family)
        all_stages[family] = stages
    for n in range(10):
        assert distributions['fixed1966', n] == distributions['submitted', n]
    w1 = fixed_children(1)
    v1 = submitted_children(1, 1, 1)
    orbit = []
    for original in [w1, w1[::-1]]:
        orbit.extend(original[k:]+original[:k] for k in range(4))
    assert v1 not in orbit
    result = {'diagnostic_scope': 'finite checks only; universal and priority claims require the report proofs',
              'bounded_local_children_cases': cases, 'bounded_facing_edge_cases': edges,
              'stage_maximum': 9, 'same_height_law_checked': True,
              'first_stage_not_rotation_or_reflection': True,
              'mass_first_quarter_fixed1966': '0', 'mass_first_quarter_submitted': '1/2',
              'stages': all_stages}
    (HERE / 'CHECKS.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'stages'}, indent=2))

if __name__ == '__main__':
    main()
