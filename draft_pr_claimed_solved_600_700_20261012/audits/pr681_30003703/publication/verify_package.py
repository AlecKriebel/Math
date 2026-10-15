#!/usr/bin/env python3
"""Offline PR681 integrity, temporary-copy replays and hostile integrity controls.

No arguments checks integrity only. --replay reproduces exact computations;
--selftest challenges integrity in disposable copies under ordinary and -O Python.
This manifest is not a digital signature, formal proof or novelty certificate.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile

HEAD = 'e92320ea5979c812089780a982fbd88136a26522'
PROBLEM = '30003703'
TITLE = "Counterexamples to Satoh's SL(2) representation-filtration conjecture"
NATIVE = 'native/unsolved_math_prioritization/attempts/30003703'
MANIFEST = 'PACKAGE_MANIFEST.json'
# Populated from stable, accepted research receipts; changing these invalidates
# the recorded package and requires fresh external comparison and review.
PINS = {}  # STABLE_RECEIPT_PINS
PUBLICATION_FILES = (
    'satoh_filtration_counterexamples.pdf', 'satoh_filtration_counterexamples.tex',
    'zenodo-deposit.json', 'README.md', 'CURRENT_PRIORITY_AND_STATUS.md',
    'CLAIM_SCOPE.json', 'requirements.txt', 'verify_package.py', 'build_package.py',
)
ROOT_FILES = (
    'SCOPE_AND_SNAPSHOT.json', 'MATH_SOURCE_GATE_ACCEPTANCE.json',
    'PRIORITY_GATE_ACCEPTANCE.json', 'ROOT_MATH_ASSESSMENT.md',
    'MATRIX_IDEAL_FAMILY_ACCEPTANCE.json', 'CLASSICAL_PRIORITY_FAMILY_ACCEPTANCE.json',
    'LITERATURE_PRIORITY_FAMILY_ACCEPTANCE.json', 'ROOT_NATIVE_REPLAY.json',
    'ROOT_FAMILY_REPLAY_SOURCE_PINS.json',
    'ROOT_MATRIX_REPLAY.normal.json', 'ROOT_MATRIX_REPLAY.optimized.json',
    'ROOT_FREEGROUP_REPLAY.normal.json', 'ROOT_FREEGROUP_REPLAY.optimized.json',
    'ROOT_CLASSICAL_PRIORITY_REPLAY.normal.json', 'ROOT_CLASSICAL_PRIORITY_REPLAY.optimized.json',
    'ROOT_LITERATURE_SCOPE_REPLAY.normal.json', 'ROOT_LITERATURE_SCOPE_REPLAY.optimized.json',
    'ROOT_PRIMARY_RETRIEVAL.json', 'ROOT_CLASSICAL_SOURCE_CHECK.json',
    'ROOT_PRIORITY_SOURCE_ACCESS_RECHECK.json', 'ROOT_PAPER_QA.json',
)
REVIEW_FILES = {
    'matrix_ideal_01': (
        'DERIVATION.md', 'FINDINGS.md', 'INPUT_PINS.json',
        'MATRIX_CONTROLS.normal.json', 'MATRIX_CONTROLS.optimized.json',
        'REPRODUCTION.json', 'RESEARCH_LOG.md', 'SOURCE_BINDINGS.json',
        'VERDICT.json', 'matrix_controls.py', 'FINAL_FREEZE.json',
    ),
    'freegroup_01': (
        'DERIVATION.md', 'FINDINGS.md', 'INPUT_PINS.json', 'RESEARCH_LOG.md',
        'SOURCES.json', 'VERDICT.json', 'controls.normal.json',
        'controls.optimized.json', 'controls.py', 'native_replay.normal.json',
        'native_replay.optimized.json', 'FINAL_FREEZE.json',
    ),
    'classical_priority_01': (
        '.gitignore', 'CONTROLS.normal.json', 'CONTROLS.optimized.json',
        'DERIVATION.md', 'FINDINGS.md', 'INPUT_PINS.json', 'REPRODUCTION.json',
        'RESEARCH_LOG.md', 'SEARCH_SCOPE.json', 'SOURCE_BINDINGS.json',
        'SOURCE_LEDGER.json', 'VERDICT.json', 'priority_controls.py', 'FINAL_FREEZE.json',
    ),
    'priority_literature_01': (
        'FINAL_QA.json', 'FINDINGS.md', 'INPUT_PINS.json', 'PRIOR_IMPLICATION_MAP.md',
        'RESEARCH_LOG.md', 'SCOPE_CONTROLS.normal.json', 'SCOPE_CONTROLS.optimized.json',
        'SEARCH_QUERIES.json', 'SOURCE_ACCESS_RECEIPTS.json', 'SOURCE_LEDGER.json',
        'VERDICT.json', 'scope_controls.py', 'FINAL_FREEZE.json',
    ),
}
EXPECTED_SCOPE = {
    'problem_id': PROBLEM, 'original_pr': 681, 'original_head': HEAD,
    'claim': 'explicit_counterexamples_to_2018_component_filtration_equality',
    'degree5_rank_min': 4, 'degree6_rank_min': 3,
    'component_algebra': 'rational_SL2_matrix_entry_functions',
    'A_uses_integral_free_group_LCS': True, 'D_acts_on_whole_J_quotient': True,
    'classical_identity_explicitly_credited': True,
    'degree5_rank3_claim': False, 'every_degree_failure_claim': False,
    'SLm_m_gt2_claim': False, 'character_algebra_claim': False,
    'ordinary_IA_LCS_conjecture_claim': False, 'new_PI_identity_claim': False,
    'new_general_PI_method_claim': False, 'historical_firstness_claim': False,
    'exhaustive_novelty_clearance': False, 'current_literature_openness_certified': False,
    'formal_proof_certificate': False, 'AI_reviews_are_human_peer_review': False,
    'AI_tools_used_extensively': True, 'unrefereed': True,
}
FAMILIES = (
    ('matrix_ideal_01', 'matrix_controls.py', 'MATRIX_CONTROLS', 'checks_count', 21),
    ('freegroup_01', 'controls.py', 'controls', 'check_family_count', 20),
    ('classical_priority_01', 'priority_controls.py', 'CONTROLS', 'count', 12),
    ('priority_literature_01', 'scope_controls.py', 'SCOPE_CONTROLS', 'check_count', 8),
)


def need(value, label):
    if not value:
        raise ValueError(label)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate JSON key: ' + key)
        result[key] = value
    return result


def finite_float(value):
    result = float(value)
    need(math.isfinite(result), 'nonfinite JSON number')
    return result


def json_data(data):
    return json.loads(data.decode('utf-8'), object_pairs_hook=unique_object,
                      parse_float=finite_float,
                      parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite JSON')))


def json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + '\n').encode()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git_blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


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
        need(stat.S_ISDIR((root / parent).lstat().st_mode), 'linked or non-directory parent')
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
    need(snapshot['original_head'] == HEAD and snapshot['problem_id'] == PROBLEM and
         snapshot['status'] == 'claimed_solved', 'snapshot identity/scope')
    need(snapshot['pr']['number'] == 681 and snapshot['pr']['headRefOid'] == HEAD,
         'snapshot original PR')
    records = snapshot['original_blobs']
    need(type(records) is dict and len(records) == 23, 'native file count')
    for name, record in records.items():
        safe_name(name)
        need(name.startswith(NATIVE[len('native/'):] + '/'), 'native path scope')
        need(record['git_mode'] == '100644', 'native Git mode')
    return records


def allowed_names(snapshot):
    names = set(PUBLICATION_FILES) | set(ROOT_FILES)
    names.update('reviews/' + family + '/' + name
                 for family, members in REVIEW_FILES.items() for name in members)
    names.update('native/' + name for name in native_bindings(snapshot))
    return names


def check_record(data, record, label, size_key='bytes'):
    need(type(record[size_key]) is int and record[size_key] >= 0 and
         len(data) == record[size_key] and digest(data) == record['sha256'], label)


def inspect_payload(payload):
    """Validate captured bytes completely before executing any packet code."""
    for name in payload:
        safe_name(name)
    need(set(PINS) == (set(ROOT_FILES) - {'ROOT_PAPER_QA.json'}) |
         {'reviews/' + family + '/FINAL_FREEZE.json' for family in REVIEW_FILES},
         'immutable pin inventory')
    for name, sha in PINS.items():
        need(digest(payload[name]) == sha, 'immutable receipt binding: ' + name)
    snapshot = json_data(payload['SCOPE_AND_SNAPSHOT.json'])
    need(set(payload) == allowed_names(snapshot), 'exact allowlisted payload inventory')
    for name, record in native_bindings(snapshot).items():
        data = payload['native/' + name]
        check_record(data, record, 'immutable native binding: ' + name, 'size')
        need(git_blob(data) == record['git_blob'], 'native Git blob: ' + name)
    for name, data in payload.items():
        if name.endswith('.json'):
            json_data(data)
    need(json.dumps(json_data(payload['CLAIM_SCOPE.json']), sort_keys=True) ==
         json.dumps(EXPECTED_SCOPE, sort_keys=True), 'exact counterexample claim scope')
    for family, names in REVIEW_FILES.items():
        prefix = 'reviews/' + family + '/'
        freeze = json_data(payload[prefix + 'FINAL_FREEZE.json'])
        rows = freeze['files']
        records = ({row['path']: row for row in rows} if type(rows) is list else rows)
        need(len(records) == len(rows) and set(records) == set(names) - {'FINAL_FREEZE.json'},
             'exact family freeze inventory: ' + family)
        for name, record in records.items():
            check_record(payload[prefix + name], record, 'frozen family bytes: ' + prefix + name)
        for _, source, stem, count_key, count in [f for f in FAMILIES if f[0] == family]:
            ordinary = payload[prefix + stem + '.normal.json']
            optimized = payload[prefix + stem + '.optimized.json']
            need(ordinary == optimized, 'frozen family mode equality: ' + family)
            result = json_data(ordinary)
            need(result.get('result', result.get('status')) == 'PASS' and
                 type(result[count_key]) is int and result[count_key] == count,
                 'frozen family scope: ' + family)
            if family == 'freegroup_01':
                need(result['coefficient_path_matrix_evaluations'] == 489 and
                     result['author_code_imported_or_executed'] is False, 'integral path scope')
    math_gate = json_data(payload['MATH_SOURCE_GATE_ACCEPTANCE.json'])
    need(math_gate['status'] == 'ACCEPTED_COMPLETE_COUNTEREXAMPLE_MATH_AND_LITERAL_SOURCE' and
         math_gate['native23_unchanged'] is True and math_gate['human_peer_review'] is False,
         'accepted mathematical gate')
    for family in ('matrix_ideal_01', 'freegroup_01'):
        pin = math_gate['family_verdicts'][family]
        need(digest(payload['reviews/' + family + '/VERDICT.json']) == pin['verdict_sha256'] and
             digest(payload['reviews/' + family + '/FINAL_FREEZE.json']) == pin['freeze_sha256'],
             'mathematical family acceptance: ' + family)
    priority = json_data(payload['PRIORITY_GATE_ACCEPTANCE.json'])
    need(priority['original_head'] == HEAD and priority['bounded_priority_only'] is True and
         priority['historical_firstness_certified'] is False, 'bounded priority gate')
    paper_qa = json_data(payload['ROOT_PAPER_QA.json'])
    need(paper_qa['all_pages_rendered_and_visually_inspected'] is True and
         type(paper_qa['pages']) is int and paper_qa['pages'] > 0, 'paper visual QA')
    for name, record in paper_qa['pins'].items():
        member = 'README.md' if name == 'PACKAGE_README.md' else name
        need(member in payload, 'paper QA unknown member')
        check_record(payload[member], record, 'paper QA bytes: ' + member)
    need({'satoh_filtration_counterexamples.pdf', 'satoh_filtration_counterexamples.tex',
          'CLAIM_SCOPE.json', 'CURRENT_PRIORITY_AND_STATUS.md', 'zenodo-deposit.json'} <=
         set(paper_qa['pins']), 'paper QA required author bindings')
    meta = json_data(payload['zenodo-deposit.json'])
    need(meta['metadata']['title'] == TITLE and
         meta['metadata']['upload_type'] == 'publication' and
         meta['metadata']['publication_type'] == 'preprint' and
         meta['metadata']['license'] == 'cc-by-4.0' and
         meta['metadata']['creators'] == [{'name': 'Kriebel, Alec',
             'affiliation': 'Independent researcher', 'orcid': '0009-0001-9320-500X'}],
         'preprint metadata identity')
    need(meta['files'] == [{'path': 'satoh_filtration_counterexamples.pdf'},
                           {'path': 'satoh_filtration_verification.zip'}], 'deposit file scope')
    need(payload['satoh_filtration_counterexamples.pdf'].startswith(b'%PDF-'), 'PDF header')
    need(payload['requirements.txt'] == b'sympy==1.14.0\n', 'exact dependency pin')
    return snapshot


def verify(root):
    files = inventory(root)
    raw = read_regular(root, MANIFEST)
    manifest = json_data(raw)
    need(set(manifest) == {'schema', 'problem_id', 'original_head', 'file_count',
                           'raw_third_party_fulltexts_included', 'files'}, 'manifest schema keys')
    need(type(manifest['schema']) is int and manifest['schema'] == 1 and
         manifest['problem_id'] == PROBLEM and manifest['original_head'] == HEAD and
         manifest['raw_third_party_fulltexts_included'] is False, 'manifest identity/scope')
    rows = manifest['files']
    need(type(rows) is list and type(manifest['file_count']) is int and
         len(rows) == manifest['file_count'], 'manifest count')
    payload = {}
    for row in rows:
        need(type(row) is dict and set(row) == {'path', 'bytes', 'sha256'}, 'file record schema')
        name = row['path']; safe_name(name)
        need(name != MANIFEST and name not in payload, 'duplicate/self manifest path')
        need(type(row['bytes']) is int and row['bytes'] >= 0 and type(row['sha256']) is str and
             re.fullmatch('[0-9a-f]{64}', row['sha256']), 'file record value')
        data = read_regular(root, name)
        check_record(data, row, 'file size/hash: ' + name)
        payload[name] = data
    need([row['path'] for row in rows] == sorted(payload), 'canonical manifest order')
    need(files == set(payload) | {MANIFEST}, 'exact package inventory')
    snapshot = inspect_payload(payload)
    for name in native_bindings(snapshot):
        need(stat.S_IMODE((root / 'native' / name).lstat().st_mode) == 0o644,
             'native filesystem mode: ' + name)
    need(inventory(root) == files, 'inventory changed during verification')
    for name, data in payload.items():
        need(read_regular(root, name) == data, 'payload changed during verification: ' + name)
    need(read_regular(root, MANIFEST) == raw, 'manifest changed during verification')
    return {'status': 'PASS', 'files': len(files), 'native_files': 23,
            'original_head': HEAD, 'problem_id': PROBLEM,
            'manifest_sha256': digest(raw),
            'pdf_sha256': digest(payload['satoh_filtration_counterexamples.pdf']),
            'raw_third_party_fulltexts_included': False,
            'formal_proof_certificate': False, 'historical_firstness_certified': False}


def child_bytes(script, arguments, cwd, optimized=False):
    # Keep the supplied venv executable spelling; resolve() loses the venv.
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONOPTIMIZE='0')
    env.pop('PYTHONPATH', None); env.pop('PYTHONHOME', None)
    flags = ['-O'] if optimized else []
    result = subprocess.run([sys.executable, '-I', '-B', *flags, str(script), *map(str, arguments)],
                            cwd=cwd, env=env, capture_output=True, timeout=600)
    need(result.returncode == 0, 'child replay failed: ' + result.stderr.decode(errors='replace'))
    return result.stdout


def replay(root):
    initial = verify(root)
    import sympy
    need(sympy.__version__ == '1.14.0', 'replay requires sympy==1.14.0')
    with tempfile.TemporaryDirectory(prefix='satoh-filtration-replay-') as tmp:
        scratch = Path(tmp); target = scratch / 'packet'
        shutil.copytree(root, target)
        verify(target)
        # Always invoke the frozen wrapper without -O, even when this verifier
        # runs under -O. Its own PYTHONOPTIMIZE=0 protects historical assertions.
        native_raw = child_bytes(target / NATIVE / 'verify_publication.py',
                                 ['--replay', '--selftest'], scratch, optimized=False)
        native = json_data(native_raw)
        retained = json_data(read_regular(target, 'ROOT_NATIVE_REPLAY.json'))
        need(len(retained['runs']) == 2 and all(native == run['result']
             for run in retained['runs']), 'native replay frozen receipt equality')
        need(native['result'] == 'PASS' and native['packet_files'] == 23 and
             native['author_negative_controls'] == 5 and native['independent_negative_controls'] == 12 and
             native['author_replay_byte_equal'] is True and native['independent_replay_byte_equal'] is True and
             native['assertions_enabled_in_frozen_subprocesses'] is True,
             'native exact replay scope')
        families = {}
        for family, source, stem, count_key, count in FAMILIES:
            prefix = 'reviews/' + family + '/'
            outputs = []
            for optimized in (False, True):
                label = 'optimized' if optimized else 'normal'
                output = child_bytes(target / prefix / source, [], scratch, optimized)
                need(output == read_regular(target, prefix + stem + '.' + label + '.json'),
                     'fresh/frozen byte equality: ' + family + '/' + label)
                report = json_data(output)
                need(report[count_key] == count and report.get('result', report.get('status')) == 'PASS',
                     'fresh family scope: ' + family)
                outputs.append(output)
            need(outputs[0] == outputs[1], 'fresh family ordinary/-O byte equality')
            families[family] = {'checks_per_mode': count, 'modes': ['normal', 'optimized'],
                                'normal_optimized_byte_equal': True,
                                'frozen_outputs_byte_equal': True,
                                'source_sha256': digest(read_regular(target, prefix + source))}
            if family == 'freegroup_01':
                families[family]['coefficient_path_matrix_evaluations_per_mode'] = 489
        need(verify(target) == initial, 'temporary packet changed during replay')
    need(verify(root) == initial, 'original package changed during replay')
    return {'status': 'PASS', 'temporary_copies_only': True,
            'native_wrapper_assertions_enabled': True, 'native': native,
            'families': families, 'sympy_version': sympy.__version__,
            'formal_proof_certificate': False, 'historical_firstness_certified': False}


def rewrite_manifest(root, name):
    manifest = json_data((root / MANIFEST).read_bytes())
    for row in manifest['files']:
        if row['path'] == name:
            data = (root / name).read_bytes()
            row.update(bytes=len(data), sha256=digest(data))
    (root / MANIFEST).write_bytes(json_bytes(manifest))


def selftest(root):
    initial = verify(root)
    # Integrity-only probes use a separately captured, verified verifier. No
    # script from a corrupted packet is imported or executed by these tests.
    source = read_regular(root, 'verify_package.py')
    cases = [
        'pdf_corruption', 'source_corruption', 'scope_expansion_rehashed',
        'native_corruption_rehashed', 'family_source_corruption_rehashed',
        'stale_root_receipt_rehashed', 'gate_corruption_rehashed',
        'metadata_title_rehashed', 'paper_qa_stale_binding_rehashed',
        'duplicate_payload_json_key_rehashed', 'nonfinite_constant_rehashed',
        'overflow_number_rehashed', 'unknown_file', 'empty_directory',
        'missing_payload', 'file_symlink', 'directory_symlink', 'nonregular_fifo',
        'native_mode_change', 'duplicate_manifest_record', 'manifest_self_entry',
        'manifest_duplicate_key', 'manifest_nonfinite', 'manifest_bool_size',
        'manifest_traversal', 'manifest_absolute', 'manifest_backslash',
        'manifest_colon', 'manifest_control_character', 'manifest_unsorted',
    ]
    with tempfile.TemporaryDirectory(prefix='satoh-filtration-hostile-') as tmp:
        scratch = Path(tmp); trusted = scratch / 'trusted_verify.py'
        trusted.write_bytes(source)
        harness = scratch / 'probe.py'
        harness.write_text("import sys\nfrom pathlib import Path\nn={'__file__':sys.argv[1],'__name__':'trusted_probe'}\nexec(compile(Path(sys.argv[1]).read_bytes(),sys.argv[1],'exec'),n)\nn['verify'](Path(sys.argv[2]))\n")
        rejected = {'normal': [], 'optimized': []}
        for case in cases:
            target = scratch / case; shutil.copytree(root, target)
            manifest = json_data((target / MANIFEST).read_bytes())
            changed = None
            if case == 'pdf_corruption':
                changed = 'satoh_filtration_counterexamples.pdf'
            elif case == 'source_corruption':
                changed = 'verify_package.py'
            elif case == 'scope_expansion_rehashed':
                changed = 'CLAIM_SCOPE.json'; obj = json_data((target / changed).read_bytes())
                obj['degree5_rank3_claim'] = True; (target / changed).write_bytes(json_bytes(obj))
            elif case == 'native_corruption_rehashed':
                changed = NATIVE + '/release/verify.py'
            elif case == 'family_source_corruption_rehashed':
                changed = 'reviews/freegroup_01/controls.py'
            elif case == 'stale_root_receipt_rehashed':
                changed = 'ROOT_NATIVE_REPLAY.json'
            elif case == 'gate_corruption_rehashed':
                changed = 'MATH_SOURCE_GATE_ACCEPTANCE.json'
            elif case == 'metadata_title_rehashed':
                changed = 'zenodo-deposit.json'; obj = json_data((target / changed).read_bytes())
                obj['metadata']['title'] = 'Unbounded result'; (target / changed).write_bytes(json_bytes(obj))
            elif case == 'paper_qa_stale_binding_rehashed':
                changed = 'ROOT_PAPER_QA.json'; obj = json_data((target / changed).read_bytes())
                obj['pins']['satoh_filtration_counterexamples.pdf']['sha256'] = '0' * 64
                (target / changed).write_bytes(json_bytes(obj))
            elif case in ('duplicate_payload_json_key_rehashed', 'nonfinite_constant_rehashed', 'overflow_number_rehashed'):
                changed = 'CLAIM_SCOPE.json'
                data = (target / changed).read_bytes().rstrip()
                extra = {'duplicate_payload_json_key_rehashed': b'"problem_id":"30003703"',
                         'nonfinite_constant_rehashed': b'"bad":NaN',
                         'overflow_number_rehashed': b'"bad":1e9999'}[case]
                (target / changed).write_bytes(data[:-1] + b',' + extra + b'}\n')
            elif case == 'unknown_file':
                (target / 'unlisted.txt').write_text('unknown')
            elif case == 'empty_directory':
                (target / 'empty').mkdir()
            elif case == 'missing_payload':
                (target / 'requirements.txt').unlink()
            elif case == 'file_symlink':
                p = target / 'requirements.txt'; p.unlink(); p.symlink_to(trusted)
            elif case == 'directory_symlink':
                shutil.rmtree(target / 'reviews/freegroup_01')
                (target / 'reviews/freegroup_01').symlink_to(root / 'reviews/freegroup_01', target_is_directory=True)
            elif case == 'nonregular_fifo':
                os.mkfifo(target / 'fifo')
            elif case == 'native_mode_change':
                (target / NATIVE / 'release/verify.py').chmod(0o755)
            elif case == 'duplicate_manifest_record':
                manifest['files'].append(dict(manifest['files'][0])); manifest['file_count'] += 1
            elif case == 'manifest_self_entry':
                manifest['files'][0]['path'] = MANIFEST
            elif case == 'manifest_duplicate_key':
                (target / MANIFEST).write_bytes((target / MANIFEST).read_bytes().rstrip()[:-1] + b',"schema":1}\n')
            elif case == 'manifest_nonfinite':
                manifest['schema'] = float('nan')
                (target / MANIFEST).write_text(json.dumps(manifest))
            elif case == 'manifest_bool_size':
                manifest['files'][0]['bytes'] = True
            elif case.startswith('manifest_') and case != 'manifest_unsorted':
                manifest['files'][0]['path'] = {
                    'manifest_traversal': '../outside', 'manifest_absolute': '/outside',
                    'manifest_backslash': 'bad\\name', 'manifest_colon': 'bad:name',
                    'manifest_control_character': 'bad\nname'}[case]
            elif case == 'manifest_unsorted':
                manifest['files'].reverse()
            if changed:
                if case in ('pdf_corruption', 'source_corruption', 'native_corruption_rehashed',
                            'family_source_corruption_rehashed', 'stale_root_receipt_rehashed',
                            'gate_corruption_rehashed'):
                    (target / changed).write_bytes((target / changed).read_bytes() + b'\n# hostile mutation\n')
                if case.endswith('_rehashed'):
                    rewrite_manifest(target, changed)
            elif case.startswith('manifest_') and case not in ('manifest_duplicate_key', 'manifest_nonfinite') or case == 'duplicate_manifest_record':
                (target / MANIFEST).write_bytes(json_bytes(manifest))
            for optimized in (False, True):
                label = 'optimized' if optimized else 'normal'
                env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONOPTIMIZE='0')
                env.pop('PYTHONPATH', None); env.pop('PYTHONHOME', None)
                flags = ['-O'] if optimized else []
                result = subprocess.run([sys.executable, '-I', '-B', *flags, str(harness),
                                         str(trusted), str(target)], cwd=scratch, env=env,
                                        capture_output=True, timeout=60)
                need(result.returncode != 0 and b'ValueError' in result.stderr or
                     result.returncode != 0 and case == 'missing_payload' and b'FileNotFoundError' in result.stderr,
                     'hostile control accepted or unexpected failure: ' + case + '/' + label)
                rejected[label].append(case)
    need(verify(root) == initial, 'original package changed during selftest')
    return {'status': 'PASS', 'temporary_copies_only': True,
            'case_count': len(cases), 'negative_controls_rejected_per_mode': len(cases),
            'total_rejections': 2 * len(cases), 'modes': ['normal', 'optimized'],
            'rejected': rejected, 'unverified_packet_code_executed': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replay', action='store_true')
    parser.add_argument('--selftest', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).absolute().parent
    result = verify(root)
    if args.replay:
        result['replay'] = replay(root)
    if args.selftest:
        result['selftest'] = selftest(root)
    verify(root)
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))


if __name__ == '__main__':
    main()
