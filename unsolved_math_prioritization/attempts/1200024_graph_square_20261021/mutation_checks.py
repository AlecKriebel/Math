"""Exact witness and recurrence mutations, using in-process stdlib replay."""
import contextlib
import copy
import gzip
import io
import json
from pathlib import Path
import runpy
import sys
import tempfile

BASE = Path(__file__).resolve().parent

def need(ok, why):
    if not ok:
        raise ValueError(why)

def execute(script, argument):
    previous = sys.argv
    try:
        sys.argv = [str(script), str(argument)]
        with contextlib.redirect_stdout(io.StringIO()):
            runpy.run_path(str(script), run_name='__main__')
    finally:
        sys.argv = previous

c = json.loads(gzip.decompress((BASE / 'square_flow_certificate.json.gz').read_bytes()))
def add_large_circulation(x):
    # A cycle preserves EVERY divergence equation but invalidates the energy bound.
    lookup = {tuple(e): i for i, e in enumerate(x['edge_order'])}
    a, b = next((a, b) for a in x['root_neighbors'] for b in x['root_neighbors'] if a < b and (a, b) in lookup)
    for u, v in ((0, a), (a, b), (b, 0)):
        x['flows'][0][lookup[tuple(sorted((u, v)))]] += (1 if u < v else -1) * 10 * x['denominator']
    x['energy_numerators'] = [sum(f*f for f in flow) for flow in x['flows']]
    x['total_energy_numerator'] = sum(x['energy_numerators'])

mutations = {
    'conserved_but_excessive_energy': add_large_circulation,
    'nonconserved_flow': lambda x: x['flows'][0].__setitem__(0, x['flows'][0][0] + 1),
    'wrong_graph_edge': lambda x: x['edge_order'][0].__setitem__(1, 999999),
    'missing_root_neighbor': lambda x: x['root_neighbors'].pop(),
    'missing_flow': lambda x: x['flows'].pop(),
    'wrong_total_energy': lambda x: x.__setitem__('total_energy_numerator', x['total_energy_numerator'] + 1),
    'wrong_per_flow_energy': lambda x: x['energy_numerators'].__setitem__(0, x['energy_numerators'][0] + 1),
    'wrong_denominator': lambda x: x.__setitem__('denominator', x['denominator'] + 1),
    'wrong_squared_denominator': lambda x: x.__setitem__('total_energy_denominator', x['total_energy_denominator'] + 1),
    'wrong_branching': lambda x: x.__setitem__('q', 3),
    'wrong_radius': lambda x: x.__setitem__('radius', 9),
    'fractional_flow': lambda x: x['flows'][0].__setitem__(0, 0.5),
    'bool_flow': lambda x: x['flows'][0].__setitem__(0, True),
    'reversed_unit_flow': lambda x: x['flows'].__setitem__(0, [-v for v in x['flows'][0]]),
    'neighbor_order_swap': lambda x: x['root_neighbors'].__setitem__(slice(0, 2), x['root_neighbors'][1::-1]),
}
results = []
with tempfile.TemporaryDirectory(prefix='graph1893-mutations-') as td:
    for label, mutate in mutations.items():
        changed = copy.deepcopy(c)
        mutate(changed)
        filename = Path(td) / (label + '.json.gz')
        filename.write_bytes(gzip.compress(json.dumps(changed).encode(), mtime=0))
        for checker in ('verify_square_certificate.py', 'independent_replay.py'):
            try:
                execute(BASE / checker, filename)
            except ValueError as exc:
                results.append({'mutation': label, 'checker': checker, 'rejected': True, 'reason': str(exc)})
            else:
                raise ValueError('accepted mathematical corruption: ' + label + '/' + checker)

source = (BASE / 'check_finite_reductions.py').read_text()
recurrences = [
    ('branch_series_denominator', 'k = (1 + q * k) / (2 + q * k)', 'k = (1 + q * k) / (3 + q * k)'),
    ('side_branch_multiplicity', '1 + (q - 1) * k', '1 + q * k'),
    ('upper_ray_series', 'B = c + B / (1 + B)', 'B = c + B / (2 + B)'),
    ('terminal_triangle', '1 / (1 + A * B / (A + B))', '1 / (2 + A * B / (A + B))'),
    ('free_leaf_initial_condition', 'k = F(1, 2)', 'k = F(1, 3)'),
]
for label, old, new in recurrences:
    need(source.count(old) == 1, 'ambiguous recurrence mutation')
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(source.replace(old, new), '<math-mutation:' + label + '>', 'exec'), {'__name__': '__main__'})
    except ValueError as exc:
        need('reduction failure' in str(exc), 'nonmathematical mutation failure')
        results.append({'mutation': label, 'checker': 'independent rational Laplacian', 'rejected': True, 'reason': str(exc)})
    else:
        raise ValueError('accepted recurrence corruption: ' + label)
print(json.dumps({'verdict': 'PASS', 'rejected_cases': len(results), 'cases': results}, indent=2))
