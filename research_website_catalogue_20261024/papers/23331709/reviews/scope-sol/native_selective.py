#!/usr/bin/env python3
"""One bounded exact diagnostic using the fully read unchanged native module.

No native main, exhaustion, SymPy, archived result, network or file write runs.
This is a finite three-configuration diagnostic, not a universal proof.
"""
from pathlib import Path
import hashlib, json, runpy

SOURCE = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23331709/sources/published-source/container-001/tree/candidate/check.py')
EXPECTED = '01f6ac866ee7cf20a6ec59f3f1f3f26ce4726368b39f1023e6a5ba26c63c9274'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED
native = runpy.run_path(str(SOURCE), run_name='scope_native_definitions_only')
fixtures = native['fixtures']()
cases = [
    ('six_normal_core', fixtures['k4_core'], None, 3, 4),
    ('one_terminal_triple_over_core', native['attach_triangle'](fixtures['k4_core'], 0), list(range(6)), 3, 5),
    ('one_terminal_fourfold_pencil', native['attach_triangle'](fixtures['four_pencil'], 0), [0, 4, 5], 0, 2),
]
results = []
for name, rows, retained, beta, rich_count in cases:
    configuration = native['Configuration'](rows)
    result = configuration.analyze()
    assert result['formal'] and result['supersolvable'], name
    assert result['incidence_components'] == 1 and result['incidence_cycle_rank'] == beta, name
    assert len(result['nontrivial_lines_indices']) == rich_count, name
    witness = None
    if retained is not None:
        mask = sum(1 << i for i in retained)
        assert configuration.close(mask) == mask, name
        assert configuration.rk(mask) == configuration.rank - 1, name
        flats = configuration.flats()
        assert all(configuration.rk(mask) + configuration.rk(other) ==
                   configuration.rk(mask | other) + configuration.rk(mask & other)
                   for other in flats), name
        witness = {'retained_indices': retained, 'rank': configuration.rk(mask),
                   'all_flat_modular_equalities': len(flats), 'modular_coatom': True}
    results.append({'name': name, 'native_result': result, 'coatom_witness': witness})
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED
print(json.dumps({'arithmetic': 'unchanged native exact Fraction arithmetic',
                  'native_program_SHA256': EXPECTED, 'selected_configurations': results,
                  'native_main_and_exhaustions_and_SymPy_executed': False,
                  'finite_diagnostic_only_not_universal_proof': True}, indent=2))
