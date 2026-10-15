#!/usr/bin/env python3
"""Offline integrity and temporary-copy replays; not a formal proof certificate.

Run from the extracted archive. The exact file allowlist excludes source scans,
operational records and later reviews. A checksum manifest detects corruption;
it is not a signature against replacement of this verifier and the whole archive.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile

HEAD = 'e31701151c331a6eed9224fb37a75a374ea1043e'
NATIVE = 'native/unsolved_math_prioritization/attempts/2306086'
MANIFEST = 'PACKAGE_MANIFEST.json'
PINS = {
    'SCOPE_AND_SNAPSHOT.json': '53736a33a43e4291cf51de8a7cbdd15f4cfedbc10ee3c585d7381723b2329e13',
    'MATH_SOURCE_GATE_ACCEPTANCE.json': 'd5c093168a3c9e62932c1ba852c8600b877a20c1fcf78547b7ee999a43d169a9',
    'PRIORITY_GATE_ACCEPTANCE.json': 'a8de66d0f9480d5142b3d4dbb69c3c7df56dab4883e4d722a417876805bc4330',
}
PUBLICATION_FILES = (
    'real_schlicht_preschwarzian.pdf', 'real_schlicht_preschwarzian.tex',
    'verify_package.py', 'build_package.py', 'README.md',
    'CURRENT_PRIORITY_AND_STATUS.md', 'CLAIM_SCOPE.json', 'requirements.txt',
    'requirements_numerical.txt', 'zenodo-deposit.json',
)
ROOT_FILES = (
    'SCOPE_AND_SNAPSHOT.json', 'MATH_SOURCE_GATE_ACCEPTANCE.json',
    'PRIORITY_GATE_ACCEPTANCE.json', 'PRE_PAPER_LIVE_GATE.json',
    'ROOT_SOURCE_AND_REPLAY_CHECKPOINT.json', 'ROOT_PUBLICATION_REPLAY.json',
    'ROOT_GEOMETRY_CONTROL_REPLAY.json', 'ROOT_COVARIANCE_CONTROL_REPLAY.json',
    'ROOT_NUMERICAL_REPRODUCTION.json', 'ROOT_RODEMICH_ADDENDUM_REPLAY.json',
    'ROOT_PRIORITY_SOURCE_ACCESS_CHECKPOINT.json',
    'ROOT_PAPER_QA.json',
)
REVIEW_FILES = {
    'geometry_01': (
        'RESEARCH_LOG.md', 'VERDICT.json', 'exact_adversarial_controls.py',
        'EXACT_CONTROLS.json', 'FINDINGS.md', 'BINDING_CHECK.json', 'DERIVATION.md',
    ),
    'covariance_source_01': (
        'TEST_RESULTS.json', 'REVIEW_MANIFEST.json', 'independent_controls.normal.json',
        'FINDINGS.md', 'independent_numerical.normal.json',
        'independent_numerical.optimized.json', 'independent_numerical.py',
        'requirements_numerical.txt', 'SOURCE_BINDINGS.json', 'REPRODUCE.md',
        'publication.numerical.normal.json', 'RESEARCH_LOG.md',
        'publication.normal.json', 'VERDICT.json', 'numerical_detail.normal.json',
        'publication.optimized.json', 'numerical_detail.optimized.json',
        'publication.numerical.optimized.json', 'independent_controls.optimized.json',
        'independent_controls.py',
    ),
    'classical_priority_01': (
        'SOURCE_BINDINGS.before_rodemich_addendum.json', 'RESEARCH_LOG.md',
        'VERDICT.json', 'rodemich_addendum_controls.py', 'FINAL_FREEZE.json',
        'ADDENDUM_PRIOR_REVIEW_BINDING.json', 'FINDINGS.md', 'SOURCE_RETRIEVALS.json',
        'SOURCE_BINDINGS.json', 'VERDICT.before_rodemich_addendum.json',
        'SEARCH_LEDGER.json', 'RODEMICH_ADDENDUM.md', 'DERIVATION.md',
        'RODEMICH_ADDENDUM_CONTROLS.json', 'BINDING_CHECK.json',
    ),
    'priority_literature_01': (
        'SEARCH_LEDGER.json', 'FINDINGS.md', 'SOURCE_RETRIEVALS.json',
        'RESEARCH_LOG.md', 'VERDICT.json', 'SOURCE_LEDGER.json',
        'REPORT_BINDING.json', 'TEPPER_PRINTED_BOUND_COUNTEREXAMPLE.json',
    ),
    'historical_source_access_01': (
        'SOURCE_BINDINGS.json', 'RESEARCH_LOG.md', 'VERDICT.json',
        'SOURCE_ACCESS_REPORT.md',
    ),
}
EXPECTED_SCOPE = {
    'problem_id': '2306086', 'original_pr': 662, 'original_head': HEAD,
    'claim': 'qualitative_fixed_nonreal_point_improvement_uniform_in_f',
    'real_diameter_radius_sharp': True, 'source_expression_at_zero': 0,
    'compact_nonreal_sets_uniform_gap': True, 'explicit_upper_gap_formula': False,
    'sharp_quantitative_radius': False, 'general_nonreal_extremizers': False,
    'full_variability_region': False, 'numerical_interval_certification': False,
    'formal_proof_certificate': False, 'historical_firstness_claim': False,
    'exhaustive_novelty_clearance': False, 'current_literature_openness_certified': False,
    'methods': 'classical_coefficient_rigidity_real_symmetry_compactness',
    'AI_tools_used_extensively': True, 'unrefereed': True,
    'AI_reviews_are_human_peer_review': False,
}


def need(value, label):
    if not value:
        raise ValueError(label)


def unique_object(pairs):
    value = {}
    for key, item in pairs:
        need(key not in value, 'duplicate JSON key: ' + key)
        value[key] = item
    return value


def json_data(data):
    return json.loads(data.decode('utf-8'), object_pairs_hook=unique_object,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError('nonfinite JSON')))


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_name(name):
    need(type(name) is str, 'path must be a string')
    path = PurePosixPath(name)
    need(bool(name) and not path.is_absolute() and path.as_posix() == name and
         '..' not in path.parts and '\\' not in name and ':' not in name and
         name != '.' and all(ord(c) >= 32 and ord(c) != 127 for c in name), 'unsafe path')
    return path


def read_regular(root, name):
    relative = safe_name(name)
    need(root.is_dir() and not root.is_symlink(), 'invalid input root')
    for parent in reversed(relative.parents):
        p = root / parent
        need(stat.S_ISDIR(p.lstat().st_mode), 'linked or non-directory input parent')
    path = root / name
    need(stat.S_ISREG(path.lstat().st_mode), 'linked or nonregular input file')
    return path.read_bytes()


def inventory(root):
    need(root.is_dir() and not root.is_symlink(), 'invalid package root')
    files, dirs = set(), set()
    for base, directory_names, file_names in os.walk(root, followlinks=False):
        for name in directory_names + file_names:
            path = Path(base) / name
            relative = path.relative_to(root).as_posix()
            safe_name(relative)
            mode = path.lstat().st_mode
            need(stat.S_ISREG(mode) or stat.S_ISDIR(mode), 'symlink or nonregular object')
            (dirs if stat.S_ISDIR(mode) else files).add(relative)
    parents = {p.as_posix() for name in files for p in PurePosixPath(name).parents
               if p.as_posix() != '.'}
    need(dirs == parents, 'unexpected or empty directory')
    return files


def native_bindings(snapshot):
    need(snapshot['original_head'] == HEAD and snapshot['problem_id'] == '2306086'
         and snapshot['status'] == 'claimed_solved', 'snapshot target or scope')
    records = snapshot['original_blobs']
    need(type(records) is dict and len(records) == 24, 'native count')
    for name in records:
        safe_name(name)
        need(name.startswith(NATIVE[len('native/'): ] + '/'), 'native path scope')
    return records


def allowed_names(snapshot):
    names = set(PUBLICATION_FILES) | set(ROOT_FILES)
    names.update('reviews/' + family + '/' + name
                 for family, members in REVIEW_FILES.items() for name in members)
    names.update('native/' + name for name in native_bindings(snapshot))
    return names


def inspect_payload(payload):
    """Check a captured byte map before executing anything or writing an archive."""
    for name in payload:
        safe_name(name)
    for name, expected in PINS.items():
        need(digest(payload[name]) == expected, 'immutable receipt binding: ' + name)
    snapshot = json_data(payload['SCOPE_AND_SNAPSHOT.json'])
    need(set(payload) == allowed_names(snapshot), 'exact allowlisted payload inventory')
    for name, record in native_bindings(snapshot).items():
        data = payload['native/' + name]
        need(type(record['size']) is int and len(data) == record['size'] and
             digest(data) == record['sha256'], 'immutable native binding: ' + name)
    scope = json_data(payload['CLAIM_SCOPE.json'])
    # Canonical JSON comparison distinguishes booleans from integers.
    need(json.dumps(scope, sort_keys=True) == json.dumps(EXPECTED_SCOPE, sort_keys=True),
         'exact qualitative claim scope')
    for name, data in payload.items():
        if name.endswith('.json'):
            json_data(data)
    for gate_name, field in (('MATH_SOURCE_GATE_ACCEPTANCE.json', 'review_inputs'),
                             ('PRIORITY_GATE_ACCEPTANCE.json', 'review_pins')):
        gate = json_data(payload[gate_name])
        for name, record in gate[field].items():
            need(name in payload and len(payload[name]) == record['bytes'] and
                 digest(payload[name]) == record['sha256'], 'gate review binding: ' + name)
    paper_qa = json_data(payload['ROOT_PAPER_QA.json'])
    need(paper_qa['pages'] == 5 and paper_qa['all_pages_rendered_and_visually_inspected'] is True,
         'paper QA scope')
    for name, record in paper_qa['pins'].items():
        member = 'README.md' if name == 'PACKAGE_README.md' else name
        need(member in payload and len(payload[member]) == record['bytes'] and
             digest(payload[member]) == record['sha256'], 'paper QA binding: ' + member)
    meta = json_data(payload['zenodo-deposit.json'])
    need(meta['metadata']['upload_type'] == 'publication' and
         meta['metadata']['publication_type'] == 'preprint' and
         meta['metadata']['license'] == 'cc-by-4.0', 'preprint metadata')
    need(meta['files'] == [{'path': 'real_schlicht_preschwarzian.pdf'},
                           {'path': 'real_schlicht_verification.zip'}], 'deposit file scope')
    need(payload['real_schlicht_preschwarzian.pdf'].startswith(b'%PDF-'), 'PDF header')
    return snapshot


def verify(root):
    files = inventory(root)
    manifest = json_data(read_regular(root, MANIFEST))
    need(set(manifest) == {'schema', 'problem_id', 'original_head', 'file_count',
                           'raw_third_party_fulltexts_included', 'files'}, 'manifest schema keys')
    need(type(manifest['schema']) is int and manifest['schema'] == 1 and
         manifest['problem_id'] == '2306086' and manifest['original_head'] == HEAD and
         manifest['raw_third_party_fulltexts_included'] is False, 'manifest identity and scope')
    records = manifest['files']
    need(type(records) is list and type(manifest['file_count']) is int and
         len(records) == manifest['file_count'], 'manifest count')
    payload = {}
    for record in records:
        need(type(record) is dict and set(record) == {'path', 'bytes', 'sha256'}, 'file record schema')
        name = record['path']; safe_name(name)
        need(name != MANIFEST and name not in payload, 'duplicate or self-referential manifest path')
        need(type(record['bytes']) is int and record['bytes'] >= 0 and
             type(record['sha256']) is str and re.fullmatch('[0-9a-f]{64}', record['sha256']),
             'file record value')
        data = read_regular(root, name)
        need(len(data) == record['bytes'] and digest(data) == record['sha256'], 'file size/hash: ' + name)
        payload[name] = data
    need(files == set(payload) | {MANIFEST}, 'exact package inventory')
    inspect_payload(payload)
    return {'status': 'PASS', 'files': len(files), 'manifest_sha256': digest(read_regular(root, MANIFEST)),
            'pdf_sha256': digest(payload['real_schlicht_preschwarzian.pdf']),
            'qualitative_scope_only': True, 'native_files': 24,
            'raw_third_party_fulltexts_included': False}


def child(script, arguments, cwd, optimized=False):
    # Preserve sys.executable as supplied: resolving a venv symlink loses the venv.
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    env.pop('PYTHONOPTIMIZE', None)
    flags = ['-O'] if optimized else []
    result = subprocess.run([sys.executable, '-I', '-B', *flags, str(script), *map(str, arguments)],
                            cwd=cwd, env=env, capture_output=True, timeout=300)
    need(result.returncode == 0, 'child replay failed: ' + result.stderr.decode(errors='replace'))
    return json_data(result.stdout)


def replay(root, numerical=False):
    initial = verify(root)
    with tempfile.TemporaryDirectory(prefix='real-schlicht-package-replay-') as tmp:
        scratch = Path(tmp)
        target = scratch / 'packet'
        shutil.copytree(root, target)
        verify(target)
        native_args = ['--replay', '--selftest'] + (['--numerical'] if numerical else [])
        native = child(target / NATIVE / 'verify_publication.py', native_args, scratch)
        r = native['replay']
        need(native['status'] == 'PASS' and native['files'] == 24 and
             r['author_exact_controls_per_mode'] == 3558 and
             r['independent_symbolic_math_checks'] == 32 and
             r['binding_replay_preservation_checks'] == 48 and
             r['numeric_reproduction_checks'] == (16 if numerical else 0) and
             r['ordinary_and_optimized_outputs_equal'] is True and
             r['numeric_interval_certification'] is False and
             r['formal_proof_certificate'] is False and
             len(native['publication_negative_controls_rejected']) == 24 and
             len(set(native['publication_negative_controls_rejected'])) == 24,
             'native replay scope/counts')
        covariance = {}
        for optimized in (False, True):
            label = 'optimized' if optimized else 'normal'
            report = child(target / 'reviews/covariance_source_01/independent_controls.py',
                           [], scratch, optimized)
            need(report['status'] == 'PASS' and report['checks'] == 87,
                 'independent covariance replay')
            covariance[label] = report
        need(covariance['normal'] == covariance['optimized'], 'independent normal/optimized equality')
        # This script writes beside itself. Copy it outside the verified packet.
        geometry_dir = scratch / 'geometry'; geometry_dir.mkdir()
        geometry_script = geometry_dir / 'exact_adversarial_controls.py'
        shutil.copyfile(target / 'reviews/geometry_01/exact_adversarial_controls.py', geometry_script)
        geometry = child(geometry_script, [], geometry_dir)
        need(geometry['check_count'] == 7 and geometry['all_pass'] is True and
             len(geometry['checks']) == 7 and all(v is True for v in geometry['checks'].values()),
             'geometric shortcut controls')
        rodemich_reports = {}
        for optimized in (False, True):
            label = 'optimized' if optimized else 'normal'
            rodemich = child(target / 'reviews/classical_priority_01/rodemich_addendum_controls.py',
                             [], scratch, optimized)
            need(rodemich['exact_check_count'] == 9 and len(rodemich['exact_checks']) == 9 and
                 all(v is True for v in rodemich['exact_checks'].values()) and
                 rodemich['countermodel_is_globally_univalent'] is False and
                 rodemich['countermodel_refutes_PR662'] is False, 'Rodemich countermodel scope')
            rodemich_reports[label] = {k: v for k, v in rodemich.items() if k != 'utc'}
        need(rodemich_reports['normal'] == rodemich_reports['optimized'],
             'Rodemich ordinary/optimized equality')
        alternative = None
        if numerical:
            alternative = child(target / 'reviews/covariance_source_01/independent_numerical.py',
                                [], scratch)
            need(alternative['status'] == 'PASS' and alternative['certified'] is False and
                 len(alternative['records']) == 4, 'independent numerical replay scope')
            for record in alternative['records']:
                need(record['certified'] is False and record['absolute_difference'] < 2e-9 and
                     record['solver_success'] == [True, True], 'uncertified numerical reproduction')
        verify(target)
    need(verify(root) == initial, 'original package changed during replay')
    return {'status': 'PASS', 'temporary_copies_only': True, 'native': native,
            'independent_covariance_checks_per_mode': 87,
            'independent_covariance_normal_optimized_equal': True,
            'geometry_exact_checks': 7, 'rodemich_exact_margins': 9,
            'rodemich_normal_optimized_equal': True,
            'rodemich_countermodel_in_target_class': False,
            'alternative_numerical': alternative,
            'numerical_interval_certification': False, 'formal_proof_certificate': False,
            'optimizer_executed': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replay', action='store_true')
    parser.add_argument('--numerical', action='store_true')
    args = parser.parse_args()
    need(not args.numerical or args.replay, '--numerical requires --replay')
    root = Path(__file__).absolute().parent
    result = verify(root)
    if args.replay:
        result['replay'] = replay(root, args.numerical)
    verify(root)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
