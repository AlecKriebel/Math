#!/usr/bin/env python3
"""SOURCE ONLY: ROOT may freeze an absent PR42 candidate after full source review.

No scientific helper is imported, compiled or executed. No network, Git mutation,
native/canonical/shared write, release, or external communication is performed.
Actual administrative attempts and failures are retained under audit-local tmp.
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
import subprocess
import sys
import traceback

HEAD = '099ae5e4d06d8789214cfaaece87309c87e914f9'
BASE = '60292bed09f59236aa192cb17aa138f7b4750e1a'
SNAPSHOT = 'fb02fd7824cbe28845f88a404f59420ccb5c794c6e7e95338e8b6d29bdb61c0f'
PARTIAL = '0b116a4593d84d7e9d02f635a080eb0e2242aaba66acfc8efeae74462ad89898'
REVIEWED = 'b51799d262ea7f633771128422708232c0522e7fddbaa5062a955911ed2e79f5'
GATE = 'PENDING_NEW_WHOLE_CURRENT_SOURCE_FIRST_ADVERSARY'
FLAGS = ['original_mathematical_body_fully_read', 'operative_primary_definitions_and_target_fully_read',
         'source_precision_and_historical_qualifications_fully_read_and_accepted',
         'whole_raw_SQL_and_absent_prior_actual_evidence_fully_read',
         'unchanged_original_helper_actual_reproductions_fully_read',
         'both_closed_independent_families_fully_read',
         'closed_input_manifests_and_retained_evidence_exactly_checked',
         'scoped_scientific_conclusions_accepted']
HEADER = ['Rank', 'ID / code', 'Problem', 'EV', 'Impact (/10)', 'Difficulty', 'Proposed',
          'Status', 'Turns', 'Chat', 'Findings', 'DOI']
NATIVE = {'unsolved_math_prioritization/' + name for name in [
    'QUEUE.md', 'state.json', 'history.jsonl', 'catalog.json', 'assessments.json', 'queue.py',
    'policy.json', 'manifest.json', 'cache/problems.json', 'cache/research_results.json',
    'cache/catalog.sqlite', 'review_v2/related_target_groups.json']}
NATIVE.add('draft_pr_publication_program_20260930/inventory.json')
IMMUTABLE = ['PARTIAL.md', 'check_spectra.py', 'check_results.json', 'source_record.json',
             'source_checksums.json', 'turns.jsonl', 'review/PARTIAL.md',
             'review/independent_checks.py', 'review/independent_results.json',
             'review/submitted_check_spectra.py', 'review/submitted_results.json']


def require(value, message):
    if not value:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encode(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + '\n').encode()


def equal(a, b):
    return json.dumps(a, sort_keys=True, ensure_ascii=False, separators=(',', ':')) == json.dumps(b, sort_keys=True, ensure_ascii=False, separators=(',', ':'))


def hex64(value):
    return type(value) is str and re.fullmatch('[0-9a-f]{64}', value) is not None


def clock(value):
    require(type(value) is str, 'Explicit UTC timestamp required')
    parsed = dt.datetime.fromisoformat(value[:-1] + '+00:00' if value.endswith('Z') else value)
    require(parsed.tzinfo is not None and parsed.utcoffset() == dt.timedelta(0), 'Aware UTC required')
    return parsed


def load(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'Duplicate JSON key: ' + key)
            result[key] = value
        return result
    def constant(value):
        raise ValueError('Invalid JSON number: ' + value)
    def floating(value):
        result = float(value)
        require(math.isfinite(result), 'Nonfinite JSON number')
        return result
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant, parse_float=floating)


def relative(value):
    require(type(value) is str and value and '\\' not in value, 'POSIX relative path required')
    path = PurePosixPath(value)
    require(not path.is_absolute() and path.as_posix() == value and not {'.', '..', '.git', '__pycache__'}.intersection(path.parts), 'Unsafe path: ' + value)
    return value


def regular(path):
    require(path.is_file() and not path.is_symlink() and all(not p.is_symlink() for p in path.parents), 'Regular nonsymlink file required: ' + str(path))
    return path.read_bytes()


def inventory(root):
    require(root.is_dir() and not root.is_symlink(), 'Regular directory required')
    files, directories = set(), set()
    for path in root.rglob('*'):
        require(not path.is_symlink(), 'Symlink member rejected')
        name = relative(path.relative_to(root).as_posix())
        if path.is_file():
            files.add(name)
        else:
            require(path.is_dir(), 'Special member rejected')
            directories.add(name)
    expected = {p.as_posix() for name in files for p in PurePosixPath(name).parents if p.as_posix() != '.'}
    require(directories == expected, 'Extra/empty directory rejected')
    return files


def rows(items):
    require(type(items) is list, 'Rows must be a list')
    names = set()
    for item in items:
        require(type(item) is dict and set(item) == {'path', 'bytes', 'sha256'}, 'Exact path/bytes/SHA row required')
        name = relative(item['path'])
        require(name not in names, 'Duplicate row path')
        names.add(name)
        require(type(item['bytes']) is int and item['bytes'] >= 0 and hex64(item['sha256']), 'Typed bytes/SHA required')
    return names


def publish_absent(source, destination):
    require(sys.platform == 'darwin', 'Reviewed macOS exclusive publication required')
    libc = ctypes.CDLL(None, use_errno=True)
    rename = libc.renamex_np
    rename.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]
    rename.restype = ctypes.c_int
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
        row = {'path': name, 'bytes': len(raw), 'sha256': sha(raw), 'roles': [role]}
        require(expected is None or row['sha256'] == expected, 'Pinned input changed: ' + name)
        if name in dependencies:
            previous = dependencies[name]
            require(all(previous[k] == row[k] for k in ['path', 'bytes', 'sha256']), 'Input changed on repeated read')
            row['roles'] = sorted(set(previous['roles'] + row['roles']))
        dependencies[name] = row
        return raw
    def checked(row, role):
        raw = bind(row['path'], role, row['sha256'])
        require(len(raw) == row['bytes'], 'Pinned byte count changed')
        return raw
    def git(*argv):
        require(argv[0] in {'branch', 'rev-parse', 'show', 'ls-tree', 'diff'}, 'Readonly Git only')
        require(argv[0] != 'branch' or argv[1:] == ('--show-current',), 'Readonly branch query only')
        directory = attempt / 'git'
        directory.mkdir(exist_ok=True)
        index = len(commands)
        rec = {'argv': ['git', *argv], 'cwd': str(repo), 'started_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'actual_execution': False, 'completed': False, 'pid': None, 'exit_code': None, 'stdin_supplied': False}
        commands.append(rec)
        try:
            with (directory / (str(index) + '.stdout')).open('xb') as out, (directory / (str(index) + '.stderr')).open('xb') as err:
                child = subprocess.Popen(rec['argv'], cwd=repo, stdin=subprocess.DEVNULL, stdout=out, stderr=err, env=dict(os.environ, GIT_OPTIONAL_LOCKS='0'))
                rec.update(actual_execution=True, pid=child.pid)
                try:
                    rec['exit_code'] = child.wait(timeout=180)
                    rec['completed'] = True
                except BaseException:
                    child.kill()
                    rec['exit_code'] = child.wait()
                    raise
        except BaseException:
            rec['failure'] = traceback.format_exc()
            raise
        finally:
            rec['finished_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
            for channel in ['stdout', 'stderr']:
                path = directory / (str(index) + '.' + channel)
                if path.exists():
                    raw = path.read_bytes()
                    rec[channel] = {'path': path.relative_to(attempt).as_posix(), 'bytes': len(raw), 'sha256': sha(raw)}
            (attempt / 'GIT_COMMANDS.json').write_bytes(encode(commands))
        require(rec['completed'] is True and type(rec['exit_code']) is int and rec['exit_code'] == 0, 'Actual readonly Git failed; retained')
        return (directory / (str(index) + '.stdout')).read_bytes()

    prep_raw = bind('current_preparation_family/PREPARATION_MANIFEST.json', 'closed_source_preparation')
    prep = load(prep_raw)
    require(prep['status'] == 'CLOSED_SOURCE_ONLY_CURRENT_PREPARATION' and prep['self_excluded'] == ['PREPARATION_MANIFEST.json'], 'Closed source-only preparation required')
    names = rows(prep['files'])
    require(inventory(script.parent) == names | {'PREPARATION_MANIFEST.json'}, 'Preparation recursive closure changed')
    for row in prep['files']:
        local = dict(row, path='current_preparation_family/' + row['path'])
        outputs['build/source_preparation/' + row['path']] = checked(local, 'reviewed_source_preparation')
    outputs['build/source_preparation/PREPARATION_MANIFEST.json'] = prep_raw
    pins = load(bind('current_preparation_family/INPUT_PINS.json', 'exact_input_contract'))
    require(pins['status'] == 'SOURCE_ONLY_FIXED_INPUTS_FUTURE_ROOT_PREREQUISITES_PENDING', 'No future verdict in source preparation')
    require(git('branch', '--show-current').strip() == b'main', 'Stay on main')
    snapshot_raw = bind('snapshot_manifest_v2.json', 'original17_snapshot', SNAPSHOT)
    snapshot = load(snapshot_raw)
    require(snapshot['head'] == HEAD and snapshot['base'] == BASE and len(snapshot['files']) == 17 and len(snapshot['changed_paths']) == 18, 'PR42 original17/diff18 exact identities required')
    original = {}
    for row in snapshot['files']:
        name = relative(row['path'])
        require(name not in original and type(row['size']) is int and row['size'] >= 0 and hex64(row['sha256']), 'Typed unique original file')
        raw = bind('source_snapshot_v2/' + name, 'immutable_original17', row['sha256'])
        require(len(raw) == row['size'], 'Original byte count differs')
        native = 'unsolved_math_prioritization/attempts/2233/' + name
        require(git('show', HEAD + ':' + native) == raw, 'Original Git object bytes differ')
        require(git('ls-tree', HEAD, '--', native).decode().strip() == row['mode'] + ' blob ' + row['git_blob'] + '\t' + native, 'Original Git mode/blob differs')
        original[name] = raw
    require(inventory(audit / 'source_snapshot_v2') == set(original) and sha(original['PARTIAL.md']) == PARTIAL and sha(original['review/PARTIAL.md']) == REVIEWED, 'Exact original archive required')
    diff = bind('original_diff_v2.patch', 'whole_original18_path_diff', snapshot['diff_sha256'])
    require(len(diff) == snapshot['diff_bytes'] and git('diff', BASE, HEAD) == diff and git('diff', '--name-only', BASE, HEAD).decode().splitlines() == snapshot['changed_paths'], 'Full original diff changed')
    require(inventory(audit / 'source_snapshot') == set(), 'Preserved failed wrong-base source export must remain empty')
    for info in pins['retained_closures']:
        prefix = relative(info['directory'])
        expected = rows(info['files'])
        require(inventory(audit / prefix) == expected, 'Retained original/capture closure changed: ' + prefix)
        for row in info['files']:
            outputs['root_evidence/' + prefix + '/' + row['path']] = checked(dict(row, path=prefix + '/' + row['path']), 'complete_retained_actual_root_evidence')
    for row in pins['auxiliary']:
        outputs['root_evidence/' + row['path']] = checked(row, 'original_root_record_or_source')
    for family, info in pins['families'].items():
        manifest = checked(dict(info['manifest'], path=family + '/' + info['manifest']['path']), 'closed_independent_manifest')
        authored, foreign = rows(info['copied_members']), rows(info['foreign_members'])
        require(not authored.intersection(foreign), 'Family classes overlap')
        require(inventory(audit / family) == authored | foreign | {info['manifest']['path']}, 'Exact independent family closure changed')
        outputs['family_evidence/' + family + '/' + info['manifest']['path']] = manifest
        for row in info['copied_members'] + info['foreign_members']:
            raw = checked(dict(row, path=family + '/' + row['path']), 'foreign_primary_or_derivative_hash_only' if row['path'] in foreign else 'independent_first_party_evidence')
            if row['path'] in authored:
                outputs['family_evidence/' + family + '/' + row['path']] = raw

    actual = load(bind('root_original_actual_reproduction_v2/RESULT.json', 'whole_genuine_original_reproduction'))
    require(actual['status'] == 'PASS_ROOT_GENUINE_ORIGINAL_REPRODUCTION' and actual['all_original17_full_bytes_verified'] is True, 'Actual original reproduction required')
    require(type(actual['author_assertions']) is int and actual['author_assertions'] == 18306 and type(actual['independent_assertions']) is int and actual['independent_assertions'] == 1263, 'Actual original18306/1263 required')
    require(type(actual['whole_raw_bytes']) is int and actual['whole_raw_bytes'] == 149266659 and type(actual['whole_SQL_rows']) is int and actual['whole_SQL_rows'] == 15458, 'Whole raw/allSQL evidence required')
    require(actual['original_prior_raw_key_present'] is False and actual['prior_SQL_empty_object_is_fallback'] is True and actual['reviewed_author_and_independent_saved_files_byte_exact'] is True, 'Absent prior/fallback and full original byte comparison required')
    require(all(type(actual[k]) is int and actual[k] == v for k, v in [('original_substantive_attempts', 2), ('new_substantive_attempts', 0), ('audit_turns', 0)]), 'Original2/new0/audit0 required')
    require(actual['full_problem_solved'] is False and all(actual[k] is None for k in ['current_model', 'current_reasoning_effort', 'current_deadline_utc']), 'No solved/runtime inference')
    require(len(actual['actual_outer_runs']) == 3, 'Three actual original replays required')
    for run in actual['actual_outer_runs']:
        require(run['actual_execution'] is True and run['completed'] is True and type(run['pid']) is int and run['pid'] > 0 and type(run['exit_code']) is int and run['exit_code'] == 0 and run['stdin_supplied'] is False, 'Genuine complete actual replay required')
        require(clock(run['started_utc']) <= clock(run['finished_utc']), 'Actual clocks ordered')
        for channel in ['stdout', 'stderr', 'source', 'output_file']:
            checked(dict(run[channel], path='root_original_actual_reproduction_v2/' + run[channel]['path']), 'full_actual_original_' + channel)
    saved = load(original['check_results.json'])
    expected = dict(saved, partial_sha256=PARTIAL)
    require(equal(actual['entire_current_author_result'], expected) and equal(actual['entire_reviewed_author_result'], saved) and equal(actual['entire_original_independent_result'], load(original['review/independent_results.json'])), 'Whole typed actual/saved FILE objects differ')
    independent = actual['entire_original_independent_result']
    require(type(independent['passed']) is int and independent['passed'] == len(independent['checks']) == 1263 and type(independent['failed']) is int and independent['failed'] == 0 and all(type(v) is str and v == 'PASS' for v in independent['checks'].values()), 'Every independent check must be preserved')
    ledger = [load(line) for line in original['turns.jsonl'].splitlines()]
    require(len(ledger) == 2 and all(type(row['turn']) is int for row in ledger) and [row['turn'] for row in ledger] == [1, 2] and equal(ledger, actual['whole_original_ledger']), 'Exact complete original two-turn ledger required')
    require(equal(load(original['source_record.json']), load(bind('pinned_problem.json', 'whole_original_problem'))) and load(bind('pinned_prior_report.json', 'absent_raw_prior_SQL_fallback')) == {}, 'Whole source/fallback differs')

    future = {}
    for name, option in [('ROOT_CURRENT_PARTIAL_SCOPE_CERTIFICATE.md', 'root_scope_certificate_sha256'), ('ROOT_PRIMARY_READ_LEDGER.json', 'root_read_ledger_sha256'), ('ROOT_SCIENCE_CARD.json', 'root_science_card_sha256'), ('ROOT_CURRENT_INPUT_PREIMAGES.json', 'root_current_input_manifest_sha256')]:
        future[name] = bind(name, 'genuine_fresh_ROOT_prerequisite', getattr(args, option))
    reading = load(future['ROOT_PRIMARY_READ_LEDGER.json'])
    science = load(future['ROOT_SCIENCE_CARD.json'])
    current = load(future['ROOT_CURRENT_INPUT_PREIMAGES.json'])
    for obj in [reading, science]:
        require(equal(obj['root_flags'], {flag: True for flag in FLAGS}) and obj['reading_completed'] is True, 'ROOT must genuinely finish all specified reading')
        require(obj['scope_certificate_sha256'] == args.root_scope_certificate_sha256 and obj['preparation_manifest_sha256'] == sha(prep_raw) and obj['actual_reproduction_manifest_sha256'] == pins['actual_reproduction_manifest_sha256'], 'ROOT reading pins differ')
        require(obj['source_qualification_sha256'] == pins['qualification_sha256'] and equal(obj['family_manifest_sha256'], pins['family_manifest_sha256']), 'ROOT source/family pins differ')
        require(all(type(obj[k]) is int and obj[k] == v for k, v in [('original_substantive_attempts', 2), ('new_substantive_attempts', 0), ('audit_turns', 0)]), 'ROOT exact attempt accounting required')
    require(science['status'] == 'UNSOLVED' and science['partial_valid'] is True and science['full_problem_solved'] is False and science['novelty_claimed'] is False and science['turn_limit'] == 5 and type(science['turn_limit']) is int, 'Only scoped unsolved partial approval allowed')
    require(science['read_ledger_sha256'] == args.root_read_ledger_sha256 and science['current_input_manifest_sha256'] == args.root_current_input_manifest_sha256 and science['new_whole_current_gate'] == 'PENDING', 'No future whole-current approval')
    require(all(science[k] is None for k in ['current_model', 'current_reasoning_effort', 'current_deadline_utc', 'current_verdict']), 'Current unknown runtime/verdict must be explicit nulls')
    require(current['approved_by_root'] is True and type(current['reason']) is str and len(current['reason'].strip()) >= 20 and clock(current['created_utc']) <= dt.datetime.now(dt.timezone.utc), 'Fresh genuine ROOT input approval required')
    require(rows(current['files']) == NATIVE and len(current['files']) == 13 and type(current['current_head']) is str and re.fullmatch('[0-9a-f]{40}', current['current_head']), 'Exactly13 current native inputs and HEAD required')
    def validate_native():
        require(git('branch', '--show-current').strip() == b'main' and git('rev-parse', 'HEAD').decode().strip() == current['current_head'], 'Approved current main HEAD changed')
        for row in current['files']:
            raw = regular(repo / row['path'])
            require(len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'Genuinely fresh current native preimage changed: ' + row['path'])
    validate_native()
    queue = regular(repo / 'unsolved_math_prioritization/QUEUE.md')
    lines = queue.splitlines(keepends=True)
    headers = [line for line in lines if line.startswith(b'|') and [x.strip() for x in line.decode().split('|')[1:-1]] == HEADER]
    require(len(headers) == 1, 'Exact unique named queue header required')
    hits = []
    for line in lines:
        if not line.startswith(b'|'):
            continue
        fields = line.decode().split('|')
        if len(fields) == len(HEADER) + 2 and fields[2].strip() == '2233 / EP-653':
            hits.append((line, fields))
    require(len(hits) == 1, 'Unique exact target queue row required')
    before, fields = hits[0]
    indexes = {name: HEADER.index(name) + 1 for name in HEADER}
    require(fields[indexes['Status']].strip() == 'queued' and fields[indexes['Turns']].strip() == '0/5', 'Expected native queued0/5 preimage')
    after_fields = list(fields)
    finding = 'Scoped generic-gluing and line/circle obstructions verified; full EP-653 UNSOLVED. No novelty or best-known claim. NEW whole-current review PENDING; original2/5, new0.'
    for name, value in [('Status', 'unsolved'), ('Turns', '2/5'), ('Findings', finding)]:
        after_fields[indexes[name]] = ' ' + value + ' '
    require(all(a == b for i, (a, b) in enumerate(zip(fields, after_fields)) if i not in {indexes[x] for x in ['Status', 'Turns', 'Findings']}), 'Only three named queue fields allowed')
    after = '|'.join(after_fields).encode()
    prospective = b''.join(after if line == before else line for line in lines)

    qualification = bind('current_preparation_family/SOURCE_PRECISION_QUALIFICATIONS.md', 'current_precision_correction', pins['qualification_sha256'])
    overview = bind('current_preparation_family/CURRENT_OVERVIEW.md', 'current_scoped_presentation')
    notice = b'Historical body follows. Its model/reasoning, search/access and review labels are reported archival claims; this administrative packet does not certify genuine historic runtime or transfer old PASS to the NEW whole-current review. See SOURCE_PRECISION_QUALIFICATIONS.md.\n\n'
    outputs.update({'original_archive/' + name: raw for name, raw in original.items()})
    outputs.update({name: original[name] for name in IMMUTABLE})
    corrected = original['SOURCE_AUDIT.md'].replace(b'The corresponding research-results entry is null, with only a dated OPEN-TRIAGE note embedded in the problem background.', b'The raw research-results key EP-653 is absent. The supplied empty object is a SQL fallback, not a fetched prior result or a null-valued entry. A dated OPEN-TRIAGE note is embedded in the problem background.')
    require(corrected != original['SOURCE_AUDIT.md'] and original['SOURCE_AUDIT.md'].count(b'The corresponding research-results entry is null, with only a dated OPEN-TRIAGE note embedded in the problem background.') == 1, 'Exact single prior precision repair required')
    outputs.update({'README.md': overview + b'\n' + qualification, 'CURRENT_CONTEXT.md': overview + b'\n' + qualification,
                    'SOURCE_AUDIT.md': qualification + b'\n' + notice + corrected,
                    'review/REVIEW.md': qualification + b'\n' + notice + original['review/REVIEW.md'],
                    'SOURCE_PRECISION_QUALIFICATIONS.md': qualification, 'HISTORICAL_ORIGINAL_NOTICE.md': notice,
                    'pr_body.md': overview + b'\n' + qualification, 'original_snapshot_manifest.json': snapshot_raw,
                    'original_diff.patch': diff, 'queue_proposal/QUEUE_PREIMAGE.md': queue,
                    'queue_proposal/QUEUE_PROSPECTIVE.md': prospective})
    outputs.update({'root_approval/' + name: raw for name, raw in future.items()})
    common = {'id': 2233, 'problem_number': 'EP-653', 'status': 'unsolved_scoped_partial_pending_NEW_whole_gate',
              'partial_valid_from_root_scientific_reading': True, 'full_problem_solved': False, 'novelty_claimed': False,
              'current_model': None, 'current_reasoning_effort': None, 'current_deadline_utc': None, 'current_verdict': None,
              'current_gate': GATE, 'original_substantive_attempts': 2, 'substantive_attempt_limit': 5,
              'new_substantive_attempts': 0, 'audit_turns': 0, 'historical_runtime_certified': False,
              'historical_verdict_transferred': False, 'exact_remaining_gap': 'Construct n-o(n) distinct pinned-count values for all sufficiently large n, or prove a universal fixed-proportion obstruction.'}
    for name in ['status.json', 'readiness.json', 'review/verdict.json']:
        outputs[name] = encode(common)
    outputs['CURRENT_PRECISION_RECEIPT.json'] = encode({'raw_prior_key_present': False, 'stored_empty_object_is_SQL_fallback': True, 'background_OPEN_triage_is_dated_not_fetched_prior': True, 'current_source_audit_single_sentence_precision_repair': True, 'original17_archive_byte_exact': True, 'current_immutable_scientific_source_ledger_bytes_exact': True, 'saved_author_partial_sha256': REVIEWED, 'actual_current_author_partial_sha256': PARTIAL, 'reviewed_to_final_diff': 'Only review-status header replacement; mathematics unchanged', 'genuine_historic_runtime_certified': False, 'NEW_whole_current_gate': 'PENDING'})
    outputs['CURRENT_QUEUE_PATCH.json'] = encode({'phase': 'Local prospective proposal only; no native write', 'id': 2233, 'allowed_named_changes': ['Status', 'Turns', 'Findings'], 'whole_preimage_sha256': sha(queue), 'whole_prospective_sha256': sha(prospective), 'row_before': before.decode(), 'row_prospective': after.decode(), 'other_rows_columns_Chat_DOI_byte_preserved': True})
    outputs['RESEARCH_LOG.md'] = (dt.datetime.now(dt.timezone.utc).isoformat() + ' — actual administrative freeze; workflow75%, full discovery0%. Scoped partial accepted by genuine ROOT reading; full EP-653 UNSOLVED. Original2/5,new0/audit0. NEW whole-current source-first review PENDING. No paper/DOI/tracker or native/canonical/shared/Git/remote writes. All actual attempt evidence and failures retained.\n').encode()
    for row in dependencies.values():
        raw = regular(audit / row['path'])
        require(len(raw) == row['bytes'] and sha(raw) == row['sha256'], 'Dependency changed before freeze')
    validate_native()
    require(regular(repo / 'unsolved_math_prioritization/QUEUE.md') == queue, 'Queue changed before freeze')
    outputs['CURRENT_DEPENDENCIES.json'] = encode({'anchor_repository_relative': audit.relative_to(repo).as_posix(), 'resolution': 'repository_root / anchor_repository_relative / files.path; never scratch', 'files': sorted(dependencies.values(), key=lambda row: row['path']), 'foreign_primary_and_derivative_members_hash_bound_not_copied': True, 'preserved_empty_failed_export_directory': 'source_snapshot', 'current_native13': current['files']})
    # Preserve complete failed attempt files and explicitly record their trees.
    # Failed empty stage directories remain at their original locations; they
    # are named in the receipt rather than copied as extra empty packet dirs.
    for previous in sorted((audit / 'tmp').glob('root_pr42_current_build_*')):
        require(previous.is_dir() and not previous.is_symlink(), 'Regular retained attempt required')
        previous_files, previous_dirs = [], []
        for path in sorted(previous.rglob('*')):
            require(not path.is_symlink(), 'Retained attempt symlink rejected')
            name = relative(path.relative_to(previous).as_posix())
            if path.is_file():
                raw = regular(path)
                previous_files.append({'path': name, 'bytes': len(raw), 'sha256': sha(raw)})
                outputs['build/actual_attempts/' + previous.name + '/' + name] = raw
            else:
                require(path.is_dir(), 'Retained attempt special member rejected')
                previous_dirs.append(name)
        outputs['build/actual_attempt_trees/' + previous.name + '.json'] = encode({'audit_relative_directory': previous.relative_to(audit).as_posix(), 'files': previous_files, 'directories': previous_dirs, 'all_original_members_preserved': True})
    stage = attempt / 'stage'
    stage.mkdir(exist_ok=False)
    for name, raw in sorted(outputs.items()):
        path = stage / relative(name)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as handle:
            handle.write(raw)
        path.chmod(0o444)
    require(inventory(stage / 'original_archive') == set(original), 'Original archive17 exact closure required')
    for name, raw in original.items():
        require(regular(stage / 'original_archive' / name) == raw, 'Original archive bytes changed')
    for name in IMMUTABLE:
        require(regular(stage / name) == original[name], 'Current immutable bytes changed')
    members = [{'path': name, 'bytes': len(regular(stage / name)), 'sha256': sha(regular(stage / name)), 'mode': '0444'} for name in sorted(inventory(stage))]
    manifest = {'schema': 'PR42_STRICT_CURRENT_PACKET_v1', 'self_excluded': ['MANIFEST.json'], 'files_count': len(members), 'files': members, 'current_gate': GATE, 'full_problem_solved': False}
    with (stage / 'MANIFEST.json').open('xb') as handle:
        handle.write(encode(manifest))
    (stage / 'MANIFEST.json').chmod(0o444)
    require(inventory(stage) == {row['path'] for row in members} | {'MANIFEST.json'}, 'Exact self-only packet closure required')
    for row in members:
        path = stage / row['path']
        raw = regular(path)
        require(len(raw) == row['bytes'] and sha(raw) == row['sha256'] and path.stat().st_mode & 0o777 == 0o444, 'Staged bytes/mode differ')
    require((stage / 'MANIFEST.json').stat().st_mode & 0o777 == 0o444, 'Manifest readonly mode required')
    require(not destination.exists() and not destination.is_symlink(), 'Candidate appeared; retain stage')
    publish_absent(stage, destination)
    print(json.dumps({'status': 'ACTUAL_CURRENT_FREEZE_NEW_WHOLE_GATE_PENDING', 'destination': str(destination), 'manifest_sha256': sha(regular(destination / 'MANIFEST.json')), 'full_problem': 'UNSOLVED', 'original_attempts': '2/5', 'new_attempts': 0, 'audit_turns': 0, 'native_writes': 0}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true')
    for name in ['root-scope-certificate', 'root-read-ledger', 'root-science-card', 'root-current-input-manifest']:
        parser.add_argument('--' + name + '-sha256', required=True)
    args = parser.parse_args()
    require(args.execute and all(hex64(value) for key, value in vars(args).items() if key.endswith('sha256')), 'ROOT explicit execution and four genuine prerequisite SHA pins required')
    require(not sys.flags.optimize and os.environ.get('PYTHONOPTIMIZE', '') in ('', '0'), 'Optimization must not suppress checks')
    script = Path(__file__).resolve()
    require(script.parent.name == 'current_preparation_family' and script.parent.parent.name == 'pr42_2233', 'Exact PR42 audit anchor required')
    audit = script.parent.parent
    repo = audit.parents[2]
    (audit / 'tmp').mkdir(exist_ok=True)
    require(not (audit / 'tmp').is_symlink(), 'Regular audit-local tmp required')
    attempt = audit / 'tmp' / ('root_pr42_current_build_' + dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ'))
    attempt.mkdir(exist_ok=False)
    (attempt / 'PRELAUNCH_BUILDER_SOURCE.py').write_bytes(regular(script))
    (attempt / 'INVOCATION.json').write_bytes(encode({'argv': sys.argv, 'cwd': str(Path.cwd()), 'pid': os.getpid(), 'utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'source_sha256': sha(regular(script)), 'administrative_only': True}))
    try:
        build(args, script, audit, repo, attempt)
    except BaseException:
        error = traceback.format_exc()
        (attempt / 'BUILD_FAILURE.json').write_bytes(encode({'utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'status': 'FAILED_ACTUAL_BUILD_PRESERVED', 'traceback': error, 'current_positive_verdict': False}))
        print(error, file=sys.stderr)
        raise


if __name__ == '__main__':
    main()
