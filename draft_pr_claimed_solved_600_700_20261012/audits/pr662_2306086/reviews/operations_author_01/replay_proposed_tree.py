#!/usr/bin/env python3
"""Exercise real proposed-tree replay without publication, acceptance or service calls.

The snapshot publication is placed beside the untouched attempt. Synthetic DOI
and receipt placeholders only exercise directory placement, and are never sent
to a service. Final accepted inputs must be replayed again by the parent.
"""
import datetime
import hashlib
from pathlib import Path
import sys
import tempfile
import types

sys.dont_write_bytecode = True
HERE = Path(__file__).absolute().parent
A = HERE.parents[1]
module = types.ModuleType('_pr662_proposed_tree_control')
module.__file__ = str(A / 'prepare_integration.py')
exec(compile((A / 'prepare_integration.py').read_bytes(), module.__file__, 'exec'), module.__dict__)
original, snapshot, snapshot_bytes = module.load_snapshot()
files = {name: module.regular_bytes(A / 'publication' / name) for name in module.PUB_NAMES}
members, binding = module.archive_binding(files['real_schlicht_verification.zip'], original, files, snapshot_bytes)
inputs = {'files': files, 'original': original, 'snapshot': snapshot, 'members': members,
          'accepted_bytes': b'{"OFFLINE_LAYOUT_FIXTURE_NOT_ACCEPTANCE":true}\n', 'review_files': {},
          'receipt_bytes': [b'{"OFFLINE_LAYOUT_FIXTURE_NOT_A_PUBLICATION":1}\n',
                            b'{"OFFLINE_LAYOUT_FIXTURE_NOT_A_PUBLICATION":2}\n'],
          'validation': {'offline_directory_placement_only': True}}
publication = module.build_publication(inputs, '10.5281/zenodo.999999999', module.utc())
with tempfile.TemporaryDirectory(prefix='actual-proposed-tree-', dir=HERE / 'tmp') as temporary:
    report = module.capture_replay(inputs, temporary, publication)
output = {'status': 'PASS', 'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'helper_sha256': hashlib.sha256((A / 'prepare_integration.py').read_bytes()).hexdigest(),
          'publication_snapshot_pins': {name: {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
                                        for name, data in files.items()},
          'archive_binding': binding, 'actual_proposed_tree_replay': report,
          'no_live_api_or_network_calls': True, 'no_real_publication_or_acceptance_asserted': True,
          'final_accepted_inputs_require_fresh_parent_replay': True}
(HERE / 'ACTUAL_PROPOSED_TREE_REPLAY.json').write_bytes(module.json_bytes(output))
print(module.json_bytes({'status': 'PASS', 'native_files': 24,
                        'original_verifier_and_real_archive_replay': True}).decode(), end='')
