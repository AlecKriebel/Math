#!/usr/bin/env python3
"""Replay frozen supplied scripts in ignored scratch and compare exact receipts.

Run from repository root:
  .venv/bin/python draft_pr_publication_program_20260930/audits/pr14_30005934/reproduction_family/reproduce_historical.py

Requires the existing SymPy runtime. Mutates only this family and its tmp/.
"""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
from datetime import datetime, timezone


base = Path(__file__).resolve().parent
snapshot = base.parent / 'source_snapshot'
scratch = base / 'tmp' / 'historical_replay'
scratch.mkdir(parents=True, exist_ok=True)


def digest(data):
    return hashlib.sha256(data).hexdigest()


import sympy
out = {
    'generated_at_utc': datetime.now(timezone.utc).isoformat(),
    'source_head': 'a81fa89f6613791dd55ad5b79bfe8053bd1585f3',
    'python': sys.version,
    'sympy': sympy.__version__,
    'runtime_changed': False,
    'runs': [],
    'scope': 'Reproduction of supplied computations only; no proof certification.',
}
for label, script_path, receipt_path, expected_checks in [
    ('author', Path('check_identities.py'), Path('check_results.json'), 8),
    ('historical_independent', Path('independent_review/independent_checks.py'),
     Path('independent_review/independent_results.json'), 19),
]:
    run_dir = scratch / label
    run_dir.mkdir(exist_ok=True)
    source_bytes = (snapshot / script_path).read_bytes()
    dest = run_dir / script_path.name
    dest.write_bytes(source_bytes)
    replay = subprocess.run([sys.executable, str(dest)], cwd=run_dir,
                            capture_output=True, text=True, check=False)
    (run_dir / 'stdout.txt').write_text(replay.stdout)
    (run_dir / 'stderr.txt').write_text(replay.stderr)
    generated_path = dest.with_name(receipt_path.name)
    actual = generated_path.read_bytes() if generated_path.exists() else b''
    expected = (snapshot / receipt_path).read_bytes()
    row = {
        'suite': label,
        'source_script': str(script_path),
        'source_script_sha256': digest(source_bytes),
        'returncode': replay.returncode,
        'stored_receipt_sha256': digest(expected),
        'replayed_receipt_sha256': digest(actual),
        'receipt_byte_identical': actual == expected,
        'recorded_check_count': expected_checks,
        'stderr': replay.stderr,
    }
    out['runs'].append(row)
    assert replay.returncode == 0, row
    assert actual == expected, row
    shutil.copyfile(generated_path, base / (label + '_replayed_receipt.json'))
out['passed'] = True
out['total_recorded_checks'] = 27
(base / 'historical_replay_results.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))
