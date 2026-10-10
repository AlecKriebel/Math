#!/usr/bin/env python3
"""Verify this source-free audit packet; optionally verify the reviewed inputs."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def verify_record(root, record):
    path = root / record['file']
    raw = path.read_bytes()
    if len(raw) != record['bytes'] or hashlib.sha256(raw).hexdigest() != record['sha256']:
        raise ValueError('File mismatch: ' + record['file'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--packet', type=Path, help='Directory containing the two reviewed mathematical files')
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    manifest = json.loads((here/'AUDIT_MANIFEST.json').read_text())
    for record in manifest['audit_artifacts']:
        verify_record(here, record)
    checked = 0
    if args.packet is not None:
        for record in manifest['reviewed_inputs']:
            verify_record(args.packet.resolve(), record)
            checked += 1
    run = subprocess.run([sys.executable, '-I', '-B', str(here/'audit_math.py')], check=True, text=True, capture_output=True)
    actual = json.loads(run.stdout)
    expected = json.loads((here/'AUDIT_MATH_RESULTS.json').read_text())
    if actual != expected:
        raise ValueError('Independent exact controls disagree with recorded result')
    print(json.dumps({
        'status': 'pass',
        'audit_artifacts_verified': len(manifest['audit_artifacts']),
        'reviewed_inputs_verified': checked,
        'reviewed_input_verification_requested': args.packet is not None,
        'independent_exact_controls': 'pass',
        'analytic_proof_certified_by_computation': False,
        'global_spectral_realization': 'unproved',
    }, indent=2))


if __name__ == '__main__':
    main()
