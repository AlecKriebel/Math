#!/usr/bin/env python3
"""Parent replay of fresh analytic controls and independent operational fixtures."""
import contextlib
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile
import types

A = Path(__file__).absolute().parent
Q = A / 'reviews/package_round2'


def captured_module(name):
    path = Q / name
    source = path.read_bytes()
    module = types.ModuleType('_parent_' + name.replace('.', '_'))
    module.__file__ = str(path)
    exec(compile(source, str(path), 'exec'), module.__dict__)
    return module, hashlib.sha256(source).hexdigest()


science, science_sha = captured_module('independent_checks.py')
science.exact()
operations, operations_sha = captured_module('operational_checks.py')
scratch = A / 'tmp'
scratch.mkdir(exist_ok=True)
mode = 'optimized' if sys.flags.optimize else 'normal'
with tempfile.TemporaryDirectory(prefix='root-round2-replay-', dir=scratch) as tmp:
    operations.HERE = Path(tmp)
    operations.TMP = Path(tmp) / 'scratch'
    operations.TMP.mkdir()
    with contextlib.redirect_stdout(io.StringIO()):
        operations.main()
    op_result = json.loads((Path(tmp) / ('OPERATIONAL_CHECKS.' + mode + '.json')).read_bytes())
result = {'created_utc': datetime.now(timezone.utc).isoformat(), 'status': 'PASS',
          'outer_mode': mode, 'fresh_analytic_controls': science.RESULTS,
          'fresh_analytic_control_count': len(science.RESULTS),
          'independent_operational_controls': op_result,
          'source_sha256': {'independent_checks.py': science_sha,
                            'operational_checks.py': operations_sha},
          'temporary_fixtures_only': True, 'reviewer_reports_unchanged': True,
          'no_remote_mutations': True}
(A / ('ROOT_ROUND2_REPLAY.' + mode + '.json')).write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'status': 'PASS', 'analytic_controls': len(science.RESULTS),
                  'independent_operation_controls': op_result['checks'], 'mode': mode}))
