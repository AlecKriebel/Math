#!/usr/bin/env python3
"""Offline fail-closed binding and assertion-enabled replay of scoped partials."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import zipfile

PINS = {
    'safe_release/MANIFEST.json': '913457490b8f076c4a5035e6bcb32016a69dfe1a6c97a56ad396fc16882e23cf',
    'audit_release/MANIFEST.json': 'bfe47987a59ac1e9ec5f32527411a6ede96495ae42ebb647a6576a1a4c991cba',
    'LITTLEWOOD_30003114_SAFE_PACKET.zip': '443d5dc030e08c32e7a758c0eb1f5ab63eb8673f0a4dfd13930f2a60f568f228',
    'LITTLEWOOD_30003114_INDEPENDENT_AUDIT.zip': '09e9cffe79b52aadad8aaa263998b0326018abef8d01781fd41ae1774ce8a294',
}

def need(condition, message):
    if not condition:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def regular(path):
    need(path.is_file() and not path.is_symlink(), 'nonregular file: ' + str(path))
    return path.read_bytes()

def bind(root, expected):
    need(re.fullmatch('[0-9a-f]{64}', expected) is not None, 'invalid external pin')
    raw = regular(root / 'MANIFEST.json')
    need(sha(raw) == expected, 'external publication manifest mismatch')
    manifest = json.loads(raw)
    need(manifest['schema'] == 'littlewood-publication-manifest-v1', 'manifest schema')
    names = set()
    for item in manifest['files']:
        need(set(item) == {'path', 'bytes', 'sha256'}, 'record schema')
        name = item['path']
        need(isinstance(name, str) and name not in names and name != 'MANIFEST.json', 'duplicate/self path')
        p = Path(name)
        need(not p.is_absolute() and '..' not in p.parts and str(p) == name, 'unsafe path')
        need(type(item['bytes']) is int and item['bytes'] >= 0, 'invalid byte count')
        need(isinstance(item['sha256'], str) and re.fullmatch('[0-9a-f]{64}', item['sha256']) is not None, 'invalid digest')
        data = regular(root / name)
        need(len(data) == item['bytes'] and sha(data) == item['sha256'], 'file mismatch: ' + name)
        names.add(name)
    entries = list(root.rglob('*'))
    need(not any(p.is_symlink() for p in entries), 'symlink in packet')
    need({p.relative_to(root).as_posix() for p in entries if p.is_file()} == names | {'MANIFEST.json'}, 'unexpected or missing file')
    expected_dirs = {str(p) for name in names for p in Path(name).parents if str(p) != '.'}
    need({p.relative_to(root).as_posix() for p in entries if p.is_dir()} == expected_dirs, 'unexpected directory')
    for name, pin in PINS.items():
        need(sha(regular(root / name)) == pin, 'frozen pin mismatch: ' + name)
    for folder, prefix, archive, count, size in [
        ('safe_release', 'safe', 'LITTLEWOOD_30003114_SAFE_PACKET.zip', 8, 16914),
        ('audit_release', 'independent_audit', 'LITTLEWOOD_30003114_INDEPENDENT_AUDIT.zip', 10, 27071),
    ]:
        need(len(regular(root / archive)) == size, 'archive size mismatch')
        inner = json.loads(regular(root / folder / 'MANIFEST.json'))
        inner_names = ['MANIFEST.json'] + list(inner['files'])
        need(len(inner_names) == count and len(set(inner_names)) == count, 'inner manifest inventory')
        need(set(inner_names) == {p.name for p in (root / folder).iterdir()}, 'inner inventory mismatch')
        for name, row in inner['files'].items():
            need(Path(name).name == name, 'unsafe inner path')
            data = regular(root / folder / name)
            need(len(data) == row['bytes'] and sha(data) == row['sha256'], 'inner manifest binding')
        with zipfile.ZipFile(root / archive) as stream:
            members = stream.infolist()
            need(len(members) == count, 'archive member count')
            need({m.filename for m in members} == {prefix + '/' + x for x in inner_names}, 'archive member set')
            for member in members:
                need(not member.is_dir() and (member.external_attr >> 16) & 0o170000 != 0o120000, 'nonregular archive member')
                name = member.filename.split('/', 1)[1]
                need(stream.read(member) == regular(root / folder / name), 'archive member mismatch')
    metadata = json.loads(regular(root / 'PUBLICATION.json'))
    need(metadata['status'] == 'unsolved' and metadata['turns'] == '5/5' and metadata['target_resolved'] is False and metadata['novelty_claim'] is False, 'status scope')
    return len(names) + 1

def run(arguments, cwd, env):
    return subprocess.run([sys.executable, '-B'] + list(map(str, arguments)), cwd=cwd, env=env, capture_output=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--expected-manifest', required=True)
    parser.add_argument('--queue', type=Path)
    args = parser.parse_args()
    need(__debug__ and sys.flags.optimize == 0, 'Python optimization is forbidden; disabled assertions are not verification')
    sys.dont_write_bytecode = True
    root = Path(__file__).resolve().parent
    count = bind(root, args.expected_manifest)
    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    with tempfile.TemporaryDirectory(prefix='littlewood-publication-replay-') as temp:
        debug = run(['-c', 'print(__debug__)'], temp, env)
        need(debug.returncode == 0 and debug.stdout == b'True\n', 'author assertions not enabled')
        author = run([root / 'safe_release/verify.py'], temp, env)
        need(author.returncode == 0, 'author replay failed: ' + author.stderr.decode())
        need(author.stdout == regular(root / 'safe_release/VERIFICATION.json') == regular(root / 'audit_release/AUTHOR_REPLAY.json'), 'author byte mismatch')
        independent = run([root / 'audit_release/independent_verify.py', '--safe', root / 'safe_release', '--archive', root / 'LITTLEWOOD_30003114_SAFE_PACKET.zip'], temp, env)
        need(independent.returncode == 0, 'independent replay failed: ' + independent.stderr.decode())
        need(independent.stdout == regular(root / 'audit_release/INDEPENDENT_RESULTS.json'), 'independent byte mismatch')
        mutant = Path(temp) / 'author_assertion_mutant.py'
        source = regular(root / 'safe_release/verify.py')
        need(source.count(b'assert GAMMA>0') == 1, 'assertion mutant anchor changed')
        mutant.write_bytes(source.replace(b'assert GAMMA>0', b'assert GAMMA<0', 1))
        failure = run([mutant], temp, env)
        need(failure.returncode != 0 and b'AssertionError' in failure.stderr, 'false assertion was not rejected')
    queue_verified = False
    if args.queue is not None:
        data = regular(args.queue)
        metadata = json.loads(regular(root / 'PUBLICATION.json'))['queue']
        need(len(data) == metadata['updated_bytes'] and sha(data) == metadata['updated_sha256'], 'queue bytes mismatch')
        need(hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == metadata['updated_git_blob_sha1'], 'queue Git blob mismatch')
        queue_verified = True
    need(bind(root, args.expected_manifest) == count, 'packet changed during replay')
    result = json.loads(independent.stdout)
    print(json.dumps({'outcome': 'PASS_FOR_SCOPED_PARTIALS', 'target_resolved': False, 'novelty_claim': False,
        'status': 'unsolved', 'turns': '5/5', 'publication_files': count,
        'external_manifest_sha256': args.expected_manifest, 'assertions_enabled': True,
        'author_byte_exact_match': True, 'independent_byte_exact_match': True, 'false_author_assertion_rejected': True,
        'both_archives_match_frozen_directories': True, 'mathematical_negative_controls': len(result['negative_controls']),
        'independent_integrity_mutations_rejected': len(result['corruption_controls']), 'queue_verified': queue_verified,
        'finite_checks_are_not_all_degree_proof': True}, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
