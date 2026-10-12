#!/usr/bin/env python3
"""Byte-preserving original replay; no write to source_snapshot or canonical work."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import sys
import sympy

root = Path(__file__).resolve().parent
source = root/'frozen_original'
receipts = []
for label, script, saved in [('submitted', 'verify.py', 'verification.json'),
                             ('old_submitted', 'review/submitted_verify.py', 'review/submitted_results.json'),
                             ('old_independent', 'review/independent_checks.py', 'review/independent_results.json')]:
    d = root/'original_replay_documented_runtime'/label
    d.mkdir(parents=True, exist_ok=True)
    f = d/Path(script).name
    f.write_bytes((source/script).read_bytes())
    result = subprocess.run(['/usr/bin/python3', str(f)], capture_output=True)
    stdout = root/'streams'/('documented_'+label+'.stdout')
    stderr = root/'streams'/('documented_'+label+'.stderr')
    stdout.write_bytes(result.stdout)
    stderr.write_bytes(result.stderr)
    generated = f.with_name('independent_results.json' if label == 'old_independent' else 'verification.json')
    actual = generated.read_bytes() if generated.exists() else b''
    expected = (source/saved).read_bytes()
    row = {'label': label, 'command': ['/usr/bin/python3', str(f)], 'exit_code': result.returncode,
           'executable_sha256': hashlib.sha256(f.read_bytes()).hexdigest(),
           'expected_receipt_sha256': hashlib.sha256(expected).hexdigest(),
           'actual_receipt_sha256': hashlib.sha256(actual).hexdigest(),
           'stdout_sha256': hashlib.sha256(result.stdout).hexdigest(),
           'stderr_sha256': hashlib.sha256(result.stderr).hexdigest(),
           'receipt_byte_equal': actual == expected,
           'whole_json_equal': json.loads(actual) == json.loads(expected) if actual else False,
           'stdout_byte_equal_saved': result.stdout == expected}
    receipts.append(row)
    assert result.returncode == 0 and actual == expected and result.stdout == expected, row

# A corruption outside pass counts must be caught by the complete comparison.
saved_json = json.loads((source/'review/independent_results.json').read_text())
corrupt = dict(saved_json)
corrupt['scope'] = 'FALSE: these diagnostics prove the exact random-shift target'
corrupt_raw = (json.dumps(corrupt, indent=2)+'\n').encode()
(root/'receipt_scope_corruption.json').write_bytes(corrupt_raw)
assert corrupt['named_checks_passed'] == saved_json['named_checks_passed']
assert corrupt != saved_json
control = {'pass_count_unchanged': True, 'whole_json_equal': False,
           'byte_equal': corrupt_raw == (source/'review/independent_results.json').read_bytes(),
           'scope_corruption_rejected': True}
out = {'utc': datetime.now(timezone.utc).isoformat(), 'sys_executable': sys.executable,
       'python_version': sys.version, 'sympy_version': sympy.__version__,
       'sympy_source': sympy.__file__, 'replays': receipts, 'whole_receipt_control': control}
(root/'documented_runtime_replay_receipts.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(out, indent=2))
