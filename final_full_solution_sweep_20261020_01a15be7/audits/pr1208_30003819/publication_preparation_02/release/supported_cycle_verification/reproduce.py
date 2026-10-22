#!/usr/bin/env python3
"""Offline exact checks and closed-inventory verification. Standard library only."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify_manifest(root, expected_digest=None):
    raw = (root / 'SOURCE_MANIFEST.json').read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if expected_digest is not None:
        require(digest == expected_digest, 'independent manifest digest differs')
    manifest = json.loads(raw)
    expected = set()
    for entry in manifest['members']:
        relative = entry['path']
        require(relative not in expected, 'duplicate manifest member')
        require(not Path(relative).is_absolute() and '..' not in Path(relative).parts, 'unsafe manifest path')
        path = root / relative
        require(path.is_file() and not path.is_symlink(), 'member absent or symlink: '+relative)
        data = path.read_bytes()
        require(len(data) == entry['bytes'], 'member size mismatch: '+relative)
        require(hashlib.sha256(data).hexdigest() == entry['sha256'], 'member hash mismatch: '+relative)
        expected.add(relative)
    actual = {path.relative_to(root).as_posix() for path in root.rglob('*') if path.is_file()}
    require(actual == expected | {'SOURCE_MANIFEST.json'}, 'closed inventory differs')
    return digest, len(expected)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest-sha256')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    digest, count = verify_manifest(root, args.manifest_sha256)
    expected = (root/'verification'/'EXPECTED.json').read_bytes()
    require(json.loads(expected)['status'] == 'PASS', 'expected result is not PASS')
    checker_bytes = (root/'verification'/'exact_checks.py').read_bytes()
    receipts = []
    with tempfile.TemporaryDirectory(prefix='supported-cycle-checks-') as temp:
        script = Path(temp)/'exact_checks.py'
        script.write_bytes(checker_bytes)
        for mode in [None, '-O', '-OO']:
            command = [sys.executable, '-B'] + ([] if mode is None else [mode]) + [str(script)]
            result = subprocess.run(command, cwd=temp, capture_output=True, timeout=120, check=False)
            require(result.returncode == 0, 'checker failed: '+str(mode))
            require(result.stderr == b'', 'checker emitted stderr: '+str(mode))
            require(result.stdout == expected, 'full output bytes differ: '+str(mode))
            receipts.append({'mode':mode or 'normal','bytes':len(result.stdout),'sha256':hashlib.sha256(result.stdout).hexdigest(),'exit_code':0,'stderr_bytes':0})
    verify_manifest(root, digest)
    print(json.dumps({'status':'PASS','source_manifest_sha256':digest,'hashed_members':count,'exact_outputs':receipts,'network_used':False,'release_inputs_modified':False,'claim_limit':'Finite exact checks and file integrity; no proof of general recurrence, exhaustive priority or formal proof certification.'},sort_keys=True,indent=2))


if __name__ == '__main__':
    main()
