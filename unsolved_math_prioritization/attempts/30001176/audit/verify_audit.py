#!/usr/bin/env python3
"""Strict audit inventory, checksums, code pins and independent finite replay."""
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys


def require(value, message):
    if not value:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key: ' + key)
        result[key] = value
    return result


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_object)


def main():
    root = Path(__file__).resolve().parent
    names = set()
    for path in root.iterdir():
        require(stat.S_ISREG(path.lstat().st_mode), 'nonregular inventory node: ' + path.name)
        require(path.name != '__pycache__', 'cache node')
        names.add(path.name)
    manifest = read_json(root / 'MANIFEST.json')
    require(manifest.get('schema') == 1, 'manifest schema')
    entries = manifest['files']
    require(isinstance(entries, dict), 'manifest file map')
    require('MANIFEST.json' not in entries, 'manifest may not list itself')
    require(names == set(entries) | {'MANIFEST.json'}, 'inventory mismatch')
    for name, expected in entries.items():
        require(Path(name).name == name and name not in ('', '.', '..'), 'unsafe name')
        data = (root / name).read_bytes()
        require(len(data) == expected['bytes'] and sha(data) == expected['sha256'], 'content mismatch: ' + name)
    pins = read_json(root / 'CODE_PINS.json')['files']
    require(set(pins) == {'independent_checks.py','verify_audit.py','test_audit_package.py'}, 'code-pin inventory')
    for name, expected in pins.items():
        data = (root / name).read_bytes()
        require(len(data) == expected['bytes'] and sha(data) == expected['sha256'], 'code pin: ' + name)
    cmd = [sys.executable, '-B'] + (['-O'] if sys.flags.optimize else []) + [str(root/'independent_checks.py')]
    run = subprocess.run(cmd,cwd='/tmp',env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,timeout=90,check=False)
    require(run.returncode == 0, 'finite replay: ' + run.stderr.decode(errors='replace'))
    require(run.stdout == (root/'INDEPENDENT_RESULTS.json').read_bytes(), 'finite replay bytes')
    result = json.loads(run.stdout)
    print(json.dumps({'status':'PASS','problem_id':'30001176','files':len(names),
                      'manifest_sha256':sha((root/'MANIFEST.json').read_bytes()),
                      'independent_finite_checks':result['total_checks'],
                      'scope':'Integrity and finite replay, not mathematical certification.'},sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('FAIL: ' + str(exc),file=sys.stderr)
        sys.exit(1)
