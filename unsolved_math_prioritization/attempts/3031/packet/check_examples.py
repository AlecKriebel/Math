#!/usr/bin/env python3
"""Deterministic tests and independently inspectable sample models."""
import json
from pathlib import Path
from rooted_verify import verify, validate

HERE = Path(__file__).resolve().parent

def cycle_model(m):
    edges = [[0] * m for _ in range(m)]
    for i in range(m):
        j = (i + 1) % m
        edges[i][j] = edges[j][i] = i + 1
    return {'c': m + 1, 'm': m, 'spokes': [0] * m, 'edges': edges}

models = {
    'known_rooted_4_3': {'c':4, 'm':3, 'spokes':[1,2], 'edges':[[0,3],[3,0]]},
    'rooted_5_4': {'c':5, 'm':4, 'spokes':[1,2,0], 'edges':[[0,1,3],[1,0,4],[3,4,0]]},
}
for m in range(3, 13):
    models[f'rainbow_cycle_{m+1}_{m}'] = cycle_model(m)
reports = {}
for name, model in models.items():
    result = verify(model, full_spectrum=True)
    assert result['is_counterexample'], (name, result)
    if name.startswith('rainbow_cycle_'):
        assert result['vertex_minimal_for_full_palette']
        assert all(len(loss) == 2 for loss in result['vertex_deletion_lost_colors'])
    (HERE / (name + '.json')).write_text(json.dumps(model, indent=2) + '\n')
    reports[name] = result
# Test the non-counterexample direction and m=1 edge case.
assert not verify({'c':2,'m':2,'spokes':[1],'edges':[[0]]})['is_counterexample']
assert not verify({'c':1,'m':1,'spokes':[],'edges':[]})['is_counterexample']
# Surjectivity must be rejected; a missing-color candidate is no certificate.
try:
    validate({'c':3,'m':2,'spokes':[1],'edges':[[0]]})
except ValueError:
    pass
else:
    raise AssertionError('Accepted a non-surjective model')
(HERE / 'verified_examples.json').write_text(json.dumps(reports, indent=2) + '\n')
print(f'All {len(models)} positive examples and 3 validation/negative checks passed.')
# Compare the bounded target check against all subsets on deterministic samples.
import random
rng = random.Random(3031)
compared = 0
for _ in range(500):
    n, c = rng.randrange(1, 9), rng.randrange(2, 8)
    m = rng.randrange(1, c + 1)
    edges = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i):
            edges[i][j] = edges[j][i] = rng.randrange(c)
    sample = {'c':c, 'm':m, 'spokes':[rng.randrange(c) for _ in range(n)], 'edges':edges}
    try:
        small, full = verify(sample), verify(sample, True)
    except ValueError:
        continue
    assert small['is_counterexample'] == full['is_counterexample']
    compared += 1
print(f'Bounded-vs-full target checks agreed on {compared} surjective random models.')
