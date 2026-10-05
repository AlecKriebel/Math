#!/usr/bin/env python3
"""Replay the frozen partial-result publication; no network or third-party modules."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

AUTHOR_PIN = '13a5055116fbed43fe1b2f355da34b8ff12d1e4aba0deac99ee1cbe26b023941'
AUDIT_PIN = '549abc3827d4d6f453a10628dc366e4e8662d47d4fe0e4c9c8d3af60575d7ed7'
AUDIT_REPORT_PIN = 'bb6d01569a67b009181f5cccacb1ac0a8897da513789bf010181268274bba85d'

def need(condition, message):
    if not condition:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def read_regular(path):
    need(not path.is_symlink() and path.is_file(), 'nonregular file: ' + str(path))
    return path.read_bytes()

def bind(root, pin):
    need(re.fullmatch(r'[0-9a-f]{64}', pin) is not None, 'invalid external manifest pin')
    raw = read_regular(root / 'MANIFEST.json')
    need(sha(raw) == pin, 'external publication manifest mismatch')
    manifest = json.loads(raw)
    need(manifest['schema'] == 'prym-publication-manifest-v1', 'manifest schema')
    names = set()
    for item in manifest['files']:
        need(set(item) == {'path', 'bytes', 'sha256'}, 'record schema')
        name = item['path']
        need(isinstance(name, str) and name not in names and name != 'MANIFEST.json', 'duplicate or self record')
        p = Path(name)
        need(not p.is_absolute() and '..' not in p.parts and str(p) == name, 'unsafe path')
        names.add(name)
        need(type(item['bytes']) is int and item['bytes'] >= 0, 'invalid size')
        need(isinstance(item['sha256'], str) and re.fullmatch(r'[0-9a-f]{64}', item['sha256']) is not None, 'invalid digest')
        data = read_regular(root / name)
        need(len(data) == item['bytes'] and sha(data) == item['sha256'], 'file mismatch: ' + name)
    objects = list(root.rglob('*'))
    need(not any(x.is_symlink() for x in objects), 'symlink in publication')
    actual = {x.relative_to(root).as_posix() for x in objects if x.is_file()}
    need(actual == names | {'MANIFEST.json'}, 'unexpected or missing file')
    expected_dirs = {str(p) for name in names for p in Path(name).parents if str(p) != '.'}
    need({x.relative_to(root).as_posix() for x in objects if x.is_dir()} == expected_dirs, 'unexpected directory')
    need(sha(read_regular(root / 'safe/MANIFEST.json')) == AUTHOR_PIN, 'author manifest pin')
    need(sha(read_regular(root / 'audit/MANIFEST.json')) == AUDIT_PIN, 'audit manifest pin')
    need(sha(read_regular(root / 'audit/AUDIT.md')) == AUDIT_REPORT_PIN, 'audit report pin')
    return len(names) + 1

def assertion_probe(path, function, arguments, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        getattr(module, function)(*arguments)
    except AssertionError:
        return True
    raise ValueError('disabled assertion guard: ' + name)

def run(command, directory):
    environment = dict(os.environ)
    environment.pop('PYTHONOPTIMIZE', None)
    environment['PYTHONDONTWRITEBYTECODE'] = '1'
    result = subprocess.run(command, cwd=directory, env=environment, capture_output=True, text=True)
    need(result.returncode == 0, 'replay failed: ' + result.stderr)
    return json.loads(result.stdout)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--expected-manifest', required=True, help='Externally recorded SHA-256, supplied by the caller.')
    parser.add_argument('--queue', type=Path)
    args = parser.parse_args()
    need(__debug__ and sys.flags.optimize == 0, 'run without Python optimization')
    sys.dont_write_bytecode = True
    root = Path(__file__).resolve().parent
    count = bind(root, args.expected_manifest)
    probes = {
        'author': assertion_probe(root / 'safe/verify.py', 'check', (False, 'publication false-input probe'), 'prym_author_probe'),
        'independent': assertion_probe(root / 'audit/independent_controls.py', 'chk', (False, 'publication false-input probe'), 'prym_audit_probe'),
    }
    with tempfile.TemporaryDirectory(prefix='prym-portable-replay-') as temporary:
        author = run([sys.executable, '-B', str(root / 'safe/verify.py')], temporary)
        output = Path(temporary) / 'independent.json'
        independent = run([sys.executable, '-B', str(root / 'audit/independent_controls.py'), '--packet', str(root / 'safe'), '--output', str(output)], temporary)
        need(output.read_bytes() == read_regular(root / 'audit/INDEPENDENT_RESULTS.json'), 'independent replay differs')
    need(author == json.loads(read_regular(root / 'audit/AUTHOR_REPLAY.json')), 'author replay differs')
    need(author['assertions'] == 5325 and author['total_graphs'] == 772, 'author counts')
    need(independent['assertions'] == 578827 and independent['full_cycle_lattice_graphs'] == 27476, 'audit counts')
    need(independent['fixed_node_algebraic_graphs'] == 3848 and independent['fixed_node_even_branch_degree_realizable_graphs'] == 424, 'geometric fixture scope')
    need(len(author['integrity_negative_controls_rejected']) == 8 and len(independent['integrity_negative_controls_rejected']) == 11, 'mutation control counts')
    queue_verified = False
    if args.queue is not None:
        data = read_regular(args.queue)
        record = json.loads(read_regular(root / 'PUBLICATION.json'))['queue']
        need(len(data) == record['updated_bytes'] and sha(data) == record['updated_sha256'], 'queue mismatch')
        need(hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == record['updated_git_blob_sha1'], 'queue Git blob mismatch')
        queue_verified = True
    need(bind(root, args.expected_manifest) == count, 'publication changed during replay')
    print(json.dumps({'outcome': 'PASS_SCOPED_REPLAY_NOT_UNIVERSAL_PROOF', 'files': count, 'external_manifest_sha256': args.expected_manifest, 'assertion_failure_probes': probes, 'author_assertions': author['assertions'], 'independent_assertions': independent['assertions'], 'author_integrity_negatives': 8, 'independent_integrity_negatives': 11, 'independent_result_byte_identical': True, 'queue_verified': queue_verified, 'full_target_status': 'unsolved', 'approaches': '5/5'}, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
