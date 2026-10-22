#!/usr/bin/env python3
"""Verify the public projection and replay both exact finite checks."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

def verify(root, manifest):
    for name, rec in manifest['files'].items():
        data = (root/name).read_bytes()
        assert len(data) == rec['bytes'], name
        assert hashlib.sha256(data).hexdigest() == rec['sha256'], name

def main():
    assert __debug__, 'Assertions must be enabled; do not use python -O.'
    parser = argparse.ArgumentParser()
    parser.add_argument('--replay', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    manifest = json.loads((root/'PUBLIC_MANIFEST.json').read_text())
    verify(root, manifest)
    if args.replay:
        for name in ['verify_small_counterexample.py', 'review/independent_dense_fixedspace_check.py']:
            subprocess.run([sys.executable, str(root/name)], check=True, stdout=subprocess.DEVNULL)
        verify(root, manifest)
    print(json.dumps({'public_hashes_match':True, 'files':len(manifest['files']),
        'both_exact_replays_identical': args.replay, 'scope':'credited finite degree-19683 counterexample only'}, sort_keys=True))

if __name__ == '__main__':
    main()
