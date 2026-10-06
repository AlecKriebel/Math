#!/usr/bin/env python3
"""Replay both independent exact controls. Python 3 standard library only."""
from pathlib import Path
import json
import subprocess
import sys

root = Path(__file__).resolve().parent
checks = [
    ('author', root / 'verify_controls.py', root / 'control_results.json'),
    ('independent', root / 'audit/independent_matrix_controls.py',
     root / 'audit/independent_matrix_results.json'),
]
results = {}
for name, script, expected_path in checks:
    compile(script.read_text(), str(script), 'exec')
    run = subprocess.run([sys.executable, str(script)], cwd=root,
                         capture_output=True, text=True, check=True)
    actual = json.loads(run.stdout)
    expected = json.loads(expected_path.read_text())
    if actual != expected:
        raise AssertionError(f'{name} result differs from stored exact result')
    results[name] = 'pass'
print(json.dumps({'checks': results,
                  'scope': 'Two finite controls only; the full problem remains unresolved.'},
                 indent=2))
