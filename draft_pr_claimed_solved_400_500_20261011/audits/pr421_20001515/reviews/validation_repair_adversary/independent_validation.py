#!/usr/bin/env python3
"""Independent sealed PR421 validation audit. No repair-generator code is used.

All raw sources, generated/mutated fixtures and subprocess capture files stay in
private_sources/validation_repair_adversary. Public JSON records exact observed
stdout/stderr, exception metadata, byte hashes and comparisons.
"""
import ast
import builtins
import copy
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

PUBLIC = Path(__file__).resolve().parent
CASE = PUBLIC.parent.parent
SOURCE = CASE / 'source_snapshot/unsolved_math_prioritization/attempts/20001515'
CANDIDATE = CASE / 'reviews/reproduction_adversary/overlay'
PRIVATE = CASE / 'private_sources/validation_repair_adversary'
PROGRAMS = ['verify.py', 'audit/independent_audit.py', 'audit/independent_algebra.py']
COUNTS = dict(zip(PROGRAMS, [34, 24, 4]))
EXPECTED_OUTPUT = dict(zip(PROGRAMS, ['checks.json', 'audit/independent_results.json', 'audit/independent_algebra_results.json']))
EXPECTED_CANDIDATES = dict(zip(PROGRAMS, [
    'e3357a9af58d68c2f450d2901ab71c58ed955112017fe0ec758d1adc3b36ca42',
    '281ebf97900d047447a2a3865f233cfba1c41df6dd6c4e8aaae66150250b1903',
    '3fda0f889aa454390c6f30c54c842a0a49a5f5a3d1bdea0bce5819711e3dbc96']))

def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(data):
    return hashlib.sha256(data).hexdigest()

def require(condition, label):
    if not condition:
        raise RuntimeError(label)

def write(name, value):
    (PUBLIC / name).write_text(json.dumps(value, indent=2) + '\n')

def dump(node):
    return ast.dump(node, include_attributes=False)

def typed(value):
    if isinstance(value, dict):
        return {'type': 'dict', 'items': [[typed(k), typed(v)] for k, v in value.items()]}
    if isinstance(value, (tuple, list)):
        return {'type': type(value).__name__, 'items': [typed(v) for v in value]}
    return {'type': type(value).__name__, 'value': value}

def checkpoint(message, percent):
    with (PUBLIC / 'RESEARCH_LOG.md').open('a') as f:
        f.write(f'- {utc()}: {message} Estimated validation-audit completion:{percent}%. Author proof budget1/5; new attempts0.\n')

def compare_node(original, candidate, location, gates):
    """Correspondence established from original structure, independently of generation.

    Return a reconstruction made from candidate children. Every original assert
    must align with exactly one exact candidate if-not/raise shape; every other
    node field is compared recursively, including statements and constants.
    """
    if isinstance(original, ast.Assert):
        require(isinstance(candidate, ast.If), f'{location}: replacement is not If')
        require(isinstance(candidate.test, ast.UnaryOp) and isinstance(candidate.test.op, ast.Not), f'{location}: wrong negation')
        require(dump(original.test) == dump(candidate.test.operand), f'{location}: changed test')
        require(candidate.orelse == [] and len(candidate.body) == 1, f'{location}: wrong branch body/else')
        raised = candidate.body[0]
        require(isinstance(raised, ast.Raise) and raised.cause is None, f'{location}: wrong Raise/cause')
        require(isinstance(raised.exc, ast.Call), f'{location}: exception not instantiated')
        require(isinstance(raised.exc.func, ast.Name) and raised.exc.func.id == 'AssertionError' and isinstance(raised.exc.func.ctx, ast.Load), f'{location}: wrong exception name')
        require(not raised.exc.keywords, f'{location}: exception keywords')
        wanted = [] if original.msg is None else [original.msg]
        require(len(wanted) == len(raised.exc.args), f'{location}: wrong exception arg count')
        for a, b in zip(wanted, raised.exc.args):
            require(dump(a) == dump(b), f'{location}: changed lazy message')
        gates.append({'path': location, 'original_line': original.lineno, 'original_column': original.col_offset,
                      'candidate_line': candidate.lineno, 'candidate_column': candidate.col_offset,
                      'test_ast': dump(original.test), 'message_ast': None if original.msg is None else dump(original.msg),
                      'original_assert': ast.unparse(original), 'candidate_gate': ast.unparse(candidate)})
        return ast.Assert(test=copy.deepcopy(candidate.test.operand), msg=copy.deepcopy(raised.exc.args[0]) if wanted else None)
    require(type(original) is type(candidate), f'{location}: node type {type(original).__name__} != {type(candidate).__name__}')
    if isinstance(original, ast.AST):
        require(original._fields == candidate._fields, f'{location}: fields differ')
        restored = copy.copy(candidate)
        for field in original._fields:
            setattr(restored, field, compare_node(getattr(original, field), getattr(candidate, field), location + '.' + field, gates))
        return restored
    if isinstance(original, list):
        require(len(original) == len(candidate), f'{location}: list length changed')
        return [compare_node(a, b, f'{location}[{i}]', gates) for i, (a, b) in enumerate(zip(original, candidate))]
    require(original == candidate, f'{location}: changed scalar {original!r} != {candidate!r}')
    return candidate

def static_checks():
    receipt = json.loads((CASE / 'SOURCE_RECEIPT.json').read_bytes())
    require(receipt['head_sha'] == 'd5bf8b5a25cabb177433338fae60af52ebfecf1c', 'source HEAD')
    source_pins = []
    for item in receipt['files']:
        data = (CASE / 'source_snapshot' / item['path']).read_bytes()
        good = len(data) == item['bytes'] and sha(data) == item['sha256']
        require(good, 'source pin ' + item['path'])
        source_pins.append({**item, 'matched': good})
    require(len(source_pins) == 13, 'source receipt must bind13 files')
    seal = CASE / 'reviews/reproduction_adversary/CANDIDATE_SEAL.json'
    require(sha(seal.read_bytes()) == '8cb14cc0d1e88c4ad48158004e8b90c8b144b326c24e25f35fe4722b44cd90dd', 'candidate seal hash')
    results = []
    global GATES
    GATES = {}
    for program in PROGRAMS:
        old = ast.parse((SOURCE / program).read_bytes())
        new = ast.parse((CANDIDATE / program).read_bytes())
        require(sha((CANDIDATE / program).read_bytes()) == EXPECTED_CANDIDATES[program], 'candidate pin ' + program)
        gates = []
        reconstructed = compare_node(old, new, 'Module', gates)
        require(dump(reconstructed) == dump(old), 'whole reconstructed AST ' + program)
        require(len(gates) == COUNTS[program], 'assert count ' + program)
        require(not any(isinstance(n, ast.Assert) for n in ast.walk(new)), 'candidate retains assert ' + program)
        bindings = [ast.unparse(n) for n in ast.walk(new) if isinstance(n, ast.Name) and n.id == 'AssertionError' and isinstance(n.ctx, (ast.Store, ast.Del))]
        require(not bindings, 'candidate shadows AssertionError ' + program)
        import_bindings = [ast.unparse(n) for n in ast.walk(new) if isinstance(n, (ast.Import, ast.ImportFrom)) and any((a.asname or a.name.split('.')[0]) == 'AssertionError' for a in n.names)]
        require(not import_bindings, 'candidate imports shadow AssertionError ' + program)
        GATES[program] = sorted(gates, key=lambda g: (g['original_line'], g['original_column']))
        results.append({'program': program, 'original_sha256': sha((SOURCE / program).read_bytes()),
                        'candidate_sha256': sha((CANDIDATE / program).read_bytes()), 'asserts': len(gates),
                        'whole_nonvalidation_AST_unchanged': True, 'tests_and_messages_AST_identical': True,
                        'AssertionError_store_or_import_bindings': bindings + import_bindings, 'gates': GATES[program]})
    write('STATIC_CHECKS.json', {'checked_at_utc': utc(), 'source_head': receipt['head_sha'], 'source_pins': source_pins,
                               'candidate_seal_sha256': sha(seal.read_bytes()), 'total_gates': sum(COUNTS.values()), 'programs': results})
    checkpoint('All13 frozen source pins and three candidate pins verified. Independent recursive alignment reconstructs exactly62 gates (34/24/4); restored entire AST equals originals, including all test/message and non-validation fields.', 30)

def fixture(label, version, program, mutation=None, proof_corruption=False):
    base = PRIVATE / 'runs' / label / version
    if base.exists():
        shutil.rmtree(base)
    shutil.copytree(SOURCE, base)
    deleted = []
    for name in EXPECTED_OUTPUT.values():
        p = base / name
        if p.exists():
            p.unlink()
            deleted.append(name)
    if version == 'candidate':
        for name in PROGRAMS:
            shutil.copyfile(CANDIDATE / name, base / name)
    p = base / program
    if mutation:
        tree = ast.parse(p.read_bytes())
        mutation(tree, version)
        p.write_text(ast.unparse(ast.fix_missing_locations(tree)) + '\n')
    if proof_corruption:
        with (base / 'ATTEMPT_1.md').open('ab') as f:
            f.write(b'\nValidation-audit private changed-byte control.\n')
    return base, p, deleted

def launch(base, p, optimized, seed, wrapper=False, namespace_shadow=False):
    flags = ['-O'] if optimized else []
    cmd = [sys.executable, *flags]
    capture = base / 'exception_capture.json'
    if wrapper:
        cmd += [str(PRIVATE / 'capture_exception.py'), str(p), str(capture), 'shadow' if namespace_shadow else 'plain']
    else:
        cmd += [str(p)]
    env = os.environ.copy()
    env['PYTHONHASHSEED'] = str(seed)
    env.pop('PYTHONOPTIMIZE', None)
    completed = subprocess.run(cmd, cwd=PRIVATE, env=env, capture_output=True, timeout=30)
    result = {'command': cmd, 'cwd': str(PRIVATE), 'pythonhashseed': seed, 'optimized': optimized,
              'returncode': completed.returncode, 'stdout': completed.stdout.decode(), 'stderr': completed.stderr.decode(),
              'stdout_sha256': sha(completed.stdout), 'stderr_sha256': sha(completed.stderr),
              'executed_script_sha256': sha(p.read_bytes()), 'proof_sha256_after': sha((base / 'ATTEMPT_1.md').read_bytes())}
    if wrapper:
        require(capture.exists(), 'exception wrapper output missing')
        result['capture'] = json.loads(capture.read_bytes())
    return result

def baseline_checks():
    expected = {n: (SOURCE / EXPECTED_OUTPUT[n]).read_bytes() for n in PROGRAMS}
    require(list(json.loads(expected['audit/independent_audit.py'])) != list(json.loads(expected['verify.py'])), 'distinct expected artifacts')
    results = []
    for program in PROGRAMS:
        wanted = json.loads(expected[program])
        shorter = wanted if program != 'audit/independent_audit.py' else {k: wanted[k] for k in ['status', 'frozen_proof_hash_matches', 'Z_link_f_vector', 'Z_all_cliques_by_size', 'negative_controls', 'cell_f_vector']}
        for seed in [0, 1, 42]:
            normal_original_stdout = None
            for version in ['original', 'candidate']:
                for optimized in [False, True]:
                    label = f'baseline_{PROGRAMS.index(program)}_{seed}_{int(optimized)}'
                    base, p, deleted = fixture(label, version, program)
                    r = launch(base, p, optimized, seed)
                    r.update(program=program, version=version, deleted_stale_outputs=deleted)
                    require(r['returncode'] == 0 and r['stderr'] == '', 'baseline execution failure')
                    require(json.loads(r['stdout']) == shorter, 'baseline stdout JSON mismatch')
                    if version == 'original' and not optimized:
                        normal_original_stdout = r['stdout']
                    require(r['stdout'] == normal_original_stdout, 'stdout bytes changed vs original normal')
                    target = base / EXPECTED_OUTPUT[program]
                    r['stdout_matches_correct_expected_JSON'] = True
                    r['stdout_matches_original_normal_bytes'] = True
                    if program == 'verify.py':
                        require(not target.exists(), 'author unexpectedly writes checks.json')
                        require(r['stdout'].encode() == expected[program], 'author stdout bytes differ frozen checks.json')
                        r['generated_output_absent_as_expected'] = True
                    else:
                        require(target.exists(), 'generated artifact missing')
                        actual = target.read_bytes()
                        require(actual == expected[program], 'full generated artifact bytes mismatch')
                        r['generated_artifact'] = {'path': EXPECTED_OUTPUT[program], 'bytes': len(actual), 'sha256': sha(actual), 'full_JSON_matches_frozen': True, 'bytes_match_frozen': True}
                    require(r['proof_sha256_after'] == 'c022afdfe003d0692a032cee48855ddf712de22953b358b895c485215875d8a6', 'proof bytes changed')
                    results.append(r)
    write('FRESH_BASELINES.json', {'checked_at_utc': utc(), 'runtime': sys.version, 'sys_executable': sys.executable,
                                 'expected_artifact_pins': {p: {'path': EXPECTED_OUTPUT[p], 'sha256': sha(v), 'bytes': len(v)} for p, v in expected.items()},
                                 'runs': results, 'all_passed': True})
    checkpoint('36 fresh direct subprocess baselines succeeded across original/candidate, normal/-O, and hash seeds0/1/42. Stale outputs deleted; author only prints checks.json; geometry full file and shorter stdout distinguished; algebra full file/stdout identical to frozen expected bytes; proof bytes unchanged.', 50)

def force_gate(program, index):
    gate = GATES[program][index]
    def change(tree, version):
        line = gate[version + '_line']
        column = gate[version + '_column']
        matches = [n for n in ast.walk(tree) if getattr(n, 'lineno', -1) == line and getattr(n, 'col_offset', -1) == column and isinstance(n, ast.Assert if version == 'original' else ast.If)]
        require(len(matches) == 1, 'forced gate location ambiguous')
        node = matches[0]
        if version == 'original':
            node.test = ast.Constant(False)
        else:
            node.test.operand = ast.Constant(False)
    return change

def gate_checks():
    results = []
    for program in PROGRAMS:
        for index, gate in enumerate(GATES[program]):
            runset = []
            expected = None
            for version in ['original', 'candidate']:
                for optimized in [False, True]:
                    base, p, deleted = fixture(f'gate_{PROGRAMS.index(program)}_{index}_{int(optimized)}', version, program, force_gate(program, index))
                    r = launch(base, p, optimized, 0, wrapper=True)
                    r.update(version=version, deleted_stale_outputs=deleted)
                    capture = r['capture']
                    if version == 'original' and not optimized:
                        require(capture['exception_type'] == 'builtins.AssertionError', 'original false gate not AssertionError')
                        expected = capture['args_typed']
                    if version == 'original' and optimized:
                        require(capture['exception_type'] is None, 'original optimized forced assert should be deleted')
                    else:
                        require(capture['exception_type'] == 'builtins.AssertionError' and capture['args_typed'] == expected, 'candidate false gate type/args mismatch')
                        require(r['stdout'] == '', 'false gate reached success stdout')
                    runset.append(r)
            results.append({'program': program, 'gate_index': index, 'original_line': gate['original_line'], 'candidate_line': gate['candidate_line'],
                            'matches_original_normal_type_and_typed_args': True, 'runs': runset})
    write('ALL_GATE_FAILURES.json', {'checked_at_utc': utc(), 'gates_tested': len(results), 'subprocess_runs': len(results) * 4, 'all_passed': True, 'gates': results})
    checkpoint('Every one of62 original gates was independently forced false in private copies.248 subprocess runs verify original normal and candidate normal/-O raise builtin AssertionError with identical typed .args; original -O deletes each historical assert and reaches success.', 70)

def assign(name, value):
    def mutate(tree, version):
        nodes = [n for n in ast.walk(tree) if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in n.targets)]
        require(len(nodes) == 1, 'mutation assignment uniqueness ' + name)
        nodes[0].value = ast.parse(value, mode='eval').body
    return mutate

def geometry_lambda(tree, version):
    fn = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'lamb']
    require(len(fn) == 1, 'geometry lamb uniqueness')
    returns = [n for n in ast.walk(fn[0]) if isinstance(n, ast.Return)]
    require(len(returns) == 1, 'geometry lamb return uniqueness')
    returns[0].value = ast.parse("{'x':('y',s),'y':('x',s),'b':('b',s)}[e]", mode='eval').body

def vertical_B(tree, version):
    nodes = [n for n in ast.walk(tree) if isinstance(n, ast.Assign) and any(isinstance(t, ast.Subscript) and isinstance(t.value, ast.Name) and t.value.id == 'zv' and isinstance(t.slice, ast.Constant) and t.slice.value == 'B' for t in n.targets)]
    require(len(nodes) == 1, 'vertical B uniqueness')
    nodes[0].value = ast.parse('prod(x,z,y)', mode='eval').body

def mutation_checks():
    specs = [
        ('author_duplicate_K_square', PROGRAMS[0], assign('K_FACES', '[(1,2,-1,-2),(1,2,-1,-2)]'), False, 'Duplicates a genuine square and its link corners.'),
        ('author_nonclosed_Q_square', PROGRAMS[0], assign('Q_FACES', '[(1,2,-3,4),(5,1,-6,-2)]'), False, 'Changes one edge orientation so first Q square is not closed.'),
        ('geometry_b_sign', PROGRAMS[1], geometry_lambda, False, 'Changes geometric lambda(b)=b^-1 to lambda(b)=b.'),
        ('geometry_omitted_cube_corner', PROGRAMS[1], assign('ztri', 'set(tri_counts)-{sorted(tri_counts,key=lambda t:sorted(t))[0]}'), False, 'Deletes one actual reconstructed cube corner triangle before flag validation.'),
        ('geometry_wrong_cube_side', PROGRAMS[1], assign('side', '[l,vertical(v),inv(lamb(l)),vertical(u)]'), False, 'Changes cube side terminal vertical sign; side no longer matches product square.'),
        ('geometry_changed_proof_byte', PROGRAMS[1], None, True, 'Appends bytes to copied ATTEMPT_1.md while leaving validator unchanged.'),
        ('algebra_inverse_monodromy', PROGRAMS[2], assign('psi', "{'a':'a','b':'Ab','c':'BacB'}"), False, 'Removes terminal a from proposed inverse monodromy image of c.'),
        ('algebra_b_sign', PROGRAMS[2], assign('lam', "{'x':y,'y':x,'b':b}"), False, 'Changes algebraic lambda(b) from inverse(b) to b.'),
        ('algebra_vertical_generator', PROGRAMS[2], vertical_B, False, 'Changes z_B=x z y^-1 to x z y.'),
        ('algebra_stable_letter_sign', PROGRAMS[2], assign('z', 'prod(inverse(c),t)'), False, 'Changes z=c^-1 t^-1 to c^-1 t.'),
    ]
    records = []
    for label, program, mutation, proof_bad, purpose in specs:
        runs = []
        wanted = None
        for version in ['original', 'candidate']:
            for optimized in [False, True]:
                base, p, deleted = fixture(label + '_' + str(int(optimized)), version, program, mutation, proof_bad)
                r = launch(base, p, optimized, 0, wrapper=True)
                r.update(version=version, deleted_stale_outputs=deleted)
                if version == 'original' and not optimized:
                    require(r['capture']['exception_type'] == 'builtins.AssertionError', label + ': original normal wrong rejection')
                    wanted = r['capture']['args_typed']
                if version == 'original' and optimized:
                    require(r['capture']['exception_type'] is None, label + ': optimized original has non-gate runtime failure')
                    require(json.loads(r['stdout'])['status'].startswith('PASS'), label + ': old optimized bypass not observed')
                else:
                    require(r['capture']['exception_type'] == 'builtins.AssertionError' and r['capture']['args_typed'] == wanted, label + ': repaired type/args mismatch')
                    require(r['stdout'] == '', label + ': invalid candidate reaches success output')
                generated = base / EXPECTED_OUTPUT[program]
                r['generated_artifact_exists_after'] = generated.exists()
                if generated.exists():
                    r['generated_artifact_sha256'] = sha(generated.read_bytes())
                    r['generated_artifact_exact_text'] = generated.read_text()
                runs.append(r)
        records.append({'mutation': label, 'program': program, 'purpose': purpose, 'normal_original_and_both_candidate_modes_reject_with_identical_type_args': True,
                        'original_optimized_publishes_PASS_despite_corruption': True, 'runs': runs})
    write('MEANINGFUL_CORRUPTIONS.json', {'checked_at_utc': utc(), 'controls': len(records), 'runs': len(records) * 4, 'all_passed': True, 'controls_detail': records})
    checkpoint('Ten meaningful controls (two author, four geometry including changed proof bytes, four algebra) rejected as AssertionError with unchanged typed args in repaired normal/-O. All corresponding original -O runs publish PASS; no syntax/import failure is used as evidence.', 85)

def outcome(node, optimized, case):
    events = []
    class Truth:
        def __init__(self, value):
            self.value = value
        def __bool__(self):
            events.append('bool')
            return self.value
    def test():
        events.append('test')
        if case == 'test_raises':
            raise LookupError('test sentinel')
        return Truth(case in ['truth_custom', 'message_raises_on_truth']) if case in ['truth_custom', 'false_custom', 'message_raises_on_truth'] else case in ['truth', 'message_raises_on_truth']
    def message():
        events.append('message')
        if case in ['message_raises_on_truth', 'message_raises_on_false']:
            raise ValueError('message sentinel')
        return ('tuple payload', {'nested': [3, 'x']})
    def left_false():
        events.append('left_false')
        return False
    def left_true():
        events.append('left_true')
        return True
    def bomb():
        events.append('bomb')
        raise RuntimeError('should be short circuited')
    def right():
        events.append('right')
        return True
    tests = {'and_false': '_left_false() and _bomb()', 'or_true': '_left_true() or _bomb()', 'and_true': '_left_true() and _right()'}
    expr = ast.parse(tests.get(case, '_test()'), mode='eval').body
    selected = copy.deepcopy(node)
    if isinstance(selected, ast.Assert):
        selected.test = expr
        if selected.msg is not None:
            selected.msg = ast.Call(func=ast.Name(id='_message', ctx=ast.Load()), args=[], keywords=[])
    else:
        selected.test.operand = expr
        if selected.body[0].exc.args:
            selected.body[0].exc.args[0] = ast.Call(func=ast.Name(id='_message', ctx=ast.Load()), args=[], keywords=[])
    namespace = {'_test': test, '_message': message, '_left_false': left_false, '_left_true': left_true, '_bomb': bomb, '_right': right}
    try:
        exec(compile(ast.fix_missing_locations(ast.Module(body=[selected], type_ignores=[])), '<isolated exact gate shape>', 'exec', optimize=2 if optimized else 0), namespace)
        kind, args = None, None
    except BaseException as e:
        kind, args = type(e).__module__ + '.' + type(e).__qualname__, typed(e.args)
    return {'events': events, 'exception_type': kind, 'args_typed': args}

def semantics_checks():
    records = []
    cases = ['truth', 'false', 'truth_custom', 'false_custom', 'test_raises', 'message_raises_on_truth', 'message_raises_on_false', 'and_false', 'or_true', 'and_true']
    for program in PROGRAMS:
        original = ast.parse((SOURCE / program).read_bytes())
        candidate = ast.parse((CANDIDATE / program).read_bytes())
        for index, gate in enumerate(GATES[program]):
            old = next(n for n in ast.walk(original) if isinstance(n, ast.Assert) and n.lineno == gate['original_line'] and n.col_offset == gate['original_column'])
            new = next(n for n in ast.walk(candidate) if isinstance(n, ast.If) and n.lineno == gate['candidate_line'] and n.col_offset == gate['candidate_column'])
            for case in cases:
                wanted = outcome(old, False, case)
                actual = [outcome(new, False, case), outcome(new, True, case)]
                require(actual[0] == wanted and actual[1] == wanted, 'lazy/short-circuit semantics differ')
                records.append({'program': program, 'gate_index': index, 'case': case, 'original_normal': wanted, 'candidate_normal': actual[0], 'candidate_optimized': actual[1]})
    boundaries = []
    for program in PROGRAMS:
        old = next(n for n in ast.walk(ast.parse((SOURCE / program).read_bytes())) if isinstance(n, ast.Assert) and n.msg is None)
        g = next(g for g in GATES[program] if g['original_line'] == old.lineno and g['original_column'] == old.col_offset)
        new = next(n for n in ast.walk(ast.parse((CANDIDATE / program).read_bytes())) if isinstance(n, ast.If) and n.lineno == g['candidate_line'] and n.col_offset == g['candidate_column'])
        o = copy.deepcopy(old); o.test = ast.Constant(False)
        c = copy.deepcopy(new); c.test.operand = ast.Constant(False)
        observed = []
        for name, node in [('original', o), ('candidate', c)]:
            try:
                exec(compile(ast.fix_missing_locations(ast.Module(body=[node], type_ignores=[])), '<namespace-shadow boundary>', 'exec', optimize=0), {'AssertionError': RuntimeError})
            except BaseException as e:
                observed.append({'version': name, 'exception_type': type(e).__module__ + '.' + type(e).__qualname__, 'args_typed': typed(e.args)})
        require(observed[0]['exception_type'] == 'builtins.AssertionError' and observed[1]['exception_type'] == 'builtins.RuntimeError', 'namespace shadow boundary not reproduced')
        boundaries.append({'program': program, 'injected_global_AssertionError': 'builtins.RuntimeError', 'observed': observed,
                           'scope': 'Deliberately injected foreign globals are not the standalone launch namespace. Exact source contains no AssertionError rebinding; universal embedding equivalence would require an additional binding policy.'})
    write('LAZY_AND_SHORT_CIRCUIT.json', {'checked_at_utc': utc(), 'gate_shapes': 62, 'cases_per_gate': len(cases), 'comparisons': len(records) * 2,
                                        'all_scoped_semantic_probes_passed': True, 'probe_method': 'Extract each exact candidate/original gate shape, independently substitute observable test/message expressions, preserve message/no-message arity, compile at explicit optimization levels. Actual test/message AST identity separately checked in STATIC_CHECKS.',
                                        'records': records, 'namespace_boundary': boundaries})
    checkpoint('620 extracted-gate semantic scenarios yield1240 original-normal versus repaired normal/-O comparisons: single truth evaluation, lazy once-only messages, propagated exceptions, and and/or short circuit match. Foreign namespace injection documents the explicit unshadowed builtin lookup assumption.', 95)

def setup_wrapper():
    PRIVATE.mkdir(parents=True, exist_ok=True)
    wrapper = '''import builtins, contextlib, io, json, pathlib, sys, traceback
def typed(v):
    if isinstance(v,dict): return {'type':'dict','items':[[typed(k),typed(x)] for k,x in v.items()]}
    if isinstance(v,(tuple,list)): return {'type':type(v).__name__,'items':[typed(x) for x in v]}
    return {'type':type(v).__name__,'value':v}
p=pathlib.Path(sys.argv[1]); target=pathlib.Path(sys.argv[2])
ns={'__name__':'__main__','__file__':str(p)}
if sys.argv[3]=='shadow': ns['AssertionError']=RuntimeError
stream=io.StringIO()
try:
    with contextlib.redirect_stdout(stream): exec(compile(p.read_bytes(),str(p),'exec'),ns)
    result={'exception_type':None,'args_typed':None,'args_repr':None,'traceback':None,'optimization':sys.flags.optimize}
    code=0
except BaseException as e:
    result={'exception_type':type(e).__module__+'.'+type(e).__qualname__,'args_typed':typed(e.args),'args_repr':repr(e.args),'traceback':traceback.format_exc(),'optimization':sys.flags.optimize}
    code=10
target.write_text(json.dumps(result,indent=2)+'\\n')
sys.stdout.write(stream.getvalue())
sys.exit(code)
'''
    (PRIVATE / 'capture_exception.py').write_text(wrapper)
    # Publish exact wrapper code for reproducibility, excluding raw/mutated inputs.
    (PUBLIC / 'exception_capture.py').write_text(wrapper)

def main():
    setup_wrapper()
    static_checks()
    baseline_checks()
    gate_checks()
    mutation_checks()
    semantics_checks()
    pinned = {n: {'sha256': sha((PUBLIC / n).read_bytes()), 'bytes': (PUBLIC / n).stat().st_size} for n in [
        'CRITERIA_SEAL.json', 'STATIC_CHECKS.json', 'FRESH_BASELINES.json', 'ALL_GATE_FAILURES.json',
        'MEANINGFUL_CORRUPTIONS.json', 'LAZY_AND_SHORT_CIRCUIT.json', 'independent_validation.py', 'exception_capture.py']}
    write('INDEPENDENT_RESULT_SEAL.json', {'sealed_at_utc': utc(), 'source_head': 'd5bf8b5a25cabb177433338fae60af52ebfecf1c',
                                         'candidate_sha256': EXPECTED_CANDIDATES, 'all_independent_checks_passed': True,
                                         'independence': 'Prior reproduction reports, verdicts, provenance and replays remain unread at this seal.',
                                         'author_proof_attempts_added': 0, 'audit_completion_percent': 95, 'pinned_files': pinned})
    print(json.dumps({'all_independent_checks_passed': True, 'gate_count': 62, 'baseline_runs': 36, 'forced_gate_runs': 248,
                      'meaningful_corruption_runs': 40, 'semantic_comparisons': 1240, 'result_seal_sha256': sha((PUBLIC / 'INDEPENDENT_RESULT_SEAL.json').read_bytes())}, indent=2))

if __name__ == '__main__':
    main()
