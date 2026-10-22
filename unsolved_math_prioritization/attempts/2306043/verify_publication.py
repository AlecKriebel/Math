#!/usr/bin/env python3
"""Strict portable integrity and finite replays; not a formal proof engine."""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
AUTHOR = '21ac6f2720eb4492499e1034053e9652bbc41fca6b47613077cfb05eece936f6'
AUDIT = '29f15cd74cf5fe9b2c8f4ee02b87322d495c625a9b4c7af4e75549e504e58b77'


def need(condition, label):
    if not condition:
        raise ValueError(label)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def unique(pairs):
    result = {}
    for k, v in pairs:
        need(k not in result, 'duplicate JSON key: ' + k)
        result[k] = v
    return result


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique)


def inventory(root, manifest):
    rows = read_json(root / manifest)['files']
    expected = {}
    for row in rows:
        name = row['path']
        need(isinstance(name, str), 'invalid path type')
        p = PurePosixPath(name)
        need(name and not p.is_absolute() and '..' not in p.parts
             and '\\' not in name and name == p.as_posix(), 'unsafe path')
        need(name != manifest and name not in expected, 'duplicate manifest path')
        need(type(row['bytes']) is int and row['bytes'] >= 0, 'invalid size')
        expected[name] = row
    need(not any(p.is_symlink() for p in root.rglob('*')), 'symlink in packet')
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    need(actual == set(expected) | {manifest}, 'strict inventory mismatch')
    expected_dirs = {parent.as_posix() for name in expected
                     for parent in PurePosixPath(name).parents if parent.as_posix() != '.'}
    actual_dirs = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_dir()}
    need(actual_dirs == expected_dirs, 'strict directory inventory mismatch')
    for name, row in expected.items():
        data = (root / name).read_bytes()
        need(len(data) == row['bytes'] and sha(data) == row['sha256'],
             'content mismatch: ' + name)
    return len(expected)


def main():
    count = inventory(ROOT, 'PUBLICATION_MANIFEST.json')
    packet = ROOT / 'freeze/public'
    audit = ROOT / 'independent_audit'
    need(sha((packet / 'FROZEN_MANIFEST.json').read_bytes()) == AUTHOR, 'author freeze identity')
    need(sha((audit / 'AUDIT_MANIFEST.json').read_bytes()) == AUDIT, 'audit freeze identity')
    need(inventory(packet, 'FROZEN_MANIFEST.json') == 13, 'author file count')
    need(inventory(audit, 'AUDIT_MANIFEST.json') == 3, 'audit file count')
    scope = read_json(ROOT / 'PUBLICATION_SCOPE.json')
    need(scope['queue_status'] == 'unsolved' and scope['turns'] == '5/5', 'queue disposition')
    need(scope['full_problem_solved'] is False and scope['discovery_count'] == 0
         and scope['novelty_claim'] is False, 'full target scope')
    need(scope['positive_index_radial_limit'] == 1
         and scope['positive_index_cesaro_limit'] == 1
         and scope['zero_index_full_class_resolved'] is False, 'index scope')
    need(scope['relaxed_map_univalent'] is False
         and scope['counterexample_in_S'] is False, 'non-univalence safeguard')
    need(scope['hayman_original_construction_inspected'] is False
         and scope['full_imported_theorem_proofs_reconstructed'] is False
         and scope['original_source_corpora_freshly_verified'] is False, 'source-proof limits')
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    for flags in ([], ['-O']):
        for script, arguments, expected in [
            (packet / 'verify_controls.py', [], packet / 'CONTROL_RESULTS.json'),
            (audit / 'verify_independent.py', [str(packet)], audit / 'AUDIT_RESULTS.json'),
        ]:
            run = subprocess.run([sys.executable, *flags, str(script), *arguments],
                                 capture_output=True, text=True, check=True, env=env)
            actual = json.loads(run.stdout, object_pairs_hook=unique)
            need(actual == read_json(expected), 'complete replay result mismatch')
    need(read_json(packet / 'CONTROL_RESULTS.json')['checks_passed'] == 2945, 'original count')
    need(read_json(audit / 'AUDIT_RESULTS.json')['independent_control_assertions'] == 8564,
         'independent count')
    inventory(ROOT, 'PUBLICATION_MANIFEST.json')
    print(json.dumps({'result': 'PASS', 'files_verified': count + 1,
                      'strict_inventory': True, 'frozen_manifests_verified': 2,
                      'frozen_payload_files': 16, 'normal_and_optimized_replays': 'PASS',
                      'original_assertions': 2945, 'independent_assertions': 8564,
                      'full_problem_solved': False, 'relaxed_map_univalent': False,
                      'formal_proof_certificate': False}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
