#!/usr/bin/env python3
"""Fail-closed offline publication binding and assertion-enabled scoped replay."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import zipfile

PINS = {
    'author/safe/MANIFEST.json': 'bb24c27fef83fcc14106cbcc068a02f740c0b35385b79e6c7799371764ea9bdb',
    'author/SIS_30003676_SAFE.zip': '70191b3887e8863701651cdb54382958e1f8190fd889889a2ed81c46f16ee6a6',
    'independent_audit/MANIFEST.json': '2afb4fb797ff8db6b265ba97799681b31c29219d709b3a0b83e8e5cebb0828aa',
    'SIS_30003676_INDEPENDENT_AUDIT.zip': '00b486a241fb56a1fb9a935756384e1a0943ec8669fb61ffa825fdf2db3ee325',
    'independent_audit/AUTHORITATIVE_CORRECTIONS.md': 'd333f7378912baa55942451a495e30a3ebe63722567cd5352325541c26ed22ca',
}

def need(condition, message):
    if not condition:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def regular(path):
    need(path.is_file() and not path.is_symlink(), 'Nonregular file: ' + str(path))
    return path.read_bytes()

def bind(root, expected):
    need(re.fullmatch('[0-9a-f]{64}', expected) is not None, 'Invalid external pin')
    raw = regular(root / 'MANIFEST.json')
    need(sha(raw) == expected, 'External manifest mismatch')
    manifest = json.loads(raw)
    need(manifest['schema'] == 'sis-30003676-publication-manifest-v1', 'Manifest schema')
    names = set()
    for item in manifest['files']:
        need(set(item) == {'path', 'bytes', 'sha256'}, 'Record schema')
        name = item['path']
        need(isinstance(name, str) and name not in names and name != 'MANIFEST.json', 'Duplicate/self path')
        p = Path(name)
        need(not p.is_absolute() and '..' not in p.parts and str(p) == name, 'Unsafe path')
        need(type(item['bytes']) is int and item['bytes'] >= 0, 'Invalid bytes')
        need(isinstance(item['sha256'], str) and re.fullmatch('[0-9a-f]{64}', item['sha256']) is not None, 'Invalid hash')
        data = regular(root / name)
        need(len(data) == item['bytes'] and sha(data) == item['sha256'], 'File mismatch: ' + name)
        names.add(name)
    entries = list(root.rglob('*'))
    need(not any(p.is_symlink() for p in entries), 'Symlink in packet')
    need({p.relative_to(root).as_posix() for p in entries if p.is_file()} == names | {'MANIFEST.json'}, 'File inventory mismatch')
    dirs = {str(p) for name in names for p in Path(name).parents if str(p) != '.'}
    need({p.relative_to(root).as_posix() for p in entries if p.is_dir()} == dirs, 'Directory inventory mismatch')
    for name, pin in PINS.items():
        need(sha(regular(root / name)) == pin, 'Frozen pin mismatch: ' + name)
    for folder, prefix, archive, count, size in [
        ('author/safe', 'safe', 'author/SIS_30003676_SAFE.zip', 10, 22001),
        ('independent_audit', 'independent_audit', 'SIS_30003676_INDEPENDENT_AUDIT.zip', 11, 27205),
    ]:
        need(len(regular(root / archive)) == size, 'Archive size mismatch')
        inner = json.loads(regular(root / folder / 'MANIFEST.json'))['files']
        inner_names = ['MANIFEST.json'] + [x['path'] for x in inner]
        need(len(inner_names) == len(set(inner_names)) == count, 'Inner duplicate/count')
        need(set(inner_names) == {p.name for p in (root / folder).iterdir()}, 'Inner inventory')
        for row in inner:
            need(Path(row['path']).name == row['path'], 'Unsafe inner path')
            data = regular(root / folder / row['path'])
            need(len(data) == row['bytes'] and sha(data) == row['sha256'], 'Inner binding')
        with zipfile.ZipFile(root / archive) as stream:
            members = stream.infolist()
            need(len(members) == count, 'Archive count')
            need({m.filename for m in members} == {prefix + '/' + x for x in inner_names}, 'Archive names')
            for member in members:
                need(not member.is_dir() and (member.external_attr >> 16) & 0o170000 != 0o120000, 'Archive nonregular')
                need(stream.read(member) == regular(root / folder / member.filename.split('/', 1)[1]), 'Archive content')
    metadata = json.loads(regular(root / 'PUBLICATION.json'))
    need(metadata['status'] == 'unsolved' and metadata['turns'] == '5/5' and metadata['target_resolved'] is False and metadata['novelty_claim'] is False, 'Status scope')
    need(metadata['frozen_report_alone'] == 'REVISE_REQUIRED' and metadata['composite_with_authoritative_overlay'] == 'PASS_FOR_SCOPED_PARTIALS', 'Composite-only verdict')
    need(metadata['mandatory_overlay'] == 'independent_audit/AUTHORITATIVE_CORRECTIONS.md' and metadata['correction_ids'] == ['C1', 'C2', 'C3'], 'Overlay gate')
    return len(names) + 1

def run(arguments, cwd, env):
    return subprocess.run([sys.executable, '-B'] + list(map(str, arguments)), cwd=cwd, env=env, capture_output=True)

def compare_diagnostics(actual, expected):
    need(type(actual) is type(expected), 'Diagnostic type')
    if isinstance(expected, dict):
        need(actual.keys() == expected.keys(), 'Diagnostic keys')
        for key in expected:
            compare_diagnostics(actual[key], expected[key])
    elif isinstance(expected, list):
        need(len(actual) == len(expected), 'Diagnostic count')
        for left, right in zip(actual, expected):
            compare_diagnostics(left, right)
    elif isinstance(expected, float):
        need(math.isfinite(actual) and math.isclose(actual, expected, rel_tol=1e-11, abs_tol=1e-10), 'Diagnostic tolerance')
    else:
        need(actual == expected, 'Diagnostic parameter')

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
    with tempfile.TemporaryDirectory(prefix='sis-publication-replay-') as temp:
        debug = run(['-c', 'print(__debug__)'], temp, env)
        need(debug.returncode == 0 and debug.stdout == b'True\n', 'Assertions not enabled')
        frozen = run([root / 'independent_audit/verify_frozen.py', root / 'author'], temp, env)
        need(frozen.returncode == 0, 'Frozen replay failed: ' + frozen.stderr.decode())
        need(frozen.stdout == regular(root / 'independent_audit/frozen_replay.json'), 'Frozen replay bytes')
        audit_manifest = run([root / 'independent_audit/verify_audit_manifest.py'], temp, env)
        need(audit_manifest.returncode == 0 and json.loads(audit_manifest.stdout)['status'] == 'PASS', 'Audit manifest replay')
        independent = run([root / 'independent_audit/independent_checks.py'], temp, env)
        need(independent.returncode == 0, 'Independent replay failed: ' + independent.stderr.decode())
        actual = json.loads(independent.stdout)
        expected = json.loads(regular(root / 'independent_audit/independent_results.json'))
        floating = {'floating_diagnostics_not_proofs', 'fast_immigration_diagnostics_not_proofs'}
        need({k: v for k, v in actual.items() if k not in floating} == {k: v for k, v in expected.items() if k not in floating}, 'Independent exact fields')
        need(actual['exact_checks'] == 1407 and actual['wrong_model_rejections'] == 8, 'Independent counts')
        for key in floating:
            compare_diagnostics(actual[key], expected[key])
        mutant = Path(temp) / 'false_author_assertion.py'
        source = regular(root / 'author/safe/verify.py')
        anchor = b'assert all(len(row) == n + 1 for row in m)'
        need(source.count(anchor) == 1, 'Assertion mutant anchor')
        mutant.write_bytes(source.replace(anchor, b'assert False, "synthetic execution control"', 1))
        failure = run([mutant], temp, env)
        need(failure.returncode != 0 and b'AssertionError' in failure.stderr, 'False assertion escaped')
    queue_verified = False
    if args.queue is not None:
        data = regular(args.queue)
        metadata = json.loads(regular(root / 'PUBLICATION.json'))['queue']['updated']
        need(len(data) == metadata['bytes'] and sha(data) == metadata['sha256'], 'Queue bytes')
        need(hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == metadata['git_blob_sha1'], 'Queue Git blob')
        queue_verified = True
    need(bind(root, args.expected_manifest) == count, 'Packet changed during replay')
    print(json.dumps({'status': 'PASS_FOR_SCOPED_PARTIALS_WITH_MANDATORY_OVERLAY', 'target_resolved': False,
        'frozen_report_alone': 'REVISE_REQUIRED', 'queue_status': 'unsolved', 'turns': '5/5',
        'publication_files': count, 'manifest_sha256': args.expected_manifest, 'assertions_enabled': True,
        'author_exact_checks': 436, 'author_replay_byte_identical': True, 'independent_exact_checks': 1407,
        'independent_exact_fields_equal': True, 'independent_wrong_model_rejections': 8,
        'frozen_replay_byte_identical': True, 'both_archives_match_frozen_directories': True,
        'author_integrity_controls_rejected': 2, 'independent_integrity_controls_rejected': 4,
        'false_author_assertion_rejected': True, 'floating_diagnostics_compared': 63,
        'floating_relative_tolerance': 1e-11, 'floating_absolute_tolerance': 1e-10,
        'finite_checks_do_not_prove_asymptotics': True, 'queue_verified': queue_verified}, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
