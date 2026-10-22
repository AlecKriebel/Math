#!/usr/bin/env python3
"""Fail-closed, relocatable replay. No operator-algebra theorem is machine proved."""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
PINS = {
    'safe_packet_v1/MANIFEST.json': '43863e0dbc15491bf5ee67adf3cd1a516c487e3224a193fd267ed5a5c7ae3dfd',
    'independent_audit_v1/MANIFEST.json': '3faf757fd24527706179c0ed91c8fd17b4b9e3d7ea0ee7c89d6aaf40786d6a15',
    'independent_audit_v1/AUDIT.md': '8bea6082b72876dd0fec1eae4e2550d2d69f87682e0c18efeb5433dbab70fd13',
}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def child_env():
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONOPTIMIZE='0')
    env.pop('PYTHONPATH', None)
    env.pop('PYTHONHOME', None)
    return env


def run(script, *arguments):
    return subprocess.check_output([sys.executable, '-B', str(ROOT / script),
                                    *map(str, arguments)], cwd=ROOT, env=child_env())


def main():
    require(sys.version_info >= (3, 8), 'Python 3.8 or newer required')
    raw_manifest = (ROOT / 'PUBLICATION_MANIFEST.json').read_bytes()
    manifest = json.loads(raw_manifest)
    require(manifest['problem_id'] == '30004279', 'Wrong target')
    require(manifest['status'] == 'unsolved' and manifest['turns'] == '5/5', 'Wrong disposition')
    records = {row['path']: row for row in manifest['files']}
    require(len(records) == len(manifest['files']) == 19, 'Wrong payload inventory')
    for name in records:
        path = PurePosixPath(name)
        require(not path.is_absolute() and '..' not in path.parts and str(path) == name, 'Unsafe path')
    for path in ROOT.rglob('*'):
        require(not path.is_symlink(), 'Symlink in packet')
        require(path.is_file() or path.is_dir(), 'Special file in packet')
    actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}
    require(actual == set(records) | {'PUBLICATION_MANIFEST.json'}, 'Unexpected or missing file')
    require({p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_dir()}
            == {'safe_packet_v1', 'independent_audit_v1'}, 'Unexpected directory set')
    before = {}
    for name, row in records.items():
        raw = (ROOT / name).read_bytes()
        require(len(raw) == row['bytes'] and digest(raw) == row['sha256'], 'Integrity mismatch: ' + name)
        before[name] = raw
    for name, sha in PINS.items():
        require(digest(before[name]) == sha, 'Frozen binding mismatch: ' + name)
    for dirname, payload_count in [('safe_packet_v1', 8), ('independent_audit_v1', 6)]:
        inner = json.loads(before[dirname + '/MANIFEST.json'])
        require(len(inner['files']) == payload_count, 'Frozen payload count differs')
        expected = {row['path'] for row in inner['files']} | {'MANIFEST.json'}
        require({p.name for p in (ROOT / dirname).iterdir()} == expected, 'Frozen file set differs')
        for row in inner['files']:
            raw = before[dirname + '/' + row['path']]
            require(len(raw) == row['bytes'] and digest(raw) == row['sha256'], 'Frozen payload differs')
    binding = json.loads(before['independent_audit_v1/BINDING.json'])
    results = json.loads(before['independent_audit_v1/RESULTS.json'])
    status = json.loads(before['PUBLICATION_STATUS.json'])
    require(binding['expected_manifest_sha256'] == PINS['safe_packet_v1/MANIFEST.json'], 'Input binding differs')
    require(binding['payloads'] == json.loads(before['safe_packet_v1/MANIFEST.json'])['files'], 'Audit payload binding differs')
    require(results['verdict'] == status['audit_verdict'] == 'pass_as_bounded_unsuccessful_research', 'Wrong audit verdict')
    require(not results['original_target_solved'] and not results['substantive_mathematical_corrections_required'], 'Audit disposition differs')
    require(results['substantive_approach_units'] == 5 and status['turns'] == '5/5' and status['status'] == 'unsolved', 'Route budget differs')
    # An actual assert failure proves Python assertions execute in this child mode.
    # No -O flag is forwarded, even if this entrypoint was invoked under -O/-OO.
    probe = subprocess.run([sys.executable, '-B', '-c',
                            'import sys; assert sys.flags.optimize == 0; assert False, "assertion_probe"'],
                           cwd=ROOT, env=child_env(), capture_output=True)
    require(probe.returncode != 0 and b'AssertionError: assertion_probe' in probe.stderr,
            'Child assertions disabled or probe failed unexpectedly')
    authored = run('safe_packet_v1/verify.py')
    require(authored == before['safe_packet_v1/checks.json'], 'Author replay bytes differ')
    independent = run('independent_audit_v1/independent_controls.py', '--packet', ROOT / 'safe_packet_v1')
    require(independent == before['independent_audit_v1/independent_checks.json'], 'Independent replay bytes differ')
    a, b = json.loads(authored), json.loads(independent)
    require(a['passed_assertions'] == 47 and b['passed_assertions'] == 113, 'Assertion counts differ')
    require(not a['verified_original_conjecture'] and not b['complete_original_solution'], 'Incorrect solution claim')
    require(len(b['author_mutation_controls']) == 3 and all(r['assertion_failure'] and r['exit_code'] != 0
            for r in b['author_mutation_controls']), 'Mutation rejection differs')
    require(all((ROOT / name).read_bytes() == raw for name, raw in before.items()), 'Packet changed during replay')
    require((ROOT / 'PUBLICATION_MANIFEST.json').read_bytes() == raw_manifest, 'Manifest changed')
    require({p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()} == actual, 'Replay created files')
    print(json.dumps({
        'result': 'PASS', 'problem_id': '30004279', 'status': 'unsolved', 'turns': '5/5',
        'packet_files': 20, 'original_files_preserved': 16,
        'author_assertions': 47, 'independent_controls': 113,
        'author_replay_byte_equal': True, 'independent_replay_byte_equal': True,
        'author_mutation_rejections': 3, 'child_optimization': 0,
        'assert_false_probe_failed_as_required': True,
        'publication_manifest_sha256': digest(raw_manifest),
        'scope': 'Integrity and finite controls supplement written operator-algebra arguments. No full soliton equivalence, novelty, or global openness certified.'
    }, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
