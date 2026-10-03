#!/usr/bin/env python3
"""Check frozen author files; optionally replay both exact programs."""
import argparse
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--replay', action='store_true')
    args = parser.parse_args()
    root = pathlib.Path(__file__).resolve().parent
    manifest = json.loads((root / 'MANIFEST.json').read_text())
    expected = set(manifest['files']) | {'MANIFEST.json'}
    actual = {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
    assert actual == expected, {'unexpected': sorted(actual-expected), 'missing': sorted(expected-actual)}
    for name, record in manifest['files'].items():
        data = (root / name).read_bytes()
        assert len(data) == record['bytes'], name
        assert hashlib.sha256(data).hexdigest() == record['sha256'], name
    replayed = []
    if args.replay:
        witness = subprocess.check_output([sys.executable, str(root / 'verify_witness.py')])
        assert witness == (root / 'witness_results.json').read_bytes()
        replayed.append('minimal_witness')
        compiler = shutil.which('c++') or shutil.which('g++')
        if compiler is None:
            raise RuntimeError('A C++17 compiler is required for the optional exact-count replay')
        with tempfile.TemporaryDirectory(prefix='kourovka-2609-') as tmp:
            binary = str(pathlib.Path(tmp) / 'count')
            subprocess.run([compiler, '-O2', '-std=c++17', str(root / 'verify_exact_count.cpp'), '-o', binary], check=True)
            counts = subprocess.check_output([binary])
        assert counts == (root / 'exact_count_results.json').read_bytes()
        replayed.append('complete_invariant_character_count')
    print(json.dumps({'status': 'PASS', 'hashed_files': len(manifest['files']), 'replayed': replayed}, sort_keys=True))


if __name__ == '__main__':
    main()
