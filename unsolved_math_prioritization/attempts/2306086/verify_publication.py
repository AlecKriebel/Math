#!/usr/bin/env python3
"""Strict portable freeze/replay checks, not a formal proof or ODE certificate."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent
AUTHOR = '20a2db82ec67e614e4e564c0fd289cc4fe737bd1b8470004ff6306f58e07def2'
AUDIT = 'bc50aa56fffe8abdf775e2190a87ef4405e1ca7e3c49844e3772d52f8245095c'
ARCHIVES = (
    ('author', 'FUNCTION_THEORY_2306086_AUTHORED_FREEZE.zip', 19163,
     '6897b0a5f2efc08daddd87ff4ce44c35d61fc29ba44b1dc5a8179df2dc7f35a5'),
    ('audit', 'FUNCTION_THEORY_2306086_INDEPENDENT_SAFE_AUDIT.zip', 13192,
     'b0e8d9c5ed802c09835f4620f153d85be3f1bf8d6a44cda20935cbbb50817fbf'),
)
TRUE_FLAGS = ('fixed_nonreal_uniform_in_f_strict_gap', 'real_nonzero_classical_radius_sharp',
              'zero_display_degenerate', 'compact_nonreal_uniform_gap',
              'original_author_files_preserved', 'original_audit_files_preserved')
FALSE_FLAGS = ('explicit_positive_gap_determined', 'sharp_quantitative_formula_determined',
               'full_variability_region_determined', 'all_quantitative_questions_solved',
               'novelty_established', 'current_literature_status_verified',
               'formal_proof_certificate', 'numerical_interval_certification')


def need(value, label):
    if not value:
        raise ValueError(label)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_object)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_name(name):
    need(type(name) is str, 'path type')
    path = PurePosixPath(name)
    need(name and not path.is_absolute() and '..' not in path.parts and
         path.as_posix() == name and '\\' not in name and name != '.', 'unsafe path')
    return path


def inventory(root):
    need(root.is_dir() and not root.is_symlink(), 'invalid root')
    files, dirs = set(), set()
    for path in root.rglob('*'):
        need(not path.is_symlink(), 'symlink forbidden')
        need(path.is_file() or path.is_dir(), 'nonregular object')
        (files if path.is_file() else dirs).add(path.relative_to(root).as_posix())
    parents = {str(p) for name in files for p in PurePosixPath(name).parents if str(p) != '.'}
    need(dirs == parents, 'unexpected empty directory')
    return files


def entries(root, records):
    need(type(records) is list, 'manifest entries type')
    names = set()
    for record in records:
        name = record['path']; relative = safe_name(name)
        need(name not in names, 'duplicate manifest path'); names.add(name)
        path = root / name
        need(path.is_file() and not path.is_symlink(), 'missing or linked file')
        need(all(not (root / p).is_symlink() for p in relative.parents), 'linked parent')
        need(type(record['bytes']) is int and record['bytes'] >= 0 and
             path.stat().st_size == record['bytes'], 'byte count')
        need(sha(path) == record['sha256'], 'file hash')
    return names


def verify(root):
    manifest = read_json(root / 'PUBLICATION_MANIFEST.json')
    need((manifest['problem_id'], manifest['rank'], manifest['status'], manifest['turns']) ==
         (2306086, 687, 'claimed_solved', '5/5'), 'target and disposition')
    names = entries(root, manifest['files'])
    need(inventory(root) == names | {'PUBLICATION_MANIFEST.json'}, 'exact inventory')
    need(len(names) + 1 == 24, 'package file count')
    for folder, filename, size, digest in ARCHIVES:
        path = root / 'archives' / filename
        need(path.stat().st_size == size and sha(path) == digest, 'immutable ZIP')
        with zipfile.ZipFile(path) as archive:
            members = archive.namelist()
            need(len(members) == len(set(members)), 'duplicate ZIP member')
            need(set(members) == inventory(root / folder), 'ZIP inventory')
            for name in members:
                safe_name(name)
                need(archive.read(name) == (root / folder / name).read_bytes(), 'ZIP file binding')
    need(sha(root / 'author/FROZEN_MANIFEST.json') == AUTHOR, 'author manifest freeze')
    need(sha(root / 'audit/AUDIT_MANIFEST.json') == AUDIT, 'audit manifest freeze')
    for folder, filename in [('author', 'FROZEN_MANIFEST.json'), ('audit', 'AUDIT_MANIFEST.json')]:
        records = read_json(root / folder / filename)['files']
        need(entries(root / folder, records) | {filename} == inventory(root / folder), 'inner manifest inventory')
    audit = read_json(root / 'audit/AUDIT_BINDING.json')
    need((audit['target_id'], audit['rank'], audit['blocking_mathematical_defects']) ==
         ('2306086', 687, 0), 'audit target and verdict')
    need(audit['audit_status'] == 'PASS: qualitative fixed-point improvement established; explicit/sharp quantitative result not determined; novelty and current literature status unverified', 'audit scope')
    need(entries(root / 'author', audit['author_freeze']['files']) == inventory(root / 'author'), 'audited author binding')
    need(audit['author_freeze']['sha256'] == ARCHIVES[0][3], 'audited ZIP identity')
    need(audit['authored_exact_controls_each_mode'] == 3558 and
         audit['independent_audit_checks'] == 96 and
         audit['independent_exact_or_symbolic_math_checks'] == 32 and
         audit['independent_numeric_reproduction_checks'] == 16 and
         audit['independent_binding_replay_preservation_checks'] == 48,
         'exact and numerical audit separation')
    need(audit['numerical_interval_certification'] is False, 'audit numerical limit')
    binding = read_json(root / 'BINDING.json')
    need((binding['problem_id'], binding['rank'], binding['status'], binding['turns'], binding['approaches_used']) ==
         (2306086, 687, 'claimed_solved', '5/5', 5), 'binding disposition')
    need(binding['claim_scope'] == 'qualitative fixed-point improvement only', 'qualitative scope')
    need(binding['author_manifest_sha256'] == AUTHOR and binding['audit_manifest_sha256'] == AUDIT, 'binding identities')
    for key in TRUE_FLAGS:
        need(binding[key] is True, 'required scoped result: ' + key)
    for key in FALSE_FLAGS:
        need(binding[key] is False, 'unestablished claim: ' + key)
    need(entries(root, binding['archives']) == {'archives/' + a[1] for a in ARCHIVES}, 'archive records')
    for path in root.rglob('*.json'):
        read_json(path)
    return len(names) + 1


def child(arguments, cwd, optimized=False):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    env.pop('PYTHONOPTIMIZE', None)
    flags = ['-O'] if optimized else []
    return subprocess.run([sys.executable, '-I', '-B', *flags, *map(str, arguments)],
                          cwd=cwd, env=env, capture_output=True)


def replay(root, numerical):
    outputs = {}
    with tempfile.TemporaryDirectory(prefix='preschwarzian-replay-') as tmp:
        target = Path(tmp) / 'packet'; shutil.copytree(root, target)
        verify(target)
        expected = read_json(target / 'author/EXACT_CONTROL_RESULTS.json')
        saved_audit = read_json(target / 'audit/AUDIT_CHECKS.json')
        for optimized in (False, True):
            label = 'optimized' if optimized else 'normal'
            result = child([target / 'author/exact_controls.py'], tmp, optimized)
            need(result.returncode == 0, result.stderr.decode())
            need(json.loads(result.stdout) == expected and expected['checks'] == 3558, 'authored exact replay')
            arguments = [target / 'audit/audit_controls.py', '--freeze-directory', target / 'author',
                         '--freeze-zip', target / 'archives' / ARCHIVES[0][1]]
            if numerical:
                arguments.append('--numerical')
            result = child(arguments, tmp, optimized)
            need(result.returncode == 0, result.stderr.decode())
            report = json.loads(result.stdout)
            need(report['status'] == 'PASS' and report['audit_checks'] == (96 if numerical else 80), 'audit replay count')
            need(report['authored_replays'] == saved_audit['authored_replays'], 'nested exact controls')
            families = dict(saved_audit['by_family'])
            if not numerical:
                for key in ('independent_ode_solver_success', 'saved_tail_is_real_koebe', 'independent_ode_reproduction'):
                    families.pop(key)
            need(report['by_family'] == families, 'audit check families')
            if numerical:
                need(report['numerical']['certified'] is False, 'numeric qualification')
                for record in report['numerical']['records']:
                    need(record['absolute_difference'] < 2e-9 and record['certified'] is False, 'numeric reproduction only')
            else:
                need(report['numerical'] is None, 'numerical mode separation')
            outputs[label] = report
        need(outputs['normal'] == outputs['optimized'], 'ordinary and optimized equality')
        verify(target)
    verify(root)
    return {'author_exact_controls_per_mode': 3558, 'independent_symbolic_math_checks': 32,
            'binding_replay_preservation_checks': 48, 'numeric_reproduction_checks': 16 if numerical else 0,
            'ordinary_and_optimized_outputs_equal': True, 'temporary_copies_only': True,
            'numeric_interval_certification': False, 'formal_proof_certificate': False}


def selftest(root):
    cases = ['extra_file', 'extra_pycache', 'empty_directory', 'changed_file', 'missing_file',
             'duplicate_entry', 'unsafe_path', 'symlink', 'symlink_directory', 'duplicate_json_key',
             'changed_author_manifest', 'changed_audit_manifest', 'changed_archive',
             'changed_approach_count', 'changed_disposition', 'changed_claim_scope',
             *['inflated_' + key for key in FALSE_FLAGS]]
    rejected = []
    for case in cases:
        with tempfile.TemporaryDirectory(prefix='preschwarzian-negative-') as tmp:
            target = Path(tmp) / 'packet'; shutil.copytree(root, target)
            path = target / 'PUBLICATION_MANIFEST.json'; manifest = read_json(path); changed = None
            if case == 'extra_file':
                (target / 'unexpected.txt').write_text('reject\n')
            elif case == 'extra_pycache':
                (target / 'audit/__pycache__').mkdir(); (target / 'audit/__pycache__/extra').write_text('reject\n')
            elif case == 'empty_directory':
                (target / 'unexpected').mkdir()
            elif case == 'changed_file':
                (target / 'author/PROOF_PARTIALS.md').write_text('tampered\n')
            elif case == 'missing_file':
                (target / 'audit/INDEPENDENT_AUDIT.md').unlink()
            elif case == 'duplicate_entry':
                manifest['files'].append(dict(manifest['files'][0]))
            elif case == 'unsafe_path':
                manifest['files'][0]['path'] = '../outside'
            elif case == 'symlink':
                (target / 'linked').symlink_to(target / 'README.md')
            elif case == 'symlink_directory':
                (target / 'linked_directory').symlink_to(target / 'author', target_is_directory=True)
            elif case in ('changed_author_manifest', 'changed_audit_manifest', 'changed_archive'):
                changed = {'changed_author_manifest':'author/FROZEN_MANIFEST.json',
                           'changed_audit_manifest':'audit/AUDIT_MANIFEST.json',
                           'changed_archive':'archives/' + ARCHIVES[0][1]}[case]
                p = target / changed; p.write_bytes(p.read_bytes() + b'\n')
            elif case == 'changed_disposition':
                manifest['status'] = 'verified_solved'
            elif case == 'changed_approach_count' or case == 'changed_claim_scope' or case.startswith('inflated_'):
                changed = 'BINDING.json'; binding = read_json(target / changed)
                if case == 'changed_approach_count': binding['approaches_used'] = 1
                elif case == 'changed_claim_scope': binding['claim_scope'] = 'all quantitative questions'
                else: binding[case[len('inflated_'):]] = True
                (target / changed).write_text(json.dumps(binding))
            if changed:
                p = target / changed
                for record in manifest['files']:
                    if record['path'] == changed:
                        record.update(bytes=p.stat().st_size, sha256=sha(p))
            encoded = json.dumps(manifest, indent=2) + '\n'
            if case == 'duplicate_json_key':
                encoded = encoded.replace('{', '{"problem_id":2306086,', 1)
            path.write_text(encoded)
            try:
                verify(target)
            except (ValueError, KeyError, FileNotFoundError):
                rejected.append(case)
            else:
                raise ValueError('negative control accepted: ' + case)
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replay', action='store_true')
    parser.add_argument('--numerical', action='store_true')
    parser.add_argument('--selftest', action='store_true')
    args = parser.parse_args()
    need(not args.numerical or args.replay, '--numerical requires --replay')
    result = {'problem_id': 2306086, 'status': 'PASS', 'files': verify(HERE)}
    if args.replay: result['replay'] = replay(HERE, args.numerical)
    if args.selftest: result['publication_negative_controls_rejected'] = selftest(HERE)
    verify(HERE)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
