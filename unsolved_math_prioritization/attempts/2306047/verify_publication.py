#!/usr/bin/env python3
"""Strict portable integrity and replay for audited partial results, not a formal proof."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
AUTHOR = 'cf78e841bb4c939d8dadefd05f76447a6a5b18629748290a047c9fb03996f932'
AUDIT = '71f7d78c0aa0845cfbc14f1f092fab0e5c2dab09f6b23c0869722333dd4393c3'
LIMITS = ('full_target_solved', 'sharpness_certified', 'novelty_certified',
          'current_global_open_status_certified', 'candidate_membership_independently_proved')


def need(value, label):
    if not value:
        raise ValueError(label)


def unique_object(pairs):
    out = {}
    for key, value in pairs:
        need(key not in out, 'duplicate JSON key')
        out[key] = value
    return out


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_object)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(root):
    need(root.is_dir() and not root.is_symlink(), 'invalid root')
    files, dirs = set(), set()
    for p in root.rglob('*'):
        need(not p.is_symlink(), 'symlink forbidden')
        need(p.is_file() or p.is_dir(), 'nonregular object')
        (files if p.is_file() else dirs).add(p.relative_to(root).as_posix())
    expected_dirs = {str(p) for name in files for p in PurePosixPath(name).parents if str(p) != '.'}
    need(dirs == expected_dirs, 'unexpected empty directory')
    return files


def entries(root, records):
    need(type(records) is list, 'manifest entries must be a list')
    names = set()
    for rec in records:
        name = rec['path']
        need(type(name) is str, 'path must be a string')
        p = PurePosixPath(name)
        need(name and not p.is_absolute() and '..' not in p.parts and p.as_posix() == name
             and '\\' not in name and name != '.', 'unsafe path')
        need(name not in names, 'duplicate manifest path')
        names.add(name)
        path = root / name
        need(path.is_file() and not path.is_symlink(), 'missing or linked file')
        for parent in p.parents:
            need(not (root / parent).is_symlink(), 'linked parent')
        raw = path.read_bytes()
        need(type(rec['bytes']) is int and rec['bytes'] >= 0 and len(raw) == rec['bytes'], 'byte count')
        need(sha(path) == rec['sha256'], 'file hash')
    return names


def verify(root):
    m = read_json(root / 'PUBLICATION_MANIFEST.json')
    need((m['problem_id'], m['rank'], m['status'], m['turns']) ==
         (2306047, 685, 'unsolved', '5/5'), 'target and disposition')
    names = entries(root, m['files'])
    need(inventory(root) == names | {'PUBLICATION_MANIFEST.json'}, 'exact inventory')
    need(sha(root / 'author/MANIFEST.json') == AUTHOR, 'author freeze')
    need(sha(root / 'audit/AUDIT_BINDING.json') == AUDIT, 'audit freeze')
    author = read_json(root / 'author/MANIFEST.json')
    need(entries(root / 'author', author['files']) | {'MANIFEST.json'} == inventory(root / 'author'),
         'author inventory')
    audit = read_json(root / 'audit/AUDIT_BINDING.json')
    need(entries(root / 'audit', audit['safe_audit_files']) | {'AUDIT_BINDING.json'} ==
         inventory(root / 'audit'), 'audit inventory')
    need(entries(root / 'author', audit['frozen_input_files']) == inventory(root / 'author'),
         'audited author inventory')
    need(audit['input_manifest_sha256'] == AUTHOR and
         audit['verdict'] == 'pass_partial_exhausted_5_of_5' and
         audit['blocking_defects'] == [] and audit['required_mathematical_revisions'] == [],
         'independent audit gate')
    need(audit['original_checks_replayed'] == 48 and audit['additional_checks_passed'] == 55,
         'audit control counts')
    for k in ('full_target_solved', 'candidate_membership_independently_proved',
              'sharpness_certified', 'current_open_status_certified', 'novelty_certified'):
        need(audit[k] is False, 'audit limit: ' + k)
    binding = read_json(root / 'BINDING.json')
    need(binding['author_manifest_sha256'] == AUTHOR and binding['audit_binding_sha256'] == AUDIT,
         'binding identities')
    need((binding['problem_id'], binding['rank'], binding['status'], binding['turns'],
          binding['approaches_used']) == (2306047, 685, 'unsolved', '5/5', 5), 'binding disposition')
    need(binding['injectivity_domain'] == 'open unit disk', 'domain guard')
    need(binding['author_checks'] == 48 and binding['independent_checks'] == 55, 'binding counts')
    for k in LIMITS:
        need(binding[k] is False, 'publication limit: ' + k)
    outcome = read_json(root / 'author/READINESS_AND_OUTCOME.json')
    need(outcome['attempt_status'] == 'exhausted' and outcome['turns_used'] == 5 and
         outcome['full_target_solved'] is False, 'frozen author disposition')
    for path in root.rglob('*.json'):
        read_json(path)
    return len(names) + 1


def replay(root):
    # Isolated children ignore inherited -O/PYTHONOPTIMIZE; the originals remain unchanged.
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    env.pop('PYTHONOPTIMIZE', None)
    with tempfile.TemporaryDirectory(prefix='univalent-derivative-replay-') as tmp:
        target = Path(tmp) / 'packet'
        shutil.copytree(root, target)
        verify(target)
        probe = subprocess.run([sys.executable, '-I', '-B', '-c', 'print(__debug__)'],
                               env=env, check=True, capture_output=True)
        need(probe.stdout == b'True\n', 'assertions must remain enabled')
        jobs = [(['author/exact_controls.py'], 'author/EXACT_RESULTS.json', 'checks_passed', 48),
                (['audit/adversarial_checks.py', 'author', 'audit/ADVERSARIAL_RESULTS.json'],
                 'audit/ADVERSARIAL_RESULTS.json', 'independent_checks_passed', 55)]
        for args, output, count_key, count in jobs:
            result = subprocess.run([sys.executable, '-I', '-B', *[str(target / a) for a in args]],
                                    cwd=tmp, env=env, capture_output=True, check=True)
            report = json.loads(result.stdout)
            need(report['status'] == 'passed' and report[count_key] == count, 'control count')
            need((target / output).read_bytes() == (root / output).read_bytes(), 'byte-exact replay')
        verify(target)
    return {'original_controls': 48, 'independent_controls': 55, 'results_byte_exact': True,
            'temporary_copy_only': True, 'frozen_inputs_unchanged': True, 'assertions_enabled': True,
            'formal_proof_certificate': False, 'candidate_membership_independently_proved': False}


def selftest(root):
    cases = ('extra_file', 'empty_directory', 'changed_file', 'missing_file', 'duplicate_entry',
             'unsafe_path', 'symlink', 'symlink_directory', 'duplicate_json_key',
             'changed_author_binding', 'changed_audit_binding', 'changed_turn_count',
             'changed_proof_limit', 'changed_domain', 'changed_disposition')
    rejected = []
    for case in cases:
        with tempfile.TemporaryDirectory(prefix='univalent-derivative-negative-') as tmp:
            target = Path(tmp) / 'packet'
            shutil.copytree(root, target)
            path = target / 'PUBLICATION_MANIFEST.json'
            m = read_json(path)
            changed = None
            if case == 'extra_file':
                (target / 'unexpected.txt').write_text('reject\n')
            elif case == 'empty_directory':
                (target / 'unexpected').mkdir()
            elif case == 'changed_file':
                (target / 'author/README.md').write_bytes(b'tampered\n')
            elif case == 'missing_file':
                (target / 'audit/INDEPENDENT_AUDIT.md').unlink()
            elif case == 'duplicate_entry':
                m['files'].append(dict(m['files'][0]))
            elif case == 'unsafe_path':
                m['files'][0]['path'] = '../outside'
            elif case == 'symlink':
                (target / 'linked').symlink_to(target / 'README.md')
            elif case == 'symlink_directory':
                (target / 'linked_directory').symlink_to(target / 'author', target_is_directory=True)
            elif case in ('changed_author_binding', 'changed_audit_binding'):
                changed = 'author/MANIFEST.json' if case == 'changed_author_binding' else 'audit/AUDIT_BINDING.json'
                p = target / changed
                p.write_bytes(p.read_bytes() + b'\n')
            elif case in ('changed_turn_count', 'changed_proof_limit', 'changed_domain'):
                changed = 'BINDING.json'
                b = read_json(target / changed)
                if case == 'changed_turn_count':
                    b['approaches_used'] = 0
                elif case == 'changed_proof_limit':
                    b['candidate_membership_independently_proved'] = True
                else:
                    b['injectivity_domain'] = 'entire plane'
                (target / changed).write_text(json.dumps(b))
            elif case == 'changed_disposition':
                m['status'] = 'solved'
            if changed:
                p = target / changed
                for rec in m['files']:
                    if rec['path'] == changed:
                        rec.update(bytes=p.stat().st_size, sha256=sha(p))
            encoded = json.dumps(m, indent=2) + '\n'
            if case == 'duplicate_json_key':
                encoded = encoded.replace('{', '{"problem_id":2306047,', 1)
            path.write_text(encoded)
            try:
                verify(target)
            except (ValueError, KeyError, FileNotFoundError):
                rejected.append(case)
            else:
                raise ValueError('negative test accepted: ' + case)
    return rejected


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--replay', action='store_true')
    p.add_argument('--selftest', action='store_true')
    args = p.parse_args()
    result = {'problem_id': 2306047, 'status': 'PASS', 'files': verify(HERE)}
    if args.replay:
        result['replay'] = replay(HERE)
    if args.selftest:
        result['negative_tests_rejected'] = selftest(HERE)
    verify(HERE)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
