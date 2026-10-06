#!/usr/bin/env python3
"""Verify external archive pins, then independently relocate and replay inputs."""
import argparse
import hashlib
import json
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import zipfile

PINS = {
    'author': (12753, 'e82e3a8349c00e74199090c3463918f5a83b915d85003438fa030adabf797978',
               {'README.md','audit.py','case.json','expected_results.json','manifest.json','proof.md','sources.json','verify.py'}),
    'first_audit': (18009, 'a795cf78699d7dc0a87bf0b04c15f9ec5f5afb02869ab9cb1432a1824e86c572',
                    {'README.md','acceptance_results.json','audit_gate.py','author_replay_results.json',
                     'independent_check.py','independent_results.json','manifest.json','mathematical_audit.md',
                     'public_source_verification.json','replay_author.py','test_gate.py'})}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def extract(path, kind, destination):
    size, digest, names = PINS[kind]
    require(stat.S_ISREG(path.lstat().st_mode), 'nonregular input archive')
    data = path.read_bytes()
    require(len(data) == size and hashlib.sha256(data).hexdigest() == digest, 'input archive pin mismatch')
    destination.mkdir(parents=True)
    with zipfile.ZipFile(path) as archive:
        infos = archive.infolist()
        require(len(infos) == len(names) and {i.filename for i in infos} == names, 'input inventory mismatch')
        for info in infos:
            require(not info.is_dir() and stat.S_IFMT(info.external_attr >> 16) in (0, stat.S_IFREG),
                    'nonregular archive member')
            (destination / info.filename).write_bytes(archive.read(info))
    return {'bytes': size, 'sha256': digest, 'files': len(names)}


def run(script, args, cwd, optimized):
    command = [sys.executable, '-B'] + (['-O'] if optimized else []) + [str(script), *map(str,args)]
    completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=120)
    require(completed.returncode == 0, 'input replay failed: ' + completed.stderr)
    data = json.loads(completed.stdout)
    require(data.get('status') == 'PASS', 'input replay did not report PASS')
    checks = data.get('checks')
    if isinstance(checks, list):
        require(all(c.get('passed') is True for c in checks), 'a mutation control failed')
    return {'optimized': optimized, 'status': 'PASS',
            'output_sha256': hashlib.sha256(completed.stdout.encode()).hexdigest(),
            'control_count': len(checks) if isinstance(checks,list) else None}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('author_zip', type=Path)
    parser.add_argument('first_audit_zip', type=Path)
    args = parser.parse_args()
    args.author_zip, args.first_audit_zip = args.author_zip.resolve(), args.first_audit_zip.resolve()
    results, anchors = [], {}
    with tempfile.TemporaryDirectory(prefix='young-tops-second-review-') as temporary:
        root = Path(temporary)
        for kind,path in [('author',args.author_zip),('first_audit',args.first_audit_zip)]:
            target = root / 'relocated path with spaces' / kind
            anchors[kind] = extract(path, kind, target)
            script = target / ('audit.py' if kind == 'author' else 'audit_gate.py')
            for optimized in (False, True):
                result = run(script, [], root, optimized)
                result.update({'test': kind + '_relocated_gate', 'unrelated_working_directory': True})
                results.append(result)
        target = root / 'relocated path with spaces' / 'first_audit'
        for optimized in (False, True):
            result = run(target/'replay_author.py', [args.author_zip], root, optimized)
            result['test'] = 'author_adversarial_controls'
            results.append(result)
            result = run(target/'test_gate.py', [], root, optimized)
            result['test'] = 'first_audit_adversarial_controls'
            results.append(result)
    print(json.dumps({'status':'PASS', 'input_archives':anchors, 'checks':results,
                      'scope':'Frozen archives authenticated before execution; both prior gates relocated; prior control suites rerun under normal and optimized drivers.'},
                     sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
