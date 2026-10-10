#!/usr/bin/env python3
"""Portable integrity and exact-control replay; not formal geometric verification."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

AUTHOR_ANCHOR = 'b25e29914341432f65924b883eb5361158e3fee1249bcdab57b2281cfbb662b2'
AUDIT_ANCHOR = '52273269abfb884acd862281b5ddce93e95734a9e2dd2c9d5c2d6b32d7040c40'
REPORT_ANCHOR = '4716d9bbf449d068608d1f6642c1d802e0543185105762ffbe5c6340b67759b0'

def require(ok, message):
    if not ok:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def verify_files(root, expected_anchor=None):
    manifest = root / 'PUBLICATION_MANIFEST.json'
    require(manifest.is_file() and not manifest.is_symlink(), 'publication manifest kind')
    raw = manifest.read_bytes()
    if expected_anchor is not None:
        require(digest(raw) == expected_anchor, 'external publication anchor mismatch')
    record = json.loads(raw)
    require(record.get('problem_id') == '6700077', 'wrong publication target')
    require(record.get('author_manifest_sha256') == AUTHOR_ANCHOR, 'author anchor metadata')
    require(record.get('audit_manifest_sha256') == AUDIT_ANCHOR, 'audit anchor metadata')
    expected = {'PUBLICATION_MANIFEST.json'}
    for row in record['files']:
        name = row['path']
        p = Path(name)
        require(isinstance(name, str) and not p.is_absolute() and '..' not in p.parts
                and name == p.as_posix() and name not in expected, 'unsafe publication path')
        expected.add(name)
        f = root / p
        require(f.is_file() and not f.is_symlink(), 'missing, non-file, or symlink: ' + name)
        b = f.read_bytes()
        require(len(b) == row['bytes'] and digest(b) == row['sha256'], 'changed payload: ' + name)
    found = set()
    for f in root.rglob('*'):
        require(not f.is_symlink(), 'symlink in publication')
        if f.is_file():
            found.add(f.relative_to(root).as_posix())
        else:
            require(f.is_dir() and f.relative_to(root).as_posix() in ('author', 'audit'),
                    'unexpected directory or special file')
    require(found == expected, 'publication file-set mismatch')
    require(digest((root / 'author/AUTHOR_MANIFEST.json').read_bytes()) == AUTHOR_ANCHOR,
            'frozen author manifest changed')
    require(digest((root / 'audit/AUDIT_MANIFEST.json').read_bytes()) == AUDIT_ANCHOR,
            'frozen audit manifest changed')
    require(digest((root / 'audit/AUDIT.md').read_bytes()) == REPORT_ANCHOR,
            'frozen audit report changed')
    return len(expected) - 1

def run_json(root, mode, script, *args):
    command = [sys.executable, '-B']
    if mode == 'optimized':
        command.append('-O')
    command.extend([str(root / script), *map(str, args)])
    result = subprocess.run(command, cwd=root.parent, capture_output=True, text=True, check=False)
    require(result.returncode == 0, script + ' failed: ' + result.stderr)
    return json.loads(result.stdout)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest-sha256')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    count = verify_files(root, args.manifest_sha256)
    frozen = json.loads((root / 'audit/RESULTS.json').read_bytes())
    outputs = {}
    for mode in ('normal', 'optimized'):
        current = {
            'author_controls': run_json(root, mode, 'author/verify_controls.py'),
            'author_packet_verification': run_json(root, mode, 'author/verify_packet.py', '--self-test'),
            'independent_external_binding': run_json(root, mode, 'audit/VERIFY_BINDING.py',
                                                     root / 'author', '--self-test'),
            'independent_symbolic_controls': run_json(root, mode, 'audit/INDEPENDENT_CONTROLS.py'),
        }
        require(current == frozen['execution'][mode], 'replay differs from frozen audit: ' + mode)
        audit = run_json(root, mode, 'audit/VERIFY_AUDIT.py', root / 'audit',
                         '--manifest-sha256', AUDIT_ANCHOR)
        require(audit['outcome'] == 'PASS' and audit['audit_payload_files'] == 8, 'audit verification')
        outputs[mode] = current
    require(outputs['normal'] == outputs['optimized'], 'optimization-dependent replay')
    require(verify_files(root, args.manifest_sha256) == count, 'post-replay file-set change')
    r = outputs['normal']
    print(json.dumps({
        'outcome': 'PASS', 'problem_id': '6700077',
        'status': 'unsolved', 'substantive_approaches': 5, 'approach_limit': 5,
        'publication_payload_files': count, 'publication_manifest_self_excluded': True,
        'author_manifest_sha256': AUTHOR_ANCHOR, 'audit_manifest_sha256': AUDIT_ANCHOR,
        'audit_report_sha256': REPORT_ANCHOR,
        'normal_and_optimized_identical': True,
        'replays_match_frozen_audit': True,
        'author_exact_checks_per_mode': r['author_controls']['exact_assertions'],
        'author_mathematical_negatives_per_mode': r['author_controls']['negative_controls_rejected'],
        'author_tamper_rejections_per_mode': len(r['author_packet_verification']['rejected_negative_controls']),
        'independent_exact_checks_per_mode': r['independent_symbolic_controls']['independent_exact_checks'],
        'independent_mathematical_negatives_per_mode': r['independent_symbolic_controls']['deliberate_mathematical_negatives'],
        'external_anchor_tamper_rejections_per_mode': len(r['independent_external_binding']['independent_binding_negatives_rejected']),
        'scope': 'Byte integrity and finite exact controls supplement the qualified analytic audit. General closure, source identity, novelty, and openness are not mechanically certified.'
    }, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
