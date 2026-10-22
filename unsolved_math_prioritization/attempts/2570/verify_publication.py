#!/usr/bin/env python3
"""Portable strict binding and finite replay; not a full solution certificate."""
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
AUTHOR = '0ec82991eabebee6e9366a9795ea75beb2806962b458f9b288ad3688c444db5b'
AUDIT = 'b8f6b69c558d939af7e0f89b4c0fd8e5683ff26da1902af583787ee562efbdb1'

def need(value, message):
    if not value:
        raise ValueError(message)

def unique(pairs):
    out = {}
    for k, v in pairs:
        need(k not in out, 'duplicate JSON key')
        out[k] = v
    return out

def read(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inventory(root):
    need(root.is_dir() and not root.is_symlink(), 'invalid root')
    files, dirs = set(), set()
    for p in root.rglob('*'):
        need(not p.is_symlink(), 'symlink forbidden')
        need(p.is_file() or p.is_dir(), 'nonregular object')
        (files if p.is_file() else dirs).add(p.relative_to(root).as_posix())
    needed_dirs = {str(p) for f in files for p in PurePosixPath(f).parents if str(p) != '.'}
    need(dirs == needed_dirs, 'extra empty directory')
    return files

def entries(root, records):
    need(type(records) is list, 'records must be list')
    names = set()
    for rec in records:
        name = rec['path']
        need(type(name) is str, 'path type')
        p = PurePosixPath(name)
        need(name and name != '.' and not p.is_absolute() and '..' not in p.parts
             and '\\' not in name and p.as_posix() == name, 'unsafe path')
        need(name not in names, 'duplicate path')
        names.add(name)
        path = root / name
        need(path.is_file() and not path.is_symlink(), 'missing or linked file')
        for parent in p.parents:
            need(not (root / parent).is_symlink(), 'linked parent')
        raw = path.read_bytes()
        need(type(rec['bytes']) is int and rec['bytes'] >= 0 and len(raw) == rec['bytes'], 'size mismatch')
        need(hashlib.sha256(raw).hexdigest() == rec['sha256'], 'hash mismatch')
    return names

def verify(root):
    m = read(root / 'PUBLICATION_MANIFEST.json')
    need((m['schema'], m['problem_id'], m['rank'], m['status'], m['turns']) ==
         ('kourovka-2570-publication-v1', 2570, 691, 'unsolved', '5/5'), 'publication identity')
    names = entries(root, m['files'])
    need(names | {'PUBLICATION_MANIFEST.json'} == inventory(root), 'publication inventory')
    need(sha(root / 'author/AUTHOR_MANIFEST.json') == AUTHOR, 'author freeze')
    need(sha(root / 'audit/AUDIT_BINDING.json') == AUDIT, 'audit freeze')
    author = read(root / 'author/AUTHOR_MANIFEST.json')
    need(author['problem_id'] == 2570 and author['turns_used'] == 5 and
         author['outcome'] == 'unresolved_scoped_partials', 'author outcome')
    need(entries(root / 'author', author['files']) | {'AUTHOR_MANIFEST.json'} ==
         inventory(root / 'author'), 'author inventory')
    audit = read(root / 'audit/AUDIT_BINDING.json')
    need(audit['author_manifest_sha256'] == AUTHOR and
         audit['verdict'] == 'scoped_pass_no_full_solution' and
         audit['author_helpers_executed'] is False, 'audited history')
    need(entries(root / 'audit', audit['files']) | {'AUDIT_BINDING.json'} ==
         inventory(root / 'audit'), 'audit inventory')
    b = read(root / 'BINDING.json')
    need((b['problem_id'], b['rank'], b['status'], b['turns'], b['approaches_used']) ==
         (2570, 691, 'unsolved', '5/5', 5), 'binding disposition')
    need(b['author_manifest_sha256'] == AUTHOR and b['audit_binding_sha256'] == AUDIT,
         'binding hashes')
    for name in ('full_target_resolved', 'general_effective_coherence_proved', 'undecidability_proved',
                 'novelty_claim', 'formal_proof_certificate', 'current_dataset_row_immutably_pinned',
                 'separate_prior_ai_report_inspected', 'duplicate_row_changed'):
        need(b[name] is False, 'scope inflation: ' + name)
    need(b['gray_linton_general_algorithm_requires_supplied_presentation'] is True,
         'source input boundary')
    need(b['frozen_files_preserved'] is True and b['mandatory_mathematical_corrections'] == [],
         'frozen audit disposition')
    for p in root.rglob('*.json'):
        read(p)
    return len(names) + 1

def child(args, cwd):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    env.pop('PYTHONOPTIMIZE', None)
    return subprocess.run([sys.executable, '-I', '-B', *map(str, args)], cwd=cwd,
                          env=env, capture_output=True, timeout=120)

def replay(root):
    with tempfile.TemporaryDirectory(prefix='kourovka2570-replay-') as t:
        dest = Path(t) / 'packet'
        shutil.copytree(root, dest)
        verify(dest)
        reports = {}
        for name, args in [('author_math', [dest / 'author/verify_math.py']),
                           ('author_binding', [dest / 'author/verify_manifest.py']),
                           ('independent', [dest / 'audit/independent_controls.py', dest / 'author'])]:
            result = child(args, t)
            need(result.returncode == 0, name + ': ' + result.stderr.decode())
            reports[name] = json.loads(result.stdout, object_pairs_hook=unique)
        need(reports['author_math'] == read(root / 'author/CHECK_RESULTS.json'), 'author replay values')
        need(reports['independent'] == read(root / 'audit/INDEPENDENT_CONTROL_RESULTS.json'),
             'independent replay values')
        need(reports['author_binding'] == {'passed': True, 'bound_files': 8,
             'math_output_matches': True, 'rejected_integrity_mutations':
             ['changed_proof', 'missing_proof', 'extra_payload', 'changed_manifest_identity']},
             'author binding replay')
        verify(dest)
        need(all((dest / f).read_bytes() == (root / f).read_bytes() for f in inventory(root)),
             'replay changed frozen bytes')
    verify(root)
    return {'author_counts': reports['author_math']['counts'],
            'author_integrity_mutations_rejected': 4,
            'independent_periodic_coordinates': reports['independent']['periodic_outer_coordinate_cases'],
            'independent_quotient_cases': reports['independent']['finite_quotient_cases'],
            'independent_plateau_cases': reports['independent']['plateau_cases'],
            'independent_fibonacci_cases': len(reports['independent']['fibonacci_controls']),
            'recorded_outputs_exact': True, 'all_input_bytes_unchanged': True,
            'temporary_copy_only': True, 'child_assertions_enabled': True}

def selftest(root):
    cases = ('extra_file', 'extra_pycache', 'empty_directory', 'changed_file', 'missing_file',
             'duplicate_entry', 'unsafe_path', 'symlink', 'symlink_directory', 'duplicate_json_key',
             'changed_author_freeze', 'changed_audit_freeze', 'changed_turn_count',
             'changed_novelty', 'changed_scope', 'changed_source_boundary',
             'changed_prior_report_limit', 'changed_disposition')
    rejected = []
    for case in cases:
        with tempfile.TemporaryDirectory(prefix='kourovka2570-negative-') as t:
            dest = Path(t) / 'packet'
            shutil.copytree(root, dest)
            p = dest / 'PUBLICATION_MANIFEST.json'
            m = read(p)
            changed = None
            if case == 'extra_file':
                (dest / 'extra.txt').write_text('reject')
            elif case == 'extra_pycache':
                (dest / 'audit/__pycache__').mkdir(); (dest / 'audit/__pycache__/extra').write_text('reject')
            elif case == 'empty_directory':
                (dest / 'extra').mkdir()
            elif case == 'changed_file':
                (dest / 'author/PROOFS.md').write_text('tampered')
            elif case == 'missing_file':
                (dest / 'audit/PARTIALS_AUDIT.md').unlink()
            elif case == 'duplicate_entry':
                m['files'].append(dict(m['files'][0]))
            elif case == 'unsafe_path':
                m['files'][0]['path'] = '../outside'
            elif case == 'symlink':
                (dest / 'linked').symlink_to(dest / 'README.md')
            elif case == 'symlink_directory':
                (dest / 'linked_directory').symlink_to(dest / 'author', target_is_directory=True)
            elif case in ('changed_author_freeze', 'changed_audit_freeze'):
                changed = 'author/AUTHOR_MANIFEST.json' if case == 'changed_author_freeze' else 'audit/AUDIT_BINDING.json'
                q = dest / changed; q.write_bytes(q.read_bytes() + b'\n')
            elif case in ('changed_turn_count', 'changed_novelty', 'changed_scope',
                          'changed_source_boundary', 'changed_prior_report_limit'):
                changed = 'BINDING.json'; b = read(dest / changed)
                k, v = {'changed_turn_count': ('approaches_used', 1),
                        'changed_novelty': ('novelty_claim', True),
                        'changed_scope': ('full_target_resolved', True),
                        'changed_source_boundary': ('gray_linton_general_algorithm_requires_supplied_presentation', False),
                        'changed_prior_report_limit': ('separate_prior_ai_report_inspected', True)}[case]
                b[k] = v; (dest / changed).write_text(json.dumps(b))
            elif case == 'changed_disposition':
                m['status'] = 'verified_solved'
            if changed:
                for rec in m['files']:
                    if rec['path'] == changed:
                        rec.update(bytes=(dest / changed).stat().st_size, sha256=sha(dest / changed))
            data = json.dumps(m)
            if case == 'duplicate_json_key':
                data = data.replace('{', '{"problem_id":2570,', 1)
            p.write_text(data)
            try:
                verify(dest)
            except (ValueError, KeyError, FileNotFoundError):
                rejected.append(case)
            else:
                raise ValueError('negative accepted: ' + case)
    return rejected

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replay', action='store_true')
    parser.add_argument('--selftest', action='store_true')
    args = parser.parse_args()
    result = {'problem_id': 2570, 'status': 'PASS', 'files': verify(HERE)}
    if args.replay:
        result['replay'] = replay(HERE)
    if args.selftest:
        result['negative_tests_rejected'] = selftest(HERE)
    verify(HERE)
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
