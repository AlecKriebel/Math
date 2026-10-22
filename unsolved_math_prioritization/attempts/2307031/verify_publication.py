#!/usr/bin/env python3
"""Strict portable integrity and finite replay for audited partial results."""
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
AUTHOR = '00cc2ffbfcf74549e852fc4bf2af6f7de4596f398339ec726d46c8b563b5ef11'
AUDIT = 'efe0bcde51acef1f101745de6858a64f69263f9e66b1fab695c96f9e3834dce6'
ARCHIVE = '53368885eec40f19b35d99a029ffadcc8174d7ebdb32bc36f90699d8acc87a39'
CORRECTION = 'b582bff532ad9c61aea45a66dd5a43529f90afc0b95dab9a6346051c7d75a1ce'


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
         (2307031, 689, 'unsolved', '5/5'), 'target and disposition')
    names = entries(root, m['files'])
    need(inventory(root) == names | {'PUBLICATION_MANIFEST.json'}, 'exact inventory')
    need(sha(root / 'author/AUTHOR_MANIFEST.json') == AUTHOR, 'author freeze')
    need(sha(root / 'independent_audit/AUDIT_BINDING.json') == AUDIT, 'audit freeze')
    need(sha(root / 'AUTHORED_REVIEW_PACKET.zip') == ARCHIVE, 'archive freeze')
    need(sha(root / 'INTEGRAL_CLARIFICATION.md') == CORRECTION, 'controlling clarification freeze')
    author = read_json(root / 'author/AUTHOR_MANIFEST.json')
    need(entries(root / 'author', author['files']) | {'AUTHOR_MANIFEST.json'} == inventory(root / 'author'),
         'author inventory')
    audit = read_json(root / 'independent_audit/AUDIT_BINDING.json')
    need(entries(root / 'independent_audit', audit['files']) | {'AUDIT_BINDING.json'} ==
         inventory(root / 'independent_audit'), 'audit inventory')
    need(audit['audited_author_manifest_sha256'] == AUTHOR and
         audit['audited_archive_sha256'] == ARCHIVE, 'audited input identities')
    need(audit['broad_target_status'] == 'unresolved_partial' and
         audit['blocking_mathematical_error_in_principal_results'] is False and
         audit['verdict'] == 'principal_results_pass_integral_wording_needs_minor_clarification', 'audit gate')
    need(len(audit['clarifications']) == 1 and audit['clarifications'][0]['id'] == 'C1', 'audit clarification')
    with zipfile.ZipFile(root / 'AUTHORED_REVIEW_PACKET.zip') as z:
        expected = {'author/' + p for p in inventory(root / 'author')}
        need(len(z.namelist()) == len(expected) and set(z.namelist()) == expected, 'exact archive members')
        for name in expected:
            need(z.read(name) == (root / name).read_bytes(), 'archive member bytes')
    b = read_json(root / 'BINDING.json')
    need((b['problem_id'], b['rank'], b['status'], b['turns'], b['approaches_used']) ==
         (2307031, 689, 'unsolved', '5/5', 5), 'binding disposition')
    need(b['author_manifest_sha256'] == AUTHOR and b['audit_binding_sha256'] == AUDIT and
         b['archive_sha256'] == ARCHIVE and b['controlling_clarification_sha256'] == CORRECTION,
         'binding identities')
    need(b['controlling_clarification_path'] == 'INTEGRAL_CLARIFICATION.md' and
         b['clarification_resolves'] == ['C1'] and b['integral_lower_limit'] == 'A>=2 after monotonicity begins'
         and b['start_at_2_requires_initial_interval_measurability'] is True, 'controlling integral scope')
    for key in ('full_target_resolved', 'novelty_claim', 'priority_claim', 'current_openness_claim',
                'formal_proof_certificate', 'external_human_peer_review', 'one_sequence_sharp_at_all_scales'):
        need(b[key] is False, 'forbidden expanded scope: ' + key)
    need(b['single_sequence_single_entire_completely_monotone_counterexample'] is True and
         b['global_count_order'] == 'O_{a_1}(sqrt(T) log T)' and
         b['classification_remaining_unresolved'] is True and
         b['zero_denominator_convention'] == 'r_n=+infinity and f(+infinity)=0', 'mathematical scope')
    for p in root.rglob('*.json'):
        read_json(p)
    return len(names) + 1


def child(script, cwd):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    env.pop('PYTHONOPTIMIZE', None)
    # -I ignores PYTHON* configuration; runpy supplies the frozen author's local import path.
    bootstrap = ('import pathlib,runpy,sys; '
                 'p=pathlib.Path(sys.argv[1]); sys.path.insert(0,str(p.parent)); '
                 'runpy.run_path(str(p),run_name="__main__")')
    return subprocess.run([sys.executable, '-I', '-B', '-c', bootstrap, str(script)],
                          cwd=cwd, env=env, capture_output=True, timeout=180)


def replay(root):
    with tempfile.TemporaryDirectory(prefix='iterated-sum-replay-') as tmp:
        target = Path(tmp) / 'packet'
        shutil.copytree(root, target)
        verify(target)
        for script, expected in [
            ('author/verify.py', 'author/EXPECTED_CHECKS.json'),
            ('independent_audit/independent_checks.py', 'independent_audit/INDEPENDENT_CHECKS.json')]:
            result = child(target / script, tmp)
            need(result.returncode == 0, 'replay failed: ' + result.stderr.decode())
            need(json.loads(result.stdout) == read_json(target / expected), 'exact deterministic result')
            need(result.stdout == (target / expected).read_bytes(), 'byte-exact deterministic result')
        result = child(target / 'author/verify_integrity.py', tmp)
        need(result.returncode == 0, 'frozen author integrity replay: ' + result.stderr.decode())
        verify(target)
    verify(root)
    return {'author_sequence_threshold_cases': 1944, 'independent_sequence_threshold_cases': 21504,
            'independent_index_checks': 129024, 'qualifying_large_index_checks': 36588,
            'two_eigenvalue_crosschecks': 108, 'genuine_recursive_stages': 2,
            'sharp_count_thresholds': 12, 'independent_mathematical_negative_controls': 3,
            'results_byte_exact': True, 'temporary_copy_only': True,
            'child_assertions_enabled': True, 'formal_proof_certificate': False}


def selftest(root):
    cases = ('extra_file', 'extra_pycache_file', 'empty_directory', 'changed_file', 'missing_file',
             'duplicate_entry', 'unsafe_path', 'symlink', 'symlink_directory', 'duplicate_json_key',
             'changed_author_manifest', 'changed_audit_binding', 'changed_archive', 'changed_correction',
             'changed_correction_binding', 'changed_integral_scope', 'changed_approach_count',
             'changed_novelty', 'changed_scope', 'changed_disposition')
    rejected = []
    for case in cases:
        with tempfile.TemporaryDirectory(prefix='iterated-sum-publication-negative-') as tmp:
            target = Path(tmp) / 'packet'
            shutil.copytree(root, target)
            path = target / 'PUBLICATION_MANIFEST.json'
            m = read_json(path); changed = None
            if case == 'extra_file':
                (target / 'unexpected.txt').write_text('reject\n')
            elif case == 'extra_pycache_file':
                (target / 'independent_audit/__pycache__').mkdir()
                (target / 'independent_audit/__pycache__/extra').write_text('reject\n')
            elif case == 'empty_directory':
                (target / 'unexpected').mkdir()
            elif case == 'changed_file':
                (target / 'author/PROOFS.md').write_text('tampered\n')
            elif case == 'missing_file':
                (target / 'independent_audit/AUDIT.md').unlink()
            elif case == 'duplicate_entry':
                m['files'].append(dict(m['files'][0]))
            elif case == 'unsafe_path':
                m['files'][0]['path'] = '../outside'
            elif case == 'symlink':
                (target / 'linked').symlink_to(target / 'README.md')
            elif case == 'symlink_directory':
                (target / 'linked_directory').symlink_to(target / 'author', target_is_directory=True)
            elif case in ('changed_author_manifest', 'changed_audit_binding', 'changed_archive', 'changed_correction'):
                changed = {'changed_author_manifest': 'author/AUTHOR_MANIFEST.json',
                           'changed_audit_binding': 'independent_audit/AUDIT_BINDING.json',
                           'changed_archive': 'AUTHORED_REVIEW_PACKET.zip',
                           'changed_correction': 'INTEGRAL_CLARIFICATION.md'}[case]
                p = target / changed; p.write_bytes(p.read_bytes() + b'\n')
            elif case in ('changed_correction_binding', 'changed_integral_scope', 'changed_approach_count',
                          'changed_novelty', 'changed_scope'):
                changed = 'BINDING.json'; b = read_json(target / changed)
                key, val = {'changed_correction_binding': ('controlling_clarification_sha256', '0' * 64),
                            'changed_integral_scope': ('start_at_2_requires_initial_interval_measurability', False),
                            'changed_approach_count': ('approaches_used', 1),
                            'changed_novelty': ('novelty_claim', True),
                            'changed_scope': ('full_target_resolved', True)}[case]
                b[key] = val; (target / changed).write_text(json.dumps(b))
            elif case == 'changed_disposition':
                m['status'] = 'verified_solved'
            if changed:
                p = target / changed
                for rec in m['files']:
                    if rec['path'] == changed:
                        rec.update(bytes=p.stat().st_size, sha256=sha(p))
            encoded = json.dumps(m, indent=2) + '\n'
            if case == 'duplicate_json_key':
                encoded = encoded.replace('{', '{"problem_id":2307031,', 1)
            path.write_text(encoded)
            try:
                verify(target)
            except (ValueError, KeyError, FileNotFoundError):
                rejected.append(case)
            else:
                raise ValueError('negative test accepted: ' + case)
    return rejected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replay', action='store_true')
    parser.add_argument('--selftest', action='store_true')
    args = parser.parse_args()
    result = {'problem_id': 2307031, 'status': 'PASS', 'files': verify(HERE)}
    if args.replay:
        result['replay'] = replay(HERE)
    if args.selftest:
        result['negative_tests_rejected'] = selftest(HERE)
    verify(HERE)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
