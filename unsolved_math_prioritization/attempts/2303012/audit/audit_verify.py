#!/usr/bin/env python3
"""Replay frozen packet integrity/fixtures. This is not a potential-theory proof."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

EXPECTED = 'b7c33cc6ea9aa6757e260c9bfc0648af2f9840122d0e94a793d492685e1629ba'
HERE = Path(__file__).resolve().parent
DEFAULT = HERE.parent / 'public' if (HERE.parent / 'public').is_dir() else HERE.parent
parser = argparse.ArgumentParser()
parser.add_argument('--packet', type=Path, default=DEFAULT)
parser.add_argument('--source-dir', type=Path)
args = parser.parse_args()
p = args.packet.resolve()
raw = (p / 'SHA256SUMS.json').read_bytes()
assert hashlib.sha256(raw).hexdigest() == EXPECTED
manifest = json.loads(raw)
assert {x.name for x in p.iterdir() if x.is_file() and x.name != 'SHA256SUMS.json'} == set(manifest['files'])
for name, spec in manifest['files'].items():
    data = (p / name).read_bytes()
    assert len(data) == spec['bytes'], name
    assert hashlib.sha256(data).hexdigest() == spec['sha256'], name
result = json.loads(subprocess.check_output([sys.executable, str(p / 'verify.py')], text=True))
assert result == json.loads((p / 'CHECKS.json').read_text())
assert result['passed'] is True
assert result['poisson_normalization_exact_checks'] == 50
assert result['finite_radius_rational_fixtures'] == 108
assert result['coefficient_uniqueness_rational_fixtures'] == 12
source_result = None
if args.source_dir:
    source_result = json.loads(subprocess.check_output([sys.executable, str(p / 'verify.py'), '--source-dir', str(args.source_dir.resolve())], text=True))
    assert source_result['source_hashes_checked'] == ['hayman_lingham_2018', 'benedicks_1980']
print(json.dumps({'passed': True, 'frozen_manifest_sha256': EXPECTED, 'frozen_files_verified': len(manifest['files']), 'author_replay': result, 'matches_saved_checks': True, 'source_replay': source_result, 'mathematical_scope': 'Finite consistency fixtures and byte integrity only; not a universal proof or a formal analytic verification.'}, indent=2))
