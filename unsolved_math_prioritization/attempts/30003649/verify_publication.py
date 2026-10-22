#!/usr/bin/env python3
"""Strict portable package checks; optional full replay of pinned public inputs."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
ARCHIVES = {
    'authored': ('CP_FACTORIZATION_30003649_AUTHORED_FREEZE.zip', 23238, 'e07292e0950de7e75576263d9ed69ecbd2b70f0d2d02660521ded791f4c85e8d'),
    'independent_audit': ('CP_FACTORIZATION_30003649_INDEPENDENT_AUDIT.zip', 25890, '90d2e4516683ec8346944e3b6830578178d7af87e413e8d397d2c1b0b32f8b98'),
}

def need(ok, message):
    if not ok:
        raise ValueError(message)

def pairs(items):
    result = {}
    for k, v in items:
        need(k not in result, 'duplicate JSON key: ' + k)
        result[k] = v
    return result

def read_json(path):
    return json.loads(path.read_text(), object_pairs_hook=pairs)

def safe(path):
    p = PurePosixPath(path)
    need(isinstance(path, str) and path == str(p) and not p.is_absolute()
         and all(x not in ('', '.', '..') for x in p.parts) and '\\' not in path, 'unsafe path')
    return path

def match(blob, item):
    return len(blob) == item['bytes'] and hashlib.sha256(blob).hexdigest() == item['sha256']

def integrity():
    manifest = read_json(ROOT / 'PUBLICATION_MANIFEST.json')
    paths = [safe(x['path']) for x in manifest['files']]
    need(len(paths) == len(set(paths)), 'duplicate manifest path')
    nodes = list(ROOT.rglob('*'))
    need(not any(p.is_symlink() for p in nodes), 'symlink in package')
    actual = {p.relative_to(ROOT).as_posix() for p in nodes if p.is_file()}
    need(actual == set(paths) | {'PUBLICATION_MANIFEST.json'}, 'strict inventory mismatch')
    for item in manifest['files']:
        need(match((ROOT / item['path']).read_bytes(), item), 'content mismatch: ' + item['path'])
    for folder, (name, size, digest) in ARCHIVES.items():
        path = ROOT / 'freeze' / name
        need(match(path.read_bytes(), {'bytes': size, 'sha256': digest}), 'archive pin mismatch')
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            need(len(names) == len(set(names)), 'duplicate archive path')
            names = [safe(n) for n in names]
            frozen = json.loads(archive.read('MANIFEST.json'), object_pairs_hook=pairs)
            members = [safe(x['path']) for x in frozen['files']]
            need(len(members) == len(set(members)), 'duplicate frozen manifest path')
            need(set(names) == set(members) | {'MANIFEST.json'}, 'archive inventory mismatch')
            need({p.relative_to(ROOT / folder).as_posix() for p in (ROOT / folder).rglob('*') if p.is_file()} == set(names), 'expanded inventory mismatch')
            for name in names:
                need(archive.read(name) == (ROOT / folder / name).read_bytes(), 'archive member mismatch: ' + name)
            for item in frozen['files']:
                need(match(archive.read(item['path']), item), 'frozen content mismatch')
    return {'status': 'PASS', 'file_count': len(actual), 'archives': 2, 'expanded_frozen_files': 39}

def stable(value):
    if isinstance(value, dict):
        return {k: stable(v) for k, v in value.items() if k != 'elapsed_seconds'}
    if isinstance(value, list):
        return [stable(x) for x in value]
    return value

def run(script, arguments=(), recorded=None):
    command = [sys.executable, '-B'] + (['-OO'] if sys.flags.optimize else []) + [str(ROOT / script)] + list(map(str, arguments))
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    with tempfile.TemporaryDirectory() as cwd:
        p = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True)
    need(p.returncode == 0, 'replay failed: ' + script + '\n' + p.stderr)
    result = json.loads(p.stdout, object_pairs_hook=pairs)
    need(result.get('status') == 'PASS', 'replay did not pass: ' + script)
    if recorded:
        need(stable(result) == stable(read_json(ROOT / recorded)), 'stable output mismatch: ' + script)
    return {'status': 'PASS', 'script': script, 'recorded_result_match': bool(recorded), 'result': result}

def main(data=None):
    result = {'integrity': integrity(), 'optimization': sys.flags.optimize, 'portable': [], 'source_dependent': {'status': 'NOT_RUN', 'reason': 'No external witness directory supplied.'}}
    result['portable'].append(run('authored/verify_certificate.py', ['--selftest']))
    result['portable'].append(run('authored/integer2_controls.py', recorded='authored/integer2_result.json'))
    result['portable'].append(run('independent_audit/integer2_independent.py', recorded='independent_audit/integer2_independent_result.json'))
    if data is not None:
        data = data.resolve()
        pins = read_json(ROOT / 'independent_audit/input_pins.json')['files']
        missing = [x['name'] for x in pins if not (data / x['name']).is_file()]
        if missing:
            result['source_dependent'] = {'status': 'NOT_RUN', 'reason': 'Required external witness files are missing.', 'missing_files': missing}
        else:
            for item in pins:
                need(match((data / item['name']).read_bytes(), item), 'pinned input mismatch: ' + item['name'])
            results = []
            for script, recorded in [
                ('authored/verify_certificate.py', 'authored/verification_result.json'),
                ('independent_audit/independent_verifier.py', 'independent_audit/independent_result.json'),
                ('authored/test_corruption.py', 'authored/corruption_result.json'),
                ('independent_audit/adversarial_controls.py', 'independent_audit/adversarial_result.json'),
            ]:
                results.append(run(script, [data], recorded))
            result['source_dependent'] = {'status': 'PASS', 'mandatory_input_hash_gate': 'PASS', 'results': results}
    result['portable_status'] = 'PASS'
    result['full_replay_status'] = result['source_dependent']['status']
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', type=Path)
    args = parser.parse_args()
    print(json.dumps(main(args.data), sort_keys=True, indent=2))
