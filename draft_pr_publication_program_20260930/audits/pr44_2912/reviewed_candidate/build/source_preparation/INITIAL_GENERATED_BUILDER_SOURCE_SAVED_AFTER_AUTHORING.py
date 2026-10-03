#!/usr/bin/env python3
"""SOURCE ONLY. ROOT may freeze an absent PR44 packet after genuine source reading.

This program performs administrative copying and read-only Git queries. It never
imports, compiles or executes any candidate or family mathematical helper. It
never changes native inputs, canonical attempts, Git/index, a remote or people.
Actual attempts, failures and complete streams remain in the audit-local tmp.
"""
import argparse
import ctypes
import datetime as dt
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import traceback

HEAD = 'c772dc5b851ec91da9d46d534577609e5d3ca389'
BASE = '01358d66fc67d1c462bddf31c0d4ee5b120e6737'
SCIENCE = '69a3ffb7b6c2ba3bf1a4df8d7d83960d66095db9d175d78cfe49e2324aac1a71'
GATE = 'PENDING_NEW_WHOLE_CURRENT_SOURCE_FIRST_ADVERSARY'
FLAGS = ['original18_science_helpers_results_metadata_and_complete19_path_diff_fully_read', 'operative_primary_target_categories_and_relevant_proofs_fully_read', 'both_realization_gaps_and_no_novelty_disposition_accepted', 'whole_raw_SQL_and_prior_presence_actual_evidence_fully_read', 'unchanged_author507_and_independent29933_actual_reproductions_fully_read', 'both_closed_independent_families_fully_read', 'first_party_closures_and_individual_foreign_exclusions_mechanically_checked', 'standard_conditional_deductions_only_scoped_partial_accepted', 'new_source_adversary_closed_clean_complete_report_personally_read']
HEADER = ['Rank', 'ID / code', 'Problem', 'EV', 'Impact (/10)', 'Difficulty',
          'Proposed', 'Status', 'Turns', 'Chat', 'Findings', 'DOI']
NATIVE = {'unsolved_math_prioritization/' + name for name in [
    'QUEUE.md', 'state.json', 'history.jsonl', 'catalog.json', 'assessments.json',
    'queue.py', 'policy.json', 'manifest.json', 'cache/problems.json',
    'cache/research_results.json', 'cache/catalog.sqlite',
    'review_v2/related_target_groups.json']}
NATIVE.add('draft_pr_publication_program_20260930/inventory.json')
IMMUTABLE = ['OBSTRUCTION.md', 'SOURCES.md', 'group_block_verification.json', 'source_manifest.json', 'source_record.json', 'turns.jsonl', 'verify_group_block.py', 'review/submitted_verifier.py', 'review/submitted_results.json', 'review/reviewed_obstruction.md', 'review/independent_checks.py', 'review/independent_results.json']

def require(value, message):
    if not value:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encode(value):
    return (json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode()


def equal(a, b):
    # Serialized scalar tokens distinguish integers, booleans and nulls.
    return json.dumps(a, sort_keys=True, ensure_ascii=False, allow_nan=False,
                      separators=(',', ':')) == json.dumps(
        b, sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(',', ':'))


def hex64(value):
    return type(value) is str and re.fullmatch('[0-9a-f]{64}', value) is not None


def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def clock(value):
    require(type(value) is str, 'Explicit aware UTC timestamp required')
    parsed = dt.datetime.fromisoformat(value[:-1] + '+00:00' if value.endswith('Z') else value)
    require(parsed.tzinfo is not None and parsed.utcoffset() == dt.timedelta(0), 'UTC required')
    return parsed


def load(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'Duplicate JSON key: ' + key)
            result[key] = value
        return result
    def constant(value):
        raise ValueError('Invalid JSON constant: ' + value)
    def floating(value):
        result = float(value)
        require(math.isfinite(result), 'Nonfinite JSON number')
        return result
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant, parse_float=floating)


def structured(name, raw):
    if name.endswith('.json'):
        load(raw)
    elif name.endswith('.jsonl'):
        for line in raw.splitlines():
            require(line.strip(), 'Blank JSONL row rejected')
            load(line)


def relative(value):
    require(type(value) is str and value and '\\' not in value, 'POSIX relative path required')
    path = PurePosixPath(value)
    require(not path.is_absolute() and path.as_posix() == value and
            not {'.', '..', '.git', '__pycache__'}.intersection(path.parts), 'Unsafe path: ' + value)
    return value


def regular(path):
    require(not path.is_symlink() and all(not p.is_symlink() for p in path.parents),
            'Symlink path rejected: ' + str(path))
    require(stat.S_ISREG(path.stat().st_mode), 'Regular file required: ' + str(path))
    return path.read_bytes()


def inventory(root):
    require(root.is_dir() and not root.is_symlink() and
            all(not p.is_symlink() for p in root.parents), 'Regular directory required')
    files, directories = set(), set()
    for path in root.rglob('*'):
        require(not path.is_symlink(), 'Symlink member rejected')
        name = relative(path.relative_to(root).as_posix())
        mode = path.stat().st_mode
        if stat.S_ISREG(mode):
            files.add(name)
        else:
            require(stat.S_ISDIR(mode), 'Special member rejected')
            directories.add(name)
    expected = {p.as_posix() for name in files for p in PurePosixPath(name).parents
                if p.as_posix() != '.'}
    require(directories == expected, 'Extra/empty directory rejected')
    return files


def rows(items):
    require(type(items) is list, 'Rows must be a list')
    names = set()
    for item in items:
        require(type(item) is dict and set(item) == {'path', 'bytes', 'sha256'},
                'Exact path/bytes/SHA row required')
        name = relative(item['path'])
        require(name not in names, 'Duplicate row path')
        names.add(name)
        require(type(item['bytes']) is int and item['bytes'] >= 0 and hex64(item['sha256']),
                'Typed bytes/SHA required')
    return names


def publish_absent(source, destination):
    require(sys.platform == 'darwin', 'Reviewed macOS exclusive publication required')
    libc = ctypes.CDLL(None, use_errno=True)
    rename = libc.renamex_np
    rename.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]
    rename.restype = ctypes.c_int
    # RENAME_EXCL is 0x00000004 on macOS; never use replacement rename.
    if rename(os.fsencode(source), os.fsencode(destination), 4) != 0:
        number = ctypes.get_errno()
        raise OSError(number, os.strerror(number), str(destination))


def build(args, script, audit, repo, attempt):
    destination = audit / 'reviewed_candidate'
    require(not destination.exists() and not destination.is_symlink(), 'Never overwrite a candidate')
    dependencies, outputs, commands = {}, {}, []
    def bind(name, role, expected=None):
        name = relative(name)
        raw = regular(audit / name)
        structured(name, raw)
        row = {'path': name, 'bytes': len(raw), 'sha256': sha(raw), 'roles': [role]}
        require(expected is None or row['sha256'] == expected, 'Pinned input changed: ' + name)
        if name in dependencies:
            old = dependencies[name]
            require(all(old[k] == row[k] for k in ['path', 'bytes', 'sha256']), 'Repeated input changed')
            row['roles'] = sorted(set(old['roles'] + row['roles']))
        dependencies[name] = row
        return raw
    def checked(row, role):
        rows([row])
        raw = bind(row['path'], role, row['sha256'])
        require(len(raw) == row['bytes'], 'Pinned byte count changed')
        return raw
    def git(*argv):
        require(argv[0] in {'branch', 'rev-parse', 'show', 'ls-tree', 'diff'}, 'Read-only Git only')
        require(argv[0] != 'branch' or argv[1:] == ('--show-current',), 'Read-only branch query only')
        directory = attempt / 'git'
        directory.mkdir(exist_ok=True)
        index = len(commands)
        rec = {'argv': ['git', *argv], 'cwd': str(repo), 'started_utc': utc(),
               'actual_execution': False, 'completed': False, 'pid': None,
               'exit_code': None, 'stdin_supplied': False}
        commands.append(rec)
        try:
            with (directory / (str(index) + '.stdout')).open('xb') as out, \
                    (directory / (str(index) + '.stderr')).open('xb') as err:
                child = subprocess.Popen(rec['argv'], cwd=repo, stdin=subprocess.DEVNULL,
                                         stdout=out, stderr=err,
                                         env=dict(os.environ, GIT_OPTIONAL_LOCKS='0'))
                rec.update(actual_execution=True, pid=child.pid)
                try:
                    rec['exit_code'] = child.wait(timeout=60)
                    rec['completed'] = True
                except BaseException:
                    child.kill()
                    rec['exit_code'] = child.wait()
                    raise
        except BaseException:
            rec['failure'] = traceback.format_exc()
            raise
        finally:
            rec['finished_utc'] = utc()
            for channel in ['stdout', 'stderr']:
                path = directory / (str(index) + '.' + channel)
                if path.exists():
                    raw = regular(path)
                    rec[channel] = {'path': path.relative_to(attempt).as_posix(),
                                    'bytes': len(raw), 'sha256': sha(raw)}
            (attempt / 'GIT_COMMANDS.json').write_bytes(encode(commands))
        require(rec['completed'] is True and type(rec['exit_code']) is int and
                rec['exit_code'] == 0, 'Actual read-only Git failed; retained')
        require(not regular(directory / (str(index) + '.stderr')), 'Unexpected Git stderr; retained')
        return regular(directory / (str(index) + '.stdout'))

    prep_raw = bind('current_preparation_family/PREPARATION_MANIFEST.json', 'closed_source_preparation')
    prep = load(prep_raw)
    require(prep['schema'] == 'PR44_CURRENT_SOURCE_ONLY_CLOSURE_v1' and
            prep['status'] == 'CLOSED_SOURCE_ONLY_CURRENT_PREPARATION' and
            prep['self_excluded'] == ['PREPARATION_MANIFEST.json'] and
            type(prep['files_count']) is int and prep['files_count'] == len(prep['files']),
            'Closed source-only preparation required')
    names = rows(prep['files'])
    require(inventory(script.parent) == names | {'PREPARATION_MANIFEST.json'}, 'Source closure changed')
    require(stat.S_IMODE((script.parent / 'PREPARATION_MANIFEST.json').stat().st_mode) == 0o444,
            'Source manifest full0444 required')
    for row in prep['files']:
        require(stat.S_IMODE((script.parent / row['path']).stat().st_mode) == 0o444,
                'Source member full0444 required')
        outputs['build/source_preparation/' + row['path']] = checked(
            dict(row, path='current_preparation_family/' + row['path']), 'reviewed_source_preparation')
    outputs['build/source_preparation/PREPARATION_MANIFEST.json'] = prep_raw
    pins = load(bind('current_preparation_family/STATIC_INPUT_BINDINGS.json', 'fixed_input_contract'))
    require(pins['schema'] == 'PR44_FIXED_CURRENT_SOURCE_INPUTS_v1' and
            pins['status'] == 'SOURCE_ONLY_ROOT_PREREQUISITES_PENDING', 'SOURCEONLY status required')
    require(git('branch', '--show-current').strip() == b'main', 'Stay on main')
    snapshot_raw = checked(pins['snapshot_manifest'], 'original18_snapshot')
    snapshot = load(snapshot_raw)
    require(snapshot['schema'] == 'pr44-root-readonly-original-snapshot/v1' and
            snapshot['head'] == HEAD and snapshot['base'] == BASE and
            type(snapshot['pr']) is int and snapshot['pr'] == 44 and
            type(snapshot['id']) is int and snapshot['id'] == 2912 and
            len(snapshot['files']) == 18 and len(snapshot['changed_paths']) == 19,
            'Exact original18/diff19 identities required')
    original = {}
    for row in snapshot['files']:
        name = relative(row['path'])
        require(name not in original and type(row['size']) is int and row['size'] >= 0 and
                hex64(row['sha256']) and row['mode'] == '100644' and
                type(row['git_blob']) is str and re.fullmatch('[0-9a-f]{40}', row['git_blob']),
                'Typed unique original Git file required')
        raw = bind('source_snapshot_v2/' + name, 'immutable_original18', row['sha256'])
        require(len(raw) == row['size'], 'Original size changed')
        native = 'unsolved_math_prioritization/attempts/2912/' + name
        require(git('show', HEAD + ':' + native) == raw, 'Original Git object bytes differ')
        require(git('ls-tree', HEAD, '--', native).decode().strip() ==
                row['mode'] + ' blob ' + row['git_blob'] + '\t' + native, 'Original mode/blob differs')
        original[name] = raw
    require(inventory(audit / 'source_snapshot_v2') == set(original) and
            sha(original['OBSTRUCTION.md']) == SCIENCE, 'Complete original science required')
    tree = git('ls-tree', '-r', '-z', HEAD, '--', 'unsolved_math_prioritization/attempts/2912/').decode().split('\0')
    require({entry.split('\t', 1)[1] for entry in tree if entry} ==
            {'unsolved_math_prioritization/attempts/2912/' + name for name in original}, 'Complete original Git tree required')
    diff = bind('original_diff_v2.patch', 'whole_original19_path_diff', snapshot['diff_sha256'])
    require(type(snapshot['diff_bytes']) is int and len(diff) == snapshot['diff_bytes'] == 75046 and
            git('diff', BASE, HEAD) == diff and git('diff', '--name-only', BASE, HEAD).decode().splitlines() ==
            snapshot['changed_paths'], 'Full original diff/tree binding required')
    ledger = [load(line) for line in original['turns.jsonl'].splitlines()]
    require(len(ledger) == 2 and all(type(row['turn']) is int for row in ledger) and
            [row['turn'] for row in ledger] == [1, 2] and all(row['outcome'] == 'stalled' for row in ledger),
            'Exact original two-turn stopped ledger required')
    require(original['verify_group_block.py'] == original['review/submitted_verifier.py'] and
            original['group_block_verification.json'] == original['review/submitted_results.json'] and
            original['OBSTRUCTION.md'] == original['review/reviewed_obstruction.md'], 'Original duplicate bindings differ')
    saved, independent = load(original['group_block_verification.json']), load(original['review/independent_results.json'])
    require(saved['status'] == independent['status'] == 'PASS' and
            type(saved['exact_assertions']) is int and saved['exact_assertions'] == 507 and
            type(independent['exact_assertions']) is int and independent['exact_assertions'] == 29933 and
            all(type(n) is int and n > 0 for n in independent['categories'].values()) and
            sum(independent['categories'].values()) == 29933, 'Whole saved arithmetic scope required')
    for row in pins['auxiliary']:
        outputs['root_historical_exports/' + row['path']] = checked(row, 'retained_ROOT_export_or_failure_evidence')
    family_pins = {}
    for family, info in pins['families'].items():
        require(family in {'duality_algebra_family', 'literal_realization_family'}, 'Exact family identities required')
        own, foreign = rows(info['copied_members']), rows(info['foreign_members'])
        manifest_name = relative(info['manifest']['path'])
        require(not own.intersection(foreign) and inventory(audit / family) == own | foreign | {manifest_name},
                'Exact disjoint independent-family closure required')
        directories = {p.relative_to(audit / family).as_posix() for p in (audit / family).rglob('*') if p.is_dir()}
        require(directories == set(info['directories']), 'Independent family directory topology changed')
        mf = checked(dict(info['manifest'], path=family + '/' + manifest_name), 'closed_independent_manifest')
        require(stat.S_IMODE((audit / family / manifest_name).stat().st_mode) == 0o444, 'Family manifest full0444 required')
        family_pins[family] = sha(mf)
        outputs['family_evidence/' + family + '/' + manifest_name] = mf
        for row in info['copied_members'] + info['foreign_members']:
            body = checked(dict(row, path=family + '/' + row['path']),
                           'individually_excluded_foreign' if row['path'] in foreign else 'independent_authored_evidence')
            require(stat.S_IMODE((audit / family / row['path']).stat().st_mode) == 0o444, 'Family full0444 required')
            if row['path'] in own:
                outputs['family_evidence/' + family + '/' + row['path']] = body
        for row in info['external_inputs']:
            checked(row, 'individual_foreign_parent_input_not_fresh_native_authority')
    require(set(family_pins) == {'duality_algebra_family', 'literal_realization_family'}, 'Both independent families required')
    dual = load(bind('duality_algebra_family/VERDICT.json', 'full_scoped_duality_verdict'))
    lit = load(bind('literal_realization_family/verdict.json', 'full_scoped_literal_verdict'))
    require(dual['verdict'] == 'PASS_SCOPED_DUALITY_AND_ALGEBRA_DEDUCTIONS' and
            dual['mandatory_mathematical_corrections'] == [] and dual['original_target_solved'] is False and
            dual['no_novelty_claim'] is True and lit['verdict'] == 'PASS_SCOPED_PARTIAL_DEDUCTIONS' and
            lit['mandatory_corrections'] == [] and lit['full_target_solved'] is False and lit['novelty_verified'] is False,
            'Independent scoped reports only; no full solution')

    future = {}
    for name, option in [('ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md', 'root_scope_certificate_sha256'),
                         ('ROOT_PRIMARY_READ_LEDGER.json', 'root_read_ledger_sha256'),
                         ('ROOT_SCIENCE_CARD.json', 'root_science_card_sha256'),
                         ('ROOT_CURRENT_INPUT_PREIMAGES.json', 'root_current_input_manifest_sha256'),
                         ('ROOT_EVIDENCE_BINDINGS.json', 'root_evidence_bindings_sha256')]:
        future[name] = bind(name, 'genuine_separate_ROOT_prerequisite', getattr(args, option))
    evidence = load(future['ROOT_EVIDENCE_BINDINGS.json'])
    require(set(evidence) == {'schema', 'approved_by_root', 'created_utc', 'notes', 'manifest', 'proof_notes', 'summary'} and
            evidence['schema'] == 'PR44_ROOT_EVIDENCE_BINDINGS_v1' and evidence['approved_by_root'] is True and
            type(evidence['notes']) is str and len(evidence['notes'].strip()) >= 40 and
            clock(prep['utc']) <= clock(evidence['created_utc']) <= dt.datetime.now(dt.timezone.utc),
            'Genuine ROOT evidence binding required; drafts rejected')
    require(evidence['manifest']['path'] == 'root_original_actual_reproduction/MANIFEST.json' and
            evidence['proof_notes']['path'] == 'ROOT_SOURCE_MATCH_AND_PROOF_NOTES.md' and
            evidence['summary']['path'].startswith('root_original_actual_reproduction/'), 'Exact ROOT evidence anchors required')
    actual_manifest_raw = checked(evidence['manifest'], 'genuine_ROOT_reproduction_self_manifest')
    actual_manifest = load(actual_manifest_raw)
    require(actual_manifest['schema'] == 'pr44-root-original-reproduction/v1' and
            actual_manifest['self_excluded'] == ['MANIFEST.json'] and
            type(actual_manifest['files_count']) is int and actual_manifest['files_count'] == len(actual_manifest['files']) and
            actual_manifest['original_head'] == HEAD and actual_manifest['source_snapshot_manifest_sha256'] == sha(snapshot_raw) and
            all(type(actual_manifest[key]) is int and actual_manifest[key] == expected for key, expected in
                [('original_substantive_attempts', 2), ('new_substantive_attempts', 0), ('audit_turns', 0)]),
            'Exact genuine ROOT original reproduction closure required')
    actual_names = rows(actual_manifest['files'])
    require(inventory(audit / 'root_original_actual_reproduction') == actual_names | {'MANIFEST.json'}, 'ROOT reproduction topology changed')
    outputs['root_evidence/root_original_actual_reproduction/MANIFEST.json'] = actual_manifest_raw
    for row in actual_manifest['files']:
        outputs['root_evidence/root_original_actual_reproduction/' + row['path']] = checked(
            dict(row, path='root_original_actual_reproduction/' + row['path']), 'full_ROOT_actual_reproduction_member')
    summary_raw = checked(evidence['summary'], 'ROOT_full_actual_reproduction_summary')
    summary = load(summary_raw)
    require(summary['schema'] == 'PR44_ROOT_CURRENT_REPRODUCTION_SUMMARY_v1' and
            summary['actual_reproductions_completed'] is True and
            equal(summary['entire_author_result'], saved) and equal(summary['entire_independent_result'], independent) and
            summary['author_receipt_byte_exact'] is True and summary['independent_receipt_byte_exact'] is True and
            summary['full_original18_verified'] is True and equal(summary['whole_original_ledger'], ledger) and
            summary['finite_checks_do_not_prove_geometric_realization_or_full_problem'] is True and
            type(summary['whole_raw_bytes']) is int and summary['whole_raw_bytes'] == 149266659 and
            type(summary['whole_SQL_rows']) is int and summary['whole_SQL_rows'] == 15458 and
            type(summary['prior_raw_key_present']) is bool and
            all(type(summary[key]) is int and summary[key] == expected for key, expected in
                [('original_substantive_attempts', 2), ('new_substantive_attempts', 0), ('audit_turns', 0)]),
            'Whole actual results, source inputs and original accounting required')
    require(type(summary['actual_replay_captures']) is list and len(summary['actual_replay_captures']) == 2,
            'Two genuine complete ROOT helper captures required')
    for row in summary['actual_replay_captures']:
        cap = load(checked(row, 'genuine_actual_ROOT_helper_capture'))
        require(cap['schema'] == 'root-explicit-command-capture/v1' and cap['actual_execution'] is True and
                cap['completed'] is True and type(cap['pid']) is int and cap['pid'] > 0 and
                type(cap['exit_code']) is int and cap['exit_code'] == 0 and cap['stdin_supplied'] is False and
                cap['operator_unchanged'] is True and clock(cap['started_utc']) <= clock(cap['finished_utc']),
                'Actual ROOT child capture required')
        parent = PurePosixPath(row['path']).parent.as_posix()
        for channel in ['stdout', 'stderr']:
            checked(dict(cap[channel], path=parent + '/' + relative(cap[channel]['path'])), 'whole_actual_helper_' + channel)
    notes = checked(evidence['proof_notes'], 'completed_ROOT_proof_and_source_notes')
    require(notes.decode().strip() and 'DRAFT' not in notes.decode(), 'Completed ROOT proof notes required')

    certificate = future['ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md'].decode()
    require(certificate.splitlines()[0] == '# ROOT PR44 scoped standard-partial acceptance' and
            certificate.splitlines().count('ROOT_SCOPE_ACCEPTED_STANDARD_PARTIAL_ONLY') == 1 and 'DRAFT' not in certificate,
            'Completed separate ROOT certificate required')
    for literal in ['PR44 / 2912 / KP-4.36', HEAD, BASE, 'Status: unsolved',
                    'Original turns: 2/5; new: 0; audit: 0', 'Full problem solved: false',
                    'Novelty: false', 'NEW whole-current review: PENDING', 'Paper/new DOI/tracker: false']:
        require(literal in certificate, 'Missing literal ROOT scope: ' + literal)
    reading, science = load(future['ROOT_PRIMARY_READ_LEDGER.json']), load(future['ROOT_SCIENCE_CARD.json'])
    qualification = bind('current_preparation_family/SOURCE_PRECISION_QUALIFICATIONS.md', 'global_qualification')
    for obj, schema in [(reading, 'PR44_ROOT_PRIMARY_READ_LEDGER_v1'), (science, 'PR44_ROOT_SCIENCE_CARD_v1')]:
        require(obj['schema'] == schema and obj['reading_completed'] is True and
                equal(obj['root_flags'], {flag: True for flag in FLAGS}) and
                type(obj['reading_notes']) is str and len(obj['reading_notes'].strip()) >= 40 and
                clock(prep['utc']) <= clock(obj['created_utc']) <= dt.datetime.now(dt.timezone.utc), 'Completed genuine ROOT reading required')
        require(obj['scope_certificate_sha256'] == args.root_scope_certificate_sha256 and
                obj['preparation_manifest_sha256'] == sha(prep_raw) and obj['source_qualification_sha256'] == sha(qualification) and
                obj['evidence_bindings_sha256'] == args.root_evidence_bindings_sha256 and
                equal(obj['family_manifest_sha256'], family_pins) and
                all(type(obj[key]) is int and obj[key] == expected for key, expected in
                    [('original_substantive_attempts', 2), ('new_substantive_attempts', 0), ('audit_turns', 0)]), 'ROOT reading identities/pins/accounting differ')
    require(science['status'] == 'unsolved' and science['partial_valid'] is True and
            science['full_problem_solved'] is False and science['novelty_claimed'] is False and
            type(science['turn_limit']) is int and science['turn_limit'] == 5 and
            all(science[key] is False for key in ['paper_created', 'new_DOI_created', 'tracker_row_created']) and
            science['read_ledger_sha256'] == args.root_read_ledger_sha256 and
            science['current_input_manifest_sha256'] == args.root_current_input_manifest_sha256 and
            science['new_whole_current_gate'] == 'PENDING' and all(science[key] is None for key in
                ['current_model', 'current_reasoning_effort', 'current_deadline_utc', 'current_verdict']),
            'Only scoped unsolved standard-partial acceptance with explicit unknown runtime')
    current = load(future['ROOT_CURRENT_INPUT_PREIMAGES.json'])
    require(set(current) == {'schema', 'approved_by_root', 'created_utc', 'reason', 'current_head', 'files'} and
            current['schema'] == 'PR44_ROOT_FRESH13_INPUT_PREIMAGES_v1' and current['approved_by_root'] is True and
            type(current['reason']) is str and len(current['reason'].strip()) >= 40 and
            clock(prep['utc']) <= clock(current['created_utc']) <= dt.datetime.now(dt.timezone.utc) and
            rows(current['files']) == NATIVE and len(current['files']) == 13 and
            type(current['current_head']) is str and re.fullmatch('[0-9a-f]{40}', current['current_head']),
            'Genuine fresh13 and current main HEAD required; dated foreign inputs are not authority')
    def validate_native():
        require(git('branch', '--show-current').strip() == b'main' and
                git('rev-parse', 'HEAD').decode().strip() == current['current_head'], 'Approved main HEAD changed')
        for row in current['files']:
            body = regular(repo / row['path'])
            require(len(body) == row['bytes'] and sha(body) == row['sha256'], 'Fresh native preimage changed')
            structured(row['path'], body)
    validate_native()
    outer_name = relative(os.environ.get('PR44_ROOT_OUTER_CAPTURE', ''))
    require(re.fullmatch(r'tmp/root_pr44_current_outer_[0-9]{8}T[0-9]{6}\.[0-9]{6}Z', outer_name), 'Reviewed real ROOT outer prelaunch required')
    outer_raw = bind(outer_name + '/OPERATION_PRELAUNCH.json', 'actual_ROOT_outer_prelaunch')
    outer = load(outer_raw)
    require(outer['schema'] == 'PR44_ROOT_BUILDER_PRELAUNCH_v1' and
            type(outer['operator_pid']) is int and outer['operator_pid'] == os.getppid() and
            outer['builder_sha256'] == sha(regular(script)) and
            outer['operator_sha256'] == sha(regular(script.parent / 'capture_root_builder_operation.py')) and
            outer['argv'] == ['/usr/bin/python3', '-B', str(script), *sys.argv[1:]] and outer['cwd'] == str(repo) and
            clock(outer['started_utc']) <= dt.datetime.now(dt.timezone.utc), 'Actual parent/source/argv prelaunch differs')
    for name, expected in [('PRELAUNCH_BUILDER_SOURCE.py', outer['builder_sha256']), ('PRELAUNCH_OPERATOR.py', outer['operator_sha256'])]:
        outputs['build/root_outer_prelaunch/' + name] = bind(outer_name + '/' + name, 'actual_prelaunch_source', expected)
    outputs['build/root_outer_prelaunch/OPERATION_PRELAUNCH.json'] = outer_raw
    outputs['CURRENT_EXECUTION_REFERENCE.json'] = encode({'audit_relative_outer_capture': outer_name,
        'outer_parent_pid': os.getppid(), 'audit_relative_inner_attempt': attempt.relative_to(audit).as_posix(),
        'actual_builder_pid': os.getpid(), 'outer_prelaunch_sha256': sha(outer_raw),
        'complete_outer_capture_is_written_only_after_child_exit': True,
        'current_inner_GIT_COMMANDS_record_is_final_only_after_builder_exit': True,
        'receipt_must_be_read_at_original_audit_path_before_promotion': True,
        'future_complete_outer_capture_or_whole_PASS_certified_by_freeze': False})
    queue = regular(repo / 'unsolved_math_prioritization/QUEUE.md')
    lines = queue.splitlines(keepends=True)
    require(sum(line.startswith(b'|') and [v.strip() for v in line.decode().split('|')[1:-1]] == HEADER for line in lines) == 1,
            'Unique named queue header required')
    hits = [(line, line.decode().split('|')) for line in lines if line.startswith(b'|') and
            len(line.decode().split('|')) == len(HEADER) + 2 and line.decode().split('|')[2].strip() == '2912 / KP-4.36']
    require(len(hits) == 1, 'Exact unique target queue row required')
    before, fields = hits[0]
    indexes = {name: HEADER.index(name) + 1 for name in HEADER}
    require(fields[indexes['Status']].strip() == 'queued' and fields[indexes['Turns']].strip() == '0/5', 'Expected queued0/5 preimage')
    after_fields = list(fields)
    finding = ('Standard meridional duality kernel, sufficient degree-one pair map and conditional integral amalgam block verified; '
               'unmarked full2type pair-map and actual equal2type exterior realization gaps remain. '
               'UNSOLVED original2/5,new0,audit0; no novelty/paper/new DOI/tracker. NEW whole-current review PENDING.')
    for name, value in [('Status', 'unsolved'), ('Turns', '2/5'), ('Findings', finding)]:
        after_fields[indexes[name]] = ' ' + value + ' '
    allowed = {indexes[name] for name in ['Status', 'Turns', 'Findings']}
    require(all(left == right for index, (left, right) in enumerate(zip(fields, after_fields)) if index not in allowed), 'Preserve all other fields/Chat/DOI')
    after = '|'.join(after_fields).encode()
    prospective = b''.join(after if line == before else line for line in lines)
    overview = bind('current_preparation_family/CURRENT_OVERVIEW.md', 'current_presentation')
    notice = (b'Historical literal body follows. Runtime/model/reasoning/deadline, search/access and PASS '
              b'labels are dated claims. They do not approve this current packet. Read the global '
              b'SOURCE_PRECISION_QUALIFICATIONS.md first; NEW whole-current review PENDING.\n\n')
    outputs.update({'original_archive/' + name: body for name, body in original.items()})
    outputs.update({name: original[name] for name in IMMUTABLE})
    outputs['review/REVIEW.md'] = qualification + b'\n' + notice + original['review/REVIEW.md']
    outputs.update({'README.md': overview + b'\n' + qualification,
        'CURRENT_OBSTRUCTION_CONTEXT.md': qualification + b'\n' + notice + original['OBSTRUCTION.md'],
        'CURRENT_LITERATURE_STATUS.md': qualification + b'\n' + notice + original['SOURCES.md'],
        'CURRENT_CONTEXT.md': overview + b'\n' + qualification, 'pr_body.md': overview + b'\n' + qualification,
        'SOURCE_PRECISION_QUALIFICATIONS.md': qualification, 'HISTORICAL_ORIGINAL_NOTICE.md': notice,
        'original_snapshot_manifest.json': snapshot_raw, 'original_diff.patch': diff,
        'queue_proposal/QUEUE_PREIMAGE.md': queue, 'queue_proposal/QUEUE_PROSPECTIVE.md': prospective,
        'root_evidence/ROOT_SOURCE_MATCH_AND_PROOF_NOTES.md': notes})
    outputs.update({'root_approval/' + name: body for name, body in future.items()})
    common = {'id': 2912, 'problem_number': 'KP-4.36', 'status': 'unsolved',
        'partial_valid_from_ROOT_source_reading': True, 'full_problem_solved': False, 'novelty_claimed': False,
        'current_model': None, 'current_reasoning_effort': None, 'current_deadline_utc': None,
        'current_verdict': None, 'current_gate': GATE, 'original_substantive_attempts': 2,
        'substantive_attempt_limit': 5, 'new_substantive_attempts': 0, 'audit_turns': 0,
        'historical_runtime_certified': False, 'historical_verdict_transferred': False, 'human_referee_review_claimed': False,
        'paper_created': False, 'new_DOI_created': False, 'tracker_row_created': False,
        'global_qualification': 'SOURCE_PRECISION_QUALIFICATIONS.md', 'archived_original_metadata': 'original_archive',
        'exact_remaining_scientific_gaps': ['No degree-one pair map from unmarked complete2type',
            'No two actual source-category exteriors with equal complete2types and different homotopytypes'],
        'exact_remaining_publication_gap': 'NEW whole-current adversary and ROOT final reconciliation/integration'}
    for name in ['status.json', 'readiness.json', 'review/verdict.json', 'review/review_summary.json']:
        outputs[name] = encode(common)
    outputs['CURRENT_PRECISION_RECEIPT.json'] = encode({'original18_archive_byte_exact': True,
        'current_immutable_science_code_source_results_ledger_exact': True,
        'actual_now_author507_and_old_independent29933_entire_results_byte_exact': True,
        'finite_checks_are_not_duality_group_cohomology_geometric_realization_or_full_problem_proof': True,
        'genuine_September30_runtime_certified': False, 'current_runtime_fields_explicit_null': True,
        'original_V1_failed_filename_guess_retained_V2_operative': True,
        'all_source_proof_and_geometric_qualifications_apply_globally': True,
        'no_exhaustive_priority_or_current_literature_absence_certified': True,
        'foreign_PDF_text_pixels_individually_bound_not_copied': True,
        'dated_foreign_native_bindings_are_historical_not_fresh_authority': True, 'NEW_whole_current_gate': 'PENDING'})
    outputs['CURRENT_QUEUE_PATCH.json'] = encode({'phase': 'Local prospective proposal only; no native write', 'id': 2912,
        'allowed_named_changes': ['Status', 'Turns', 'Findings'], 'whole_preimage_sha256': sha(queue),
        'whole_prospective_sha256': sha(prospective), 'row_before': before.decode(), 'row_prospective': after.decode(),
        'other_rows_columns_Chat_DOI_byte_preserved': True})
    outputs['RESEARCH_LOG.md'] = (utc() + ' — actual administrative freeze; publication workflow75%, discovery0%. '
        'Scoped standard partial deductions accepted by genuine ROOT reading; full problem UNSOLVED. '
        'Original2/5,new0,audit0. NEW whole-current review PENDING. No paper/new DOI/tracker.\n').encode()
    for row in dependencies.values():
        body = regular(audit / row['path'])
        require(len(body) == row['bytes'] and sha(body) == row['sha256'], 'Dependency changed before staging')
    validate_native()
    require(regular(repo / 'unsolved_math_prioritization/QUEUE.md') == queue, 'Queue changed before staging')
    outputs['CURRENT_DEPENDENCIES.json'] = encode({'anchor_repository_relative': audit.relative_to(repo).as_posix(),
        'resolution': 'repository_root / anchor_repository_relative / files.path; never scratch',
        'files': sorted(dependencies.values(), key=lambda row: row['path']),
        'foreign_primary_and_derivative_members_individually_hash_bound_not_copied': True,
        'current_native13': current['files'], 'current_main_head': current['current_head']})
    trees = []
    for previous in sorted((audit / 'tmp').glob('root_pr44_current_build_*')):
        require(previous.is_dir() and not previous.is_symlink(), 'Regular retained attempt required')
        previous_files, previous_dirs = [], []
        for path in sorted(previous.rglob('*')):
            require(not path.is_symlink(), 'Retained attempt symlink rejected')
            name = relative(path.relative_to(previous).as_posix())
            if stat.S_ISREG(path.stat().st_mode):
                body = regular(path)
                previous_files.append({'path': name, 'bytes': len(body), 'sha256': sha(body)})
                if previous == attempt:
                    outputs['build/actual_attempt_prepublication_prefix/' + name] = body
            else:
                require(path.is_dir(), 'Retained attempt special member rejected')
                previous_dirs.append(name)
        trees.append({'audit_relative_directory': previous.relative_to(audit).as_posix(),
            'files': previous_files, 'directories': previous_dirs, 'all_original_members_preserved_at_original_audit_path': True,
            'current_attempt_listing_is_prepublication_prefix': previous == attempt, 'positive_packet_claimed': False})
    outputs['build/RETAINED_ACTUAL_ATTEMPT_TREES.json'] = encode(trees)
    stage = attempt / 'stage'
    stage.mkdir(exist_ok=False)
    for name, body in sorted(outputs.items()):
        path = stage / relative(name)
        structured(name, body)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as handle:
            handle.write(body); handle.flush(); os.fsync(handle.fileno())
        path.chmod(0o444)
    require(inventory(stage / 'original_archive') == set(original), 'Original archive18 exact closure required')
    for name, body in original.items():
        require(regular(stage / 'original_archive' / name) == body, 'Original archive bytes changed')
    for name in IMMUTABLE:
        require(regular(stage / name) == original[name], 'Immutable science/code/source/results/ledger changed')
    members = [{'path': name, 'bytes': len(regular(stage / name)), 'sha256': sha(regular(stage / name))}
               for name in sorted(inventory(stage))]
    manifest = {'schema': 'PR44_STRICT_CURRENT_PACKET_v1', 'self_excluded': ['MANIFEST.json'],
        'files_count': len(members), 'files': members, 'current_gate': GATE, 'status': 'unsolved',
        'full_problem_solved': False, 'novelty_claimed': False, 'original_substantive_attempts': 2,
        'new_substantive_attempts': 0, 'audit_turns': 0, 'full_permission_mode': '0444'}
    with (stage / 'MANIFEST.json').open('xb') as handle:
        handle.write(encode(manifest)); handle.flush(); os.fsync(handle.fileno())
    (stage / 'MANIFEST.json').chmod(0o444)
    require(inventory(stage) == {row['path'] for row in members} | {'MANIFEST.json'}, 'Exact self-only packet closure required')
    for row in members:
        path = stage / row['path']; body = regular(path)
        require(len(body) == row['bytes'] and sha(body) == row['sha256'] and
                stat.S_IMODE(path.stat().st_mode) == 0o444, 'Staged bytes/full0444 mode differ')
    require(stat.S_IMODE((stage / 'MANIFEST.json').stat().st_mode) == 0o444, 'Manifest full0444 mode required')
    for row in dependencies.values():
        body = regular(audit / row['path'])
        require(len(body) == row['bytes'] and sha(body) == row['sha256'], 'Dependency changed after staging')
    validate_native()
    require(regular(repo / 'unsolved_math_prioritization/QUEUE.md') == queue, 'Queue changed after staging')
    require(not destination.exists() and not destination.is_symlink(), 'Candidate appeared; retain failed stage')
    publish_absent(stage, destination)
    print(json.dumps({'status': 'ACTUAL_CURRENT_FREEZE_NEW_WHOLE_GATE_PENDING', 'destination': str(destination),
        'manifest_sha256': sha(regular(destination / 'MANIFEST.json')), 'full_problem_solved': False,
        'original_attempts': '2/5', 'new_attempts': 0, 'audit_turns': 0, 'native_writes': 0, 'current_whole_verdict': None}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true')
    for name in ['root-scope-certificate', 'root-read-ledger', 'root-science-card', 'root-current-input-manifest', 'root-evidence-bindings']:
        parser.add_argument('--' + name + '-sha256', required=True)
    args = parser.parse_args()
    require(args.execute and all(hex64(value) for key, value in vars(args).items() if key.endswith('sha256')),
            'ROOT explicit execution and five genuine prerequisite SHA pins required')
    require(not sys.flags.optimize and os.environ.get('PYTHONOPTIMIZE', '') in ('', '0'),
            'Optimization must not suppress checks')
    script = Path(__file__).absolute()
    regular(script)
    require(script.parent.name == 'current_preparation_family' and script.parent.parent.name == 'pr44_2912',
            'Exact PR44 audit anchor required')
    audit, repo = script.parent.parent, script.parent.parent.parents[2]
    require(repo == Path('/Users/alec/Documents/Math'), 'Exact repository root required')
    (audit / 'tmp').mkdir(exist_ok=True)
    require(not (audit / 'tmp').is_symlink(), 'Regular audit-local tmp required')
    attempt = audit / 'tmp' / ('root_pr44_current_build_' + dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ'))
    attempt.mkdir(exist_ok=False)
    (attempt / 'PRELAUNCH_BUILDER_SOURCE.py').write_bytes(regular(script))
    (attempt / 'INVOCATION.json').write_bytes(encode({'argv': sys.argv, 'cwd': str(Path.cwd()),
        'pid': os.getpid(), 'parent_pid': os.getppid(), 'utc': utc(),
        'source_sha256': sha(regular(script)), 'administrative_only': True}))
    try:
        build(args, script, audit, repo, attempt)
    except BaseException:
        error = traceback.format_exc()
        (attempt / 'BUILD_FAILURE.json').write_bytes(encode({'utc': utc(),
            'status': 'FAILED_ACTUAL_BUILD_PRESERVED', 'traceback': error, 'current_positive_verdict': False}))
        print(error, file=sys.stderr)
        raise


if __name__ == '__main__':
    main()
