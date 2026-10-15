#!/usr/bin/env python3
"""Reproduce the authored offline controls without altering their frozen report."""
import hashlib
import json
from pathlib import Path
import tempfile
import types
import sys

A = Path(__file__).absolute().parent
source = A / 'reviews/operations_author_01/offline_controls.py'
captured = source.read_bytes()
module = types.ModuleType('_root_pr662_offline_operations_controls')
module.__file__ = str(source)
exec(compile(captured, str(source), 'exec'), module.__dict__)
scratch = A / 'tmp'
scratch.mkdir(exist_ok=True)
with tempfile.TemporaryDirectory(prefix='root-operational-controls-', dir=scratch) as tmp:
    module.HERE = Path(tmp)
    module.TMP = Path(tmp) / 'tmp'
    module.TMP.mkdir()
    module.main()
    result = json.loads((Path(tmp) / 'OFFLINE_CONTROL_RESULTS.json').read_bytes())
result['parent_control_source_sha256'] = hashlib.sha256(captured).hexdigest()
result['parent_outer_optimized_mode'] = bool(sys.flags.optimize)
result['parent_preserved_author_report'] = True
suffix = 'optimized' if sys.flags.optimize else 'normal'
(A / ('ROOT_OPERATIONS_REPLAY.' + suffix + '.json')).write_text(
    json.dumps(result, indent=2) + '\n')
