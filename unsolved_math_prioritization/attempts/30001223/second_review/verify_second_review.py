#!/usr/bin/env python3
"""Validate the complete frozen second-review inventory before computation."""
import hashlib
import json
from pathlib import Path
import stat
import subprocess
import sys

NAMES = {'README.md', 'SECOND_REVIEW.md', 'source_metadata.json',
         'weight_graph_check.py', 'weight_graph_results.json',
         'replay_frozen_inputs.py', 'frozen_replay_results.json',
         'verify_second_review.py', 'test_second_gate.py', 'second_gate_results.json'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    root = Path(__file__).absolute().parent
    require(stat.S_ISDIR(root.lstat().st_mode), 'nonregular root')
    files = {p.name:p for p in root.iterdir()}
    require(set(files) == NAMES | {'manifest.json'}, 'inventory mismatch')
    require(all(stat.S_ISREG(p.lstat().st_mode) for p in files.values()), 'nonregular entry')
    manifest = json.loads(files['manifest.json'].read_text())
    require(set(manifest) == {'schema','files'} and manifest['schema'] == 'young-tops-second-review-v1',
            'manifest schema mismatch')
    require(set(manifest['files']) == NAMES, 'manifest inventory mismatch')
    for name, metadata in manifest['files'].items():
        require(set(metadata) == {'bytes','sha256'}, 'manifest metadata keys mismatch')
        data = files[name].read_bytes()
        require(type(metadata['bytes']) is int and metadata['bytes'] == len(data), 'byte count mismatch: ' + name)
        require(metadata['sha256'] == hashlib.sha256(data).hexdigest(), 'hash mismatch: ' + name)
    command = [sys.executable, '-B'] + (['-O'] if sys.flags.optimize else [])
    completed = subprocess.run(command + [str(files['weight_graph_check.py'])], cwd=root,
                               text=True, capture_output=True, timeout=30)
    require(completed.returncode == 0, 'independent check failed: ' + completed.stderr)
    result = json.loads(completed.stdout)
    require(result == json.loads(files['weight_graph_results.json'].read_text()), 'independent result mismatch')
    print(json.dumps({'status':'PASS','regular_files':len(files),
                      'tested_odd_primes':len(result['family']),
                      'source_sha256':manifest['files']['weight_graph_check.py']['sha256']},sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, TypeError, KeyError, subprocess.TimeoutExpired) as error:
        print('REJECT: ' + str(error), file=sys.stderr)
        sys.exit(1)
