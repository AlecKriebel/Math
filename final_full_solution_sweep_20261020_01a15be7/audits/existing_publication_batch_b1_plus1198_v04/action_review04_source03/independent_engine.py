"""Independent parser review using wholly inert recorded-data adapters.

Only this review's private directories can be changed. The checked production
parser, source checks, journal and observer are never replaced. No live tools.
"""
from pathlib import Path
import builtins, contextlib, copy, datetime, gzip, hashlib, io, json, os
import shutil, socket, stat, subprocess, sys, time, traceback, types
from unittest.mock import patch

D = Path(__file__).resolve().parent
A = D.parent / 'actor01'
S = A / 'private/sourceprep03'
F = A / 'private/focused03'
CAP = 18 * 1024 * 1024
RESERVE = 64 * 1024 * 1024
MS = 'cbb1e1d261832c709802fa2ee93df61b4b4a1d3e5a59d13f41e8492c8b36e659'
BS = '909713eef4580f1891f02da691f7efad069512a55fd6a37f35ba8ff4fd643a94'

def need(value, message):
    if not value:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def save(path, obj):
    data = (json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode()
    with path.open('xb') as out:
        out.write(data)
        out.flush()
        os.fsync(out.fileno())

def load_primitive(name, path):
    data = path.read_bytes()
    module = types.ModuleType(name)
    module.__file__ = str(path)
    exec(compile(data, str(path), 'exec', optimize=0), module.__dict__)
    return module

# Provider responses and their full original provenance are reused, rather than
# creating a different incomplete model. The preparer's run_case/main are not
# called. Every scenario below and its assertions were independently written.
custody = load_primitive('review_custody', F / 'custody.py')
old_custody = sys.modules.get('custody')
sys.modules['custody'] = custody
try:
    fixtures = load_primitive('review_recorded_adapters', F / 'focused_controls.py')
finally:
    if old_custody is None:
        sys.modules.pop('custody', None)
    else:
        sys.modules['custody'] = old_custody

need(sha((S / 'SOURCE_MANIFEST.json').read_bytes()) == MS, 'Wrong source')
need(sha((S / 'bootstrap.py').read_bytes()) == BS, 'Wrong bootstrap')
need(sys.flags.optimize == 0 and sys.flags.isolated and sys.flags.no_site
     and sys.flags.dont_write_bytecode, 'Use normal Python -I -S -B')

class Budget:
    def __init__(self):
        self.peak = 0
        self.minimum_free = 10**30
    def check(self):
        allocated = sum(p.stat().st_blocks * 512 for p in [D, *D.rglob('*')])
        free = shutil.disk_usage(D).free
        self.peak = max(self.peak, allocated)
        self.minimum_free = min(self.minimum_free, free)
        need(allocated <= CAP, 'Review storage cap exceeded')
        need(free >= RESERVE, 'Actual storage reserve low')

BUDGET = Budget()

class ReviewProvider(fixtures.Provider):
    def __init__(self, root, scenario):
        super().__init__(root, {'issue': 'none'})
        self.scenario = scenario
        self.issue = scenario.get('fixture_issue', 'none')
        # More than the old191 and preparer's192 rows; all43 columns remain.
        for label in ['later-current-A', 'later-current-B']:
            row = [label, '', '', 'unrelated later row'] + [''] * 39
            row[35:43] = [False, 0, 0.0, -0.0, True, 1, 'old42', 'old43']
            self.rows.append(row)
        if self.issue == 'exact_existing':
            self.rows += copy.deepcopy([x['row'] for x in fixtures.PLAN['items']])
        if scenario.get('native_initial'):
            key, value = scenario['native_initial']
            if key == 'counter_decrease':
                self.native['stats']['views'] -= 1
            elif key == 'unknown_type':
                self.native['stats']['review_unknown_boolean'] = value
        route = scenario.get('pr_route')
        if route:
            number, route_name, spelling = route
            if route_name == 'ledger':
                self.rows.append(['different-result', '', '', spelling])
            elif route_name == 'local':
                value = {'new_nested_key': [{'note': spelling}]}
                self.local = [{'path': '/INERT_LOCAL_REVIEW/state.json',
                               'sha256': sha(fixtures.canonical(value)), 'value': value}]
            elif route_name == 'account':
                record = self.owned[-1]
                record['review_unknown_key'] = {spelling: 'new source lead'}
        self.initial_rows = copy.deepcopy(self.rows)
        self.root_events = []

    def fire(self, when):
        event = self.scenario.get('at')
        if event != when or self.root_events:
            return
        action = self.scenario['change']
        self.root_events.append({'after_actual_boundary': when, 'change': action})
        if action == 'review_evidence':
            path = self.root / '_SYNTHETIC_TEST_ONLY/fresh_independent_action_review.json'
            value = json.loads(path.read_text())
            value['action_review_accepted'] = False
            path.write_bytes(fixtures.canonical(value))
        elif action == 'journal_leaf':
            path = self.root / 'private_action/action01/BEFORE_FORMULA.json'
            value = json.loads(path.read_text())
            value['review_unrecognized_history'] = False
            path.write_bytes(fixtures.canonical(value))
        elif action == 'clock':
            self.clock += 31
        elif action == 'native_unknown':
            self.native['review_unknown_full_native'] = {'flag': False}
        elif action == 'late_owned_PR':
            self.owned[-1]['review_unknown_lead'] = 'PULL\u2003REQUEST: #0001176'
        elif action == 'raw_response':
            self.raw_flags['flag'] = 0
        else:
            raise RuntimeError('Unknown independent scenario')
        self.event('independent_change', **self.root_events[-1])

    def run(self, command, capture_output=True):
        result = super().run(command, capture_output)
        if command[:4] == ['gws', 'sheets', 'spreadsheets', 'batchUpdate']:
            if self.scenario.get('after_append') == 'old_bool_type':
                self.rows[len(self.initial_rows)-1][35] = 0
        return result

SCENARIOS = [
    {'name': 'full194_row_positive', 'expected': 'verified', 'writes': 1},
    {'name': 'complete_existing194_noop', 'fixture_issue': 'exact_existing',
     'expected': 'EXACT_EXISTING_BATCH_NOOP', 'writes': 0},
    {'name': 'lost_reply_one_attempt_exact_readback', 'fixture_issue': 'lost_after_append',
     'expected': 'verified', 'writes': 1},
    {'name': 'checked_source_buffer_replacement', 'buffer_swap': True,
     'expected': 'BOOTSTRAP_HOLD', 'writes': 0},
    {'name': 'postcandidate_specific_review_change', 'at': 'fsync:VERIFIED.json',
     'change': 'review_evidence', 'expected': 'UNKNOWN', 'writes': 1},
    {'name': 'postcandidate_old_history_change', 'at': 'fsync:VERIFIED.json',
     'change': 'journal_leaf', 'expected': 'UNKNOWN', 'writes': 1},
    {'name': 'postcandidate_native_age_expiry', 'at': 'fsync:VERIFIED.json',
     'change': 'clock', 'expected': 'UNKNOWN', 'writes': 1},
    {'name': 'postintent_complete_native_new_field', 'at': 'fsync:INTENT.json',
     'change': 'native_unknown', 'expected': 'HOLD', 'writes': 0},
    {'name': 'postattempt_complete_account_new_PR', 'at': 'fsync:WRITE_ATTEMPTED.json',
     'change': 'late_owned_PR', 'expected': 'HOLD', 'writes': 0},
    {'name': 'postcollector_unknown_range_bool_type', 'at': 'after_intent_collector',
     'change': 'raw_response', 'expected': 'HOLD', 'writes': 0},
    {'name': 'postappend_old_column36_bool_type', 'after_append': 'old_bool_type',
     'expected': 'UNKNOWN', 'writes': 1},
    {'name': 'native_view_counter_decrease', 'native_initial': ['counter_decrease', None],
     'expected': 'HOLD', 'writes': 0},
    {'name': 'native_unknown_boolean_field', 'native_initial': ['unknown_type', False],
     'expected': 'HOLD', 'writes': 0},
    {'name': 'known_PR_1176_ledger_unicode', 'pr_route': [1176, 'ledger', 'ＰＵＬＬ\u2003ＲＥＱＵＥＳＴ : #00001176'],
     'expected': 'HOLD', 'writes': 0},
    {'name': 'known_PR_1007_account_key', 'pr_route': [1007, 'account', 'pull request:\u2002#0001007'],
     'expected': 'HOLD', 'writes': 0},
    {'name': 'known_PR_1198_local_nested', 'pr_route': [1198, 'local', 'https://github.com/AlecKriebel/Math/pull/0001198'],
     'expected': 'HOLD', 'writes': 0},
]

def case_run(scenario, index):
    BUDGET.check()
    case = D / 'private/active' / (str(index).zfill(2) + '_' + scenario['name'])
    case.mkdir()
    root = case / 'mirror'
    root.mkdir()
    for entry in fixtures.SOURCE_FILES:
        shutil.copy2(S / entry['path'], root / entry['path'])
    shutil.copy2(S / 'SOURCE_MANIFEST.json', root / 'SOURCE_MANIFEST.json')
    fixtures.synthetic_approval(root)
    provider = ReviewProvider(root, scenario)
    external = []
    compiled = []
    swapped = False
    unchecked = []
    actual_fsync = os.fsync
    actual_read = Path.read_bytes
    actual_compile = builtins.compile

    def blocked(*args, **kwargs):
        external.append({'route': repr(args)[:200]})
        raise RuntimeError('Real external routes are prohibited in this review')

    def fsync(fd):
        actual_fsync(fd)
        dev_ino = (os.fstat(fd).st_dev, os.fstat(fd).st_ino)
        for leaf in ['INTENT.json', 'WRITE_ATTEMPTED.json', 'VERIFIED.json']:
            path = root / 'private_action/action01' / leaf
            if path.exists() and (path.stat().st_dev, path.stat().st_ino) == dev_ino:
                provider.fire('fsync:' + leaf)

    def read(path):
        nonlocal swapped
        data = actual_read(path)
        if scenario.get('buffer_swap') and path == root / 'ops_core.py' and not swapped:
            swapped = True
            path.write_bytes(data + b'\nraise RuntimeError("UNCHECKED_BYTES_EXECUTED")\n')
        return data

    def compile_checked(source, filename, mode, *args, **kwargs):
        if str(filename) == json.loads((S / 'RUNTIME_DEPENDENCIES.json').read_text())['read_only_account_tool']['path']:
            blocked('credentialed read client execution')
        if str(filename).startswith(str(root)) and mode == 'exec':
            compiled.append({'name': Path(filename).name, 'optimize': kwargs.get('optimize'),
                             'sha256': sha(source if type(source) is bytes else source.encode())})
            if b'UNCHECKED_BYTES_EXECUTED' in (source if type(source) is bytes else source.encode()):
                unchecked.append(str(filename))
        return actual_compile(source, filename, mode, *args, **kwargs)

    stdout = io.StringIO()
    stderr = io.StringIO()
    returned = None
    error = None
    trace = None
    argv = ['--source-manifest-sha256', MS, '--execute-reviewed']
    save(case / 'INPUT.json', {'scenario': scenario, 'source_manifest_sha256': MS,
         'bootstrap_sha256': BS, 'initial_rows': provider.initial_rows,
         'production_approval': False, 'entry': 'actual bootstrap.main then actor.main argparse'})
    try:
        with patch('subprocess.run', blocked), patch('subprocess.Popen', blocked), \
             patch('os.system', blocked), patch('http.client.HTTPSConnection', blocked), \
             patch('http.client.HTTPConnection', blocked), patch('urllib.request.urlopen', blocked), \
             patch('socket.socket', blocked), patch('os.fsync', fsync), \
             patch.object(Path, 'read_bytes', read), patch('builtins.compile', compile_checked), \
             contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            raw = (root / 'bootstrap.py').read_bytes()
            need(sha(raw) == BS, 'Entry bytes changed')
            module = types.ModuleType('independent_b1_bootstrap')
            module.__file__ = str(root / 'bootstrap.py')
            exec(compile(raw, module.__file__, 'exec', optimize=0), module.__dict__)
            returned = module.main(argv, provider=provider)
    except BaseException as exc:
        error = {'class': type(exc).__name__, 'message': str(exc)}
        trace = traceback.format_exc()
    failures = list((root / 'private_readonly').glob('run_*/FAILURE.json'))
    failure = json.loads(failures[-1].read_text()) if failures else None
    status = returned.get('status') if returned is not None else failure.get('status') if failure else 'BOOTSTRAP_HOLD'
    issues = []
    if status != scenario['expected']:
        issues.append('unexpected actor status')
    if provider.append_calls != scenario['writes']:
        issues.append('unexpected simulated append count')
    if external or provider.infra:
        issues.append('external adapter or fixture error')
    if unchecked or any(c['optimize'] != 0 for c in compiled):
        issues.append('execution bytes/compile policy')
    if scenario.get('at') and len(provider.root_events) != 1:
        issues.append('actual intended boundary not observed')
    if status == 'verified':
        need(provider.rows[:len(provider.initial_rows)] == provider.initial_rows, 'Positive old rows changed')
        need(provider.rows[len(provider.initial_rows):] == [i['row'] for i in fixtures.PLAN['items']], 'Positive batch wrong')
    if scenario.get('at') == 'fsync:VERIFIED.json':
        if not failure or failure.get('known_append_fact', {}).get('exact_prefix_plus_batch_observed') is not True:
            issues.append('known append fact lost')
        candidate = json.loads((root / 'private_action/action01/VERIFIED.json').read_text())
        if candidate.get('status') != 'CANDIDATE_REQUIRES_FINAL_POST_SYNC_CHECK' or returned is not None:
            issues.append('candidate mislabeled or successful return after change')
        if '"status": "verified"' in stdout.getvalue():
            issues.append('late failure printed certification')
    result = {'scenario': scenario, 'actor_status': status, 'returned': returned,
              'error': error, 'failure_capture': failure, 'actual_boundary_events': provider.root_events,
              'simulated_append_attempts': provider.append_calls, 'simulated_applications': provider.applied,
              'initial_rows': len(provider.initial_rows), 'final_rows': len(provider.rows),
              'compiled': compiled, 'unchecked_bytes_selected': unchecked,
              'external_attempts': external, 'provider_infrastructure_errors': provider.infra,
              'stdout': stdout.getvalue(), 'stderr': stderr.getvalue(), 'traceback': trace,
              'provider_trace': provider.trace, 'issues': issues,
              'outcome': 'PASS' if not issues else 'FAIL', 'real_service_writes': 0}
    save(case / 'CASE_RESULT.json', result)
    BUDGET.check()
    # Preserve complete evidence even if it identifies a substantive failure.
    stored = custody.preserve_case(case, D / 'private/archives')
    BUDGET.check()
    return result, stored

def main():
    need(not (D / 'RESULTS.json').exists(), 'Completed review must not be rerun')
    results = []
    for index, scenario in enumerate(SCENARIOS, 1):
        result, stored = case_run(scenario, index)
        results.append({'name': scenario['name'], 'outcome': result['outcome'],
                        'actor_status': result['actor_status'], 'issues': result['issues'],
                        'simulated_append_attempts': result['simulated_append_attempts'],
                        'custody': stored})
        print(json.dumps(results[-1]), flush=True)
        if result['issues']:
            break
    report = {'at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'results': results, 'required': len(SCENARIOS), 'completed': len(results),
              'status': 'PASS_REVIEW_CONTROLS' if len(results) == len(SCENARIOS) and all(x['outcome'] == 'PASS' for x in results) else 'HOLD_OR_INCOMPLETE',
              'peak_allocated_bytes': BUDGET.peak, 'minimum_actual_free_bytes': BUDGET.minimum_free,
              'real_service_writes': 0, 'publication_ready': False, 'root_action_accepted': False}
    save(D / 'RESULTS.json', report)
    print(json.dumps({k: v for k, v in report.items() if k != 'results'}), flush=True)

if __name__ == '__main__':
    main()
