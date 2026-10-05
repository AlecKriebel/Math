#!/usr/bin/env python3
"""Verify frozen release bytes and replay controls without modifying them."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

if not __debug__:
    raise RuntimeError('Assertions must remain enabled; do not run with -O')

ROOT = Path(__file__).resolve().parent
AUTHOR_MANIFEST = 'e67ac4e9f37d89fce822f00e4e166b20f21d1051c41e5e2acd595a5709cd95c1'
AUDIT_MANIFEST = '28302e0259c9ae21787bd695cf1d832dbcc24e02932a10e98ddfccf9c476c64d'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def verify_files():
    manifest_path = ROOT / 'RELEASE_MANIFEST.json'
    require(not manifest_path.is_symlink(), 'Release manifest symlink')
    manifest = json.loads(manifest_path.read_bytes())
    expected = {}
    for rec in manifest['files']:
        rel = Path(rec['path'])
        require(not rel.is_absolute() and '..' not in rel.parts, 'Unsafe path')
        require(rec['path'] not in expected, 'Duplicate path')
        expected[rec['path']] = rec
    actual = set()
    for path in ROOT.rglob('*'):
        require(not path.is_symlink(), 'Symlink: ' + str(path.relative_to(ROOT)))
        if path.is_file() and path != manifest_path:
            actual.add(path.relative_to(ROOT).as_posix())
    require(actual == set(expected), 'Release file set mismatch')
    for name, rec in expected.items():
        data = (ROOT / name).read_bytes()
        require(len(data) == rec['bytes'], 'Byte count mismatch: ' + name)
        require(sha(data) == rec['sha256'], 'Digest mismatch: ' + name)
    require(sha((ROOT/'author/AUTHOR_MANIFEST.json').read_bytes()) == AUTHOR_MANIFEST,
            'Pinned author manifest mismatch')
    require(sha((ROOT/'audit/AUDIT_MANIFEST.json').read_bytes()) == AUDIT_MANIFEST,
            'Pinned audit manifest mismatch')
    return len(actual) + 1


def run(script, *args):
    result = subprocess.run([sys.executable, '-B', str(script), *map(str, args)],
                            check=True, capture_output=True)
    return result.stdout


def main():
    file_count = verify_files()
    audit = json.loads(run(ROOT/'audit/verify_audit.py', '--author', ROOT/'author'))
    binding = json.loads(run(ROOT/'audit/binding_checks.py', '--author', ROOT/'author',
                            '--negative-controls'))
    require(binding['negative_control_count'] == 7, 'Integrity control count')
    require(all(x['status'] == 'REJECTED' for x in binding['negative_controls']),
            'Integrity mutation accepted')
    with tempfile.TemporaryDirectory(prefix='kp2998_release_') as temporary:
        temp = Path(temporary)
        shutil.copy2(ROOT/'author/controls.py', temp/'controls.py')
        run(temp/'controls.py')
        output = (temp/'CONTROL_RESULTS.json').read_bytes()
        require(output == (ROOT/'author/CONTROL_RESULTS.json').read_bytes(),
                'Author arithmetic replay differs')
        author_controls = json.loads(output)
    independent_raw = run(ROOT/'audit/independent_controls.py')
    require(independent_raw == (ROOT/'audit/INDEPENDENT_CONTROL_RESULTS.json').read_bytes(),
            'Independent arithmetic replay differs')
    independent = json.loads(independent_raw)
    require(independent['negative_control_count'] == 10, 'Arithmetic control count')
    require(all(x['status'] == 'REJECTED' for x in independent['negative_controls'].values()),
            'Arithmetic mutation accepted')
    require(verify_files() == file_count, 'Files changed during replay')
    print(json.dumps({
        'status': 'PASS_RELEASE_BINDINGS_AND_FINITE_ARITHMETIC_REPLAY',
        'problem_id': 2998, 'disposition': 'unsolved', 'turns': '5/5',
        'full_solution_claimed': False, 'release_files': file_count,
        'author_files': audit['author_total_files'],
        'audit_files': audit['audit_payload_files'] + 1,
        'author_manifest_sha256': AUTHOR_MANIFEST,
        'author_tree_sha256': binding['author_tree_sha256'],
        'audit_manifest_sha256': AUDIT_MANIFEST,
        'strict_integrity_negative_controls': 7,
        'independent_arithmetic_negative_controls': 10,
        'author_counted_cases': sum(author_controls['counts'].values()),
        'independent_counts': independent['counts'],
        'outputs_byte_identical': True,
        'historical_author_verifier_used_as_gate': False,
        'limitations': 'Finite controls do not prove geometric realization, topology theorems, universality, novelty, global openness or CI success.'
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
