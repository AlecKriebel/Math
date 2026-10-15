#!/usr/bin/env python3
"""Fail-closed, relocatable offline replay of the frozen Andreadakis packet."""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
PINS = {
    'release/MANIFEST.json': '9770e7f73a5ffc81f52d92c38f3bebcc9714b470b854f9281e9749b4584591be',
    'release/PROOF.md': '8af19a27cb2204bc51439c13136f8a26e99aca81bfc6e796a556cbec56bafd6e',
    'independent_audit/AUDIT_MANIFEST.json': 'db5425884a41314f3a1e5c304a0dab159b2b6c07be8ff2a17a9573b35df85921',
    'independent_audit/AUDIT.md': '2cda2067975eb38b39545afeed08495df3592e10324fbc28f788e962dafe873a',
    'independent_audit/BINDING.json': '5804cbfea42e5e90288116b2df59554000c92ba2edb68f5fad586b09ff8ec526',
}


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def run(script, *arguments):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONOPTIMIZE='0')
    env.pop('PYTHONPATH', None)
    env.pop('PYTHONHOME', None)
    # No -O is forwarded: all historical assert statements must execute.
    return subprocess.check_output([sys.executable, '-B', str(ROOT / script),
                                    *map(str, arguments)], cwd=ROOT, env=env)


def main():
    require(sys.version_info >= (3, 8), 'Python 3.8 or newer required')
    manifest_raw = (ROOT / 'PUBLICATION_MANIFEST.json').read_bytes()
    manifest = json.loads(manifest_raw)
    require(manifest['problem_id'] == '30003703', 'Wrong target')
    require(manifest['status'] == 'claimed_solved' and manifest['turns'] == '1/5', 'Wrong gate')
    records = {row['path']: row for row in manifest['files']}
    require(len(records) == len(manifest['files']), 'Duplicate file record')
    require(len(records) == 22, 'Wrong payload count')
    for name in records:
        path = PurePosixPath(name)
        require(not path.is_absolute() and '..' not in path.parts and str(path) == name, 'Unsafe path')
    for path in ROOT.rglob('*'):
        require(not path.is_symlink(), 'Symlink in packet')
        require(path.is_file() or path.is_dir(), 'Special file in packet')
    actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}
    require(actual == set(records) | {'PUBLICATION_MANIFEST.json'}, 'Unexpected or missing file')
    dirs = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_dir()}
    require(dirs == {'release', 'independent_audit'}, 'Unexpected directory set')
    before = {}
    for name, row in records.items():
        raw = (ROOT / name).read_bytes()
        require(len(raw) == row['bytes'] and digest(raw) == row['sha256'], 'Integrity mismatch: ' + name)
        before[name] = raw
    for name, sha in PINS.items():
        require(digest(before[name]) == sha, 'Frozen binding mismatch: ' + name)
    for dirname, filename in [('release', 'MANIFEST.json'), ('independent_audit', 'AUDIT_MANIFEST.json')]:
        inner = json.loads(before[dirname + '/' + filename])
        expected = {row['path'] for row in inner['files']} | {filename}
        require({p.name for p in (ROOT / dirname).iterdir()} == expected, 'Frozen file set differs')
        for row in inner['files']:
            raw = before[dirname + '/' + row['path']]
            require(len(raw) == row['bytes'] and digest(raw) == row['sha256'], 'Frozen payload differs')
    status = json.loads(before['PUBLICATION_STATUS.json'])
    binding = json.loads(before['independent_audit/BINDING.json'])
    require(status['accepted_claims'] == binding['claims_accepted'], 'Accepted claims differ')
    require(binding['verdict'] == 'ACCEPT_COMPLETE_COUNTEREXAMPLE', 'Audit verdict differs')
    require(not binding['unresolved_mathematical_gaps'], 'Unresolved gap')
    authored = run('release/verify.py')
    require(authored == before['release/verification.json'], 'Author replay bytes differ')
    author_validation = json.loads(run('release/validate_release.py'))
    independent = run('independent_audit/independent_controls.py', '--release', ROOT / 'release')
    require(independent == before['independent_audit/independent_results.json'], 'Independent replay bytes differ')
    audit_validation = json.loads(run('independent_audit/validate_audit.py', '--release', ROOT / 'release'))
    require(author_validation['result'] == audit_validation['result'] == 'PASS', 'Validator failed')
    require(len(json.loads(independent)['negative_controls']) == 12, 'Negative control count differs')
    require(len(json.loads(authored)['negative_controls']) == 5, 'Author control count differs')
    require(all((ROOT / name).read_bytes() == raw for name, raw in before.items()), 'Packet changed during replay')
    require((ROOT / 'PUBLICATION_MANIFEST.json').read_bytes() == manifest_raw, 'Manifest changed')
    require({p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()} == actual, 'Replay created files')
    print(json.dumps({'result': 'PASS', 'problem_id': '30003703',
                      'status': 'claimed_solved', 'turns': '1/5',
                      'packet_files': 23, 'original_files_preserved': 19,
                      'author_replay_byte_equal': True, 'independent_replay_byte_equal': True,
                      'author_negative_controls': 5, 'independent_negative_controls': 12,
                      'assertions_enabled_in_frozen_subprocesses': True,
                      'author_validation': author_validation, 'audit_validation': audit_validation,
                      'publication_manifest_sha256': digest(manifest_raw),
                      'scope': 'Integrity and exact symbolic controls supplement the written proof; no novelty certification.'}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
