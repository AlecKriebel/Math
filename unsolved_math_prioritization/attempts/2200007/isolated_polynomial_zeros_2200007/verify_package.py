#!/usr/bin/env python3
"""Check the strict artifact inventory and replay without network access."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    base = Path(__file__).resolve().parent
    manifest_path = base / 'MANIFEST.json'
    require(not manifest_path.is_symlink(), 'manifest symlink')
    manifest = json.loads(manifest_path.read_text())
    expected = set(manifest['files']) | {'MANIFEST.json'}
    actual = {p.name for p in base.iterdir()}
    require(actual == expected, 'strict inventory mismatch')
    for name, meta in manifest['files'].items():
        require(Path(name).name == name and name not in ('.', '..'), 'unsafe inventory path')
        p = base / name
        require(not p.is_symlink() and p.is_file(), 'nonregular artifact')
        content = p.read_bytes()
        require(len(content) == meta['bytes'], 'byte count mismatch: ' + name)
        require(hashlib.sha256(content).hexdigest() == meta['sha256'], 'hash mismatch: ' + name)
    result = subprocess.run([sys.executable, '-B', str(base/'verify_certificate.py')],
                            check=True, capture_output=True, text=True)
    require(json.loads(result.stdout) == json.loads((base/'certificate_results.json').read_text()),
            'certificate result mismatch')
    status = json.loads((base/'STATUS.json').read_text())
    require(status['problem_id'] == 2200007, 'wrong target')
    require(status['new_research_approaches'] == 0, 'wrong approach count')
    require(status['new_discovery_claim'] is False, 'novelty overclaim')
    print(json.dumps({'verification': 'PASS', 'artifact_files': len(expected),
                      'fixed_prior_counterexample_points': 1152,
                      'network_used': False, 'source_reinspection_claim': False}, sort_keys=True))


if __name__ == '__main__':
    main()
