"""Independent read-only input inspector plus finite, manually copied controls.

Does not import, compile, or execute any proposed builder or scientific helper.
Writes only in this new adversary family. Read-only Git child streams are retained.
"""
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

F = Path(__file__).resolve().parent
A = F.parent
P = A / 'current_preparation_family'
R = A.parents[2]
EXPECTED = {
    'PREPARATION_MANIFEST.json': 'af4f28f77df2b7541b099a47fb89a5a454dda5a64272be6e9b70254d17b5c5fa',
    'prepare_current_packet.py': '66a5bc427e90032f6f86bd1007479fadf154282e3f41dfb047a9dd44551c8730',
    'INPUT_PINS.json': '54c0aa6f06615a0ff6c106f9025a8b4ac788da09f3dfb8c242bc669fa76684f3',
    'SOURCE_PRECISION_QUALIFICATIONS.md': '3529898445960cde70381bf99ea8287ec88a1003d8ca1cb4c3e0d088abdee570',
}
BOUND = {}
CHECKS = {}
GIT = []

def h(raw):
    return hashlib.sha256(raw).hexdigest()

def require(v, message):
    if not v:
        raise ValueError(message)

def check(label, v):
    require(v, label)
    CHECKS[label] = 'PASS'

def encode(v):
    return (json.dumps(v, indent=2, ensure_ascii=False) + '\n').encode()

# Manually copied finite predicates; no extraction/AST/compile/import of builder.
def equal(a, b):
    return json.dumps(a, sort_keys=True, ensure_ascii=False, separators=(',', ':')) == json.dumps(b, sort_keys=True, ensure_ascii=False, separators=(',', ':'))

def hex64(v):
    return type(v) is str and re.fullmatch('[0-9a-f]{64}', v) is not None

def clock(v):
    require(type(v) is str, 'Explicit UTC timestamp required')
    p = dt.datetime.fromisoformat(v[:-1] + '+00:00' if v.endswith('Z') else v)
    require(p.tzinfo is not None and p.utcoffset() == dt.timedelta(0), 'Aware UTC required')
    return p

def load(raw):
    def pairs(items):
        d = {}
        for k, v in items:
            require(k not in d, 'Duplicate JSON key: ' + k)
            d[k] = v
        return d
    def constant(v):
        raise ValueError('Invalid JSON number: ' + v)
    def floating(v):
        x = float(v)
        require(math.isfinite(x), 'Nonfinite JSON number')
        return x
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant, parse_float=floating)

def relative(v):
    require(type(v) is str and v and '\\' not in v, 'POSIX relative path required')
    p = PurePosixPath(v)
    require(not p.is_absolute() and p.as_posix() == v and not {'.', '..', '.git', '__pycache__'}.intersection(p.parts), 'Unsafe path: ' + v)
    return v

def regular(p):
    require(p.is_file() and not p.is_symlink() and all(not x.is_symlink() for x in p.parents), 'Regular nonsymlink file required: ' + str(p))
    return p.read_bytes()

def inventory(root):
    require(root.is_dir() and not root.is_symlink(), 'Regular directory required')
    files, dirs = set(), set()
    for p in root.rglob('*'):
        require(not p.is_symlink(), 'Symlink member rejected')
        name = relative(p.relative_to(root).as_posix())
        if p.is_file():
            files.add(name)
        else:
            require(p.is_dir(), 'Special member rejected')
            dirs.add(name)
    expected = {x.as_posix() for name in files for x in PurePosixPath(name).parents if x.as_posix() != '.'}
    require(dirs == expected, 'Extra/empty directory rejected')
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

def read(p, role):
    raw = regular(p)
    name = p.relative_to(R).as_posix()
    row = dict(path=name, bytes=len(raw), sha256=h(raw), roles=[role])
    if name in BOUND:
        old = BOUND[name]
        require(all(row[k] == old[k] for k in ['path', 'bytes', 'sha256']), 'Repeated input changed')
        row['roles'] = sorted(set(old['roles'] + row['roles']))
    BOUND[name] = row
    return raw

def bind(root, row, role):
    raw = read(root / relative(row['path']), role)
    check('binding:' + (root / row['path']).relative_to(R).as_posix(), type(row['bytes']) is int and len(raw) == row['bytes'] and h(raw) == row['sha256'])
    return raw

def git(*argv, okay=(0,)):
    require(argv[0] in {'branch', 'rev-parse', 'show', 'ls-tree', 'diff', 'ls-files', 'check-ignore'}, 'Read-only Git inspector only')
    require(argv[0] != 'branch' or argv[1:] == ('--show-current',), 'Read-only branch query')
    d = F / 'git_readonly_v2'
    d.mkdir(exist_ok=True)
    i = len(GIT)
    rec = dict(argv=['git', *argv], cwd=str(R), started_utc=dt.datetime.now(dt.timezone.utc).isoformat(), actual_execution=False, completed=False, pid=None, exit_code=None, stdin_supplied=False)
    with (d / (str(i) + '.stdout')).open('xb') as out, (d / (str(i) + '.stderr')).open('xb') as err:
        c = subprocess.Popen(rec['argv'], cwd=R, stdin=subprocess.DEVNULL, stdout=out, stderr=err, env=dict(os.environ, GIT_OPTIONAL_LOCKS='0'))
        rec.update(actual_execution=True, pid=c.pid)
        rec['exit_code'] = c.wait(timeout=60)
        rec['completed'] = True
    rec['finished_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
    for channel in ['stdout', 'stderr']:
        raw = (d / (str(i) + '.' + channel)).read_bytes()
        rec[channel] = dict(path='git_readonly_v2/' + str(i) + '.' + channel, bytes=len(raw), sha256=h(raw))
    GIT.append(rec)
    (F / 'GIT_READONLY_COMMANDS_v2.json').write_bytes(encode(GIT))
    require(rec['exit_code'] in okay, 'Read-only Git failure retained')
    return (d / (str(i) + '.stdout')).read_bytes()

def rejects(label, f):
    try:
        f()
    except (ValueError, TypeError, KeyError, json.JSONDecodeError):
        CHECKS[label] = 'PASS_REJECTED'
    else:
        raise ValueError('Failed rejection control: ' + label)

for name, expected in EXPECTED.items():
    check('requested_pin:' + name, h(read(P / name, 'current_preparation_exact_request_pin')) == expected)
prep = load(read(P / 'PREPARATION_MANIFEST.json', 'closed_manifest'))
check('preparation_self_only_exact22', rows(prep['files']) | {'PREPARATION_MANIFEST.json'} == inventory(P) and len(prep['files']) == prep['files_count'] == 21)
for row in prep['files']:
    bind(P, row, 'closed_current_preparation_member')
pins = load(read(P / 'INPUT_PINS.json', 'input_contract'))
check('candidate_absent', not (A / 'reviewed_candidate').exists() and not (A / 'reviewed_candidate').is_symlink())
check('live_main', git('branch', '--show-current').strip() == b'main')
head_now = git('rev-parse', 'HEAD').decode().strip()
snapshot = load(bind(A, pins['original_manifest'], 'original_snapshot_manifest'))
check('original17_diff18', len(snapshot['files']) == 17 and len(snapshot['changed_paths']) == 18 and snapshot['head'] == pins['original_head'] and snapshot['base'] == pins['original_base'])
original = {}
for row in snapshot['files']:
    normalized = dict(path=row['path'], bytes=row['size'], sha256=row['sha256'])
    raw = bind(A / 'source_snapshot_v2', normalized, 'original17')
    path = 'unsolved_math_prioritization/attempts/2233/' + row['path']
    check('original_git_bytes:' + row['path'], git('show', snapshot['head'] + ':' + path) == raw)
    check('original_git_mode_blob:' + row['path'], git('ls-tree', snapshot['head'], '--', path).decode().strip() == row['mode'] + ' blob ' + row['git_blob'] + '\t' + path)
    original[row['path']] = raw
check('original_recursive17', inventory(A / 'source_snapshot_v2') == set(original))
check('wrong_base_failed_export_remains_empty', inventory(A / 'source_snapshot') == set())
diff = read(A / 'original_diff_v2.patch', 'whole_diff18')
check('whole_diff18_exact_bytes', len(diff) == snapshot['diff_bytes'] and h(diff) == snapshot['diff_sha256'] and git('diff', snapshot['base'], snapshot['head']) == diff)
check('whole_diff18_exact_paths', git('diff', '--name-only', snapshot['base'], snapshot['head']).decode().splitlines() == snapshot['changed_paths'])
check('input_pin_original17_matches_snapshot', equal(pins['original17'], [dict(path=x['path'], bytes=x['size'], sha256=x['sha256']) for x in snapshot['files']]))

retained_count = 0
for info in pins['retained_closures']:
    root = A / info['directory']
    check('retained_recursive:' + info['directory'], inventory(root) == rows(info['files']))
    retained_count += len(info['files'])
    for row in info['files']:
        bind(root, row, 'retained_root_closure_member')
check('retained104', retained_count == 104)
check('auxiliary14', len(pins['auxiliary']) == 14)
for row in pins['auxiliary']:
    bind(A, row, 'retained_root_auxiliary')

family_counts = {}
for family, info in pins['families'].items():
    root = A / family
    manifest = load(bind(root, info['manifest'], 'closed_independent_family_manifest'))
    authored, foreign = rows(info['copied_members']), rows(info['foreign_members'])
    check('foreign_disjoint:' + family, not authored.intersection(foreign))
    check('whole_family_closure:' + family, inventory(root) == authored | foreign | {info['manifest']['path']})
    for row in info['copied_members']:
        bind(root, row, 'foreign_family_first_party_to_be_copied')
    for row in info['foreign_members']:
        bind(root, row, 'foreign_primary_derivative_individually_excluded')
    family_counts[family] = dict(copied=len(authored), excluded=len(foreign), self_manifest=1)
    if family == 'literal_geometry_family':
        derivative = 'controls/primary_pdf_extract.stdout.txt'
        check('literal54_plus26_plusself', len(authored) == 54 and len(foreign) == 26 and len(manifest['first_party_closed_files']) == 55)
        check('literal_exact_extraction_stdout_excluded', derivative in foreign and derivative not in authored)
        check('literal_reclassification_matches_closed_seal', authored == {x['path'] for x in manifest['first_party_closed_files']} - {derivative} and foreign == {x['path'] for x in manifest['foreign_primary_excluded_files']} | {derivative})
    else:
        check('exact41_plus5_plusself', len(authored) == 41 and len(foreign) == 5 and len(manifest['own_files_including_self']) == 42)
        check('exact_reclassification_matches_closed_manifest', authored == {x['relative_path'] for x in manifest['own_files_including_self']} - {'OWN_CLOSED_MANIFEST.json'} and foreign == {x['relative_path'] for x in manifest['foreign_files_inside_root_individually_excluded']})
        for row in manifest['foreign_external_read_files_individually_pinned_and_excluded']:
            raw = read(Path(row['path']), 'exact_family_individual_external_binding')
            check('exact_external_binding:' + Path(row['path']).relative_to(R).as_posix(), type(row['bytes']) is int and len(raw) == row['bytes'] and h(raw) == row['sha256'])

actual = load(read(A / 'root_original_actual_reproduction_v2/RESULT.json', 'whole_result'))
check('actual_whole_raw_and_SQL_dimensions', type(actual['whole_raw_bytes']) is int and actual['whole_raw_bytes'] == 149266659 and type(actual['whole_SQL_rows']) is int and actual['whole_SQL_rows'] == 15458)
check('actual_absent_prior_fallback', actual['original_prior_raw_key_present'] is False and actual['prior_SQL_empty_object_is_fallback'] is True)
saved = load(original['check_results.json'])
check('actual_whole_typed_author_results', equal(actual['entire_current_author_result'], dict(saved, partial_sha256=h(original['PARTIAL.md']))) and equal(actual['entire_reviewed_author_result'], saved))
independent = load(original['review/independent_results.json'])
check('actual_whole_independent_object', equal(actual['entire_original_independent_result'], independent))
check('all1263_typed_PASS_labels', type(independent['passed']) is int and independent['passed'] == len(independent['checks']) == 1263 and type(independent['failed']) is int and independent['failed'] == 0 and all(type(x) is str and x == 'PASS' for x in independent['checks'].values()))
ledger = [load(x) for x in original['turns.jsonl'].splitlines()]
check('two_turn_ledger_complete', len(ledger) == 2 and [x['turn'] for x in ledger] == [1, 2] and all(type(x['turn']) is int for x in ledger) and equal(ledger, actual['whole_original_ledger']))
check('source_record_equals_pinned_complete_problem', equal(load(original['source_record.json']), load(read(A / 'pinned_problem.json', 'pinned_full_problem'))))
check('pinned_prior_is_empty_object', load(read(A / 'pinned_prior_report.json', 'prior_SQL_fallback')) == {})
for i, run in enumerate(actual['actual_outer_runs']):
    check('actual_run_metadata:' + str(i), run['actual_execution'] is True and run['completed'] is True and type(run['pid']) is int and run['pid'] > 0 and type(run['exit_code']) is int and run['exit_code'] == 0 and run['stdin_supplied'] is False and clock(run['started_utc']) <= clock(run['finished_utc']))
    for key in ['stdout', 'stderr', 'source', 'output_file']:
        bind(A / 'root_original_actual_reproduction_v2', run[key], 'full_original_actual_' + key)
check('accounting_unresolved_actual', all(type(actual[k]) is int and actual[k] == v for k, v in [('original_substantive_attempts', 2), ('new_substantive_attempts', 0), ('audit_turns', 0)]) and actual['full_problem_solved'] is False)

native = []
for row in pins['native13_at_preparation']:
    raw = read(R / row['path'], 'live13_dated_observation_only')
    native.append(dict(path=row['path'], bytes=len(raw), sha256=h(raw), differs_from_preparation=(len(raw) != row['bytes'] or h(raw) != row['sha256'])))
check('dated_native13_unique_typed', len(native) == 13 and len(rows(pins['native13_at_preparation'])) == 13)
ignored3 = ['unsolved_math_prioritization/cache/problems.json', 'unsolved_math_prioritization/cache/research_results.json', 'unsolved_math_prioritization/cache/catalog.sqlite']
ignore = git('check-ignore', '--', *ignored3).decode().splitlines()
check('ignored3_are_still_whole_byte_dependencies', set(ignore) == set(ignored3))
tracked = git('ls-files', '--', *[row['path'] for row in native]).decode().splitlines()
check('native13_git_distinction10tracked3ignored', len(tracked) == 10 and set(tracked) == {x['path'] for x in native} - set(ignored3))
raw_results = read(R / ignored3[1], 'whole_current_raw_prior_absence')
raw_obj = load(raw_results)
check('current_raw_EP653_key_absent_not_null', 'EP-653' not in raw_obj)

for name in ['DRAFT_ROOT_READ_LEDGER.json', 'DRAFT_ROOT_SCIENCE_CARD.json']:
    draft = load(read(P / name, 'false_null_draft'))
    check('draft_cannot_pass_true_flags:' + name, draft['reading_completed'] is False and not equal(draft['root_flags'], {k: True for k in draft['root_flags']}))
current_draft = load(read(P / 'DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json', 'false_null_draft'))
check('fresh13_draft_cannot_pass', current_draft['approved_by_root'] is False and current_draft['files'] == [] and current_draft['current_head'] is None)

for i, bad in enumerate([b'{"x":1,"x":2}', b'{"a":{"x":1,"x":2}}', b'NaN', b'Infinity', b'-Infinity', b'1e9999']):
    rejects('strict_JSON_reject:' + str(i), lambda bad=bad: load(bad))
check('JSON_equal_distinguishes_boolean_int', not equal(True, 1) and not equal({'x': True}, {'x': 1}))
for i, bad in enumerate(['', '/x', '../x', './x', 'x/../y', 'x//y', 'x/', 'x\\y', '.git/x', '__pycache__/x', True]):
    rejects('unsafe_path_reject:' + str(i), lambda bad=bad: relative(bad))
good_row = dict(path='nested/f', bytes=0, sha256='a' * 64)
for i, bad in enumerate([[dict(good_row, bytes=True)], [dict(good_row, bytes=-1)], [dict(good_row, sha256='A' * 64)], [good_row, good_row], [dict(good_row, extra=1)], {'x': good_row}]):
    rejects('strict_rows_reject:' + str(i), lambda bad=bad: rows(bad))
for i, bad in enumerate(['2026-10-02T00:00:00', '2026-10-02T00:00:00-07:00', None]):
    rejects('UTC_reject:' + str(i), lambda bad=bad: clock(bad))
check('aware_UTC_accept', clock('2026-10-02T00:00:00Z').utcoffset() == dt.timedelta(0))

# Copied queue predicate on the actual live preimage, no native write.
HEADER = ['Rank', 'ID / code', 'Problem', 'EV', 'Impact (/10)', 'Difficulty', 'Proposed', 'Status', 'Turns', 'Chat', 'Findings', 'DOI']
queue = read(R / 'unsolved_math_prioritization/QUEUE.md', 'live_queue_preimage')
lines = queue.splitlines(keepends=True)
headers = [line for line in lines if line.startswith(b'|') and [x.strip() for x in line.decode().split('|')[1:-1]] == HEADER]
hits = []
for line in lines:
    if not line.startswith(b'|'):
        continue
    fields = line.decode().split('|')
    if len(fields) == len(HEADER) + 2 and fields[2].strip() == '2233 / EP-653':
        hits.append((line, fields))
check('queue_unique_header_target', len(headers) == len(hits) == 1)
before, fields = hits[0]
indexes = {name: HEADER.index(name) + 1 for name in HEADER}
check('queue_target_queued0of5', fields[indexes['Status']].strip() == 'queued' and fields[indexes['Turns']].strip() == '0/5')
after_fields = list(fields)
finding = 'Scoped generic-gluing and line/circle obstructions verified; full EP-653 UNSOLVED. No novelty or best-known claim. NEW whole-current review PENDING; original2/5, new0.'
for name, value in [('Status', 'unsolved'), ('Turns', '2/5'), ('Findings', finding)]:
    after_fields[indexes[name]] = ' ' + value + ' '
check('queue_only_named3_fields', all(a == b for i, (a, b) in enumerate(zip(fields, after_fields)) if i not in {indexes[x] for x in ['Status', 'Turns', 'Findings']}))
after = '|'.join(after_fields).encode()
prospective_lines = [after if line == before else line for line in lines]
check('queue_only_one_row_changed', sum(a != b for a, b in zip(lines, prospective_lines)) == 1 and len(lines) == len(prospective_lines))
check('Chat_DOI_bytes_unchanged', fields[indexes['Chat']] == after_fields[indexes['Chat']] and fields[indexes['DOI']] == after_fields[indexes['DOI']])
old = b'The corresponding research-results entry is null, with only a dated OPEN-TRIAGE note embedded in the problem background.'
new = b'The raw research-results key EP-653 is absent. The supplied empty object is a SQL fallback, not a fetched prior result or a null-valued entry. A dated OPEN-TRIAGE note is embedded in the problem background.'
corrected = original['SOURCE_AUDIT.md'].replace(old, new)
check('source_correction_exactly_one_sentence', original['SOURCE_AUDIT.md'].count(old) == 1 and corrected.replace(new, old) == original['SOURCE_AUDIT.md'])
pending = b'Separate adversarial AI review is pending. Finite checks alone do not supply that review, and no claim of novelty or external peer review is made.'
check('reviewed_to_final_math_body_unchanged', original['review/PARTIAL.md'].replace(b'Separate adversarial review is pending.', b'Separate adversarial AI review passed; see [the report](review/REVIEW.md). This has not undergone human peer review.') == original['PARTIAL.md'])

# Closed-tree and actual exclusive-publication controls are confined to this family.
C = F / 'FINITE_CONTROL_SANDBOX_v2'
C.mkdir(exist_ok=False)
valid = C / 'valid'
(valid / 'nested').mkdir(parents=True)
(valid / 'nested/f').write_bytes(b'exact')
check('inventory_valid', inventory(valid) == {'nested/f'})
empty = C / 'empty_extra'
empty.mkdir()
(empty / 'extra').mkdir()
rejects('empty_extra_directory_rejected', lambda: inventory(empty))
symlink = C / 'symlink'
symlink.mkdir()
(symlink / 'link').symlink_to(valid / 'nested/f')
rejects('symlink_member_rejected', lambda: inventory(symlink))
fifo = C / 'fifo'
fifo.mkdir()
os.mkfifo(fifo / 'pipe')
rejects('special_member_rejected', lambda: inventory(fifo))
check('macOS_exclusive_control_environment', sys.platform == 'darwin')
libc = ctypes.CDLL(None, use_errno=True)
rename = libc.renamex_np
rename.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]
rename.restype = ctypes.c_int
def exclusive(source, destination):
    status = rename(os.fsencode(source), os.fsencode(destination), 4)
    return status, ctypes.get_errno()
src = C / 'publication_stage'
src.mkdir()
(src / 'member').write_bytes(b'own finite stage')
(src / 'member').chmod(0o444)
dst = C / 'publication_existing'
dst.mkdir()
(dst / 'sentinel').write_bytes(b'existing destination retained')
failed, err = exclusive(src, dst)
check('exclusive_existing_destination_rejected', failed == -1 and err == 17 and (dst / 'sentinel').read_bytes() == b'existing destination retained' and (src / 'member').read_bytes() == b'own finite stage')
published = C / 'publication_absent'
status, err2 = exclusive(src, published)
check('exclusive_absent_destination_succeeds', status == 0 and not src.exists() and (published / 'member').read_bytes() == b'own finite stage')
check('published_control_0444', (published / 'member').stat().st_mode & 0o777 == 0o444)

mode_probe = C / 'mode_probe_04444'
mode_probe.write_bytes(b'own finite permission probe')
mode_probe.chmod(0o4444)
observed_mode = mode_probe.stat().st_mode
check('concrete_old_permission_mask_false_positive', observed_mode & 0o777 == 0o444 and stat.S_IMODE(observed_mode) == 0o4444 and stat.S_IMODE(observed_mode) != 0o444)
(F / 'MODE_FALSE_POSITIVE.json').write_bytes(encode(dict(path=mode_probe.relative_to(F).as_posix(), observed_st_mode_octal=oct(observed_mode), observed_permission_octal=oct(stat.S_IMODE(observed_mode)), copied_old_predicate_accepts=(observed_mode & 0o777 == 0o444), full_permission_predicate_accepts=(stat.S_IMODE(observed_mode) == 0o444), current_builder_lines=[380, 381], classification='mandatory narrow literal candidate-mode guard correction; no existing candidate/math defect', exposure='ROOT identified this mask class after this agent had read the builder; finite reproduction and classification are this agent own work.')))

# Remove only deliberately created nonregular controls after recording rejection;
# no failed build evidence or first-party inputs are removed. Record this explicitly.
(symlink / 'link').unlink()
(fifo / 'pipe').unlink()
(F / 'NONREGULAR_FINITE_CONTROL_RECORD.json').write_bytes(encode(dict(symlink_control_rejected=True, fifo_control_rejected=True, own_test_nonregular_members_unlinked_after_check=True, historical_or_builder_failure_evidence_removed=False, paths=['FINITE_CONTROL_SANDBOX_v2/symlink/link', 'FINITE_CONTROL_SANDBOX_v2/fifo/pipe'])))
result = dict(schema='PR42_INDEPENDENT_CURRENT_SOURCE_ONLY_ADVERSARY_INSPECTION_v1', utc=dt.datetime.now(dt.timezone.utc).isoformat(), status='PASS_SOURCE_ONLY_FINITE_AND_BINDING_INSPECTION', checks_count=len(CHECKS), checks=CHECKS, current_head_observed=head_now, original_head=snapshot['head'], original_base=snapshot['base'], family_counts=family_counts, retained_ROOT_members=retained_count, auxiliary_members=14, native13_observations=native, git_tracked_native_count=len(tracked), ignored_cache_dependencies=ignored3, foreign_members_individually_bound=sum(x['excluded'] for x in family_counts.values()), all_bound_files=sorted(BOUND.values(), key=lambda x:x['path']), git_commands_count=len(GIT), builder_or_scientific_helper_import_compile_execute=False, candidate_created=False, no_future_ROOT_attestation=True, full_problem_solved=False, original_substantive_attempts=2, new_substantive_attempts=0, audit_turns=0, semantic_reading_limit='Hashes and complete JSON structures do not certify every mathematical proof in closed imported controls or current external papers. Complete current builder/contract and original stated proofs are reviewed separately in the report.')
(F / 'INSPECTION_RESULT.json').write_bytes(encode(result))
print(json.dumps(dict(status=result['status'], checks=len(CHECKS), bindings=len(BOUND), original17=17, diff18=18, retained_ROOT104=retained_count, auxiliary14=14, families=family_counts, git_readonly_commands=len(GIT), current_head_observed=head_now, changed_native13=[x['path'] for x in native if x['differs_from_preparation']], builder_or_scientific_helper_import_compile_execute=False), indent=2))
