"""Read exact PR49 originals and in-place native/raw/SQL provenance, without scientific execution."""
from pathlib import Path
import collections, datetime as dt, hashlib, json, os, sqlite3, stat, subprocess

A = Path(__file__).resolve().parent
R = A.parents[2]
ID = '30000703'
HEAD = '036a5ed59bee5ed79f08349290481584610f1456'

def sha(body): return hashlib.sha256(body).hexdigest()
def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def write(path, body):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(body); stream.flush(); os.fsync(stream.fileno())
def js(path, value): write(path, (json.dumps(value, indent=2, sort_keys=True) + '\n').encode())
def same(left, right):
    if type(left) is not type(right): return False
    if isinstance(left, dict): return left.keys() == right.keys() and all(same(left[k], right[k]) for k in left)
    if isinstance(left, list): return len(left) == len(right) and all(same(a, b) for a, b in zip(left, right))
    return left == right

def in_place(path):
    full = R / path
    before = full.stat(); body = full.read_bytes(); after = full.stat()
    assert stat.S_ISREG(before.st_mode) and not full.is_symlink()
    assert (before.st_size, before.st_mtime_ns, before.st_mode) == (after.st_size, after.st_mtime_ns, after.st_mode)
    return body, dict(path=path, bytes=len(body), sha256=sha(body), full_mode=stat.S_IMODE(before.st_mode), mtime_ns=before.st_mtime_ns, body_read_in_full=True, raw_body_copied=False, captured_utc=now(), actual_pid=os.getpid())

def git_native(path):
    source = Path(__file__).read_bytes()
    commands = []
    tree_argv = ['git', 'ls-tree', '-z', HEAD, '--', path]
    start = now(); child = subprocess.Popen(tree_argv, cwd=R, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    tree, error = child.communicate(); finish = now()
    assert child.returncode == 0 and not error and tree.endswith(b'\0') and tree.count(b'\0') == 1
    metadata, literal = tree[:-1].split(b'\t'); mode, kind, oid = metadata.decode().split(' ')
    assert kind == 'blob' and literal.decode() == path
    commands.append(dict(argv=tree_argv, pid=child.pid, operator_pid=os.getpid(), started_utc=start, finished_utc=finish, completed=True, exit_code=child.returncode, stdout=dict(bytes=len(tree), sha256=sha(tree), literal_utf8=tree.decode()), stderr=dict(bytes=0, sha256=sha(error), literal_utf8=''), actual_execution=True, stdin_supplied=False, operator_sha256=sha(source)))
    argv = ['git', 'cat-file', 'blob', oid]
    start = now(); child = subprocess.Popen(argv, cwd=R, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    body, error = child.communicate(); finish = now()
    assert child.returncode == 0 and not error and Path(__file__).read_bytes() == source
    commands.append(dict(argv=argv, pid=child.pid, operator_pid=os.getpid(), started_utc=start, finished_utc=finish, completed=True, exit_code=child.returncode, stdout=dict(bytes=len(body), sha256=sha(body), raw_body_retained=False, full_body_read_in_place=True), stderr=dict(bytes=0, sha256=sha(error), literal_utf8=''), actual_execution=True, stdin_supplied=False, operator_sha256=sha(source)))
    return body, dict(path=path, git_ref=HEAD, git_mode=mode, git_object=oid, bytes=len(body), sha256=sha(body), full_body_read_in_place=True, unrelated_native_raw_body_copied=False, complete_actual_read_operations=commands)

def selected_native(name, value):
    if name.endswith('.jsonl') or name == 'catalog.json':
        assert isinstance(value, list)
        return [row for row in value if isinstance(row, dict) and type(row.get('id')) in (str, int) and str(row['id']) == ID]
    if name in ('assessments.json', 'state.json'):
        assert isinstance(value, dict)
        return dict(key=ID, key_present=ID in value, value=value.get(ID))
    if name == 'review_v2/related_target_groups.json':
        return dict(policy=value['policy'], groups=[group for group in value['groups'] if ID in [str(x) for x in group['ids']]])
    assert name in ('policy.json', 'manifest.json')
    return value

def parse(name, body):
    return [json.loads(line) for line in body.splitlines() if line.strip()] if name.endswith('.jsonl') else json.loads(body)

def main():
    source = Path(__file__).read_bytes()
    write(A / 'INSPECTION_PRELAUNCH_SOURCE.py', source)
    manifest = json.loads((A / 'snapshot_manifest.json').read_bytes())
    original_objects = {}; all_originals = []; originals = {}
    for row in manifest['files']:
        path = A / 'source_snapshot' / row['relative_path']; body = path.read_bytes()
        assert len(body) == row['bytes'] and sha(body) == row['sha256'] and row['git_mode'] == '100644' and stat.S_IMODE(path.stat().st_mode) == 0o444
        text = body.decode('utf-8'); originals[row['relative_path']] = body
        if row['relative_path'].endswith('.json'): original_objects[row['relative_path']] = json.loads(text)
        all_originals.append(dict(relative_path=row['relative_path'], bytes=len(body), sha256=sha(body), complete_utf8_body_read=True, original_git_object=row['git_object'], helper_execution_performed=False))
    assert len(all_originals) == 16
    assert originals['verify.py'] == originals['review/submitted_verify.py']
    assert originals['verification.json'] == originals['review/verification.json']
    assert originals['prior_report.json'] == b'null\n'
    ledger = original_objects['turns.json']
    assert type(ledger['id']) is int and ledger['id'] == 30000703 and type(ledger['count']) is int and ledger['count'] == 0 and ledger['substantive_attempts'] == []
    author = original_objects['verification.json']; independent = original_objects['review/independent_results.json']
    assert type(author['passed']) is int and author['passed'] == len(author['checks']) == 69 and type(author['failed']) is int and author['failed'] == 0
    assert type(independent['passed']) is int and independent['passed'] == len(independent['checks']) == 187 and type(independent['failed']) is int and independent['failed'] == 0
    assert set(author['checks'].values()) == set(independent['checks'].values()) == {'PASS'}
    old_verdict = original_objects['review/verdict.json']; readiness = original_objects['readiness.json']
    assert sha(originals['SOURCE_STATUS.md']) == old_verdict['artifact_sha256'] == readiness['artifact_sha256']
    assert sha(originals['review/REVIEW.md']) == old_verdict['review_sha256'] == readiness['review_sha256']
    assert old_verdict['recommended_queue_status'] == readiness['recommended_status'] == 'already_solved'
    assert old_verdict['new_result_claimed'] is False and readiness['new_result'] is False
    # Reconstruct every added scientific file from the full Git diff, including exact final newlines.
    diff = (A / 'original_diff.patch').read_bytes(); rebuilt = {}
    for block in diff.split(b'diff --git ')[1:]:
        lines = block.splitlines(keepends=True); header = lines[0].decode().strip(); left, right = header.split(' ')
        assert left.startswith('a/') and right.startswith('b/') and left[2:] == right[2:]
        path = right[2:]
        if not path.startswith('unsolved_math_prioritization/attempts/' + ID + '/'): continue
        assert b'new file mode 100644\n' in lines and b'--- /dev/null\n' in lines
        additions = b''.join(line[1:] for line in lines if line.startswith(b'+') and not line.startswith(b'+++'))
        assert not any(line.startswith(b'\\ No newline') for line in lines)
        relative = path.split('/' + ID + '/', 1)[1]
        assert additions == originals[relative]; rebuilt[relative] = sha(additions)
    assert set(rebuilt) == set(originals)
    js(A / 'ORIGINAL_COMPLETE_READ_RECEIPT.json', dict(schema='pr49-original-complete-read-receipt/v1', captured_utc=now(), actual_pid=os.getpid(), original_files_read_in_full=len(all_originals), originals=all_originals, complete_original_JSON_values=original_objects, all_16_added_scientific_hunks_reconstructed_byte_exact=True, original_source_semantics='plain selected problem object, not queue.py show wrapper', original_prior_report_literal='null\n', original_ledger_kind='JSON turns.json', original_substantive_turns=0, turn_limit=5, new_substantive_turns=0, original_known_result_artifact_hash_matches=True, old_review_historical_metadata_hash_matches=True, author_control_count_attributed_only=69, independent_control_count_attributed_only=187, helper_execution_performed=False, mathematical_predicates_reproduced=False, primary_pdf_hashes_freshly_authenticated=False, source_claims_validated=False, mathematical_verdict=None, acceptance_verdict=None))
    native_names = ['catalog.json', 'assessments.json', 'state.json', 'history.jsonl', 'assessment_history.jsonl', 'policy.json', 'manifest.json', 'review_v2/related_target_groups.json']
    head_bindings = []; head_selected = {}; working_bindings = []; working_selected = {}
    for name in native_names:
        body, binding = git_native('unsolved_math_prioritization/' + name)
        value = selected_native(name, parse(name, body)); head_selected[name] = value; head_bindings.append(binding)
        js(A / 'original_native_selected' / name.replace('/', '__'), dict(original_path=binding['path'], original_git_binding=binding, selected_problem_id=ID, complete_selected_objects=value, selection_method='literal string/int id retained; exact dictionary key; selected relevant groups; full first-party policy/manifest', selection_only=True, future_acceptance_authority=False))
        body, binding = in_place('unsolved_math_prioritization/' + name)
        working_selected[name] = selected_native(name, parse(name, body)); working_bindings.append(binding)
    current_paths = ['draft_pr_publication_program_20260930/inventory.json'] + ['unsolved_math_prioritization/' + name for name in ['QUEUE.md', 'state.json', 'history.jsonl', 'catalog.json', 'assessments.json', 'queue.py', 'policy.json', 'manifest.json', 'cache/problems.json', 'cache/research_results.json', 'cache/catalog.sqlite', 'review_v2/related_target_groups.json']]
    current = []
    for path in current_paths:
        body, binding = in_place(path); current.append(binding)
    assert len(current) == 13
    js(A / 'ORIGINAL_NATIVE_SELECTED_READ.json', dict(schema='pr49-original-and-dated-working-native-selected/v1', captured_utc=now(), actual_pid=os.getpid(), head_native_bindings=head_bindings, head_complete_selected_objects=head_selected, working_native_bindings=working_bindings, working_complete_selected_objects=working_selected, current_canonical13_bindings=current, canonical_count=len(current), native_writes=False, transition_performed=False, authority_for_future_main=False, unrelated_native_raw_bodies_copied=False))
    # Reproduce only queue.py's importer in memory, never invoking its mutating sync/show paths.
    raw_problems_body, problems_binding = in_place('unsolved_math_prioritization/cache/problems.json')
    raw_reports_body, reports_binding = in_place('unsolved_math_prioritization/cache/research_results.json')
    problems = json.loads(raw_problems_body); reports = json.loads(raw_reports_body)
    assert isinstance(problems, list) and isinstance(reports, dict)
    counts = collections.Counter(problem['problem_number'] for problem in problems)
    imported = []; keys = []
    for raw_problem in problems:
        problem = dict(raw_problem)
        if counts[problem['problem_number']] > 1 and problem['problem_number'] in reports: problem['_ambiguous_report'] = True
        key = str(problem['id']); keys.append(key)
        report = {} if problem.get('_ambiguous_report') else reports.get(problem['problem_number'], {})
        imported.append((key, problem, report, json.dumps(problem), json.dumps(report)))
    assert len(keys) == len(set(keys)) == 15458
    sqlite_path = R / 'unsolved_math_prioritization/cache/catalog.sqlite'
    before_body, sqlite_binding = in_place('unsolved_math_prioritization/cache/catalog.sqlite')
    database = sqlite3.connect(sqlite_path.as_uri() + '?mode=ro&immutable=1', uri=True)
    database.execute('PRAGMA query_only=ON')
    sql_rows = database.execute('SELECT key,payload,report FROM records ORDER BY key').fetchall()
    metadata_rows = database.execute('SELECT revision FROM metadata').fetchall(); database.close()
    assert len(sql_rows) == 15458
    sql = {row[0]: row[1:] for row in sql_rows}; assert len(sql) == 15458 and set(sql) == set(keys)
    checked_rows = []; selected = None
    for key, problem, report, payload_text, report_text in imported:
        actual_payload, actual_report = sql[key]
        assert type(actual_payload) is type(actual_report) is str
        assert actual_payload == payload_text and actual_report == report_text
        assert same(json.loads(actual_payload), problem) and same(json.loads(actual_report), report)
        checked_rows.append(dict(key=key, payload_utf8_bytes=len(actual_payload.encode()), payload_utf8_sha256=sha(actual_payload.encode()), report_utf8_bytes=len(actual_report.encode()), report_utf8_sha256=sha(actual_report.encode()), literal_importer_payload_equal=True, literal_importer_report_equal=True, recursive_scalar_types_equal=True))
        if key == ID:
            raw_problem = next(row for row in problems if str(row['id']) == ID)
            plain = json.dumps(raw_problem, indent=2) + '\n'
            assert plain.encode() == originals['source_record.json']
            code = raw_problem['problem_number']; present = code in reports
            assert report is None and present and reports[code] is None
            assert originals['prior_report.json'] == (json.dumps(report, indent=2) + '\n').encode()
            review_hash = sha(json.dumps([problem, report], sort_keys=True).encode())
            statement_hash = sha(problem['statement'].encode())
            assert review_hash == readiness['review_hash'] and statement_hash == readiness['statement_hash']
            selected = dict(key=key, problem_code=code, raw_problem_id_type=type(raw_problem['id']).__name__, original_plain_source_bytes=len(originals['source_record.json']), original_plain_source_sha256=sha(originals['source_record.json']), original_plain_source_byte_exact_default_pretty_JSON=True, source_record_semantics='plain original selected problem, not queue.py show wrapper', upstream_report_key_present=present, upstream_report_presence='EXPLICIT_NULL', upstream_report_type='NoneType', sqlite_report_literal=actual_report, original_prior_report_bytes=len(originals['prior_report.json']), original_prior_report_sha256=sha(originals['prior_report.json']), original_prior_report_byte_exact=True, review_hash=review_hash, statement_hash=statement_hash, fresh_prior_or_priority_verdict=None)
    assert selected is not None and metadata_rows == [(working_selected['manifest.json']['revision'],)]
    after_body, after_binding = in_place('unsolved_math_prioritization/cache/catalog.sqlite')
    assert sha(before_body) == sha(after_body) and sqlite_binding['mtime_ns'] == after_binding['mtime_ns']
    assert problems_binding['sha256'] == working_selected['manifest.json']['files']['problems.json']['sha256'] and problems_binding['bytes'] == working_selected['manifest.json']['files']['problems.json']['bytes']
    assert reports_binding['sha256'] == working_selected['manifest.json']['files']['research_results.json']['sha256'] and reports_binding['bytes'] == working_selected['manifest.json']['files']['research_results.json']['bytes']
    js(A / 'ORIGINAL_COMPLETE_RAW_SQL_READ.json', dict(schema='pr49-original-complete-in-place-raw-SQL-importer-read/v1', captured_utc=now(), actual_pid=os.getpid(), raw_inputs=[problems_binding, reports_binding], sqlite_binding=sqlite_binding, sqlite_post_read_binding=after_binding, metadata_revision_rows=metadata_rows, raw_problem_count=len(problems), unique_numeric_ID_count=len(set(keys)), all_SQL_rows_read=len(sql_rows), literal_importer_verified_rows=len(checked_rows), all_recursive_scalar_types_verified=True, importer_source_path='unsolved_math_prioritization/queue.py', importer_source_sha256=next(row['sha256'] for row in current if row['path'].endswith('/queue.py')), rows=checked_rows, selected=selected, raw_foreign_bodies_copied=False, foreign_selected_problem_duplicate_body_copied=False, SQLite_writes=False, native_writes=False, primary_source_claims_validated=False, mathematical_verdict=None, future_acceptance_authority=False))
    with (A / 'RESEARCH_LOG.md').open('a') as stream:
        stream.write('\n' + now() + ' — Actual inspection PID' + str(os.getpid()) + ' read all16 original scientific bodies, complete10 original JSON values, reconstructed all16 added hunks byte exactly, and confirmed original0/5 ledger. Original helpers remain unexecuted;69/187 controls are historical attributed counts. Plain selected record matches full raw record byte exactly under default pretty JSON. Upstream prior-report key is PRESENT EXPLICIT_NULL, SQL literal null, original prior_report.json null plus newline; this is not ABSENT/empty-object fallback. All15458 raw/SQL importer payloads/reports match literal serialization and recursive scalar types; complete raw foreign bodies and SQL bytes read in place but not copied. Head native selected records and dated working13 inputs bound without native writes or future authority. Original-source preparation90%; mathematical/source-claim validation0%; new substantive turns0; program ROOT-supplied checkpoint35/180=19.444444444444446%, current acceptance46.\n')
        stream.flush(); os.fsync(stream.fileno())
    assert Path(__file__).read_bytes() == source
    print(json.dumps(dict(status='ORIGINAL_FULL_READ_AND_IN_PLACE_PROVENANCE_COMPLETE_ONLY', actual_pid=os.getpid(), original_files=16, original_JSON_values=len(original_objects), original_substantive_turns=0, raw_records=len(problems), SQL_rows=len(sql_rows), prior_report_presence=selected['upstream_report_presence'], current_canonical13_inputs=13, helper_execution_performed=False, native_writes=False, acceptance_verdict=None), sort_keys=True))

if __name__ == '__main__': main()
