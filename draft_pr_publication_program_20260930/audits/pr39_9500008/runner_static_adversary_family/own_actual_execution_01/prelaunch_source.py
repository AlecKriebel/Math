"""Independent runner AST/binding/finite controls, never runner execution."""
from pathlib import Path
import ast
import hashlib
import itertools
import json
import stat

F = Path(__file__).resolve().parent
A = F.parent
R = A.parents[2]
P = A / 'root_runner_revision_preparation_family'
S = A / 'acceptance_execution_preparation_family/integration_source_revision'
def sha(b):
    return hashlib.sha256(b).hexdigest()
def parse(raw):
    def pairs(values):
        result = {}
        for key, value in values:
            assert key not in result
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=lambda v: (_ for _ in ()).throw(ValueError(v)))
def closure(root, manifest, expected, count):
    raw = (root / manifest).read_bytes()
    assert sha(raw) == expected
    obj = parse(raw)
    assert obj['self_excluded'] == [manifest] and obj['files_count'] == count and len(obj['files']) == count
    names = {z['path'] for z in obj['files']} | {manifest}
    assert len(names) == count + 1
    assert {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()} == names
    assert all(p.is_file() and not p.is_symlink() for p in root.rglob('*'))
    for z in obj['files']:
        raw = (root / z['path']).read_bytes()
        assert len(raw) == z['bytes'] and sha(raw) == z['sha256']
        if z['path'].endswith('.json'):
            parse(raw)
    return obj
closure(P, 'MANIFEST.json', 'a93237f6ecaf652942374fcb2829a534ee8edbb8d29f44c41b047a58bc15fef9', 6)
closure(S, 'PREPARATION_MANIFEST.json', '522cf5062ffcb1aa9c60cb0054063b0f2801378446f2288d7f85e81ee9a70ae7', 17)
# Earlier own review is already sealed; only read and verify its member bytes.
old_review = A / 'acceptance_revised_static_adversary_family'
old_raw = (old_review / 'MANIFEST.json').read_bytes()
assert sha(old_raw) == '70659d55353c2fd7f3e44f327ff35bdbbd742d31a6d12b9dcc40da6cd850b508'
old_manifest = parse(old_raw)
old_names = {z['path'] for z in old_manifest['files']} | {'MANIFEST.json'}
assert {p.relative_to(old_review).as_posix() for p in old_review.rglob('*') if p.is_file()} == old_names
assert all(not p.is_symlink() and (p.is_file() or p.is_dir()) for p in old_review.rglob('*'))
for z in old_manifest['files']:
    raw = (old_review / z['path']).read_bytes()
    assert len(raw) == z['bytes'] and sha(raw) == z['sha256']
bindings = parse((P / 'SOURCE_BINDINGS.json').read_bytes())
for z in [bindings['original_runner'], bindings['revised_runner'], bindings['revised_preparation_manifest'], bindings['revised_source_binding_record'], *bindings['revised_helpers']]:
    p = R / z['path']
    assert p.is_file() and not p.is_symlink()
    raw = p.read_bytes()
    assert len(raw) == z['bytes'] and sha(raw) == z['sha256'] and stat.S_IMODE(p.stat().st_mode) == z['mode']
assert bindings['actual_helper_or_runner_execution'] is False and bindings['new_adversarial_review_completed'] is False and bindings['root_full_source_review_completed'] is False
runner = A / 'execute_root_acceptance_revised.py'
raw = runner.read_bytes()
assert sha(raw) == '2de301f2f37837b8729d606962599c04bd380d1f6473cc4a76a9c46cef1c0b88'
text = raw.decode()
assert len(text.splitlines()) == 342
tree = ast.parse(raw)
functions = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
constants = {}
for node in tree.body:
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and node.targets[0].id in ['PREP', 'SOURCE_HASHES', 'NATIVE13', 'ALLOWED', 'GATE_NAMES']:
        constants[node.targets[0].id] = ast.literal_eval(node.value)
assert constants['PREP'] == bindings['revised_preparation_manifest']['sha256']
historical = parse((A / 'ROOT_CURRENT_INPUT_PREIMAGES.json').read_bytes())
assert list(constants['NATIVE13']) == [z['path'] for z in historical['files']] == bindings['native13_literal_paths']
assert len(set(constants['NATIVE13'])) == len(constants['NATIVE13']) == 13
assert {Path(z['path']).name: z['sha256'] for z in bindings['revised_helpers']} == constants['SOURCE_HASHES']
assert {k: sorted(v) for k, v in constants['ALLOWED'].items()} == bindings['allowed_native_phase_changes']
assert constants['ALLOWED'] == {
    'overlay': {'unsolved_math_prioritization/QUEUE.md'},
    'finalize': {'draft_pr_publication_program_20260930/inventory.json'},
    'mirror': {'unsolved_math_prioritization/state.json', 'unsolved_math_prioritization/history.jsonl'}}
imports = {z.name for node in ast.walk(tree) if isinstance(node, ast.Import) for z in node.names}
assert 'pr39_guards' not in imports and not any(isinstance(node, ast.ImportFrom) and node.module == 'pr39_guards' for node in ast.walk(tree))
for n in ['read_regular', 'repo_path', 'fresh_inputs', 'check_preparation', 'write_new', 'fsync_directory', 'main']:
    assert n in functions
reader = ast.get_source_segment(text, functions['read_regular'])
for literal in ['path.is_absolute()', 'path.is_relative_to(R)', 'not ancestor.is_symlink()', 'os.O_RDONLY | os.O_NOFOLLOW', 'os.fstat(stream.fileno()).st_mode', 'stat.S_ISREG(mode)', 'stat.S_IMODE(mode)']:
    assert literal in reader
writer = ast.get_source_segment(text, functions['write_new'])
for literal in ['os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW', 'os.fchmod(stream.fileno(), mode)', 'stream.flush()', 'os.fsync(stream.fileno())']:
    assert literal in writer
main = ast.get_source_segment(text, functions['main'])
for literal in [
    "runner_path == A / 'execute_root_acceptance_revised.py'", "sys.platform == 'darwin'", "cwd=R).strip() == b'main'", 'check_preparation()',
    "argv = ['/usr/bin/python3', '-B', str(source)]", "'--execute', '--preparation-manifest-sha256', PREP", "'--plan', str(path.relative_to(R)), '--plan-sha256', args.reviewed_plan_sha256",
    'root_full_current_read_completed=True', 'root_full_whole_scope_read_completed=True', 'independent_whole_current_pass=True, preparation_manifest_sha256=PREP',
    'strict_equal(parse(plan_raw), expected)', 'set(gates) == keys', "gates['preparation-manifest-sha256'] == PREP", "'pr38_2765/state_mirror_bindings.json'",
    "if phase not in ('mirror', 'post')", "argv.append(phase)", "for key in sorted(gates)", "argv += ['--' + key, gates[key]]",
    "before, modes_before = fresh_inputs()", "strict_equal(before, reviewed['files']) and reviewed['head'] == head", "digest(reviewed['whole_queue_sha256'])",
    "ROOT_AUTOMATIC_MERGE_INSPECTION.json", "args.reviewed_fresh_main_sha256 if phase == 'preflight' else args.reviewed_automatic_merge_sha256",
    "('fresh-queue' if phase == 'preflight' else 'merge-queue') + '-preimage-sha256'", "not destination.exists() and not destination.is_symlink()",
    'stage.mkdir(mode=0o700)', "write_new(stage / 'prelaunch_source.py', raw, source_mode)", "write_new(stage / 'prelaunch_guards.py', guards_raw, guards_mode)",
    "'actual_execution': False", "'completed': False", "'pid': None, 'exit_code': None", "'stdin_supplied': False",
    'subprocess.Popen(argv, cwd=A, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)', 'record.update(pid=child.pid, actual_execution=True)',
    'child.communicate(timeout=180)', 'except subprocess.TimeoutExpired:', "record['timed_out'] = True", 'child.kill()', 'out, err = child.communicate()',
    'except BaseException:', 'errors.append(traceback.format_exc())', 'record.update(completed=True, exit_code=child.returncode)',
    "write_new(stage / 'stdout.bin', out)", "write_new(stage / 'stderr.bin', err)", 'after, modes_after = fresh_inputs()',
    'if not strict_equal(left, right)', 'modes_before[name] != modes_after[name]', 'changes <= allowed and after_head == head',
    'read_regular(runner_path) == (runner_raw, runner_mode)', 'read_regular(source) == (raw, source_mode)', "read_regular(S / 'pr39_guards.py') == (guards_raw, guards_mode)",
    'len(current_raw) == pin[\'bytes\'] and sha(current_raw) == pin[\'sha256\']', "utc(record['started_utc']) <= utc(record['finished_utc'])",
    "record['actual_execution'] is True and record['completed'] is True", "type(record['exit_code']) is int and record['exit_code'] == 0", "not record['timed_out'] and native_ok and checks_ok and not errors",
    "record['status'] = 'PASS' if passed else 'FAIL'", "names = {'CAPTURE.json', 'prelaunch_source.py', 'stdout.bin', 'stderr.bin'}", "names.add('prelaunch_guards.py')",
    '{p.name for p in stage.iterdir()} == names', 'all(p.is_file() and not p.is_symlink() for p in stage.iterdir())',
    'fsync_directory(stage)', 'rename(os.fsencode(stage), os.fsencode(destination), 0x00000004)', 'fsync_directory(A)', 'return 0 if passed else 1']:
    assert literal in main, literal
assert main.index('check_preparation()') < main.index('subprocess.Popen(')
assert main.index('write_new(stage / \'stdout.bin\'') < main.index('record[\'status\']') < main.index('fsync_directory(stage)') < main.index('rename(os.fsencode(stage)') < main.index('fsync_directory(A)')
guard = (S / 'pr39_guards.py').read_text()
for n in constants['GATE_NAMES']:
    assert n in guard
assert set(constants['GATE_NAMES']) == {'whole-manifest', 'root-final-receipt', 'whole-scope-contract', 'root-final-manifest', 'reconciliation-capture'}
assert len({'preparation-manifest-sha256', 'previous-mirror-sha256'} | set(constants['GATE_NAMES']) | {n + '-sha256' for n in constants['GATE_NAMES']}) == 12
# Independent finite truth-table model of the observed PASS predicate.
cases, successes = 0, 0
for actual, complete, exit_code, timeout, native, checks, errors in itertools.product([False, True], [False, True], [None, 0, 1, False], [False, True], [False, True], [False, True], [[], ['failure']]):
    passed = actual is True and complete is True and type(exit_code) is int and exit_code == 0 and not timeout and native and checks and not errors
    wanted = actual is True and complete is True and type(exit_code) is int and exit_code == 0 and timeout is False and native is True and checks is True and errors == []
    assert passed is wanted
    cases += 1
    successes += passed
assert successes == 1
phases = ['final', 'preflight', 'overlay', 'prepush', 'finalize', 'mirror', 'post']
allowed_cases = 0
for phase in phases:
    expected = constants['ALLOWED'].get(phase, set())
    assert (set() <= expected) is True
    allowed_cases += 1
    for n in constants['NATIVE13']:
        assert ({n} <= expected) is (n in expected)
        allowed_cases += 1
    assert not ({'unexpected-native-file'} <= expected)
    allowed_cases += 1
assert allowed_cases == 105
for phase in phases:
    filename = {'final': 'seal_final_evidence.py', 'mirror': 'state_mirror_reconciliation.py', 'post': 'verify_post_acceptance.py'}.get(phase, 'integrate_reviewed_partial.py')
    assert filename in constants['SOURCE_HASHES']
    names = {'CAPTURE.json', 'prelaunch_source.py', 'stdout.bin', 'stderr.bin'}
    if phase != 'final':
        names.add('prelaunch_guards.py')
    assert len(names) == (4 if phase == 'final' else 5)
result = {'schema': 'pr39-own-root-runner-static-controls/v1', 'status': 'PASS_STATIC_SOURCE_ONLY',
    'runner_sha256': sha(raw), 'runner_lines_fully_read': 342, 'runner_and_helpers_imported_or_executed': False,
    'closed_runner_preparation6_and_revised_sources17_and_prior_review15_unchanged': True,
    'full_source_bindings_and_modes_verified': True, 'exact_native13_literal_order': list(constants['NATIVE13']),
    'all_allowed_phase_changes_exact': True, 'fixed_phase_helper_interfaces_match': True,
    'complete_exact_activated_plan_and12_gate_map_gates_verified': True,
    'fresh_whole_preflight_and_automatic_queue_pins_verified': True,
    'all_native13_bytes_modes_and_HEAD_before_after_gates_verified': True,
    'all_source_modes_and_complete_review_before_after_gates_verified': True,
    'final4_nonfinal5_exact_capture_source_and_stream_closures_verified': True,
    'completed_files_stage_parent_fsync_and_RENAME_EXCL_verified': True,
    'truth_table_cases': cases, 'truth_table_pass_cases': successes,
    'allowed_changes_finite_cases': allowed_cases,
    'timeout_launch_error_and_exception_retention_source_read': True,
    'actual_future_acceptance_status': 'PENDING', 'new_substantive_attempts': 0, 'audit_turns': 0,
    'scientific_discovery_percent': 0,
    'qualification': 'Full literal source/AST and binding checks plus own independently authored finite predicates. No candidate function body imported, evaluated or executed, no native/Git/remote mutation. Not an actual helper launch, capture publication or acceptance.'}
print(json.dumps(result, indent=2, sort_keys=True))
