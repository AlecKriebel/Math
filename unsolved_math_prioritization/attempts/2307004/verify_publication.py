#!/usr/bin/env python3
"""Strict portable integrity and exact finite replays; no all-degree claim."""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
AUTHOR = 'cd89e252a6d2e0ad4eeaa9696e361c99f68c4fb89419f94c6f78e66402a16dac'
AUDIT = '8cf2334148e42caee99ea64a5b0ebcba72898126564035021c2c421dde6dd7ce'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def unique(pairs):
    out = {}
    for key, value in pairs:
        need(key not in out, 'duplicate JSON key: ' + key)
        out[key] = value
    return out


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique)


def inventory(root, rows, extra):
    expected = {}
    for row in rows:
        name = row['path']
        need(isinstance(name, str), 'invalid path type')
        path = PurePosixPath(name)
        need(name and not path.is_absolute() and '..' not in path.parts
             and '\\' not in name and name == path.as_posix(), 'unsafe path')
        need(name not in extra and name not in expected, 'duplicate manifest path')
        need(type(row['bytes']) is int and row['bytes'] >= 0, 'invalid size')
        expected[name] = row
    need(not any(p.is_symlink() for p in root.rglob('*')), 'symlink in packet')
    names = set(expected) | set(extra)
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    need(actual == names, 'strict file inventory mismatch')
    dirs = {p.as_posix() for name in names for p in PurePosixPath(name).parents
            if p.as_posix() != '.'}
    need({p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_dir()} == dirs,
         'strict directory inventory mismatch')
    for name, row in expected.items():
        data = (root / name).read_bytes()
        need(len(data) == row['bytes'] and sha(data) == row['sha256'], 'content mismatch: ' + name)
    return len(names)


def main():
    manifest = read_json(ROOT / 'PUBLICATION_MANIFEST.json')
    need(manifest['problem_id'] == '2307004', 'publication target mismatch')
    count = inventory(ROOT, manifest['files'], {'PUBLICATION_MANIFEST.json'})
    need(count == 28 and manifest['file_count_excluding_manifest'] == 27, 'publication count')
    packet = ROOT / 'safe_output'
    audit = ROOT / 'independent_audit'
    need(sha((packet / 'FREEZE_MANIFEST.json').read_bytes()) == AUTHOR, 'author freeze identity')
    need(sha((audit / 'AUDIT_BINDING.json').read_bytes()) == AUDIT, 'audit freeze identity')
    frozen = read_json(packet / 'FREEZE_MANIFEST.json')
    need(frozen['file_count'] == 15 and len(frozen['files']) == 15, 'author entry count')
    need(inventory(packet, frozen['files'], {'FREEZE_MANIFEST.json'}) == 16, 'author count')
    binding = read_json(audit / 'AUDIT_BINDING.json')
    need(binding['input_manifest_sha256'] == AUTHOR and binding['input_frozen_file_count'] == 16,
         'audit input binding')
    need(inventory(packet, binding['input_files'], set()) == 16, 'audit-bound author count')
    need(binding['audit_artifact_count_excluding_binding'] == 6, 'audit entry count')
    need(inventory(audit, binding['audit_files'], {'AUDIT_BINDING.json'}) == 7, 'audit count')
    scope = read_json(ROOT / 'PUBLICATION_SCOPE.json')
    need(scope['queue_status'] == 'unsolved' and scope['turns'] == '5/5', 'queue disposition')
    for key in ('full_problem_solved', 'novelty_claim', 'human_peer_review', 'formal_proof_assistant',
                'finite_certificate_is_optimal', 'strict_half_proof_supplies_uniform_positive_gap',
                'inf_all_n_identified_with_limsup', 'recent_2026_proposal_adopted_as_theorem',
                'source_pdfs_or_text_included', 'source_corpora_freshly_verified'):
        need(scope[key] is False, 'scope guard: ' + key)
    need(scope['discovery_count'] == 0 and scope['n2_exact_optimum'] == 'sqrt(3-sqrt(5))',
         'mathematical disposition')
    need(scope['finite_certificate_n'] == 32 and scope['finite_certificate_strict_radius'] == '29/40',
         'finite certificate scope')
    need(scope['author_manifest_sha256'] == AUTHOR and scope['audit_binding_sha256'] == AUDIT,
         'scope binding')
    meta = read_json(audit / 'AUDIT_METADATA.json')
    need(meta['verdict'] == scope['audit_verdict'] == 'PASS_SCOPED_PARTIALS_UNSOLVED_5_OF_5'
         and meta['blocking_findings'] == [] and meta['required_corrections'] == [], 'audit verdict')
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    env.pop('PYTHONOPTIMIZE', None)
    # Never disable the original verifier's assertions, even when this wrapper uses -O.
    author = subprocess.run([sys.executable, '-B', str(packet / 'verify_exact.py')],
                            capture_output=True, check=True, env=env)
    need(author.stdout == (packet / 'VERIFICATION.json').read_bytes()
         == (audit / 'AUTHOR_REPLAY.json').read_bytes(), 'author replay bytes')
    denied = subprocess.run([sys.executable, '-B', '-O', str(packet / 'verify_exact.py')],
                            capture_output=True, env=env)
    need(denied.returncode != 0 and b'Assertions must be enabled' in denied.stderr,
         'author optimized-mode refusal missing')
    for flags in ([], ['-O']):
        run = subprocess.run([sys.executable, '-B', *flags,
                              str(audit / 'check_certificate_independent.py'), str(packet)],
                             capture_output=True, check=True, env=env)
        need(run.stdout == (audit / 'INDEPENDENT_REPLAY.json').read_bytes(), 'independent replay bytes')
    inventory(ROOT, manifest['files'], {'PUBLICATION_MANIFEST.json'})
    print(json.dumps({'result': 'PASS', 'files_verified': count, 'frozen_author_files': 16,
                      'audit_files': 7, 'strict_inventory': True, 'author_replay': 'byte-identical',
                      'author_assertions_enabled': True, 'author_optimized_mode': 'correctly refused',
                      'independent_normal_and_optimized': 'byte-identical',
                      'strict_moment_inequalities': 32, 'strict_radius': '29/40',
                      'full_problem_solved': False, 'formal_proof_assistant': False},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
