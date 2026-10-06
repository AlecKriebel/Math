"""Actual, bounded read-only context collection. Writes only beside this file."""
from pathlib import Path
import datetime, hashlib, json, os, sqlite3, subprocess

D = Path(__file__).resolve().parent
A = D.parent
C = A.parents[2]
R = Path('/Users/alec/Documents/Math')
K = '30003996'
P = 'unsolved_math_prioritization/'
records = []

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(data):
    return hashlib.sha256(data).hexdigest()

def file_pin(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return {'path': str(path), 'bytes': path.stat().st_size, 'sha256': h.hexdigest()}

def dump(path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')

def run(argv, retain=True):
    start = now()
    process = subprocess.Popen(argv, cwd=C, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    index = len(records)
    stem = str(index)
    if retain:
        (D / 'context_receipts' / (stem + '.stdout.bin')).write_bytes(out)
    (D / 'context_receipts' / (stem + '.stderr.bin')).write_bytes(err)
    records.append({'argv': argv, 'cwd': str(C), 'PID': process.pid,
                    'UTC_start': start, 'UTC_end': now(), 'exit_code': process.returncode,
                    'stdout_bytes': len(out), 'stdout_sha256': sha(out),
                    'stdout_file': 'context_receipts/' + stem + '.stdout.bin' if retain else None,
                    'large_blob_not_duplicated': not retain,
                    'stderr_bytes': len(err), 'stderr_sha256': sha(err),
                    'stderr_file': 'context_receipts/' + stem + '.stderr.bin'})
    dump(D / 'CONTEXT_PROCESS_JOURNAL.json', {'actual_operator_PID': os.getpid(), 'records': records})
    if process.returncode:
        raise RuntimeError(err.decode('utf8', 'replace'))
    return out

def main():
    (D / 'context_receipts').mkdir(exist_ok=False)
    base = run(['/usr/bin/git', 'rev-parse', 'HEAD']).decode().strip()
    branch = run(['/usr/bin/git', 'symbolic-ref', '--short', 'HEAD']).decode().strip()
    if branch != 'main':
        raise RuntimeError('Not main')
    native = {}
    git_pins = []
    for name in ['AGENTS.md', 'README.md', 'queue.py', 'manifest.json', 'policy.json',
                 'catalog.json', 'assessments.json', 'state.json', 'QUEUE.md']:
        data = run(['/usr/bin/git', 'show', base + ':' + P + name],
                   retain=name not in ['catalog.json', 'assessments.json', 'QUEUE.md'])
        native[name] = data
        git_pins.append({'path': P + name, 'git_commit': base, 'bytes': len(data), 'sha256': sha(data)})
    run(['/usr/bin/git', 'ls-tree', '-r', '--name-only', base, '--', P + 'attempts/' + K])
    live = json.loads(run(['gh', 'pr', 'view', '108', '--repo', 'AlecKriebel/Math', '--json',
                          'number,state,isDraft,headRefName,headRefOid,baseRefName,url']))
    manifest = json.loads(native['manifest.json'])
    source_cache = R / P / 'cache/catalog.sqlite'
    db = sqlite3.connect('file:' + str(source_cache) + '?mode=ro&immutable=1', uri=True)
    payload, prior = db.execute('SELECT payload,report FROM records WHERE key=?', (K,)).fetchone()
    sql_metadata = {'revision': db.execute('SELECT revision FROM metadata').fetchone()[0],
                    'records': db.execute('SELECT count(*) FROM records').fetchone()[0]}
    db.close()
    problem, imported = json.loads(payload), json.loads(prior)
    raw_problems = json.loads((R / P / 'cache/problems.json').read_text())
    selected = [p for p in raw_problems if str(p['id']) == K]
    del raw_problems
    raw_reports = json.loads((R / P / 'cache/research_results.json').read_text())
    raw_selected = raw_reports.get(problem['problem_number'], {})
    del raw_reports
    O = A / 'original_source_authentication_20261006/original_attempt'
    original = json.loads((O / 'source_record.json').read_text())
    catalog = json.loads(native['catalog.json'])
    state = json.loads(native['state.json'])
    row = next(r for r in catalog if r['id'] == K)
    stale = []
    for r in catalog:
        s = state.get(r['id'])
        if s and (r['local_status'] != s['status'] or r['turns_used'] != s.get('turns_used', 0)):
            stale.append({'id': r['id'], 'catalog_status': r['local_status'],
                          'state_status': s['status'], 'catalog_turns': r['turns_used'],
                          'state_turns': s.get('turns_used', 0)})
    auth = A / 'original_source_authentication_20261006'
    local_inputs = [R / 'AGENTS.md', R / P / 'queue.py']
    local_inputs += [auth / name for name in ['ORIGINAL_BLOB_MANIFEST.json', 'SOURCEPAIR_AUTHENTICATION.json',
                     'SELECTED_IMPORTED_PRIOR_REPORT.json', 'QUEUE_STATUS_PROJECTION.json']]
    local_inputs += sorted(p for p in O.rglob('*') if p.is_file())
    local_inputs += sorted(p for p in (A / 'repaired_diagnostics_v1').rglob('*') if p.is_file())
    local_inputs += [A / 'ROOT_MATHEMATICAL_GATE_20261006.json']
    for sibling in ['pr107_30003997', 'pr104_600008']:
        local_inputs.append(A.parent / sibling / 'prepare_native_prior_disposition.py')
    local_inputs += [R / P / 'cache' / n for n in ['problems.json', 'research_results.json', 'catalog.sqlite']]
    inputs = [file_pin(p) for p in local_inputs]
    summary = {'schema': 'pr108-native-plan-context/v1', 'UTC': now(), 'actual_reader_PID': os.getpid(),
               'main_parent_observed': base, 'branch_observed': branch, 'live_PR_metadata': live,
               'SQL_metadata': sql_metadata, 'manifest_revision': manifest['revision'],
               'source_pair_review_hash': sha(json.dumps([problem, imported], sort_keys=True).encode()),
               'statement_hash': sha(problem['statement'].encode()),
               'raw_SQL_submitted_source_equal': selected == [problem] and original == problem,
               'raw_SQL_imported_report_equal_empty_object': raw_selected == imported == {},
               'original_structured_ledger_present': (O / 'status.json').exists() or (O / 'turns.jsonl').exists(),
               'original_attempt_file_count': len([p for p in O.rglob('*') if p.is_file()]),
               'target_catalog': row, 'target_state_present': K in state,
               'observed_unrelated_stale_catalog_projection_count': len(stale),
               'observed_unrelated_stale_catalog_projections': stale,
               'native_claimed_solved_CLI_choice_present': "'claimed_solved'" in native['queue.py'].decode().split('def now():')[0],
               'native_assess_flow_will_be_required': True, 'integration_executed': False,
               'publication_executed': False, 'new_central_proof_search_turns': 0,
               'git_blob_input_pins': git_pins}
    dump(D / 'CONTEXT_INPUT_MANIFEST.json', {'UTC': now(), 'files': inputs, 'git_blobs': git_pins})
    dump(D / 'CONTEXT_SNAPSHOT.json', summary)
    print(json.dumps({k: v for k, v in summary.items() if k not in ['observed_unrelated_stale_catalog_projections', 'git_blob_input_pins', 'target_catalog']}))

if __name__ == '__main__':
    main()
