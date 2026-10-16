#!/usr/bin/env python3
"""Run genuine failing mutations of the compression convention, preserving streams."""
from pathlib import Path
import json
import sys
from capture import capture

assert __debug__ and sys.flags.optimize == 0
root = Path(__file__).resolve().parent
source = root / 'independent_controls.py'
rows = []
for mode in ['reverse_commutator', 'prefix_suffix_mutation']:
    result = capture('mutation_' + mode, ['/usr/bin/python3', '-B', str(source), mode],
                     root, source=source, expected_exit=1)
    stderr = (root / 'captures' / ('mutation_' + mode) / 'stderr.bin').read_bytes()
    assert b'AssertionError: two_commutator_identity' in stderr
    rows.append(result)
(root / 'NEGATIVE_CONTROL_RESULT.json').write_text(json.dumps({
    'schema': 'pr48-algebra-family-actual-failing-mutation-controls/v1',
    'status': 'PASS_TWO_MUTATIONS_ACTUALLY_REJECTED', 'captures': rows,
    'negative_failures_are_not_failed_original_mathematics': True}, indent=2) + '\n')
print('Both actual mutations exited 1 at the intended identity assertion.')
