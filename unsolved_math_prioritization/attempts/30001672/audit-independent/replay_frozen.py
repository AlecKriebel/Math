#!/usr/bin/env python3
"""Replay the frozen author's controls without changing any author file."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
parser = argparse.ArgumentParser()
parser.add_argument('--author', type=Path, default=Path(__file__).resolve().parent.parent / 'author')
args = parser.parse_args()
expected = 'ff5e02d9d7dc9d20ee690b6b523de26e2bbb54cd852680d9c310bac7963b635b'
manifest = args.author / 'SHA256SUMS'
assert hashlib.sha256(manifest.read_bytes()).hexdigest() == expected
for line in manifest.read_text().splitlines():
    digest, filename = line.split(maxsplit=1)
    assert hashlib.sha256((args.author / filename.lstrip('*')).read_bytes()).hexdigest() == digest
spec = importlib.util.spec_from_file_location('frozen_bridge', args.author / 'verify_bridge.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
results = module.run()
assert results == json.loads((args.author / 'control_results.json').read_text())
assert results['function_coalition_pairs'] == 1050698
print(json.dumps({'status': 'passed', 'exact_json_match': True, 'function_coalition_pairs': 1050698,
                  'frozen_manifest_sha256': expected}, indent=2))
