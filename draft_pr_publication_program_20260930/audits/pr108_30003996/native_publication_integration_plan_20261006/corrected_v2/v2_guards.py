"""Review-only PR108 V2 guards. No Git, SQL, native assess or service invocation."""
from pathlib import Path, PurePosixPath
import collections, csv, datetime, hashlib, io, json, re, stat

K = '30003996'
CODE = 'OWR-16633-013'
N = 'unsolved_math_prioritization/attempts/30003996/'
HEAD = '3526d46bf143b08e5055ffa7728c6278e9f958ea'
SHEET = '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
GID = 1254632077
TITLE = 'Math Puzzles'
COLUMNS = ['Original Problem', 'Solution Chat URL', 'DOI', 'Notes']
PROGRAMS = ['bounded_process.py', 'native_assess_worker.py', 'prepare_review_bundle.py', 'v2_guards.py']
ORIGINAL_NAMES = {'PROOF.md', 'README.md', 'RESEARCH_LOG.md', 'SHA256SUMS', 'source_manifest.json',
    'source_record.json', 'verification.json', 'verify.py', 'independent_review/REVIEW.md',
    'independent_review/review_summary.json', 'independent_review/independent_results.json',
    'independent_review/independent_checks.py', 'independent_review/author_replay/PROOF.md',
    'independent_review/author_replay/verify.py', 'independent_review/author_replay/verification.json'}
GATE_ROLES = ['mathematics', 'priority', 'package', 'whole_package_R1', 'whole_package_R2',
              'pre_execution_adversary', 'final']
CHOICES = {'main_parent', 'queue_py_sha256', 'native_baseline_pins', 'source_cache_pin', 'raw_source_pins',
    'original_authentication_pins', 'effective_diagnostics_pins', 'package', 'publication',
    'google_sheet', 'assessment', 'campaign_note', 'process_policy', 'worker_policy', 'capacity_policy',
    'scoped_rank_interpretation', 'execution_mode', 'runtime'}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def canonical(obj):
    return (json.dumps(obj, sort_keys=True, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode()

def loads(data):
    def pairs(values):
        result = {}
        for key, value in values:
            require(key not in result, 'Duplicate JSON key: ' + key)
            result[key] = value
        return result
    return json.loads(data, object_pairs_hook=pairs, parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))

def relative(value):
    require(isinstance(value, str) and value and len(value.encode())<=512 and '\\' not in value and not any(c in value for c in '\r\n\x00'), 'Invalid path')
    path = PurePosixPath(value)
    require(not path.is_absolute() and '..' not in path.parts and str(path) == value, 'Escaping/noncanonical path')
    return value

def pin_shape(spec):
    require(isinstance(spec, dict) and set(spec) == {'path', 'bytes', 'sha256'}, 'Exact file pin required')
    relative(spec['path'])
    require(type(spec['bytes']) is int and spec['bytes'] >= 0 and
            isinstance(spec['sha256'], str) and re.fullmatch('[0-9a-f]{64}', spec['sha256']), 'Invalid pin bytes/hash')

def regular(path):
    require(path.is_absolute(), 'Absolute internal path required')
    for candidate in [*path.parents, path]:
        require(not candidate.is_symlink(), 'Symlink input')
    info = path.stat()
    require(stat.S_ISREG(info.st_mode), 'Nonregular input')
    return info

class ReviewedInputs:
    """Every non-gate input must occur in the reviewed exact inventory and be used."""
    def __init__(self, manifest, root, allowed_root):
        self.root, self.allowed_root = root, allowed_root
        self.pins, self.used, self.captured = {}, set(), {}
        require(isinstance(manifest['input_files'], list) and len(manifest['input_files']) <= 256, 'Input count cap')
        for spec in manifest['input_files']:
            pin_shape(spec)
            require(spec['bytes'] <= 8 * 1024 * 1024 and spec['path'] not in self.pins, 'Input duplicate/per-file cap')
            require((root / spec['path']).is_relative_to(allowed_root), 'Input outside PR108 audit')
            self.pins[spec['path']] = spec
        require(sum(x['bytes'] for x in self.pins.values()) <= 32 * 1024 * 1024, 'Aggregate reviewed input cap')

    def read(self, spec, allowed_root=None):
        pin_shape(spec)
        require(self.pins.get(spec['path']) == spec, 'Input absent from or changed after reviewed execution manifest')
        path = self.root / spec['path']
        require(path.is_relative_to(allowed_root or self.allowed_root), 'Input wrong allowed root')
        # Capture once. All later consumers reuse authenticated immutable bytes.
        if spec['path'] not in self.captured:
            info = regular(path)
            require(info.st_size == spec['bytes'], 'Input size changed')
            data = path.read_bytes()
            require(len(data) == spec['bytes'] and sha(data) == spec['sha256'], 'Input byte pin mismatch')
            self.captured[spec['path']] = data
        self.used.add(spec['path'])
        return path, self.captured[spec['path']]

    def finish(self):
        require(self.used == set(self.pins), 'Unused/unrepresented execution input: ' + repr(sorted(set(self.pins) - self.used)))

def validate_execution_manifest(document, data):
    require(set(document) == {'schema', 'template_only', 'effective', 'program_files', 'input_files'}, 'Execution manifest fields')
    require(document['schema'] == 'pr108-immutable-execution-inputs/v2' and document['template_only'] is False, 'Execution manifest template/schema')
    require(data == canonical(document), 'Execution manifest must use exact canonical bytes')
    require(set(document['effective']) == CHOICES, 'Every effective choice must be explicit; no unreviewed extra choice')
    require(document['effective']['execution_mode'] == 'review_bundle_only' and
            document['effective']['scoped_rank_interpretation'] == 'preserve_baseline_labels_and_positions_not_global_rerank', 'Execution/scope mode')
    require(sorted(Path(x['path']).name for x in document['program_files']) == PROGRAMS, 'Entire code family must be pinned')
    # Gate pins deliberately live only in the thin configuration, avoiding cycles.
    require('gates' not in document['effective'], 'Gate hash cycle')

def validate_thin_config(cfg):
    require(set(cfg) == {'schema', 'template_only', 'commissioned_after_independent_review', 'execution_inputs', 'gates'}, 'Thin config fields')
    require(cfg['schema'] == 'pr108-native-publication-integration-config/v2', 'Thin config schema')
    require(cfg['template_only'] is False, 'Template configuration cannot run')
    require(cfg['commissioned_after_independent_review'] is True, 'Not commissioned')
    require(set(cfg['gates']) == set(GATE_ROLES), 'All seven root gates required')

def physical_lines(text):
    """Only CR, LF and CRLF terminate a physical CSV line."""
    return re.findall(r'[^\r\n]*(?:\r\n|\r|\n|$)', text)[:-1] if text.endswith(('\r', '\n')) else [x for x in re.findall(r'[^\r\n]*(?:\r\n|\r|\n|$)', text) if x]

def csv_records(data):
    text = data.decode('utf8')
    lines = physical_lines(text)
    require(''.join(lines) == text, 'Physical line partition mismatch')
    reader = csv.reader(io.StringIO(text, newline=''), strict=True)
    records, start = [], 0
    for fields in reader:
        end = reader.line_num
        records.append({'fields': fields, 'bytes': ''.join(lines[start:end]).encode(), 'start': start, 'end': end})
        start = end
    require(start == len(lines), 'CSV physical span coverage')
    return lines, records

def csv_overlay(data, target):
    lines, before = csv_records(data)
    require(before and len(before[0]['fields']) > 1, 'CSV header missing')
    fields = before[0]['fields']
    identity = fields.index('id')
    require(all(len(x['fields']) == len(fields) for x in before[1:]), 'CSV row width')
    ids = [x['fields'][identity] for x in before[1:]]
    require(len(set(ids)) == len(ids) and ids.count(K) == 1, 'CSV identity uniqueness')
    index = ids.index(K) + 1
    old = before[index]
    last = lines[old['end'] - 1]
    ending = '\r\n' if last.endswith('\r\n') else '\r' if last.endswith('\r') else '\n' if last.endswith('\n') else ''
    stream = io.StringIO(newline='')
    # Use CRLF to quote BOTH physical separators even when target EOF has no ending.
    writer = csv.DictWriter(stream, fieldnames=fields, extrasaction='ignore', lineterminator='\r\n')
    writer.writerow({**target, 'holds': '; '.join(target['holds']), 'reasons': '; '.join(target['reasons'])})
    replacement=stream.getvalue();require(replacement.endswith('\r\n'),'CSV writer ending')
    replacement=replacement[:-2]+ending
    output = (''.join(lines[:old['start']]) + replacement + ''.join(lines[old['end']:])).encode()
    _, after = csv_records(output)
    require(len(before) == len(after) and before[0]['bytes'] == after[0]['bytes'], 'CSV count/header changed')
    require([x['fields'][identity] for x in after[1:]] == ids, 'CSV identity/order changed')
    require(all(a['bytes'] == b['bytes'] for i, (a, b) in enumerate(zip(before, after)) if i != index), 'Unrelated CSV span changed')
    require(after[index]['fields'][identity] == K, 'Target CSV span replacement failed')
    return output

def native_status_turns(row, state, policy, assessment):
    if not row['present']:
        return state.get('status',row['local_status']),row['turns_used']
    is_v2 = policy.get('turn_limit') == 5
    default = ('queued' if assessment.get('decision') == 'candidate' else 'deferred' if assessment.get('decision') in ['defer','exclude'] else 'unreviewed') if is_v2 else 'unreviewed'
    if is_v2 and default == 'queued' and row['holds']: default = 'unreviewed'
    stale = bool(assessment and assessment.get('review_hash') != row['review_hash'])
    if is_v2 and assessment.get('resolution') == 'already_solved' and not stale: default = 'already_solved'
    return state.get('status', default), state.get('turns_used', 0)

def expected_eligible(row, state, policy, assessment):
    limit = policy.get('turn_limit', 1000000)
    require(type(limit) is int and limit >= 1 and type(state.get('turns_used', row['turns_used'])) is int, 'Native turn policy')
    status, turns = native_status_turns(row, state, policy, assessment)
    require(type(turns) is int and turns >= 0, 'Native turns must be a nonnegative integer')
    return bool(row['present'] and not row['holds'] and status in ['queued', 'unreviewed', 'ready'] and turns < limit)

def scoped_catalog(before, regenerated, states, policy, assessments, key=K):
    old, new = {r['id']: r for r in before}, {r['id']: r for r in regenerated}
    require(len(old) == len(before) and len(new) == len(regenerated) and set(old) == set(new), 'Catalog identity set')
    drift = []
    for identity, row in old.items():
        if identity == key:
            continue
        changes = {f: {'before': row.get(f), 'after': new[identity].get(f)} for f in set(row) | set(new[identity])
                   if f != 'rank' and row.get(f) != new[identity].get(f)}
        if changes:
            require(set(changes) <= {'local_status', 'eligible', 'turns_used'}, 'Unrelated source/score/hold drift')
            state = states.get(identity, {})
            assessment = assessments.get(identity, {})
            status, turns = native_status_turns(row,state,policy,assessment)
            require(new[identity]['local_status'] == status and new[identity]['turns_used'] == turns, 'Unexplained status/turn projection')
            require(new[identity]['holds'] == row['holds'] and
                    new[identity]['eligible'] is expected_eligible(row, state, policy, assessment), 'Unexplained eligibility projection')
            drift.append({'id': identity, 'difference': changes, 'expected_eligible': expected_eligible(row, state, policy, assessment),
                          'baseline_preserved': True, 'explanation': 'unchanged holds, literal native status and policy turn limit'})
    return [dict(new[key]) if r['id'] == key else dict(r) for r in before], drift

def parse_tree(data):
    result = {}
    for raw in data.split(b'\0'):
        if not raw:
            continue
        metadata, path = raw.decode().split('\t', 1)
        mode, kind, blob = metadata.split()
        require(path not in result and kind == 'blob' and mode == '100644', 'Git regular-file mode/type/duplication')
        result[path] = {'mode': mode, 'blob': blob}
    return result

def validate_original_map(auth, tree):
    require(auth.get('source_head') == HEAD and auth.get('incoming_body_count') == 15 and
            auth.get('original_author_effort') == '2/5' and auth.get('literal_status') == 'claimed_solved', 'Original identity')
    require(len(auth['files']) == 15 and len(tree) == 15, 'Original inventory count')
    names, paths = set(), set()
    for entry in auth['files']:
        name = relative(entry['relative_path'])
        path = entry['path']
        require(name not in names and path not in paths and path == N + name, 'Original source/destination map')
        require(entry['Git_mode'] == '100644' and tree.get(path) == {'mode': '100644', 'blob': entry['git_blob_SHA1']}, 'Original Git mode/blob')
        names.add(name); paths.add(path)
    require(names == ORIGINAL_NAMES and paths == set(tree), 'Exact original fifteen-file names')
    return {entry['relative_path']: entry for entry in auth['files']}

def validate_original_queue(qauth, queue):
    require(qauth.get('head') == HEAD and qauth.get('PR') == 108 and qauth.get('literal_status') == 'claimed_solved' and
            qauth.get('original_budget') == '2/5', 'Original queue identity')
    require(len(queue) == qauth['whole_QUEUE_bytes'] and sha(queue) == qauth['whole_QUEUE_sha256'], 'Original whole queue pin')
    row = qauth['selected_row']
    require(sha(row.encode()) == qauth['selected_row_sha256'] and queue.decode().splitlines().count(row) == 1, 'Selected queue row hash/uniqueness')
    cells = row.split('|')
    require(len(cells) == 14 and cells[2].strip() == K + ' / ' + CODE and cells[8].strip() == 'claimed_solved' and
            cells[9].strip() == '2/5', 'Selected queue row target/status/count parse')
    require(hashlib.sha1(b'blob ' + str(len(queue)).encode() + b'\0' + queue).hexdigest() == qauth['QUEUE_git_blob_SHA1'], 'Original queue Git blob SHA1')
    return qauth['selected_row_sha256']

def utc(value):
    require(isinstance(value, str), 'UTC text required')
    stamp = datetime.datetime.fromisoformat(value.replace('Z', '+00:00'))
    require(stamp.utcoffset() == datetime.timedelta(0), 'UTC offset required')
    return stamp

def process_receipt(record, verb, read):
    require(record.get('actual_process_record') is True and type(record.get('PID')) is int and record['PID'] > 0 and
            record.get('exit_code') == 0 and not any(record.get(x) is True for x in ['fixture', 'simulated', 'dry_run']), 'Actual successful GWS process required')
    argv = record['argv']
    require(isinstance(argv, list) and Path(argv[0]).name == 'gws' and argv[1:1 + len(verb)] == verb, 'Exact GWS CLI verb')
    require(all(isinstance(x,str) for x in argv), 'GWS argv strings')
    suffix = argv[1+len(verb):]
    flags = ['--params'] + (['--json'] if verb[-1] == 'append' else [])
    require(len(suffix) == 2*len(flags) and suffix[::2] == flags, 'Exact GWS flags; no dry-run/output/page mutations')
    def flag(name):
        require(argv.count(name) == 1 and argv.index(name) + 1 < len(argv), 'GWS flag missing/duplicate')
        return argv[argv.index(name) + 1]
    params_text = flag('--params')
    require(sha(params_text.encode()) == record['params_sha256'] and len(params_text.encode()) == record['params_bytes'], 'GWS parameter body pin')
    params = loads(params_text)
    require(params['spreadsheetId'] == SHEET, 'Wrong spreadsheet service ID')
    _, stdout = read(record['stdout_pin'])
    _, stderr = read(record['stderr_pin'])
    require(record['stdout_pin'] == record['response_body_pin'] and len(stdout) <= 1024 * 1024 and len(stderr) <= 65536, 'GWS response custody/cap')
    response = loads(stdout)
    start, end = utc(record['UTC_start']), utc(record['UTC_end'])
    require(start <= end, 'GWS process chronology')
    return params, response, start, end, flag

def validate_sheet(receipt, expected, zenodo_end, read):
    require(receipt.get('schema') == 'pr108-actual-gws-sheet-service-receipt/v2' and receipt.get('actual_receipt') is True and
            receipt.get('spreadsheet_id') == SHEET and receipt.get('sheet_id') == GID and receipt.get('sheet_title') == TITLE and
            receipt.get('columns') == COLUMNS and receipt.get('problem_id') == 30003996 and receipt.get('problem_code') == CODE and
            receipt.get('DOI') == expected['DOI'] and not any(receipt.get(x) is True for x in ['fixture', 'simulated', 'dry_run']), 'Actual target-specific Sheet receipt')
    row = receipt['row_index']
    require(type(row) is int and row >= 2 and row == expected['row_index'], 'Actual Sheet row identity')
    selected = "'Math Puzzles'!A" + str(row) + ':D' + str(row)
    values = expected['values']
    require(receipt['range'] == selected and len(values) == 4 and all(isinstance(x, str) and x for x in values) and
            values[2] == 'https://doi.org/' + expected['DOI'] and K + ' / ' + CODE in values[3], 'Exact four target row values/DOI/notes')
    require(all(re.fullmatch(r'https://[^\s]+', values[i]) for i in [0, 1]), 'Original/Solution Chat URLs')
    records = receipt['processes']
    require(set(records) == {'metadata', 'headers', 'write', 'readback', 'independent_readback'}, 'Five Sheet custody operations required')
    pids = [records[x]['PID'] for x in records]
    require(len(set(pids)) == len(pids), 'Distinct actual Sheet process identities required')
    meta = process_receipt(records['metadata'], ['sheets', 'spreadsheets', 'get'], read)
    require(set(meta[0]) == {'spreadsheetId'} and meta[2] >= utc(zenodo_end) and meta[1]['spreadsheetId'] == SHEET and
            any(s['properties']['sheetId'] == GID and s['properties']['title'] == TITLE for s in meta[1]['sheets']), 'Post-Zenodo exact Sheet metadata')
    headers = process_receipt(records['headers'], ['sheets', 'spreadsheets', 'values', 'get'], read)
    require(set(headers[0]) == {'spreadsheetId','range'} and headers[0]['range'] == "'Math Puzzles'!A1:D1" and headers[1]['values'] == [COLUMNS] and headers[2] >= meta[3], 'Exact Sheet columns/header read')
    write = process_receipt(records['write'], ['sheets', 'spreadsheets', 'values', 'append'], read)
    body_text = write[4]('--json')
    _, body = read(records['write']['request_body_pin'])
    require(set(write[0]) == {'spreadsheetId','range','valueInputOption','insertDataOption','includeValuesInResponse'} and
            write[0]['insertDataOption']=='INSERT_ROWS' and write[0]['includeValuesInResponse'] is True and
            body == body_text.encode() and set(loads(body)) == {'values','majorDimension'} and loads(body)['majorDimension']=='ROWS' and loads(body)['values'] == [values] and
            write[0]['range'] == "'Math Puzzles'!A:D" and write[0]['valueInputOption'] == 'RAW' and
            write[2] >= headers[3] and write[2] >= utc(zenodo_end), 'Actual exact-row post-Zenodo append body/time')
    updates = write[1]['updates']
    require(write[1]['spreadsheetId'] == SHEET and updates['updatedRange'] == selected and
            updates['updatedRows'] == 1 and updates['updatedColumns'] == 4 and updates['updatedCells'] == 4, 'Actual appended Sheet row result')
    previous = write[3]
    for role in ['readback', 'independent_readback']:
        result = process_receipt(records[role], ['sheets', 'spreadsheets', 'values', 'get'], read)
        require(set(result[0]) == {'spreadsheetId','range'} and result[0]['range'] == selected and result[1]['range'] == selected and result[1]['values'] == [values] and
                result[2] >= previous and result[2] >= utc(zenodo_end), 'Actual exact-row Sheet readback/time')
        previous = result[3]
    require(receipt.get('independent_service_authentication_required') is True, 'Sheet service authentication obligation')
    return {'spreadsheet_id': SHEET, 'sheet_id': GID, 'row_index': row, 'range': selected,
            'DOI': expected['DOI'], 'actual_write_readback_receipts_checked': True,
            'independent_service_authentication_must_be_bound_by_final_root_gate': True}

def capacity_inventory(base_pins, copy_artifacts, gates, package, policy, process_policy):
    """Conservative maxima for ALL files, plus one exclusive atomic-write slot."""
    require(set(policy) == {'headroom_bytes', 'max_artifact_count', 'max_materialized_bytes', 'wrapper_bytes_cap',
                            'receipt_json_bytes_cap', 'per_native_growth_bytes', 'max_package_files',
                            'future_commit_overhead_bytes','runtime_overhead_bytes'}, 'Capacity policy fields')
    require(all(type(v) is int and v>=1 for v in policy.values()),'Positive integer capacity limits')
    require(32*1024*1024 <= policy['headroom_bytes'] <= 64*1024*1024 and policy['max_artifact_count'] <= 512 and
            policy['max_materialized_bytes'] <= 160*1024*1024 and policy['wrapper_bytes_cap'] <= 65536 and
            policy['receipt_json_bytes_cap'] == 128*1024 and policy['per_native_growth_bytes'] <= 512*1024 and
            policy['future_commit_overhead_bytes']>=8*1024*1024 and policy['runtime_overhead_bytes']>=8*1024*1024 and
            policy['max_package_files'] <= 64 and len(package) <= policy['max_package_files'], 'Capacity count/headroom/bytes cap')
    entries = []
    mutable = {'catalog.json', 'assessments.json', 'state.json', 'history.jsonl', 'assessment_history.jsonl',
               'ranking.csv', 'summary.json', 'SHORTLIST.md', 'QUEUE.md'}
    for spec in base_pins:
        name = Path(spec['path']).name
        cap = spec['bytes'] + (policy['per_native_growth_bytes'] if name in mutable else 0)
        entries.append({'path': 'private_native_backend/' + name, 'max_bytes': cap, 'kind': 'native_output_or_baseline'})
        if name in mutable:
            entries.append({'path': 'bundle/unsolved_math_prioritization/' + name, 'max_bytes': cap, 'kind': 'candidate_global'})
    for path, size in copy_artifacts:
        entries.append({'path': path, 'max_bytes': size, 'kind': 'exact_copy'})
    for role, spec in gates.items():
        require(spec['bytes'] <= 65536, 'Gate file size cap')
        entries.append({'path': 'bundle/' + N + 'publication/gates/' + role + '.json', 'max_bytes': spec['bytes'], 'kind': 'gate_copy'})
    for name, data in package.items():
        entries.append({'path': 'bundle/' + N + 'publication/package/' + relative(name), 'max_bytes': len(data), 'kind': 'package_copy'})
    # Generated fixed wrappers, candidate manifests and worker control/result/failure.
    for name in ['private_native_backend/assessment.json', 'WORKER_CONTROL.json', 'WORKER_RESULT.json',
                 'PREPARE_FAILURE.json', 'CANDIDATE_RECEIPT.json', 'EXECUTION_INPUTS.json', 'CONFIG.json',
                 'CAPACITY_PLAN.json', 'PROCESS_JOURNAL.json']:
        entries.append({'path': name, 'max_bytes': policy['receipt_json_bytes_cap'], 'kind': 'generated_metadata'})
    for name in ['IMPORT_BASELINE.json', 'HISTORICAL_DESK_ASSESSMENT.json', 'assessment.json', 'PUBLICATION_EVIDENCE.json',
                 'README.md', 'RESEARCH_LOG.md', 'publication/GOOGLE_SHEET_SERVICE_RECEIPT.json']:
        entries.append({'path': 'bundle/' + N + name, 'max_bytes': policy['wrapper_bytes_cap'], 'kind': 'generated_wrapper'})
    for i in range(process_policy['max_process_count']):
        for stream in ['stdout', 'stderr']:
            entries.append({'path': 'process_receipts/' + str(i) + '.' + stream + '.bin',
                            'max_bytes': process_policy['retain_bytes_per_stream'], 'kind': 'bounded_process_stream'})
    require(len({x['path'] for x in entries}) == len(entries), 'Materialization destination collision')
    require(len(entries)+1 <= policy['max_artifact_count'], 'Materialized artifact count cap including exclusive temporary slot')
    atomic = max(x['max_bytes'] for x in entries if x['path'].startswith('private_native_backend/') and
                 Path(x['path']).name in ['catalog.json', 'assessments.json', 'state.json', 'summary.json'])
    materialized = sum(x['max_bytes'] for x in entries) + atomic
    require(materialized <= policy['max_materialized_bytes'], 'Aggregate materialized capacity cap')
    return {'entries': entries, 'exclusive_atomic_write_slot_max_bytes': atomic,
            'exclusive_atomic_write_slot_names': ['catalog.json.tmp', 'assessments.json.tmp', 'state.json.tmp', 'summary.json.tmp'],
            'max_materialized_bytes': materialized, 'headroom_bytes': policy['headroom_bytes'],
            'future_commit_overhead_bytes':policy['future_commit_overhead_bytes'],'runtime_overhead_bytes':policy['runtime_overhead_bytes'],
            'required_free_bytes': materialized + policy['headroom_bytes']+policy['future_commit_overhead_bytes']+policy['runtime_overhead_bytes'], 'file_count_cap': len(entries) + 1,
            'no_SQL_copy_or_download': True}
