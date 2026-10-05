"""Independent AST/data/finite checks; no candidate import or execution.

Only this new review directory is written. The private hard-link exercise is
independently authored syscall evidence, not a run of the candidate writer.
"""
from pathlib import Path, PurePosixPath
import ast
import datetime as dt
import difflib
import hashlib
import json
import os
import stat
import sys

F = Path(__file__).resolve().parent
A = F.parent
R = A.parents[2]
S = A / 'acceptance_execution_preparation_family/integration_source_revision'
O = A / 'acceptance_preparation_family'
P = A / 'acceptance_static_adversary_family'
SEEN = {}
PARSED = {}

def require(condition, label):
    if not condition:
        raise ValueError(label)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def parse(raw):
    def pairs(values):
        result = {}
        for key, value in values:
            require(key not in result, 'duplicate key ' + key)
            result[key] = value
        return result
    def nonfinite(value):
        raise ValueError('nonfinite ' + value)
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=nonfinite)

def equal(a, b):
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return a.keys() == b.keys() and all(equal(a[k], b[k]) for k in a)
    if type(a) is list:
        return len(a) == len(b) and all(equal(x, y) for x, y in zip(a, b))
    return a == b

def name(n):
    require(type(n) is str and n and '\\' not in n and '\0' not in n, 'invalid name')
    p = PurePosixPath(n)
    require(not p.is_absolute() and '..' not in p.parts and str(p) == n, 'noncanonical name')
    return p

def read(root, n):
    name(n)
    p = root / n
    require(root.is_dir() and not root.is_symlink(), 'unsafe root')
    require(p.is_file() and not p.is_symlink(), 'nonregular member ' + str(p))
    for q in p.parents:
        if q == root:
            break
        require(not q.is_symlink(), 'symlink ancestor')
    raw = p.read_bytes()
    record = {'bytes': len(raw), 'sha256': sha(raw)}
    key = p.relative_to(R).as_posix()
    require(key not in SEEN or equal(SEEN[key], record), 'changed member while reading')
    SEEN[key] = record
    return raw

def bind(root, row):
    require(type(row) is dict, 'row object')
    size = row.get('bytes', row.get('size'))
    require(type(size) is int and size >= 0, 'row size')
    require(type(row['sha256']) is str and len(row['sha256']) == 64 and all(c in '0123456789abcdef' for c in row['sha256']), 'row sha')
    raw = read(root, row['path'])
    require(len(raw) == size and sha(raw) == row['sha256'], 'binding changed ' + row['path'])
    return raw

def rows(values):
    if type(values) is dict:
        values = [{'path': k, **v} for k, v in values.items()]
    require(type(values) is list, 'rows list')
    require(len({z['path'] for z in values}) == len(values), 'duplicate row')
    return values

def closure(root, expected, excluded=(), empty=()):
    files, dirs = set(), set()
    for p in root.rglob('*'):
        n = p.relative_to(root).as_posix()
        name(n)
        require(not p.is_symlink() and (p.is_file() or p.is_dir()), 'symlink or special entry ' + n)
        if any(n == e or n.startswith(e + '/') for e in excluded):
            continue
        (dirs if p.is_dir() else files).add(n)
    require(files == set(expected), 'wrong complete closure ' + str(root))
    wanted = {q.as_posix() for n in expected for q in PurePosixPath(n).parents if q.as_posix() != '.'}
    for n in empty:
        require((root / n).is_dir() and not any((root / n).iterdir()), 'qualified empty directory changed')
        wanted.add(n)
    require(dirs == wanted, 'wrong complete directory closure ' + str(root))

def exact_manifest(root, basename, digest, count):
    raw = read(root, basename)
    require(sha(raw) == digest, 'manifest digest')
    value = parse(raw)
    members = rows(value['files'])
    require(len(members) == count, 'manifest count')
    require(basename not in {z['path'] for z in members}, 'self member')
    if 'files_count' in value:
        require(type(value['files_count']) is int and value['files_count'] == count, 'manifest count type')
    for z in members:
        raw = bind(root, z)
        if z['path'].endswith('.json'):
            parse(raw)
    closure(root, {z['path'] for z in members} | {basename})
    return value

revision_manifest_raw = read(S, 'PREPARATION_MANIFEST.json')
revision_manifest_sha = sha(revision_manifest_raw)
exact_manifest(S, 'PREPARATION_MANIFEST.json', revision_manifest_sha, 17)
exact_manifest(O, 'PREPARATION_MANIFEST.json', 'f66df61cb4b57ae63cc007fed3c4dabf9e67e027f1d428d4e0ffbc75a6332fca', 15)
exact_manifest(P, 'MANIFEST.json', 'c782c65b31ef0f38c14bcf49577d11b66b8e19b63b0cce83718f651b3d6f0c9a', 26)
basis = parse(read(S, 'REVISION_BASIS.json'))
source = parse(read(S, 'SOURCE_BINDINGS.json'))
for z in [basis['original_preparation_manifest'], basis['fresh_static_audit_manifest'], basis['fresh_static_report'], source['revision_basis'], source['patch']]:
    bind(R, z)
require(basis['source_only'] is True and basis['root_activation_flags_remain_false'] is True, 'basis flags')
require(source['helpers_imported_or_executed'] is False, 'source execution flag')
changes = []
helper_lines = {}
for z in source['sources']:
    old, new = bind(R, z['original']), bind(R, z['revised'])
    n = PurePosixPath(z['revised']['path']).name
    require(len(new.decode().splitlines()) == z['lines'], 'source line count')
    helper_lines[n] = z['lines']
    ast.parse(new, filename=n)
    require((old == new) is z['BYTE_unchanged'], 'whole source unchanged claim')
    changes.extend(difflib.unified_diff(old.decode().splitlines(keepends=True), new.decode().splitlines(keepends=True), fromfile=z['original']['path'], tofile=z['revised']['path']))
require(''.join(changes).encode() == read(S, 'REVISION.patch'), 'entire patch reconstruction')
require(len(source['sources']) == 5 and sum(z['BYTE_unchanged'] is True for z in source['sources']) == 4, 'five source coverage')
for n, row in basis['immutable_object_copies'].items():
    require(read(S, n) == bind(R, row), 'scientific/input/draft copy changed')
require(set(basis['immutable_object_copies']) == {'INPUT_BINDINGS.json', 'SCIENTIFIC_SCOPE.json', 'DRAFT_FINAL_PLAN.json'}, 'copy set')
draft = parse(read(S, 'DRAFT_FINAL_PLAN.json'))
science = parse(read(S, 'SCIENTIFIC_SCOPE.json'))
require(all(draft[k] is False for k in ['root_full_current_read_completed', 'root_full_whole_scope_read_completed', 'independent_whole_current_pass']), 'false activation flags')
require(draft['preparation_manifest_sha256'] is None and draft['plan_status'] == 'PREPARED_ONLY_AWAITING_ROOT_ACTIVATION_AND_ACTUAL_RECONCILIATION', 'unactivated draft')
require(equal(draft['scientific_scope'], science), 'whole typed scientific scope')
for obj in [science, draft]:
    require(obj['queue_status'] == 'unsolved' and obj['full_problem_solved'] is False and obj['positive_novelty_claim'] is False and obj['original_substantive_attempts'] == 2 and type(obj['original_substantive_attempts']) is int, 'partial scope')
    require(obj['new_substantive_attempts'] == obj['audit_turns'] == 0 and type(obj['new_substantive_attempts']) is int and type(obj['audit_turns']) is int, 'zero new budget')
    require(obj['paper_or_new_doi_or_tracker'] is False and all(obj[k] is None for k in ['current_model', 'current_reasoning_effort', 'current_deadline_utc']), 'no paper/null current metadata')
inputs = parse(read(S, 'INPUT_BINDINGS.json'))
negatives = {z['path']: z for z in inputs['qualified_JSON_negative_inputs']}
require(len(negatives) == 14, 'exact 14 negative inputs')
negative_seen = set()
valid_json_occurrences = 0
def structured(root, z):
    global valid_json_occurrences
    raw = bind(root, z)
    n = (root / z['path']).relative_to(R).as_posix()
    if n in negatives:
        pin = negatives[n]
        require(len(raw) == pin['bytes'] and sha(raw) == pin['sha256'], 'negative full pin')
        try:
            parse(raw)
        except (ValueError, json.JSONDecodeError) as error:
            expected = pin['parse_failure']
            require(str(error) == expected or (expected == 'duplicate key status' and str(error) == 'duplicate key status'), 'negative failure shape')
            negative_seen.add(n)
        else:
            raise ValueError('negative became valid')
    elif z['path'].endswith('.json'):
        PARSED[n] = parse(raw)
        valid_json_occurrences += 1
    elif z['path'].endswith('.jsonl'):
        require(not raw or raw.endswith(b'\n'), 'JSONL terminal newline')
        PARSED[n] = [parse(line) for line in raw.splitlines()]

references = {}
for pin in inputs['pins'].values():
    raw = bind(R, pin)
    if pin['path'].endswith('.json'):
        PARSED[pin['path']] = parse(raw)
    references[pin['path']] = pin
closure_results = []
for c in inputs['closures']:
    m = c['manifest']
    root = (R / m['path']).parent
    value = parse(bind(R, m))
    members = rows(value[c['member_field']])
    require(len(members) == c['authored_count'], 'closed member count')
    extras = rows(c['qualified_extra_members'])
    exclusions = c['excluded_root_private_trees']
    empties = c['qualified_empty_directories']
    require(not exclusions or (c['role'] == 'rotation_family' and exclusions == ['tmp']), 'unexpected private exclusion')
    require(not empties or (c['role'] == 'uniform_family' and empties == ['manifest_control_fixtures/missing/nested']), 'unexpected empty exception')
    for z in members:
        structured(root, z)
    for z in extras:
        bind(root, z)
    closure(root, {z['path'] for z in members + extras} | {PurePosixPath(m['path']).name}, exclusions, empties)
    references[m['path']] = m
    closure_results.append({'role': c['role'], 'authored': len(members), 'foreign_itemized': len(extras), 'exact_private_exclusions': exclusions, 'exact_empty_directories': empties})
dependencies = parse(read(A / 'reviewed_candidate', 'CURRENT_PROOF_DEPENDENCIES.json'))
require(len(dependencies['files']) == 2797, 'complete dependency count')
for z in rows(dependencies['files']):
    structured(A, z)
for cap in inputs['outer_typed_captures']:
    value = parse(bind(R, cap['capture']))
    root = (R / cap['capture']['path']).parent
    require(type(value['pid']) is int and value['pid'] == cap['expected_pid'] and type(value['exit_code']) is int and value['exit_code'] == cap['expected_exit_code'], 'exact outer typed run')
    require(value['actual_execution'] is True and value['completed'] is True, 'outer actual flags')
    for z in cap['files']:
        bind(root, z)
    closure(root, {z['path'] for z in cap['files']})
    require(sha(read(root, 'prelaunch_source.py')) == value['source_sha256'], 'outer prelaunch')
    for channel in ['stdout', 'stderr']:
        bind(root, value[channel])
    references[cap['capture']['path']] = cap['capture']
require(len(references) == 33 and equal([references[n] for n in sorted(references)], draft['immutable_evidence_references']), 'complete 33 typed references')
require(negative_seen == set(negatives), 'all fourteen exact negative inputs covered')
ledger_raw = read(A / 'reviewed_candidate', 'turns.json')
require(sha(ledger_raw) == '015e5bce1a752e1d666d8afdd1637a884438c4e0497eec2c156c5a16e2f3b476' and ledger_raw == read(A / 'reviewed_candidate/original_archive', 'turns.json'), 'original ledger unchanged')
ledger = parse(ledger_raw)
require(type(ledger) is dict and type(ledger['count']) is int and ledger['count'] == 2 and [z['number'] for z in ledger['attempts']] == [1, 2], 'exact original schema/budget')
guard_raw = read(S, 'pr39_guards.py')
tree = ast.parse(guard_raw)
functions = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
body = functions['write'].body
exclusive = [n for n in body if isinstance(n, ast.If) and isinstance(n.test, ast.Name) and n.test.id == 'exclusive']
require(len(exclusive) == 2, 'writer guard and publication branches')
publication = exclusive[1]
require(len(publication.body) == 2 and len(publication.orelse) == 1, 'absent-only branch shape')
require(ast.dump(publication.body[0].value.func) == ast.dump(ast.Attribute(value=ast.Name(id='os', ctx=ast.Load()), attr='link', ctx=ast.Load())), 'atomic link call')
require(ast.dump(publication.body[1].value.func) == ast.dump(ast.Attribute(value=ast.Name(id='temporary', ctx=ast.Load()), attr='unlink', ctx=ast.Load())), 'unlink only after success')
require(isinstance(publication.body[0].value, ast.Call) and [ast.dump(n) for n in publication.body[0].value.args] == [ast.dump(ast.Name(id='temporary', ctx=ast.Load())), ast.dump(ast.Name(id='path', ctx=ast.Load()))], 'link exact operands')
require([(k.arg, ast.dump(k.value)) for k in publication.body[0].value.keywords] == [('follow_symlinks', ast.dump(ast.Constant(value=False)))], 'link no-follow')
require(isinstance(publication.orelse[0].value, ast.Call) and isinstance(publication.orelse[0].value.func, ast.Attribute) and publication.orelse[0].value.func.attr == 'replace', 'replace only nonexclusive')
writer_text = ast.get_source_segment(guard_raw.decode(), functions['write'])
require(writer_text.index('stream.write(data)') < writer_text.index('stream.flush()') < writer_text.index('os.fsync(stream.fileno())') < writer_text.index('os.link(') < writer_text.index('temporary.unlink()'), 'completed fsynced file before publication')
require('A = HERE.parents[1]' in guard_raw.decode() and S.parents[1] == A and A.parents[2] == R, 'exact relocated audit/repository anchors')
gate_text = ast.get_source_segment(guard_raw.decode(), functions['gates'])
for expected in ["paths['reconciliation_capture'].name == 'CAPTURE.json'", "capture_names = ['CAPTURE.json', 'prelaunch_source.py', capture['stdout']['path'], capture['stderr']['path']]", 'PurePosixPath(name).name == name', 'len(set(capture_names)) == 4', 'exact_closure(cap_base, capture_names)', "type(capture['started_utc']) is str", "type(capture['finished_utc']) is str", "dt.datetime.fromisoformat(capture['started_utc'])", "dt.datetime.fromisoformat(capture['finished_utc'])", 'started.tzinfo is not None', 'finished.tzinfo is not None', 'started.utcoffset() == dt.timedelta(0)', 'finished.utcoffset() == dt.timedelta(0)', 'started <= finished']:
    require(expected in gate_text, 'missing complete gate ' + expected)
require(gate_text.index('len(set(capture_names)) == 4') < gate_text.index("for key in ['stdout', 'stderr']"), 'name validation before channel bind')
require(gate_text.index('started <= finished') < gate_text.index("capture['cwd']"), 'clock validation placement')
require(any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'revision_basis' for n in ast.walk(functions['immutable_basis'])), 'revision basis invoked')
static_tree = ast.parse(read(S, 'static_revision_checks.py'))
require(not any(isinstance(n, ast.ImportFrom) and n.module == 'pr39_guards' for n in ast.walk(static_tree)), 'static checker candidate import')
require(not any(isinstance(n, ast.Import) and any(z.name == 'pr39_guards' for z in n.names) for n in ast.walk(static_tree)), 'static checker candidate import')

# Independently authored finite predicates, never extracted candidate bodies.
def clock_ok(a, b):
    if type(a) is not str or type(b) is not str:
        return False
    try:
        s, e = dt.datetime.fromisoformat(a), dt.datetime.fromisoformat(b)
    except ValueError:
        return False
    return s.tzinfo is not None and e.tzinfo is not None and s.utcoffset() == dt.timedelta(0) and e.utcoffset() == dt.timedelta(0) and s <= e

clocks = [
    ('2026-10-02T13:00:00+00:00', '2026-10-02T14:00:00+00:00', True),
    ('2026-10-02T13:00:00+00:00', '2026-10-02T13:00:00+00:00', True),
    ('2026-10-02T13:00:00.000001+00:00', '2026-10-02T13:00:00.000002+00:00', True),
    ('banana', 'earlier', False),
    ('2026-10-02T14:00:00+00:00', '2026-10-02T13:00:00+00:00', False),
    ('2026-10-02T13:00:00', '2026-10-02T14:00:00', False),
    ('2026-10-02T13:00:00+01:00', '2026-10-02T14:00:00+01:00', False),
    ('2026-10-02T13:00:00-07:00', '2026-10-02T14:00:00-07:00', False),
    (True, '2026-10-02T14:00:00+00:00', False),
    ('2026-10-02T13:00:00+00:00', None, False),
    ('2026-10-02', '2026-10-03', False),
]
for a, b, wanted in clocks:
    require(clock_ok(a, b) is wanted, 'independent clock control')

def names_ok(cap, out, err):
    if cap != 'CAPTURE.json':
        return False
    names = [cap, 'prelaunch_source.py', out, err]
    try:
        for n in names:
            p = name(n)
            if p.name != n:
                return False
        return len(set(names)) == 4
    except (ValueError, TypeError):
        return False

channels = [
    ('CAPTURE.json', 'ROOTstdout.bin', 'stderr.bin', True),
    ('CAPTURE.json', 'explicit-output', 'explicit-error', True),
    ('CAPTURE.json', 'same', 'same', False),
    ('CAPTURE.json', 'prelaunch_source.py', 'stderr.bin', False),
    ('CAPTURE.json', 'stdout.bin', 'prelaunch_source.py', False),
    ('CAPTURE.json', 'CAPTURE.json', 'stderr.bin', False),
    ('CAPTURE.json', 'stdout.bin', 'CAPTURE.json', False),
    ('capture.json', 'stdout.bin', 'stderr.bin', False),
    ('nested/CAPTURE.json', 'stdout.bin', 'stderr.bin', False),
    ('CAPTURE.json', 'nested/stdout.bin', 'stderr.bin', False),
    ('CAPTURE.json', 'stdout.bin', '/stderr.bin', False),
    ('CAPTURE.json', './stdout.bin', 'stderr.bin', False),
    ('CAPTURE.json', 'stdout.bin', '../stderr.bin', False),
    ('CAPTURE.json', 'stdout.bin', 'stderr\\bin', False),
    ('CAPTURE.json', 'stdout.bin', 'stderr\0bin', False),
    ('CAPTURE.json', 'stdout.bin', '', False),
    ('CAPTURE.json', 'stdout.bin', [], False),
]
for cap, out, err, wanted in channels:
    require(names_ok(cap, out, err) is wanted, 'independent channel control')

# Private real syscall interleaving. These are literal own operations, not code
# extracted from the reviewed writer. No preexisting output is changed.
private = F / 'private_syscall_controls'
private.mkdir()
ours = b'own complete fsynced publication bytes\n'
foreign = b'other complete creator must survive\n'
def completed(n, raw):
    p = private / n
    with p.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    return p
collision_temp = completed('collision-completed.tmp', ours)
collision_final = completed('collision-foreign.final', foreign)
try:
    os.link(collision_temp, collision_final, follow_symlinks=False)
except FileExistsError:
    pass
else:
    raise ValueError('link overwrote existing final')
require(collision_final.read_bytes() == foreign and collision_temp.read_bytes() == ours, 'collision preservation')
success_temp = completed('success-completed.tmp', ours)
success_final = private / 'success.final'
os.link(success_temp, success_final, follow_symlinks=False)
require(success_temp.stat().st_ino == success_final.stat().st_ino and success_final.read_bytes() == ours, 'atomic absent publication')
success_temp.unlink()
require(not success_temp.exists() and success_final.read_bytes() == ours, 'remove temporary only after success')
owned_final = completed('nonexclusive-owned.final', b'old owned bytes\n')
owned_temp = completed('nonexclusive-completed.tmp', ours)
os.replace(owned_temp, owned_final)
require(owned_final.read_bytes() == ours and not owned_temp.exists(), 'explicit nonexclusive replacement')
fd = os.open(private, os.O_RDONLY)
try:
    os.fsync(fd)
finally:
    os.close(fd)

result = {
    'schema': 'pr39-revised-source-independent-static-controls/v1',
    'status': 'PASS_SOURCE_ONLY_STATIC_REVIEW_CONTROLS',
    'reviewed_helpers_imported_or_executed': False,
    'source_manifest_sha256': revision_manifest_sha,
    'full_helper_line_counts': helper_lines,
    'full_static_revision_checker_lines': len(read(S, 'static_revision_checks.py').decode().splitlines()),
    'entire_patch_reconstructed': True,
    'four_other_helpers_three_complete_objects_byte_unchanged': True,
    'old_original_and_static_closed_families_intact': True,
    'exact_closed_input_families': closure_results,
    'all_current_members': 2901,
    'all_dependencies': 2797,
    'exact_negative_inputs': 14,
    'valid_JSON_occurrences': valid_json_occurrences,
    'complete_immutable_references': 33,
    'new_unique_bound_file_union': len(SEEN),
    'new_unique_bound_file_union_bytes': sum(z['bytes'] for z in SEEN.values()),
    'aware_ordered_UTC_controls': len(clocks),
    'capture_names_controls': len(channels),
    'private_real_atomic_publication_controls': ['EEXIST preserves final and fsynced temp', 'absent link followed by temporary unlink', 'explicit nonexclusive replacement'],
    'false_draft_root_flags_and_null_preparation_digest': True,
    'original_ledger_dict_id9500008_count2_attempts12_byte_unchanged': True,
    'scientific_full_target_status': 'UNSOLVED',
    'scientific_discovery_percent': 0,
    'new_substantive_attempts': 0,
    'audit_turns': 0,
    'root_actual_execution_and_fresh_native13_protocol_still_required': True,
    'python_version': sys.version,
    'qualification': 'Independent own AST/data/finite predicates and private literal filesystem operations only; no candidate helper body evaluated, imported or executed. All live canonical/native/Git/remote administration belongs to root.'
}
print(json.dumps(result, indent=2, sort_keys=True))
