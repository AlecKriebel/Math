#!/usr/bin/env python3
"""Strict portable integrity/replay checks, not a formal mathematical proof."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
AUTHOR_HASH = '5e1638e7589229caf8667fbcd6af98b2c92f5281e32b95e690d315ea9a39cf8e'
AUDIT_HASH = '7e136a536f4a4cb262cfc6ddf1036a49a838c6951fabfb38e1f5ca65babbc3d0'
ZIP_NAME = '2305073_INDEPENDENT_AUDIT_20261005.zip'
ZIP_HASH = 'e56e74f44910466ee465ecfed5935fe310394acaff0e0a24a1485dc7997cc45d'
AUTHOR = {'APPROACH_LOG.md', 'AUTHOR_MANIFEST.json', 'CONTROL_RESULTS.json',
          'PARTIAL_RESULTS.md', 'README.md', 'SOURCE_VERIFICATION.json', 'verify_controls.py'}
AUDIT = {'AUDIT_BINDING.json', 'AUDIT_CHECKS.json', 'AUDIT_MANIFEST.json',
         'INDEPENDENT_AUDIT.md', 'README.md', 'verify_audit.py'}
PAYLOAD = ({'author/'+p for p in AUTHOR} | {'audit/'+p for p in AUDIT} |
           {ZIP_NAME, 'README.md', 'RELEASE_STATUS.json', 'RELEASE_CHECKS.json', 'verify_release.py'})
MANIFEST = 'RELEASE_MANIFEST.json'


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate JSON key: '+key)
        result[key] = value
    return result


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique)


def metadata(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': digest(data)}


def validate(root):
    entries = list(root.rglob('*'))
    need(not any(p.is_symlink() for p in entries), 'symlink in packet')
    need(all(p.is_file() or p.is_dir() for p in entries), 'nonregular entry')
    need({p.relative_to(root).as_posix() for p in entries if p.is_dir()} == {'author', 'audit'},
         'unexpected or missing directory')
    actual = {p.relative_to(root).as_posix() for p in entries if p.is_file()}
    need(actual == PAYLOAD | {MANIFEST}, 'complete file inventory mismatch')
    manifest = read_json(root/MANIFEST)
    need(manifest['schema'] == 'function-theory-2305073-release-manifest/v1', 'release schema')
    rows = {}
    for row in manifest['files']:
        name = row['path']
        p = PurePosixPath(name)
        need(not p.is_absolute() and '..' not in p.parts and name == p.as_posix(), 'unsafe path')
        need(name not in rows, 'duplicate manifest path')
        need(set(row) == {'path', 'bytes', 'sha256'}, 'manifest fields')
        rows[name] = row
    need(set(rows) == PAYLOAD, 'manifest inventory mismatch')
    for name, row in rows.items():
        need(metadata(root/name) == {'bytes': row['bytes'], 'sha256': row['sha256']},
             'payload mismatch: '+name)
    need(metadata(root/'author/AUTHOR_MANIFEST.json') == {'bytes': 1025, 'sha256': AUTHOR_HASH},
         'frozen author manifest')
    am = read_json(root/'author/AUTHOR_MANIFEST.json')
    need(set(am['files']) == AUTHOR-{'AUTHOR_MANIFEST.json'}, 'author inventory')
    for name, row in am['files'].items():
        need(metadata(root/'author'/name) == row, 'frozen author bytes: '+name)
    need(metadata(root/'audit/AUDIT_MANIFEST.json') == {'bytes': 1037, 'sha256': AUDIT_HASH},
         'frozen audit manifest')
    audit_rows = read_json(root/'audit/AUDIT_MANIFEST.json')['files']
    need(len(audit_rows) == 5 and {r['path'] for r in audit_rows} == AUDIT-{'AUDIT_MANIFEST.json'},
         'audit inventory')
    for row in audit_rows:
        need(metadata(root/'audit'/row['path']) == {'bytes': row['bytes'], 'sha256': row['sha256']},
             'frozen audit bytes: '+row['path'])
    need(metadata(root/ZIP_NAME) == {'bytes': 15190, 'sha256': ZIP_HASH}, 'frozen audit ZIP')
    with zipfile.ZipFile(root/ZIP_NAME) as archive:
        names = archive.namelist()
        need(len(names) == len(set(names)) == 6 and set(names) == {'audit/'+p for p in AUDIT},
             'ZIP inventory')
        need(archive.testzip() is None, 'ZIP CRC')
        for name in names:
            need(archive.read(name) == (root/name).read_bytes(), 'ZIP member bytes: '+name)
    status = read_json(root/'RELEASE_STATUS.json')
    need(status['problem_id'] == '2305073' and status['status'] == 'unsolved' and
         status['approaches_completed'] == 5 and
         status['arbitrary_measurable_pointwise_characterization_established'] is False and
         status['novelty_claimed'] is False, 'release scope')
    return len(actual)


def mutate_manifest(root, function):
    m = read_json(root/MANIFEST)
    function(m)
    (root/MANIFEST).write_text(json.dumps(m), encoding='utf-8')


def rebind(root, name):
    def update(m):
        for row in m['files']:
            if row['path'] == name:
                row.update(metadata(root/name))
    mutate_manifest(root, update)


def mutate(root, kind):
    if kind in {'author_byte', 'audit_byte', 'zip_byte', 'frozen_author_manifest', 'frozen_audit_manifest'}:
        name = {'author_byte': 'author/PARTIAL_RESULTS.md', 'audit_byte': 'audit/INDEPENDENT_AUDIT.md',
                'zip_byte': ZIP_NAME, 'frozen_author_manifest': 'author/AUTHOR_MANIFEST.json',
                'frozen_audit_manifest': 'audit/AUDIT_MANIFEST.json'}[kind]
        with (root/name).open('ab') as f:
            f.write(b'\n')
        if kind.startswith('frozen_'):
            rebind(root, name)
    elif kind == 'missing_file':
        (root/'author/PARTIAL_RESULTS.md').unlink()
    elif kind == 'extra_file':
        (root/'unexpected.txt').write_text('unexpected')
    elif kind == 'extra_nested_file':
        (root/'audit/unexpected.txt').write_text('unexpected')
    elif kind == 'symlink':
        p = root/'author/PARTIAL_RESULTS.md'
        p.unlink()
        p.symlink_to('README.md')
    elif kind == 'duplicate_path':
        mutate_manifest(root, lambda m: m['files'].append(m['files'][0].copy()))
    elif kind == 'unsafe_path':
        mutate_manifest(root, lambda m: m['files'][0].update(path='../outside'))
    elif kind == 'omitted_manifest_entry':
        mutate_manifest(root, lambda m: m['files'].pop())
    elif kind == 'duplicate_json_key':
        p = root/MANIFEST
        p.write_text('{"schema":"invalid",'+p.read_text()[1:])
    elif kind == 'false_scope':
        p = root/'RELEASE_STATUS.json'
        s = read_json(p)
        s['status'] = 'solved'
        p.write_text(json.dumps(s))
        rebind(root, 'RELEASE_STATUS.json')
    else:
        raise ValueError('unknown mutation')


NEGATIVES = ('author_byte', 'audit_byte', 'zip_byte', 'frozen_author_manifest',
             'frozen_audit_manifest', 'missing_file', 'extra_file', 'extra_nested_file',
             'symlink', 'duplicate_path', 'unsafe_path', 'omitted_manifest_entry',
             'duplicate_json_key', 'false_scope')


def expected_result():
    return {'schema': 'function-theory-2305073-release-checks/v1', 'result': 'PASS',
            'release_files': 19, 'strict_inventory': True, 'frozen_author_files': 7,
            'frozen_audit_files': 6, 'audit_zip_members_byte_exact': 6,
            'python_modes': ['normal', 'optimized'],
            'author_checks_per_mode': 11515, 'independent_checks_per_mode': 12073,
            'author_and_audit_stdout_byte_exact': True,
            'negative_controls_rejected': list(NEGATIVES),
            'analytic_proofs_machine_verified': False,
            'arbitrary_measurable_pointwise_target_resolved': False}


def main():
    need(validate(ROOT) == 19, 'release file count')
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    for flags in ([], ['-O']):
        commands = [(['author/verify_controls.py', '--check-manifest'], 'author/CONTROL_RESULTS.json'),
                    (['audit/verify_audit.py', '--author-dir', str(ROOT/'author')], 'audit/AUDIT_CHECKS.json')]
        for command, expected in commands:
            command[0] = str(ROOT/command[0])
            completed = subprocess.run([sys.executable, *flags, *command], cwd=ROOT,
                                       env=environment, check=True, capture_output=True)
            need(completed.stdout == (ROOT/expected).read_bytes(), 'byte-exact replay: '+expected)
            need(completed.stderr == b'', 'unexpected replay stderr')
    for kind in NEGATIVES:
        with tempfile.TemporaryDirectory(prefix='riesz-majorant-negative-') as directory:
            target = Path(directory)/'packet'
            shutil.copytree(ROOT, target)
            mutate(target, kind)
            try:
                validate(target)
            except (ValueError, KeyError, FileNotFoundError, zipfile.BadZipFile):
                pass
            else:
                raise ValueError('mutation accepted: '+kind)
    need(validate(ROOT) == 19, 'post-replay integrity')
    output = (json.dumps(expected_result(), indent=2, sort_keys=True)+'\n').encode()
    need(output == (ROOT/'RELEASE_CHECKS.json').read_bytes(), 'release result bytes')
    sys.stdout.buffer.write(output)


if __name__ == '__main__':
    main()
