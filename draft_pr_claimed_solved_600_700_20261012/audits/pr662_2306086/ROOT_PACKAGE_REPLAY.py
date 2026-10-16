#!/usr/bin/env python3
"""Parent reproduction of the captured release ZIP in temporary copies."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import tempfile
import zipfile

A = Path(__file__).absolute().parent
P = A / 'publication'


def need(test, message):
    if not test:
        raise ValueError(message)


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def parse(data):
    return json.loads(data, object_pairs_hook=unique)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    zip_path = P / 'real_schlicht_verification.zip'
    data = zip_path.read_bytes()
    build = parse((P / 'PACKAGE_BUILD_RECEIPT.json').read_bytes())
    need(len(data) == build['zip_bytes'] and digest(data) == build['zip_sha256'], 'release ZIP receipt')
    with zipfile.ZipFile(zip_path) as archive:
        entries = archive.infolist()
        names = [entry.filename for entry in entries]
        need(names == sorted(set(names)), 'duplicate or unsorted archive members')
        members = {}
        for entry in entries:
            name = entry.filename
            path = PurePosixPath(name)
            need(path.as_posix() == name and not path.is_absolute() and '..' not in path.parts
                 and '\\' not in name and ':' not in name, 'unsafe archive path')
            need(stat.S_ISREG(entry.external_attr >> 16) and not entry.is_dir(), 'nonregular archive entry')
            need(entry.date_time == (2026, 10, 15, 0, 0, 0), 'nondeterministic archive date')
            members[name] = archive.read(name)
        need(archive.testzip() is None, 'ZIP CRC')
    manifest_bytes = members.pop('PACKAGE_MANIFEST.json')
    manifest = parse(manifest_bytes)
    need(len(members) == manifest['file_count'] and len(members) + 1 == build['files'], 'manifest count')
    need(digest(manifest_bytes) == build['manifest_sha256'], 'manifest receipt')
    records = manifest['files']
    need(len(records) == len(members) and len({r['path'] for r in records}) == len(records), 'manifest duplicates')
    need({r['path'] for r in records} == set(members), 'manifest inventory')
    for record in records:
        value = members[record['path']]
        need(len(value) == record['bytes'] and digest(value) == record['sha256'], 'manifest member hash')
    for name in ('real_schlicht_preschwarzian.pdf', 'real_schlicht_preschwarzian.tex',
                 'verify_package.py', 'build_package.py', 'zenodo-deposit.json', 'CLAIM_SCOPE.json',
                 'CURRENT_PRIORITY_AND_STATUS.md', 'requirements.txt', 'requirements_numerical.txt'):
        need(members[name] == (P / name).read_bytes(), 'local/publication mismatch: ' + name)
    need(members['README.md'] == (P / 'PACKAGE_README.md').read_bytes(), 'README mismatch')
    snapshot = parse((A / 'SCOPE_AND_SNAPSHOT.json').read_bytes())
    native = snapshot['original_blobs']
    need(len(native) == 24, 'native count')
    need({name for name in members if name.startswith('native/')} == {'native/' + n for n in native}, 'native inventory')
    for name, record in native.items():
        value = members['native/' + name]
        need(len(value) == record['size'] and digest(value) == record['sha256']
             and value == (A / 'native' / name).read_bytes(), 'native byte mismatch')
    scratch = A / 'tmp'
    scratch.mkdir(exist_ok=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(scratch))
    env.pop('PYTHONOPTIMIZE', None)
    with tempfile.TemporaryDirectory(prefix='root-package-replay-', dir=scratch) as tmp:
        target = Path(tmp)
        all_members = dict(members, **{'PACKAGE_MANIFEST.json': manifest_bytes})
        for name, value in all_members.items():
            path = target / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(value)
        args = [sys.executable, '-I', '-B', str(target / 'verify_package.py'), '--replay']
        if '--numerical' in sys.argv:
            args.append('--numerical')
        result = subprocess.run(args, cwd=target, env=env, capture_output=True, timeout=600)
        need(result.returncode == 0, 'replay failure: ' + result.stderr.decode(errors='replace'))
        report = parse(result.stdout)
        need(report['status'] == 'PASS' and report['replay']['status'] == 'PASS', 'replay status')
        after = {path.relative_to(target).as_posix(): path.read_bytes()
                 for path in target.rglob('*') if path.is_file()}
        need(after == all_members, 'replay changed extracted release')
    need(zip_path.read_bytes() == data, 'replay changed release ZIP')
    output = {'created_utc': datetime.now(timezone.utc).isoformat(), 'status': 'PASS',
              'zip_sha256': digest(data), 'zip_bytes': len(data), 'files': len(members) + 1,
              'native24_byte_identical': True, 'manifest_and_regular_safe_ZIP_entries': True,
              'only_temporary_copies_executed': True, 'packet_unchanged': True,
              'python_executable': sys.executable, 'package_replay': report}
    (A / 'ROOT_PACKAGE_REPLAY.json').write_text(json.dumps(output, indent=2, sort_keys=True) + '\n')
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
