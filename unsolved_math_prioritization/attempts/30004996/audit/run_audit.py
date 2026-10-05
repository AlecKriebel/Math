#!/usr/bin/env python3
"""Offline read-only replay. Run with Python 3; no third-party packages needed."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

EXPECTED_FREEZE = 'b8a4f8d40b4428baec9bdad1d74c3ab8b33c98bf73013cc5dcb4e60d749d9b4d'
HERE = Path(__file__).resolve().parent
p = argparse.ArgumentParser()
p.add_argument('--packet-dir', type=Path, default=HERE.parent / 'packet')
p.add_argument('--freeze', type=Path, default=HERE.parent / 'FREEZE_MANIFEST.json')
args = p.parse_args()

def digest(data):
    return hashlib.sha256(data).hexdigest()

def require(condition, message):
    if not condition:
        raise SystemExit('FAIL: ' + message)

raw = args.freeze.read_bytes()
require(digest(raw) == EXPECTED_FREEZE, 'external freeze manifest changed')
frozen = json.loads(raw)
require(frozen['id'] == 30004996, 'wrong problem')
require(len(frozen['files']) == 8, 'wrong input count')
expected_names = {x['path'] for x in frozen['files']}
require({x.name for x in args.packet_dir.iterdir()} == expected_names, 'packet has missing or extra entries')
checks = []
for rec in frozen['files']:
    relative = Path(rec['path'])
    require(not relative.is_absolute() and '..' not in relative.parts, 'unsafe manifest path')
    target = args.packet_dir / relative
    require(target.is_file() and not target.is_symlink(), 'not a plain packet file')
    data = target.read_bytes()
    require(len(data) == rec['bytes'] and digest(data) == rec['sha256'], 'frozen input mismatch: ' + rec['path'])
    checks.append({'path': rec['path'], 'bytes': len(data), 'sha256': digest(data), 'matched': True})

original = subprocess.run([sys.executable, '-I', str(args.packet_dir / 'verify.py')], check=True, capture_output=True, timeout=60)
require(not original.stderr, 'original verifier wrote unexpected stderr')
require(original.stdout == (args.packet_dir / 'controls.json').read_bytes(), 'original stdout differs byte-for-byte')
original_json = json.loads(original.stdout)
require(original_json['all_passed'] and original_json['assertions'] == 19861, 'original count/result mismatch')
require(json.loads((args.packet_dir / 'result.json').read_text())['controls'] == original_json, 'result.json control mismatch')
independent = subprocess.run([sys.executable, '-I', str(HERE / 'independent_checks.py')], check=True, capture_output=True, timeout=60)
require(not independent.stderr, 'independent verifier wrote unexpected stderr')
require(independent.stdout == (HERE / 'INDEPENDENT_CHECK_RESULTS.json').read_bytes(), 'independent recorded results changed')
independent_json = json.loads(independent.stdout)
require(independent_json['all_passed'] and independent_json['assertions'] == 135653, 'independent count/result mismatch')

corrections = json.loads((HERE / 'CORRECTIONS.json').read_text())
source = (args.packet_dir / corrections['file']).read_bytes()
require(digest(source) == corrections['frozen_sha256'], 'correction input mismatch')
text = source.decode()
for edit in corrections['corrections']:
    require(text.count(edit['old']) == 1, 'correction does not have exactly one match')
    text = text.replace(edit['old'], edit['new'])
corrected = text.encode()
require(corrected == (HERE / 'source_map.corrected.md').read_bytes(), 'corrected text differs from specified overlay')
require(digest(corrected) == corrections['corrected_sha256'] and len(corrected) == corrections['corrected_bytes'], 'corrected output hash/count mismatch')

print(json.dumps({
    'problem_id': 30004996, 'all_passed': True,
    'external_freeze_manifest_sha256': EXPECTED_FREEZE,
    'frozen_input_files': checks,
    'original_assertions': original_json['assertions'],
    'original_stdout_byte_identical': True,
    'result_json_controls_match': True,
    'independent_assertions': independent_json['assertions'],
    'independent_stdout_byte_identical': True,
    'correction_overlay_matched': True,
    'corrected_source_map_sha256': digest(corrected),
    'infinite_mathematical_claims': 'Written audit only; not established by finite computation.',
    'network_used': False,
    'originals_modified': False
}, indent=2, sort_keys=True))
