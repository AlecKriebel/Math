#!/usr/bin/env python3
"""SOURCE ONLY. ROOT may freeze an absent PR43 packet after genuine source reading.

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

HEAD = '86be0f85c7a37a5cad8d24abd16a32d8d1f27e62'
BASE = '60292bed09f59236aa192cb17aa138f7b4750e1a'
FINAL_SOURCE = '90402aea80b79b7713d740863b6058b43c64050c3499701b2bf8490c90b210e3'
HISTORICAL_SOURCE = '98918841ab30dd1e41d51dbc7ec8515a66f1f1c82f01ff08ccc5462b758a2727'
EMPTY = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
GATE = 'PENDING_NEW_WHOLE_CURRENT_SOURCE_FIRST_ADVERSARY'
FLAGS = [
    'original_mathematical_body_and_complete_original_diff_fully_read',
    'operative_primary_definitions_target_and_full_JKP_v2_proof_fully_read',
    'printed_source_proof_repairs_and_historical_qualifications_fully_read_and_accepted',
    'whole_raw_SQL_and_absent_prior_actual_evidence_fully_read',
    'unchanged_original_helper_actual_reproductions_and_all_results_fully_read',
    'both_closed_independent_families_fully_read',
    'all_first_party_closures_and_individual_foreign_exclusions_mechanically_checked',
    'exact_prior_published_source_match_and_scoped_partial_acceptance_accepted',
]
HEADER = ['Rank', 'ID / code', 'Problem', 'EV', 'Impact (/10)', 'Difficulty',
          'Proposed', 'Status', 'Turns', 'Chat', 'Findings', 'DOI']
NATIVE = {'unsolved_math_prioritization/' + name for name in [
    'QUEUE.md', 'state.json', 'history.jsonl', 'catalog.json', 'assessments.json',
    'queue.py', 'policy.json', 'manifest.json', 'cache/problems.json',
    'cache/research_results.json', 'cache/catalog.sqlite',
    'review_v2/related_target_groups.json']}
NATIVE.add('draft_pr_publication_program_20260930/inventory.json')
IMMUTABLE = ['SOURCE_STATUS.md', 'check_normalization.py', 'check_results.json',
             'source_record.json', 'source_checksums.json', 'turns.jsonl',
             'review/author_replay/check_normalization.py',
             'review/author_replay/check_results.json',
             'review/independent_checks.py', 'review/independent_results.json']


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
    require(prep['status'] == 'CLOSED_SOURCE_ONLY_CURRENT_PREPARATION' and
            prep['self_excluded'] == ['PREPARATION_MANIFEST.json'] and
            type(prep['files_count']) is int and prep['files_count'] == len(prep['files']),
            'Closed source-only preparation required')
    names = rows(prep['files'])
    require(inventory(script.parent) == names | {'PREPARATION_MANIFEST.json'}, 'Source closure changed')
    for row in prep['files']:
        outputs['build/source_preparation/' + row['path']] = checked(
            dict(row, path='current_preparation_family/' + row['path']), 'reviewed_source_preparation')
    outputs['build/source_preparation/PREPARATION_MANIFEST.json'] = prep_raw
    pins = load(bind('current_preparation_family/INPUT_PINS.json', 'exact_input_contract'))
    require(pins['status'] == 'SOURCE_ONLY_FIXED_INPUTS_FUTURE_ROOT_PREREQUISITES_PENDING',
            'Future approval cannot appear in source preparation')
    require(git('branch', '--show-current').strip() == b'main', 'Stay on main')
    snapshot_raw = checked(pins['snapshot_manifest'], 'original16_snapshot')
    snapshot = load(snapshot_raw)
    require(snapshot['head'] == HEAD and snapshot['base'] == BASE and
            type(snapshot['pr']) is int and snapshot['pr'] == 43 and
            type(snapshot['id']) is int and snapshot['id'] == 30004386 and
            len(snapshot['files']) == 16 and len(snapshot['changed_paths']) == 17,
            'Exact PR43 original16/diff17 identities required')
    original = {}
    for row in snapshot['files']:
        name = relative(row['path'])
        require(name not in original and type(row['size']) is int and row['size'] >= 0
                and hex64(row['sha256']) and row['mode'] == '100644'
                and type(row['git_blob']) is str and re.fullmatch('[0-9a-f]{40}', row['git_blob']),
                'Typed unique original Git file required')
        raw = bind('source_snapshot/' + name, 'immutable_original16', row['sha256'])
        require(len(raw) == row['size'], 'Original size changed')
        native = 'unsolved_math_prioritization/attempts/30004386/' + name
        require(git('show', HEAD + ':' + native) == raw, 'Original Git object bytes differ')
        require(git('ls-tree', HEAD, '--', native).decode().strip() ==
                row['mode'] + ' blob ' + row['git_blob'] + '\t' + native, 'Original mode/blob differs')
        original[name] = raw
    require(inventory(audit / 'source_snapshot') == set(original) and
            sha(original['SOURCE_STATUS.md']) == FINAL_SOURCE and original['turns.jsonl'] == b'',
            'Exact original scientific body and zero-byte ledger required')
    tree = git('ls-tree', '-r', '-z', HEAD, '--',
               'unsolved_math_prioritization/attempts/30004386/').decode().split('\0')
    require({entry.split('\t', 1)[1] for entry in tree if entry} ==
            {'unsolved_math_prioritization/attempts/30004386/' + name for name in original},
            'Complete original Git tree required')
    diff = bind('original_diff.patch', 'whole_original17_path_diff', snapshot['diff_sha256'])
    require(type(snapshot['diff_bytes']) is int and len(diff) == snapshot['diff_bytes'] == 54344
            and len(diff.splitlines()) == 957 and git('diff', BASE, HEAD) == diff and
            git('diff', '--name-only', BASE, HEAD).decode().splitlines() == snapshot['changed_paths'],
            'Full original diff/tree binding required')

    for info in pins['retained_closures']:
        prefix = relative(info['directory'])
        require(inventory(audit / prefix) == rows(info['files']), 'Retained ROOT closure changed: ' + prefix)
        for row in info['files']:
            outputs['root_evidence/' + prefix + '/' + row['path']] = checked(
                dict(row, path=prefix + '/' + row['path']), 'retained_actual_ROOT_evidence')
    for row in pins['auxiliary']:
        outputs['root_evidence/' + row['path']] = checked(row, 'original_ROOT_source_or_record')
    require(inventory(audit / 'foreign_primary') == rows(pins['root_foreign_members']),
            'Exact root foreign evidence closure required')
    for row in pins['root_foreign_members']:
        checked(dict(row, path='foreign_primary/' + row['path']), 'foreign_primary_or_derivative_hash_only')
    for family, info in pins['families'].items():
        manifest_raw = checked(dict(info['manifest'], path=family + '/' + info['manifest']['path']),
                               'closed_independent_manifest')
        manifest = load(manifest_raw)
        authored, foreign = rows(info['copied_members']), rows(info['foreign_members'])
        require(not authored.intersection(foreign) and inventory(audit / family) ==
                authored | foreign | {info['manifest']['path']}, 'Exact disjoint family closure required')
        if family == 'compactness_source_family':
            normalized_own = manifest['first_party_files']
            normalized_foreign = [{key: row[key] for key in ['path', 'bytes', 'sha256']}
                                  for row in manifest['foreign_individually_excluded']]
            require(len(authored) == 18 and len(foreign) == 8 and
                    manifest['self_manifest_files'] == [{'path': 'OWNERSHIP_MANIFEST.json',
                        'role': 'Exact ownership self-manifest; cryptographic self-hash is necessarily omitted, external final tool hash records bytes'}],
                    'Compactness ownership counts/self changed')
        elif family == 'probability_source_family':
            normalized_own = [{key: row[key] for key in ['path', 'bytes', 'sha256']}
                              for row in manifest['files'] if row['classification'] == 'first_party_audit_artifact']
            normalized_foreign = [{key: row[key] for key in ['path', 'bytes', 'sha256']}
                                  for row in manifest['files'] if row['classification'] == 'foreign_primary_or_access_evidence']
            require(type(manifest['first_party_file_count']) is int and manifest['first_party_file_count'] ==
                    len(authored) == 43 and type(manifest['individual_foreign_file_count']) is int and
                    manifest['individual_foreign_file_count'] == len(foreign) == 23 and
                    len(manifest['files']) == 66, 'Probability exact ownership counts required')
            require(all(row['novelty_claim'] is False and
                        ((row['classification'] == 'first_party_audit_artifact' and row['individual_exclusion'] is None)
                         or (row['classification'] == 'foreign_primary_or_access_evidence' and
                             type(row['individual_exclusion']) is str and row['individual_exclusion']))
                        for row in manifest['files']), 'Probability individual exclusion changed')
        else:
            raise ValueError('Unexpected family')
        require(equal(normalized_own, info['copied_members']) and
                equal(normalized_foreign, info['foreign_members']), 'Family manifest class/row binding changed')
        outputs['family_evidence/' + family + '/' + info['manifest']['path']] = manifest_raw
        for row in info['copied_members'] + info['foreign_members']:
            raw = checked(dict(row, path=family + '/' + row['path']),
                          'individual_foreign_hash_only' if row['path'] in foreign else 'independent_first_party_evidence')
            if row['path'] in authored:
                outputs['family_evidence/' + family + '/' + row['path']] = raw

    actual = load(bind('root_original_actual_reproduction/RESULT.json', 'whole_genuine_original_reproduction'))
    require(actual['status'] == 'PASS_ROOT_GENUINE_ORIGINAL_REPRODUCTION' and
            actual['all_original16_full_bytes_verified'] is True, 'Genuine original reproduction required')
    for key, value in [('author_assertions', 527), ('independent_assertions', 664),
                       ('whole_raw_bytes', 149266659), ('whole_SQL_rows', 15458),
                       ('original_substantive_attempts', 0), ('new_substantive_attempts', 0), ('audit_turns', 0)]:
        require(type(actual[key]) is int and actual[key] == value, 'Typed actual result differs: ' + key)
    require(actual['prior_raw_key_present'] is False and actual['prior_SQL_empty_object_is_fallback'] is True and
            actual['source_prior_null_retrieval_certified'] is False and equal(actual['entire_prior_report'], {}) and
            actual['historical_author_and_independent_saved_files_byte_exact'] is True and
            actual['finite_checks_are_not_LDP_proof'] is True and actual['whole_original_ledger'] == [] and
            actual['original_ledger_sha256'] == EMPTY and
            all(actual[key] is None for key in ['current_model', 'current_reasoning_effort', 'current_deadline_utc']) and
            actual['current_mathematical_and_whole_review'] == 'PENDING', 'Exact provenance/result scope required')
    require(type(actual['actual_outer_runs']) is list and len(actual['actual_outer_runs']) == 3,
            'Three complete actual original replays required')
    require(equal(load(bind('root_original_actual_reproduction/ACTUAL_RUNS.json', 'actual_replay_index')),
                  actual['actual_outer_runs']), 'Actual replay index differs')
    for run in actual['actual_outer_runs']:
        require(run['actual_execution'] is True and run['completed'] is True and
                type(run['pid']) is int and run['pid'] > 0 and type(run['exit_code']) is int and
                run['exit_code'] == 0 and run['stdin_supplied'] is False and
                type(run['optimizer_parent']) is int and run['optimizer_parent'] == 0 and
                run['PYTHONOPTIMIZE'] is None and clock(run['started_utc']) <= clock(run['finished_utc']),
                'Actual replay process/clock/optimization scope required')
        require(type(run['argv']) is list and all(type(value) is str for value in run['argv'])
                and type(run['cwd']) is str, 'Typed actual argv/cwd required')
        for channel in ['stdout', 'stderr', 'source', 'output_file']:
            checked(dict(run[channel], path='root_original_actual_reproduction/' + run[channel]['path']),
                    'full_actual_original_' + channel)
    old = bind('root_original_actual_reproduction/historical_source_status.md', 'actual_historical_source', HISTORICAL_SOURCE)
    before = b'Separate adversarial review of this identification is pending.'
    after = b'Separate adversarial AI review of this identification passed; see [the report](review/REVIEW.md).'
    require(old.count(before) == 1 and old.replace(before, after, 1) == original['SOURCE_STATUS.md'],
            'Exactly one historical/final status sentence difference required')
    saved, independent = load(original['check_results.json']), load(original['review/independent_results.json'])
    require(original['check_normalization.py'] == original['review/author_replay/check_normalization.py'] and
            original['check_results.json'] == original['review/author_replay/check_results.json'] and
            saved['source_status_sha256'] == HISTORICAL_SOURCE and saved['all_passed'] is True and
            type(saved['assertions']) is int and saved['assertions'] == 527, 'Exact saved author scope required')
    require(equal(actual['entire_current_author_result'], dict(saved, source_status_sha256=FINAL_SOURCE)) and
            equal(actual['entire_historical_author_result'], saved) and
            equal(actual['entire_original_independent_result'], independent), 'Entire typed results differ')
    require(type(independent['assertions']) is int and independent['assertions'] == 664 and
            independent['status'] == 'PASS' and type(independent['checks']) is dict and
            all(type(value) is int and value > 0 for value in independent['checks'].values()) and
            sum(independent['checks'].values()) == 664, 'Every finite independent check required')
    require(regular(audit / 'root_original_actual_reproduction/historical_author_private/check_results.json') ==
            original['check_results.json'] and regular(audit /
                'root_original_actual_reproduction/original_independent_private/actual_capture/stdout.bin') ==
            original['review/independent_results.json'], 'Actual historical saved bytes differ')
    require(equal(load(original['source_record.json']), load(bind('pinned_problem.json', 'whole_original_problem'))) and
            equal(load(bind('pinned_prior_report.json', 'absent_prior_SQL_fallback')), {}), 'Whole source/fallback differs')

    # These external files must be authored by ROOT after genuine reading. The
    # adjacent false/null drafts cannot be substituted for any of them.
    future = {}
    for name, option in [('ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md', 'root_scope_certificate_sha256'),
                         ('ROOT_PRIMARY_READ_LEDGER.json', 'root_read_ledger_sha256'),
                         ('ROOT_SCIENCE_CARD.json', 'root_science_card_sha256'),
                         ('ROOT_CURRENT_INPUT_PREIMAGES.json', 'root_current_input_manifest_sha256')]:
        future[name] = bind(name, 'genuine_separate_fresh_ROOT_prerequisite', getattr(args, option))
    certificate = future['ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md'].decode()
    require(certificate.splitlines()[0] == '# ROOT PR43 scoped source-match acceptance' and
            certificate.splitlines().count('ROOT_SCOPE_ACCEPTED_SOURCE_MATCH_ONLY') == 1 and
            'DRAFT' not in certificate, 'Separate actual ROOT certificate, not the pending draft, required')
    for literal in ['ROOT_SCOPE_ACCEPTED_SOURCE_MATCH_ONLY', 'PR43 / 30004386 / OWR-17469-011',
                    HEAD, BASE, 'Status: already_solved', 'Prior publication: 10.4064/sm210413-16-9',
                    'NEW whole-current review: PENDING', 'Original turns: 0/5; new: 0; audit: 0',
                    'Project discovery: false', 'Paper/new DOI/tracker: false']:
        require(literal in certificate, 'Missing literal ROOT certificate scope: ' + literal)
    reading = load(future['ROOT_PRIMARY_READ_LEDGER.json'])
    science = load(future['ROOT_SCIENCE_CARD.json'])
    current = load(future['ROOT_CURRENT_INPUT_PREIMAGES.json'])
    for obj, schema in [(reading, 'PR43_ROOT_PRIMARY_READ_LEDGER_v1'), (science, 'PR43_ROOT_SCIENCE_CARD_v1')]:
        require(obj['schema'] == schema and obj['reading_completed'] is True and
                equal(obj['root_flags'], {flag: True for flag in FLAGS}), 'ROOT must genuinely finish all reading')
        require(type(obj['reading_notes']) is str and len(obj['reading_notes'].strip()) >= 40 and
                clock(prep['utc']) <= clock(obj['created_utc']) <= dt.datetime.now(dt.timezone.utc),
                'Genuine dated substantive ROOT record required')
        require(obj['scope_certificate_sha256'] == args.root_scope_certificate_sha256 and
                obj['preparation_manifest_sha256'] == sha(prep_raw) and
                obj['source_qualification_sha256'] == pins['qualification_sha256'] and
                obj['root_proof_notes_sha256'] == pins['root_proof_notes_sha256'] and
                obj['actual_reproduction_manifest_sha256'] == pins['actual_reproduction_manifest_sha256'] and
                equal(obj['family_manifest_sha256'], pins['family_manifest_sha256']), 'ROOT reading pins differ')
        require(all(type(obj[key]) is int and obj[key] == 0 for key in
                    ['original_substantive_attempts', 'new_substantive_attempts', 'audit_turns']),
                'ROOT original0/new0/audit0 accounting required')
    require(science['status'] == 'already_solved' and science['partial_valid'] is True and
            science['full_target_resolved_in_prior_published_literature'] is True and
            science['full_problem_solved_by_project'] is False and science['novelty_claimed'] is False and
            type(science['turn_limit']) is int and science['turn_limit'] == 5 and
            science['prior_publication_doi'] == '10.4064/sm210413-16-9' and
            science['paper_created'] is False and science['new_DOI_created'] is False and
            science['tracker_row_created'] is False, 'Only credited source-status partial acceptance allowed')
    require(science['read_ledger_sha256'] == args.root_read_ledger_sha256 and
            science['current_input_manifest_sha256'] == args.root_current_input_manifest_sha256 and
            science['new_whole_current_gate'] == 'PENDING' and all(science[key] is None for key in
                ['current_model', 'current_reasoning_effort', 'current_deadline_utc', 'current_verdict']),
            'No future whole-current or unknown runtime certification')
    require(current['schema'] == 'PR43_ROOT_FRESH13_INPUT_PREIMAGES_v1' and current['approved_by_root'] is True and
            type(current['reason']) is str and len(current['reason'].strip()) >= 40 and
            clock(prep['utc']) <= clock(current['created_utc']) <= dt.datetime.now(dt.timezone.utc) and
            rows(current['files']) == NATIVE and len(current['files']) == 13 and
            type(current['current_head']) is str and re.fullmatch('[0-9a-f]{40}', current['current_head']),
            'Genuine separate fresh13 and actual HEAD approval required')
    def validate_native():
        require(git('branch', '--show-current').strip() == b'main' and
                git('rev-parse', 'HEAD').decode().strip() == current['current_head'], 'Approved main HEAD changed')
        for row in current['files']:
            raw = regular(repo / row['path'])
            require(len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'Fresh native preimage changed: ' + row['path'])
            structured(row['path'], raw)
    validate_native()
    outer_name = relative(os.environ.get('PR43_ROOT_OUTER_CAPTURE', ''))
    require(re.fullmatch(r'tmp/root_pr43_current_outer_[0-9]{8}T[0-9]{6}\.[0-9]{6}Z', outer_name),
            'Reviewed prelaunch ROOT outer capture required')
    outer_raw = bind(outer_name + '/OPERATION_PRELAUNCH.json', 'actual_ROOT_outer_prelaunch')
    outer = load(outer_raw)
    require(outer['schema'] == 'PR43_ROOT_BUILDER_PRELAUNCH_v1' and
            type(outer['operator_pid']) is int and outer['operator_pid'] == os.getppid() and
            outer['builder_sha256'] == sha(regular(script)) and
            outer['operator_sha256'] == sha(regular(script.parent / 'capture_root_builder_operation.py')) and
            outer['argv'] == ['/usr/bin/python3', '-B', str(script), *sys.argv[1:]] and
            outer['cwd'] == str(repo) and clock(outer['started_utc']) <= dt.datetime.now(dt.timezone.utc),
            'Actual parent/prelaunch source contract differs')
    for name, expected in [('PRELAUNCH_BUILDER_SOURCE.py', outer['builder_sha256']),
                           ('PRELAUNCH_OPERATOR.py', outer['operator_sha256'])]:
        outputs['build/root_outer_prelaunch/' + name] = bind(outer_name + '/' + name, 'actual_prelaunch_source', expected)
    outputs['build/root_outer_prelaunch/OPERATION_PRELAUNCH.json'] = outer_raw
    outputs['CURRENT_EXECUTION_REFERENCE.json'] = encode({
        'audit_relative_outer_capture': outer_name, 'outer_parent_pid': os.getppid(),
        'actual_builder_pid': os.getpid(), 'outer_prelaunch_sha256': sha(outer_raw),
        'complete_outer_capture_is_written_only_after_child_exit': True,
        'current_inner_GIT_COMMANDS_record_is_final_only_after_builder_exit': True,
        'receipt_must_be_read_at_original_audit_path_before_promotion': True,
        'future_complete_outer_capture_or_whole_PASS_certified_by_freeze': False})

    queue = regular(repo / 'unsolved_math_prioritization/QUEUE.md')
    lines = queue.splitlines(keepends=True)
    headers = [line for line in lines if line.startswith(b'|') and
               [value.strip() for value in line.decode().split('|')[1:-1]] == HEADER]
    require(len(headers) == 1, 'Exact unique named queue header required')
    hits = []
    for line in lines:
        if line.startswith(b'|'):
            fields = line.decode().split('|')
            if len(fields) == len(HEADER) + 2 and fields[2].strip() == '30004386 / OWR-17469-011':
                hits.append((line, fields))
    require(len(hits) == 1, 'Unique exact target queue row required')
    before, fields = hits[0]
    indexes = {name: HEADER.index(name) + 1 for name in HEADER}
    require(fields[indexes['Status']].strip() == 'queued' and fields[indexes['Turns']].strip() == '0/5',
            'Expected native queued0/5 preimage')
    after_fields = list(fields)
    finding = ('Exact full weak-P(R) random-law LDP at speed N and whole Prohorov limit set '
               'match prior Johnston-Kabluchko-Prochno, DOI 10.4064/sm210413-16-9. '
               'Source proof and historical provenance qualified; NEW whole-current review PENDING. '
               'Original0/5, new0; no project discovery, paper, new DOI or tracker.')
    for name, value in [('Status', 'already_solved'), ('Turns', '0/5'), ('Findings', finding)]:
        after_fields[indexes[name]] = ' ' + value + ' '
    allowed = {indexes[name] for name in ['Status', 'Turns', 'Findings']}
    require(all(left == right for index, (left, right) in enumerate(zip(fields, after_fields)) if index not in allowed),
            'Only Status/Turns/Findings may change; preserve Chat/DOI')
    after = '|'.join(after_fields).encode()
    prospective = b''.join(after if line == before else line for line in lines)

    qualification = bind('current_preparation_family/SOURCE_PRECISION_QUALIFICATIONS.md',
                         'global_current_science_and_provenance_qualification', pins['qualification_sha256'])
    overview = bind('current_preparation_family/CURRENT_OVERVIEW.md', 'current_scoped_presentation')
    notice = (b'Historical literal body follows. Its runtime, model/reasoning/deadline, access/search, '
              b'pending/completed review and PASS labels are attributed dated claims. They do not '
              b'approve this current packet or certify September 30 execution. Read the current '
              b'global SOURCE_PRECISION_QUALIFICATIONS.md first; NEW whole-current review PENDING.\n\n')
    # All16 originals, including metadata and stale language, are exact archives.
    outputs.update({'original_archive/' + name: raw for name, raw in original.items()})
    outputs.update({name: original[name] for name in IMMUTABLE})
    for name in ['SOURCE_AUDIT.md', 'review/REVIEW.md']:
        outputs[name] = qualification + b'\n' + notice + original[name]
    outputs.update({'README.md': overview + b'\n' + qualification,
                    'CURRENT_SOURCE_STATUS.md': qualification + b'\n' + notice + original['SOURCE_STATUS.md'],
                    'CURRENT_CONTEXT.md': overview + b'\n' + qualification,
                    'pr_body.md': overview + b'\n' + qualification,
                    'SOURCE_PRECISION_QUALIFICATIONS.md': qualification,
                    'HISTORICAL_ORIGINAL_NOTICE.md': notice,
                    'original_snapshot_manifest.json': snapshot_raw, 'original_diff.patch': diff,
                    'queue_proposal/QUEUE_PREIMAGE.md': queue,
                    'queue_proposal/QUEUE_PROSPECTIVE.md': prospective})
    outputs.update({'root_approval/' + name: raw for name, raw in future.items()})
    common = {'id': 30004386, 'problem_number': 'OWR-17469-011',
              'status': 'already_solved', 'partial_valid_from_ROOT_source_reading': True,
              'full_target_resolved_in_prior_published_literature': True,
              'prior_publication_doi': '10.4064/sm210413-16-9',
              'full_problem_solved_by_project': False, 'novelty_claimed': False,
              'current_model': None, 'current_reasoning_effort': None,
              'current_deadline_utc': None, 'current_verdict': None, 'current_gate': GATE,
              'original_substantive_attempts': 0, 'substantive_attempt_limit': 5,
              'new_substantive_attempts': 0, 'audit_turns': 0,
              'historical_runtime_certified': False, 'historical_verdict_transferred': False,
              'human_referee_review_claimed': False, 'paper_created': False,
              'new_DOI_created': False, 'tracker_row_created': False,
              'global_qualification': 'SOURCE_PRECISION_QUALIFICATIONS.md',
              'archived_original_metadata': 'original_archive',
              'printed_source_repairs': [
                  'JKP prose variance1 corrected to1/3',
                  'Characteristic-function continuity uses finite prefix times uniform nonzero tail at head zeros',
                  'Sorted-coordinate union bound uses2^m(N)_m including ordered assignments',
                  'OWR heuristic density exponent/log/outside-sign displays corrected in audit derivation',
                  'Overbroad Proposition2.2 converse bypassed by compactW finite-cover full upper bound'],
              'exact_remaining_publication_gap': 'NEW whole-current source-first adversary and ROOT final reconciliation/integration'}
    for name in ['status.json', 'readiness.json', 'review/verdict.json', 'review/review_summary.json']:
        outputs[name] = encode(common)
    outputs['CURRENT_PRECISION_RECEIPT.json'] = encode({
        'prior_raw_key_present': False, 'stored_empty_object_is_SQL_fallback': True,
        'original_dated_20260822_open_background_is_not_retrieved_null_prior': True,
        'original_diff_changes_QUEUE_despite_archived_no_shared_edit_claim': True,
        'stale_pending_review_and_old_PASS_are_historical': True,
        'original16_archive_byte_exact': True, 'current_immutable_science_code_source_results_ledger_exact': True,
        'historical_author_saved_source_sha256': HISTORICAL_SOURCE,
        'actual_final_source_sha256': FINAL_SOURCE,
        'entire_historical_source_difference': 'Exactly one review-status sentence',
        'historical_author527_and_old_independent664_reproduced_byte_exact_now': True,
        'current_author527_entire_receipt_differs_only_by_source_status_sha256': True,
        'finite_diagnostics_are_not_LDP_proof': True, 'genuine_September30_runtime_certified': False,
        'historical_human_referee_review_claimed': False, 'current_runtime_fields_explicit_null': True,
        'printed_proof_qualifications_apply_globally': True,
        'novelty_or_exhaustive_priority_certified': False, 'NEW_whole_current_gate': 'PENDING'})
    outputs['CURRENT_QUEUE_PATCH.json'] = encode({
        'phase': 'Local prospective proposal only; no native write', 'id': 30004386,
        'allowed_named_changes': ['Status', 'Turns', 'Findings'],
        'whole_preimage_sha256': sha(queue), 'whole_prospective_sha256': sha(prospective),
        'row_before': before.decode(), 'row_prospective': after.decode(),
        'other_rows_columns_Chat_DOI_byte_preserved': True})
    outputs['RESEARCH_LOG.md'] = (utc() +
        ' — actual administrative freeze; publication workflow75%, project discovery0%. '
        'Credited prior-literature source match accepted by genuine ROOT reading. '
        'Original0/5,new0/audit0. NEW whole-current source-first review PENDING. '
        'No paper/new DOI/tracker or native/canonical/shared/Git/remote write. '
        'All actual failures remain retained at their audit locations.\n').encode()
    for row in dependencies.values():
        raw = regular(audit / row['path'])
        require(len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'Dependency changed before freeze')
    validate_native()
    require(regular(repo / 'unsolved_math_prioritization/QUEUE.md') == queue, 'Queue changed before freeze')
    outputs['CURRENT_DEPENDENCIES.json'] = encode({
        'anchor_repository_relative': audit.relative_to(repo).as_posix(),
        'resolution': 'repository_root / anchor_repository_relative / files.path; never scratch',
        'files': sorted(dependencies.values(), key=lambda row: row['path']),
        'foreign_primary_and_derivative_members_individually_hash_bound_not_copied': True,
        'current_native13': current['files'], 'current_main_head': current['current_head']})
    # Never erase a failed attempt. Bind its complete retained tree; copying
    # failed stages would recursively inflate later packets and relabel history.
    trees = []
    for previous in sorted((audit / 'tmp').glob('root_pr43_current_build_*')):
        require(previous.is_dir() and not previous.is_symlink(), 'Regular retained attempt required')
        previous_files, previous_dirs = [], []
        for path in sorted(previous.rglob('*')):
            require(not path.is_symlink(), 'Retained attempt symlink rejected')
            name = relative(path.relative_to(previous).as_posix())
            mode = path.stat().st_mode
            if stat.S_ISREG(mode):
                raw = regular(path)
                previous_files.append({'path': name, 'bytes': len(raw), 'sha256': sha(raw)})
                if previous == attempt:
                    outputs['build/actual_attempt_prepublication_prefix/' + name] = raw
            else:
                require(stat.S_ISDIR(mode), 'Retained attempt special member rejected')
                previous_dirs.append(name)
        trees.append({'audit_relative_directory': previous.relative_to(audit).as_posix(),
                      'files': previous_files, 'directories': previous_dirs,
                      'all_original_members_preserved_at_original_audit_path': True,
                      'current_attempt_listing_is_prepublication_prefix': previous == attempt,
                      'positive_packet_claimed': False})
    outputs['build/RETAINED_ACTUAL_ATTEMPT_TREES.json'] = encode(trees)
    stage = attempt / 'stage'
    stage.mkdir(exist_ok=False)
    for name, raw in sorted(outputs.items()):
        path = stage / relative(name)
        structured(name, raw)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        path.chmod(0o444)
    require(inventory(stage / 'original_archive') == set(original), 'Original archive16 exact closure required')
    for name, raw in original.items():
        require(regular(stage / 'original_archive' / name) == raw, 'Original archive bytes changed')
    for name in IMMUTABLE:
        require(regular(stage / name) == original[name], 'Current scientific/code/source/result/ledger bytes changed')
    members = [{'path': name, 'bytes': len(regular(stage / name)), 'sha256': sha(regular(stage / name)),
                'mode': '0444'} for name in sorted(inventory(stage))]
    manifest = {'schema': 'PR43_STRICT_CURRENT_PACKET_v1', 'self_excluded': ['MANIFEST.json'],
                'files_count': len(members), 'files': members, 'current_gate': GATE,
                'prior_source_status': 'already_solved', 'full_problem_solved_by_project': False,
                'novelty_claimed': False, 'original_substantive_attempts': 0,
                'new_substantive_attempts': 0, 'audit_turns': 0}
    with (stage / 'MANIFEST.json').open('xb') as handle:
        handle.write(encode(manifest))
        handle.flush()
        os.fsync(handle.fileno())
    (stage / 'MANIFEST.json').chmod(0o444)
    require(inventory(stage) == {row['path'] for row in members} | {'MANIFEST.json'}, 'Exact self-only packet closure required')
    for row in members:
        path = stage / row['path']
        raw = regular(path)
        require(len(raw) == row['bytes'] and sha(raw) == row['sha256'] and
                stat.S_IMODE(path.stat().st_mode) == 0o444, 'Staged bytes/full permission mode differ')
    require(stat.S_IMODE((stage / 'MANIFEST.json').stat().st_mode) == 0o444, 'Manifest full0444 mode required')
    # Recheck closed dependencies and native HEAD/13 after staging as well.
    for row in dependencies.values():
        raw = regular(audit / row['path'])
        require(len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'Dependency changed after staging')
    validate_native()
    require(regular(repo / 'unsolved_math_prioritization/QUEUE.md') == queue, 'Queue changed after staging')
    require(not destination.exists() and not destination.is_symlink(), 'Candidate appeared; retain failed stage')
    publish_absent(stage, destination)
    print(json.dumps({'status': 'ACTUAL_CURRENT_FREEZE_NEW_WHOLE_GATE_PENDING',
                      'destination': str(destination), 'manifest_sha256': sha(regular(destination / 'MANIFEST.json')),
                      'status_in_prior_literature': 'already_solved', 'project_discovery': False,
                      'original_attempts': '0/5', 'new_attempts': 0, 'audit_turns': 0,
                      'native_writes': 0, 'current_whole_verdict': None}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true')
    for name in ['root-scope-certificate', 'root-read-ledger', 'root-science-card', 'root-current-input-manifest']:
        parser.add_argument('--' + name + '-sha256', required=True)
    args = parser.parse_args()
    require(args.execute and all(hex64(value) for key, value in vars(args).items() if key.endswith('sha256')),
            'ROOT explicit execution and four genuine prerequisite SHA pins required')
    require(not sys.flags.optimize and os.environ.get('PYTHONOPTIMIZE', '') in ('', '0'),
            'Optimization must not suppress checks')
    script = Path(__file__).absolute()
    regular(script)
    require(script.parent.name == 'current_preparation_family' and script.parent.parent.name == 'pr43_30004386',
            'Exact PR43 audit anchor required')
    audit, repo = script.parent.parent, script.parent.parent.parents[2]
    require(repo == Path('/Users/alec/Documents/Math'), 'Exact repository root required')
    (audit / 'tmp').mkdir(exist_ok=True)
    require(not (audit / 'tmp').is_symlink(), 'Regular audit-local tmp required')
    attempt = audit / 'tmp' / ('root_pr43_current_build_' + dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ'))
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
