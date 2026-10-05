#!/usr/bin/env python3
"""Strict portable integrity and replay for a classical full-scope resolution, not a formal proof."""
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
AUTHOR = 'bf8748c37a3e7ba2ac905a6159e246ec087a7ec7b643ebe8b5e1b418f32638c5'
AUDIT = '0d9b984ef0ced5c827a7955ecf51a7f552ecd5df745320711e633d9b21beadc9'


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
         (2307045, 690, 'already_solved', '1/5'), 'target and disposition')
    names = entries(root, m['files'])
    need(inventory(root) == names | {'PUBLICATION_MANIFEST.json'}, 'exact inventory')
    need(sha(root / 'author/MANIFEST.json') == AUTHOR, 'author freeze')
    need(sha(root / 'audit/AUDIT_MANIFEST.json') == AUDIT, 'audit freeze')
    author = read_json(root / 'author/MANIFEST.json')
    need(entries(root / 'author', author['files']) | {'MANIFEST.json'} == inventory(root / 'author'),
         'author inventory')
    audit = read_json(root / 'audit/AUDIT_MANIFEST.json')
    need(entries(root / 'audit', audit['files']) | {'AUDIT_MANIFEST.json'} == inventory(root / 'audit'),
         'audit inventory')
    need(audit['frozen_packet_manifest_sha256'] == AUTHOR, 'audited identity')
    frozen = read_json(root / 'audit/FROZEN_BINDING.json')
    need(entries(root / 'author', frozen['audited_packet_files']) == inventory(root / 'author'), 'audited author inventory')
    need(frozen['audited_packet_file_count'] == 9 and frozen['audited_packet_total_bytes'] == 29052, 'author totals')
    outcome = read_json(root / 'audit/AUDIT_OUTCOME.json')
    need(outcome['verdict'] == 'PASS_SOURCE_MATCHED_PUBLISHED_PRIOR_RESOLUTION' and
         outcome['recommended_status'] == 'already_solved' and outcome['recorded_authored_turns'] == '1/5' and
         outcome['blocking_defects'] == 0 and outcome['required_corrections'] == [], 'audit gate')
    need(outcome['novelty_claim'] is False and outcome['audit_is_additional_claimed_proof_attempt'] is False,
         'audit limits')
    author_outcome = read_json(root / 'author/READINESS_AND_OUTCOME.json')
    need(author_outcome['substantive_turns_used_this_investigation'] == 1 and
         author_outcome['novelty_claim'] is False, 'frozen author count and scope')
    binding = read_json(root / 'BINDING.json')
    need(binding['author_manifest_sha256'] == AUTHOR and binding['audit_manifest_sha256'] == AUDIT,
         'binding identities')
    need((binding['problem_id'], binding['rank'], binding['status'], binding['turns'], binding['approaches_used'])
         == (2307045, 690, 'already_solved', '1/5', 1), 'binding disposition')
    need(binding['full_target_prior_resolution'] is True and binding['novelty_claim'] is False
         and binding['proof_assistant_formalization'] is False and
         binding['complete_symbol_by_symbol_primary_proof_audit'] is False and
         binding['successful_dubinin_pdf_byte_retrieval'] is False and
         binding['endpoint_uniqueness_claim'] is False, 'publication scope and limits')
    need(binding['classical_credit'] == 'V. N. Dubinin, Theorem A, Russian original 1984 / English translation 1985', 'classical credit')
    need(binding['minimum_outer_harmonic_measure'] == '(4/pi) arctan((1-ell)^(p/2))' and
         binding['minimizers'] == 'equal angular spacing, unique up to rotation and relabeling' and
         binding['parameter_scope'] == 'p >= 1 integer, 0 < ell < 1, p distinct boundary-attached straight radial cuts of common length ell' and
         binding['arbitrary_configuration_comparison_dependency'] == 'Dubinin Theorem A', 'exact full-scope result')
    need(binding['audit_archive_sha256'] == '984bbf2169f92fb7374fb2e88a9ee65b2acd414de29e9508726c00fc05281cd3' and
         binding['audit_archive_bytes'] == 19185, 'archival metadata')
    expected_top = {'README.md','RESEARCH_LOG.md','BINDING.json','verify_publication.py','PUBLICATION_MANIFEST.json'}
    actual_top = {p.name for p in root.iterdir()}
    need(actual_top == expected_top | {'author','audit'}, 'top-level exact inventory')
    for p in root.rglob('*.json'):
        read_json(p)
    return len(names) + 1


def child(args, cwd):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    env.pop('PYTHONOPTIMIZE', None)
    return subprocess.run([sys.executable, '-I', '-B', *map(str, args)], cwd=cwd,
                          env=env, capture_output=True)


def replay(root):
    with tempfile.TemporaryDirectory(prefix='radial-slit-replay-') as tmp:
        target = Path(tmp) / 'packet'
        shutil.copytree(root, target)
        verify(target)
        cases = [
            ('author/exact_controls.py', ['--check'], 'PASS: exact controls and bounded numerical sanity replay'),
            ('author/verify_manifest.py', [], 'PASS: all 8 authored packet files match the manifest'),
            ('audit/independent_controls.py', ['--check'], 'PASS: 15217 independent exact controls; recorded results match'),
            ('audit/verify_frozen_binding.py', ['--packet', target/'author'], 'PASS: 9 frozen packet files match independent binding')]
        for script, args, expected in cases:
            result = child([target/script, *args], tmp)
            need(result.returncode == 0, 'replay script: ' + result.stderr.decode())
            need(result.stdout.decode().strip() == expected, 'replay result')
        # Recompute recorded independent results in a disposable copy and require byte identity.
        result = child([target/'audit/independent_controls.py'], tmp)
        need(result.returncode == 0, 'independent full result replay')
        need((target/'audit/INDEPENDENT_RESULTS.json').read_bytes() ==
             (root/'audit/INDEPENDENT_RESULTS.json').read_bytes(), 'independent byte-exact replay')
        verify(target)
    rejected = []
    for case in ('changed_proof_byte', 'changed_manifest', 'missing_file', 'unexpected_pycache_file', 'unexpected_symlink'):
        with tempfile.TemporaryDirectory(prefix='radial-binding-negative-') as tmp:
            target = Path(tmp) / 'author'
            shutil.copytree(root / 'author', target)
            if case in ('changed_proof_byte','changed_manifest'):
                p = target / ('PROOF.md' if case == 'changed_proof_byte' else 'MANIFEST.json')
                p.write_bytes(p.read_bytes() + b'\n')
            elif case == 'missing_file':
                (target / 'README.md').unlink()
            elif case == 'unexpected_pycache_file':
                (target / '__pycache__').mkdir(); (target / '__pycache__/unexpected.txt').write_text('reject\n')
            else:
                (target / 'unexpected-link').symlink_to(target / 'README.md')
            result = child([root / 'audit/verify_frozen_binding.py', '--packet', target], tmp)
            need(result.returncode != 0, 'audit binding negative accepted: ' + case)
            rejected.append(case)
    verify(root)
    return {'author_exact_control_instances': 3186, 'author_floating_configurations': 25,
            'independent_exact_assertions': 15217, 'independent_certified_intervals': 6,
            'audit_binding_mutations_rejected': rejected, 'independent_results_byte_exact': True,
            'author_float_diagnostics_platform_tolerance': 1e-13,
            'temporary_copy_only': True, 'children_unoptimized': True, 'formal_proof_certificate': False}


def selftest(root):
    cases = ('extra_file', 'extra_pycache_file', 'empty_directory', 'changed_file', 'missing_file',
             'duplicate_entry', 'unsafe_path', 'symlink', 'symlink_directory', 'duplicate_json_key',
             'changed_author_manifest', 'changed_audit_manifest', 'changed_approach_count',
             'changed_novelty', 'changed_credit', 'changed_audit_scope', 'changed_endpoint_uniqueness', 'changed_formula',
             'changed_pdf_retrieval', 'changed_disposition')
    rejected = []
    for case in cases:
        with tempfile.TemporaryDirectory(prefix='radial-slit-publication-negative-') as tmp:
            target = Path(tmp) / 'packet'
            shutil.copytree(root, target)
            path = target / 'PUBLICATION_MANIFEST.json'
            m = read_json(path); changed = None
            if case == 'extra_file':
                (target / 'unexpected.txt').write_text('reject\n')
            elif case == 'extra_pycache_file':
                (target / 'audit/__pycache__').mkdir(); (target / 'audit/__pycache__/extra').write_text('reject\n')
            elif case == 'empty_directory':
                (target / 'unexpected').mkdir()
            elif case == 'changed_file':
                (target / 'author/PROOF.md').write_text('tampered\n')
            elif case == 'missing_file':
                (target / 'audit/AUDIT.md').unlink()
            elif case == 'duplicate_entry':
                m['files'].append(dict(m['files'][0]))
            elif case == 'unsafe_path':
                m['files'][0]['path'] = '../outside'
            elif case == 'symlink':
                (target / 'linked').symlink_to(target / 'README.md')
            elif case == 'symlink_directory':
                (target / 'linked_directory').symlink_to(target / 'author', target_is_directory=True)
            elif case in ('changed_author_manifest', 'changed_audit_manifest'):
                changed = 'author/MANIFEST.json' if case == 'changed_author_manifest' else 'audit/AUDIT_MANIFEST.json'
                p = target / changed; p.write_bytes(p.read_bytes() + b'\n')
            elif case in ('changed_approach_count', 'changed_novelty', 'changed_credit', 'changed_audit_scope',
                          'changed_endpoint_uniqueness', 'changed_formula', 'changed_pdf_retrieval'):
                changed = 'BINDING.json'; b = read_json(target / changed)
                key, val = {'changed_approach_count': ('approaches_used', 5),
                            'changed_novelty': ('novelty_claim', True),
                            'changed_credit': ('classical_credit', 'New result'),
                            'changed_audit_scope': ('complete_symbol_by_symbol_primary_proof_audit', True),
                            'changed_endpoint_uniqueness': ('endpoint_uniqueness_claim', True),
                            'changed_formula': ('minimum_outer_harmonic_measure', '2/pi atan((1-ell)^p)'),
                            'changed_pdf_retrieval': ('successful_dubinin_pdf_byte_retrieval', True)}[case]
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
                encoded = encoded.replace('{', '{"problem_id":2307045,', 1)
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
    result = {'problem_id': 2307045, 'status': 'PASS', 'files': verify(HERE)}
    if args.replay:
        result['replay'] = replay(HERE)
    if args.selftest:
        result['negative_tests_rejected'] = selftest(HERE)
    verify(HERE)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
