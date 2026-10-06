#!/usr/bin/env python3
"""DRAFT: future gated PR108 review bundle only; never exports, stages or publishes.

The real prepare entry point has NOT been run. Tests exercise only pure functions.
Run only after a fresh independent pre-execution review and explicit commissioning.
"""
from pathlib import Path, PurePosixPath
import argparse, contextlib, csv, datetime, hashlib, importlib.util, io, json
import os, shutil, sqlite3, stat, subprocess, sys, types, zipfile

D = Path(__file__).resolve().parent
A = D.parent
C = A.parents[2]
R = Path('/Users/alec/Documents/Math')
K = '30003996'
CODE = 'OWR-16633-013'
P = 'unsolved_math_prioritization/'
N = P + 'attempts/' + K + '/'
HEAD = '3526d46bf143b08e5055ffa7728c6278e9f958ea'
REV = '37e53eabe540fb458758e198be61634bd02ee008'
REVIEW = '9a2816afbdd3750d36f550dc6e91c7201aa024344a7b83fdb420aafe6c86df0d'
STATEMENT = '65c107bf152773ed079cc344cfcf853c4f7da15a10453ca6f7fb411bbf5aab97'
PROOF = '2818eab189445649ae1ba98d55e3da3e5fab918de88f1779de86962ba99a3393'
ORIGINAL_PROOF = '1a6c267c6240b66c1d804397f4bbbe246f5b6147c3930e1a68396e60b618d615'
ORIGINAL = A / 'original_source_authentication_20261006'
BASE_NAMES = ['queue.py', 'manifest.json', 'policy.json', 'catalog.json', 'assessments.json',
              'state.json', 'history.jsonl', 'assessment_history.jsonl', 'ranking.csv',
              'summary.json', 'SHORTLIST.md', 'QUEUE.md']
EXPORT = ['assessments.json', 'state.json', 'history.jsonl', 'assessment_history.jsonl',
          'catalog.json', 'ranking.csv', 'summary.json', 'SHORTLIST.md', 'QUEUE.md']

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def require(ok, message):
    if not ok:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def encode(obj):
    return (json.dumps(obj, indent=2, ensure_ascii=False) + '\n').encode()

def rel(value):
    require(isinstance(value, str) and value and '\\' not in value and '\n' not in value,
            'Invalid relative path')
    path = PurePosixPath(value)
    require(not path.is_absolute() and '..' not in path.parts and str(path) == value,
            'Noncanonical or escaping path')
    return value

def regular(path):
    require(path.is_absolute(), 'Absolute internal path required')
    for parent in [*path.parents, path]:
        require(not parent.is_symlink(), 'Symlink input: ' + str(parent))
    mode = path.stat().st_mode
    require(stat.S_ISREG(mode), 'Not a regular file: ' + str(path))
    return path

def input_file(spec, allowed_root=A):
    require(set(spec) == {'path', 'bytes', 'sha256'}, 'A pin needs exactly path, bytes, sha256')
    require(type(spec['bytes']) is int and 0 <= spec['bytes'] <= 50 * 1024 * 1024, 'Pinned artifact exceeds bounded read budget')
    path = C / rel(spec['path'])
    require(path.is_relative_to(allowed_root), 'Input outside allowed root')
    require(regular(path).stat().st_size == spec['bytes'], 'Input byte size mismatch')
    data = regular(path).read_bytes()
    require(type(spec['bytes']) is int and len(data) == spec['bytes'] and sha(data) == spec['sha256'],
            'Input pin mismatch: ' + str(path))
    return path, data

def zip_member(archive, name, expected_size):
    """Inspect an explicit ZIP member in memory. Never extract a filesystem path."""
    rel(name)
    require(len(archive) <= 50 * 1024 * 1024, 'ZIP transport exceeds bounded read budget')
    with zipfile.ZipFile(io.BytesIO(archive)) as bundle:
        entries = bundle.infolist()
        require(len(entries) <= 10000, 'Too many ZIP transport entries')
        matches = [entry for entry in entries if entry.filename == name]
        require(len(matches) == 1, 'ZIP member missing or duplicated')
        entry = matches[0]
        mode = entry.external_attr >> 16
        require(not entry.is_dir() and not stat.S_ISLNK(mode) and
                (stat.S_IFMT(mode) in [0, stat.S_IFREG]) and not entry.flag_bits & 1 and
                entry.file_size == expected_size, 'ZIP member type/encryption/size invalid')
        return bundle.read(entry)

def file_pin(path):
    h = hashlib.sha256()
    with regular(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return {'bytes': path.stat().st_size, 'sha256': h.hexdigest()}

def rows_by_id(rows):
    result = {r['id']: r for r in rows}
    require(len(result) == len(rows), 'Duplicate catalog IDs')
    return result

def scoped_catalog(before, regenerated, states, key=K):
    """Retain every unrelated baseline row, including rank and list position."""
    old, new = rows_by_id(before), rows_by_id(regenerated)
    require(set(old) == set(new), 'Catalog identity set changed')
    drift = []
    for identity, row in old.items():
        if identity == key:
            continue
        changes = {f: {'before': row.get(f), 'after': new[identity].get(f)}
                   for f in set(row) | set(new[identity])
                   if f != 'rank' and row.get(f) != new[identity].get(f)}
        if changes:
            require(set(changes) <= {'local_status', 'eligible', 'turns_used'},
                    'Unexpected unrelated source/score/hold drift: ' + identity)
            state = states.get(identity, {})
            require(new[identity]['local_status'] == state.get('status') and
                    new[identity]['turns_used'] == state.get('turns_used', 0),
                    'Unexplained unrelated state projection: ' + identity)
            drift.append({'id': identity, 'difference': changes, 'baseline_preserved': True})
    result = [dict(new[key]) if row['id'] == key else dict(row) for row in before]
    require(all(row == old[row['id']] for row in result if row['id'] != key),
            'Unrelated catalog overwrite')
    return result, drift

def campaign_overlay(data, note, doi):
    require(isinstance(note, str) and len(note.split()) >= 8 and '|' not in note and
            '\n' not in note and '\r' not in note, 'Invalid campaign note')
    lines = data.decode().splitlines(keepends=True)
    indices = [i for i, line in enumerate(lines) if '| ' + K + ' / ' + CODE + ' |' in line]
    require(len(indices) == 1, 'Campaign target row must be unique')
    index = indices[0]
    ending = '\r\n' if lines[index].endswith('\r\n') else '\n' if lines[index].endswith('\n') else ''
    cells = lines[index].rstrip('\r\n').split('|')
    require(len(cells) == 14 and cells[8].strip() == 'queued' and cells[9].strip() == '0/5' and
            not cells[12].strip(), 'Unexpected baseline campaign row')
    cells[8], cells[9], cells[11], cells[12] = ' claimed_solved ', ' 2/5 ', ' ' + note + ' ', ' https://doi.org/' + doi + ' '
    result = list(lines)
    result[index] = '|'.join(cells) + ending
    require(all(a == b for i, (a, b) in enumerate(zip(lines, result)) if i != index),
            'Unrelated campaign bytes changed')
    return ''.join(result).encode()

def csv_overlay(data, target):
    lines = data.decode().splitlines(keepends=True)
    reader = csv.reader(io.StringIO(data.decode(), newline=''))
    fields = next(reader)
    identity_index = fields.index('id')
    indices = []
    start = reader.line_num
    for record in reader:
        end = reader.line_num
        require(len(record) == len(fields), 'Malformed ranking CSV row')
        if record[identity_index] == K:
            indices.append((start, end))
        start = end
    require(len(indices) == 1, 'Ranking target row must be unique')
    start, end = indices[0]
    output = io.StringIO(newline='')
    ending = '\r\n' if lines[end - 1].endswith('\r\n') else '\n' if lines[end - 1].endswith('\n') else ''
    writer = csv.DictWriter(output, fieldnames=fields, extrasaction='ignore', lineterminator=ending)
    writer.writerow({**target, 'holds': '; '.join(target['holds']), 'reasons': '; '.join(target['reasons'])})
    return (''.join(lines[:start]) + output.getvalue() + ''.join(lines[end:])).encode()

def validate_gate(obj, role, package_manifest_sha):
    require(isinstance(obj, dict) and obj.get('schema') == 'pr108-publication-root-gate/v1', 'Gate schema')
    require(obj.get('role') == role and obj.get('PR') == 108 and obj.get('problem_id') == 30003996,
            'Gate identity/role')
    for field, expected in [('original_head', HEAD), ('review_hash', REVIEW),
                            ('statement_hash', STATEMENT), ('effective_proof_sha256', PROOF),
                            ('package_manifest_sha256', package_manifest_sha)]:
        require(obj.get(field) == expected, 'Gate binding: ' + field)
    require(obj.get('actual_root_review') is True and obj.get('clearance') is True,
            'Missing actual root clearance: ' + role)
    require(obj.get('fixture') is not True and obj.get('simulated') is not True and obj.get('dry_run') is not True,
            'Fixture/simulation cannot authorize integration')
    require(obj.get('new_central_proof_search_turns') == 0 and obj.get('original_budget') == '2/5',
            'Effort gate')
    require(isinstance(obj.get('UTC'), str) and isinstance(obj.get('exact_claim'), str) and
            obj['exact_claim'].strip() and obj.get('checked_artifacts'), 'Review content missing')
    timestamp = datetime.datetime.fromisoformat(obj['UTC'].replace('Z', '+00:00'))
    require(timestamp.utcoffset() == datetime.timedelta(0) and
            timestamp <= datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5),
            'Review UTC invalid or in future')
    requirements = {'mathematics': ['mathematical_clearance'],
                    'priority': ['priority_clearance', 'substantive_novelty_established'],
                    'package': ['package_clearance', 'metadata_and_attribution_checked'],
                    'pre_execution_adversary': ['native_scope_and_invariants_checked'],
                    'final': ['mathematical_clearance', 'priority_clearance', 'package_clearance',
                              'native_integration_clearance', 'pre_execution_adversary_clearance']}
    require(all(obj.get(field) is True for field in requirements[role]), 'Role clearance missing: ' + role)

class Reader:
    def __init__(self):
        self.records = []
        self.output = None

    def run(self, argv, retain=True):
        start = now()
        process = subprocess.Popen(argv, cwd=C, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        record = {'argv': argv, 'cwd': str(C), 'PID': process.pid, 'UTC_start': start,
                  'UTC_end': now(), 'exit_code': process.returncode, 'stdout_bytes': len(out),
                  'stdout_sha256': sha(out), 'stderr_bytes': len(err), 'stderr_sha256': sha(err),
                  'stdout_retained': retain}
        self.records.append((record, out if retain else None, err))
        if self.output:
            self.flush()
        require(process.returncode == 0, err.decode('utf8', 'replace')[:1200])
        return out

    def git(self, *args, retain=True):
        return self.run(['/usr/bin/git', *args], retain=retain)

    def flush(self):
        receipts = self.output / 'process_receipts'
        receipts.mkdir(exist_ok=True)
        journal = []
        for index, (record, out, err) in enumerate(self.records):
            rec = dict(record)
            rec['stdout_file'] = 'process_receipts/' + str(index) + '.stdout.bin' if out is not None else None
            rec['stderr_file'] = 'process_receipts/' + str(index) + '.stderr.bin'
            if out is not None:
                (self.output / rec['stdout_file']).write_bytes(out)
            (self.output / rec['stderr_file']).write_bytes(err)
            journal.append(rec)
        (self.output / 'PROCESS_JOURNAL.json').write_bytes(encode({'actual_operator_PID': os.getpid(), 'records': journal}))

def prepare(config_path):
    cfg_bytes = regular(config_path.absolute()).read_bytes()
    cfg = json.loads(cfg_bytes)
    require(cfg.get('schema') == 'pr108-native-publication-integration-config/v1' and
            cfg.get('mode') == 'review_bundle_only', 'Explicit review-bundle configuration required')
    require(cfg.get('template_only') is not True, 'Template configuration cannot run')
    require(cfg.get('commissioned_after_independent_review') is True, 'Not commissioned')
    reader = Reader()
    base = reader.git('rev-parse', 'HEAD').decode().strip()
    require(reader.git('symbolic-ref', '--short', 'HEAD').strip() == b'main', 'Not main')
    require(cfg.get('main_parent') == base, 'Main parent advanced; reconcile and renew gates')
    require(reader.git('ls-remote', 'https://github.com/AlecKriebel/Math.git', 'refs/heads/main').decode().split()[0] == base,
            'Remote main parent differs')
    live = json.loads(reader.run(['gh', 'pr', 'view', '108', '--repo', 'AlecKriebel/Math', '--json',
                                 'number,state,isDraft,headRefName,headRefOid,baseRefName,url']))
    require(live == {'number': 108, 'state': 'OPEN', 'isDraft': True, 'headRefName': 'dot/math-30003996',
                     'headRefOid': HEAD, 'baseRefName': 'main', 'url': 'https://github.com/AlecKriebel/Math/pull/108'},
            'Live PR changed; no automatic rebase or merge')
    require(not reader.git('ls-tree', '-r', '--name-only', base, '--', N) and not (C / N).exists(),
            'Native attempt exists; explicit separate reconciliation required')
    before = {name: reader.git('show', base + ':' + P + name, retain=name not in
                              ['catalog.json', 'assessments.json', 'QUEUE.md', 'ranking.csv', 'SHORTLIST.md'])
              for name in BASE_NAMES}
    require(sha(before['queue.py']) == cfg.get('queue_py_sha256'), 'Pinned native queue code changed')
    for name, data in before.items():
        local = C / P / name
        require(not local.is_symlink() and (not local.exists() or regular(local).read_bytes() == data),
                'Unknown native worktree edit: ' + name)
    package_root = C / rel(cfg['package']['root'])
    require(package_root.is_relative_to(A) and not package_root.is_relative_to(D), 'Package root must be a separate PR108 audit package')
    _, package_bytes = input_file(cfg['package']['manifest'])
    package_manifest_sha = sha(package_bytes)
    package = json.loads(package_bytes)
    require(package.get('schema') == 'pr108-publication-package-manifest/v1' and
            package.get('PR') == 108 and package.get('problem_id') == 30003996 and
            package.get('original_head') == HEAD and package.get('review_hash') == REVIEW and
            package.get('dataset_revision') == REV and package.get('imported_prior_report') == {} and
            package.get('author_orcid') == 'https://orcid.org/0009-0001-9320-500X' and
            package.get('effective_proof_sha256') == PROOF and package.get('files'), 'Package manifest binding')
    require(sum(x['bytes'] for x in package['files']) <= 50 * 1024 * 1024, 'Package exceeds bounded artifact budget')
    package_files = {}
    for spec in package['files']:
        name = rel(spec['relative_path'])
        require(name not in package_files, 'Duplicate package destination')
        path = package_root / name
        require(path.is_relative_to(package_root), 'Package escape')
        require(type(spec['bytes']) is int and spec['bytes'] >= 0 and regular(path).stat().st_size == spec['bytes'], 'Package size mismatch')
        data = regular(path).read_bytes()
        require(len(data) == spec['bytes'] and sha(data) == spec['sha256'], 'Package file pin mismatch')
        package_files[name] = data
    require(any(sha(data) == PROOF for data in package_files.values()), 'Package omits the exact effective proof source')
    gates = {}
    gate_bytes = {}
    for role in ['mathematics', 'priority', 'package', 'pre_execution_adversary', 'final']:
        _, data = input_file(cfg['gates'][role])
        gates[role] = json.loads(data)
        validate_gate(gates[role], role, package_manifest_sha)
        require(gates[role].get('main_parent') == base, 'Gate main-parent stale')
        for artifact in gates[role]['checked_artifacts']:
            input_file(artifact)
        gate_bytes[role] = data
    require(len({g['exact_claim'] for g in gates.values()}) == 1, 'Gate exact claims disagree')
    require(gates['pre_execution_adversary'].get('reviewed_helper_sha256') == file_pin(Path(__file__).resolve())['sha256'],
            'Pre-execution adversary did not review these exact helper bytes')
    require(gates['final'].get('gate_sha256') == {role: sha(data) for role, data in gate_bytes.items() if role != 'final'},
            'Final root gate does not bind the four antecedent gate files')
    _, publication_bytes = input_file(cfg['publication']['receipt'])
    publication = json.loads(publication_bytes)
    doi = publication.get('DOI', '')
    import re
    require(re.fullmatch(r'10\.5281/zenodo\.[1-9][0-9]*', doi) is not None, 'Actual Zenodo DOI missing')
    record_id = doi.rsplit('.', 1)[1]
    require(publication.get('schema') == 'pr108-actual-publication-receipt/v1' and
            publication.get('actual_receipt') is True and publication.get('PR') == 108 and
            publication.get('problem_id') == 30003996 and publication.get('published') is True and
            publication.get('original_head') == HEAD and publication.get('effective_proof_sha256') == PROOF and
            publication.get('package_manifest_sha256') == package_manifest_sha, 'Actual publication receipt binding')
    require(not any(publication.get(field) is True for field in ['fixture', 'simulated', 'dry_run']),
            'Fixture publication receipt forbidden')
    _, response_bytes = input_file(publication['metadata_response'])
    response = json.loads(response_bytes)
    require(publication.get('HTTP_method') == 'GET' and publication.get('status_code') == 200 and
            publication.get('URL') == 'https://zenodo.org/api/records/' + record_id and
            str(response.get('id')) == record_id and response.get('doi') == doi and
            (response.get('submitted') is True or response.get('is_published') is True),
            'Published DOI metadata receipt inconsistent')
    payload_receipts = {}
    require(isinstance(publication.get('payload_readbacks'), list), 'Actual published payload readbacks missing')
    for readback in publication['payload_readbacks']:
        name = rel(readback['relative_path'])
        require(name in package_files and name not in payload_receipts, 'Payload readback identity/duplication')
        _, downloaded = input_file(readback['downloaded_file'])
        require(downloaded == package_files[name], 'Published payload differs from frozen package')
        transport = readback.get('transport')
        require(transport in ['individual_file', 'zip_member'], 'Explicit published transport mode required')
        transport_bytes = downloaded
        if transport == 'zip_member':
            _, transport_bytes = input_file(readback['archive_file'])
            require(zip_member(transport_bytes, readback['member_path'], len(downloaded)) == downloaded,
                    'Published ZIP member differs from authenticated package')
        _, request_bytes = input_file(readback['HTTP_GET_receipt'])
        request = json.loads(request_bytes)
        require(request.get('actual_receipt') is True and request.get('HTTP_method') == 'GET' and
                request.get('status_code') == 200 and request.get('exit_code') == 0 and
                request.get('URL', '').startswith('https://zenodo.org/records/' + record_id + '/files/') and
                request.get('response_bytes') == len(transport_bytes) and request.get('response_sha256') == sha(transport_bytes) and
                not any(request.get(field) is True for field in ['fixture', 'simulated', 'dry_run']),
                'Published payload HTTP readback receipt inconsistent')
        payload_receipts[name] = request_bytes
    require(set(payload_receipts) == set(package_files), 'Incomplete actual published payload verification')
    _, tracker_bytes = input_file(cfg['publication']['tracker_receipt'])
    tracker = json.loads(tracker_bytes)
    tracker_path = rel(tracker['tracker_path'])
    require(tracker.get('schema') == 'pr108-actual-tracker-readback/v1' and tracker.get('actual_receipt') is True and
            tracker.get('PR') == 108 and tracker.get('problem_id') == 30003996 and tracker.get('DOI') == doi and
            tracker.get('package_manifest_sha256') == package_manifest_sha and tracker.get('git_commit') == base,
            'Actual tracker readback missing or stale')
    require(not any(tracker.get(field) is True for field in ['fixture', 'simulated', 'dry_run']),
            'Fixture tracker receipt forbidden')
    require(tracker_path in cfg['publication']['allowed_tracker_paths'], 'Tracker path not explicitly selected')
    tracker_blob = reader.git('show', base + ':' + tracker_path, retain=False)
    require(len(tracker_blob) == tracker['bytes'] and sha(tracker_blob) == tracker['sha256'] and
            isinstance(tracker.get('exact_row'), str) and K in tracker['exact_row'] and doi in tracker['exact_row'] and
            tracker_blob.decode().splitlines().count(tracker['exact_row']) == 1, 'Tracker exact row mismatch')
    auth = json.loads(regular(ORIGINAL / 'ORIGINAL_BLOB_MANIFEST.json').read_bytes())
    qauth = json.loads(regular(ORIGINAL / 'QUEUE_STATUS_PROJECTION.json').read_bytes())
    require(auth['source_head'] == HEAD and auth['incoming_body_count'] == 15 and auth['original_author_effort'] == '2/5' and
            qauth['head'] == HEAD and qauth['literal_status'] == 'claimed_solved' and qauth['original_budget'] == '2/5',
            'Original authentication metadata changed')
    original_files = {}
    inventory = reader.git('ls-tree', '-r', '--name-only', HEAD, '--', N).decode().splitlines()
    require(sorted(inventory) == sorted(x['path'] for x in auth['files']) and len(inventory) == 15,
            'Original head inventory differs')
    for entry in auth['files']:
        name = rel(entry['relative_path'])
        data = regular(ORIGINAL / 'original_attempt' / name).read_bytes()
        require(len(data) == entry['bytes'] and sha(data) == entry['sha256'] and
                data == reader.git('show', HEAD + ':' + entry['path']), 'Original byte authentication failed')
        original_files[name] = data
    require('status.json' not in original_files and 'turns.jsonl' not in original_files and
            sha(original_files['PROOF.md']) == ORIGINAL_PROOF, 'Original structured ledger/proof premise failed')
    original_queue = reader.git('show', HEAD + ':' + P + 'QUEUE.md', retain=False)
    require(len(original_queue) == qauth['whole_QUEUE_bytes'] and sha(original_queue) == qauth['whole_QUEUE_sha256'] and
            original_queue.decode().splitlines().count(qauth['selected_row']) == 1, 'Original queue authentication failed')
    manifest = json.loads(before['manifest.json'])
    require(manifest['revision'] == REV, 'Immutable source revision changed')
    source_cache = R / P / 'cache/catalog.sqlite'
    require(not any(Path(str(source_cache) + suffix).exists() for suffix in ['-wal', '-shm', '-journal']),
            'SQL writer artifacts present; stop for single-writer reconciliation')
    cache_pin = file_pin(source_cache)
    require(cache_pin == cfg['source_cache_pin'], 'Source SQL cache pin mismatch')
    for name in ['problems.json', 'research_results.json']:
        require(file_pin(R / P / 'cache' / name) == manifest['files'][name], 'Raw immutable source bytes changed')
    def readonly_db():
        return sqlite3.connect('file:' + str(source_cache) + '?mode=ro&immutable=1', uri=True)
    db = readonly_db()
    require(db.execute('SELECT revision FROM metadata').fetchone() == (REV,) and
            db.execute('SELECT count(*) FROM records').fetchone()[0] == manifest['records'], 'SQL revision/count mismatch')
    raw, prior = db.execute('SELECT payload,report FROM records WHERE key=?', (K,)).fetchone()
    db.close()
    problem, imported = json.loads(raw), json.loads(prior)
    require(imported == json.loads(regular(ORIGINAL / 'SELECTED_IMPORTED_PRIOR_REPORT.json').read_bytes()) == {} and
            problem == json.loads(original_files['source_record.json']) and
            sha(json.dumps([problem, imported], sort_keys=True).encode()) == REVIEW and
            sha(problem['statement'].encode()) == STATEMENT, 'Source-pair/empty-imported-report mismatch')
    oldrows = json.loads(before['catalog.json'])
    row = rows_by_id(oldrows)[K]
    oldass, oldstate = json.loads(before['assessments.json']), json.loads(before['state.json'])
    require(K not in oldstate and row['local_status'] == 'queued' and row['turns_used'] == 0 and
            row['review_hash'] == REVIEW and row['statement_hash'] == STATEMENT, 'Target baseline needs separate reconciliation')
    assessment = {**oldass[K], **cfg['assessment']}
    require(assessment.get('review_hash') == REVIEW and assessment.get('review_policy') == '2.0-five-turn-proof' and
            assessment.get('route') == oldass[K]['route'] and assessment.get('decision') == oldass[K]['decision'] and
            all(assessment.get(f) == oldass[K][f] for f in ['impact', 'p_solve', 'p_valid_open']) and
            assessment.get('resolution') == oldass[K].get('resolution') and
            assessment.get('holds', []) == oldass[K].get('holds', []) and
            assessment.get('clear_holds', {}) == oldass[K].get('clear_holds', {}),
            'Scores/resolutions/holds cannot be silently changed by publication integration')
    effective = {}
    effective_pins = {}
    for pin in cfg['effective_diagnostics_pins']:
        path, data = input_file(pin)
        require(path.is_relative_to(A / 'repaired_diagnostics_v1'), 'Effective diagnostic pin outside v1')
        name = str(path.relative_to(A / 'repaired_diagnostics_v1'))
        require(name not in effective_pins, 'Duplicate effective diagnostic pin')
        effective_pins[name] = data
    for path in sorted((A / 'repaired_diagnostics_v1').rglob('*')):
        if path.is_file():
            effective[str(path.relative_to(A / 'repaired_diagnostics_v1'))] = regular(path).read_bytes()
    require(effective == effective_pins and sha(effective['PROOF.md']) == PROOF and
            sha(effective['verify.py']) == '46173f3fa54eae9da12a0525494b7d73d1544980cefea9040f8341340cf7385e' and
            sha(effective['independent_review/independent_checks.py']) == 'a298835e88bf4a6528d3ff3d39f6036a5edfb4e6dc525cae13f3f9f631357a7c',
            'Effective proof/diagnostic inventory changed')
    needed_bytes = 3 * sum(map(len, before.values())) + 3 * sum(map(len, package_files.values())) + 1024 * 1024
    require(shutil.disk_usage(D).free > needed_bytes, 'Insufficient space; no backend copy/download fallback')
    output = D / ('candidate_' + sha(cfg_bytes)[:16])
    output.mkdir(exist_ok=False)
    reader.output = output
    reader.flush()
    backend = output / 'private_native_backend'
    backend.mkdir()
    for name, data in before.items():
        (backend / name).write_bytes(data)
    baseline = {'schema': 'pr108-dated-native-import-baseline/v1', 'at': now(), 'id': K,
                'status': 'claimed_solved', 'turns_used': 2, 'review_hash': REVIEW, 'statement_hash': STATEMENT,
                'original_budget': '2/5', 'original_structured_ledger_present': False,
                'original_effort_provenance': 'Authenticated original QUEUE plus two-approach prose; imported count only.',
                'new_central_proof_search_turns': 0, 'original_head': HEAD,
                'original_queue_selected_row_sha256': qauth['selected_row_sha256'],
                'original_research_log_sha256': sha(original_files['RESEARCH_LOG.md']),
                'note': 'Dated native import of historical author count; this is not a recovered original structured event.'}
    states = {**oldstate, K: baseline}
    (backend / 'state.json').write_bytes(encode(states))
    with (backend / 'history.jsonl').open('ab') as stream:
        stream.write((json.dumps({**baseline, 'event': 'dated_import_of_authenticated_historical_author_count'}, ensure_ascii=False) + '\n').encode())
    assessment.update(original_budget='2/5', new_central_proof_search_turns=0,
                      original_structured_ledger_present=False, publication_DOI=doi,
                      package_manifest_sha256=package_manifest_sha)
    (backend / 'assessment.json').write_bytes(encode(assessment))
    spec = importlib.util.spec_from_file_location('pr108_pinned_native_queue', backend / 'queue.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.ROOT = backend
    mod.connect = readonly_db
    def readonly_require_cache():
        conn = readonly_db()
        try:
            require(conn.execute('SELECT revision FROM metadata').fetchone() == (REV,) and
                    conn.execute('SELECT count(*) FROM records').fetchone()[0] == manifest['records'], 'SQL changed')
        finally:
            conn.close()
    mod.require_cache = readonly_require_cache
    start = now()
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        mod.assess(types.SimpleNamespace(id=K, file=str(backend / 'assessment.json')))
    (output / 'NATIVE_ASSESS_CALL.json').write_bytes(encode({'actual_operator_PID': os.getpid(), 'UTC_start': start,
        'UTC_end': now(), 'native_function': 'queue.py:assess', 'queue_py_sha256': sha(before['queue.py']),
        'ROOT': str(backend), 'SQL_connection': 'mode=ro&immutable=1; connect/require_cache overrides only',
        'native_status_command_called': False, 'native_assess_returned_without_exception': True,
        'stdout': stdout.getvalue()}))
    afterass, afterstate = json.loads((backend / 'assessments.json').read_bytes()), json.loads((backend / 'state.json').read_bytes())
    require({k: v for k, v in afterass.items() if k != K} == {k: v for k, v in oldass.items() if k != K}, 'Unrelated assessment changed')
    require(afterstate == states, 'Native assess changed any state')
    for name in ['history.jsonl', 'assessment_history.jsonl']:
        require(not before[name] or before[name].endswith(b'\n'), 'Historical ledger lacks terminal newline')
        require((backend / name).read_bytes().startswith(before[name]), 'Historical prefix changed')
        extra = (backend / name).read_bytes()[len(before[name]):].decode().splitlines()
        require(len(extra) == 1 and json.loads(extra[0])['id'] == K, 'Appended event scope/count differs')
    regenerated = json.loads((backend / 'catalog.json').read_bytes())
    target = rows_by_id(regenerated)[K]
    require(target['local_status'] == 'claimed_solved' and target['turns_used'] == 2 and
            target['review_hash'] == REVIEW and target['statement_hash'] == STATEMENT and not target['eligible'], 'Target projection failed')
    rows, drift = scoped_catalog(oldrows, regenerated, states)
    (backend / 'catalog.json').write_bytes(encode(rows))
    (backend / 'ranking.csv').write_bytes(csv_overlay(before['ranking.csv'], target))
    # Preserve the established campaign table and all non-target row bytes/scores.
    (backend / 'QUEUE.md').write_bytes(campaign_overlay(before['QUEUE.md'], cfg['campaign_note'], doi))
    require(('## ' + K + ' —').encode() not in before['SHORTLIST.md'], 'Target shortlist block requires separately reviewed overlay')
    (backend / 'SHORTLIST.md').write_bytes(before['SHORTLIST.md'])
    summary = json.loads(before['summary.json'])
    summary['eligible'] = sum(x['eligible'] for x in rows)
    summary['records'] = len(rows)
    summary['assessed'] = len(afterass)
    import collections
    summary['holds'] = dict(collections.Counter(h.split(':')[0] for x in rows for h in x['holds']))
    (backend / 'summary.json').write_bytes(encode(summary))
    require(file_pin(source_cache) == cache_pin, 'Shared SQL cache changed during prepare')
    require(reader.git('rev-parse', 'HEAD').decode().strip() == base, 'Main parent changed during prepare')
    require(reader.git('symbolic-ref', '--short', 'HEAD').strip() == b'main', 'Branch changed during prepare')
    require(reader.git('ls-remote', 'https://github.com/AlecKriebel/Math.git', 'refs/heads/main').decode().split()[0] == base,
            'Remote main changed during prepare')
    require(not (C / N).exists(), 'Another writer created the native attempt during prepare')
    for name, data in before.items():
        local = C / P / name
        require(not local.is_symlink() and (not local.exists() or regular(local).read_bytes() == data),
                'Another writer changed native input during prepare: ' + name)
    for name in ['problems.json', 'research_results.json']:
        require(file_pin(R / P / 'cache' / name) == manifest['files'][name], 'Raw source changed during prepare')
    live_after = json.loads(reader.run(['gh', 'pr', 'view', '108', '--repo', 'AlecKriebel/Math', '--json',
                                      'number,state,isDraft,headRefName,headRefOid,baseRefName,url']))
    require(live_after == live, 'PR changed during prepare')
    bundle = output / 'bundle'
    bundle.mkdir()
    affected = []
    def offer(path, data, baseline_data=None):
        rel(path)
        require(path.startswith(N) or path in [P + name for name in EXPORT], 'Destination outside exact native allowlist')
        if baseline_data == data:
            return
        destination = bundle / path
        require(not destination.exists(), 'Destination collision')
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
        affected.append({'path': path, 'before': None if baseline_data is None else {'bytes': len(baseline_data), 'sha256': sha(baseline_data)},
                         'after': {'bytes': len(data), 'sha256': sha(data)}})
    for name in EXPORT:
        offer(P + name, (backend / name).read_bytes(), before[name])
    for name, data in original_files.items():
        offer(N + 'historical_original/' + name, data)
    for name, data in effective.items():
        offer(N + ('EFFECTIVE_DIAGNOSTICS_README.md' if name == 'README.md' else name), data)
    offer(N + 'source_record.json', original_files['source_record.json'])
    offer(N + 'prior_imported_report.json', regular(ORIGINAL / 'SELECTED_IMPORTED_PRIOR_REPORT.json').read_bytes())
    offer(N + 'IMPORT_BASELINE.json', encode(baseline))
    offer(N + 'HISTORICAL_DESK_ASSESSMENT.json', encode(oldass[K]))
    offer(N + 'assessment.json', encode(afterass[K]))
    for role, data in gate_bytes.items():
        offer(N + 'publication/gates/' + role + '.json', data)
    offer(N + 'publication/PACKAGE_MANIFEST.json', package_bytes)
    offer(N + 'publication/ACTUAL_PUBLICATION_RECEIPT.json', publication_bytes)
    offer(N + 'publication/DOI_METADATA_RESPONSE.json', response_bytes)
    offer(N + 'publication/ACTUAL_TRACKER_READBACK.json', tracker_bytes)
    for index, name in enumerate(sorted(payload_receipts)):
        offer(N + 'publication/payload_readbacks/' + str(index) + '.json', payload_receipts[name])
    for name, data in package_files.items():
        offer(N + 'publication/package/' + name, data)
    evidence = {'original_head': HEAD, 'review_hash': REVIEW, 'statement_hash': STATEMENT,
                'dataset_revision': REV, 'imported_prior_report': {}, 'original_budget': '2/5',
                'original_structured_ledger_present': False, 'new_central_proof_search_turns': 0,
                'effective_proof_sha256': PROOF, 'original_proof_sha256': ORIGINAL_PROOF,
                'exact_claim': gates['final']['exact_claim'], 'DOI': doi,
                'package_manifest_sha256': package_manifest_sha, 'original_status_retained': 'claimed_solved'}
    offer(N + 'PUBLICATION_EVIDENCE.json', encode(evidence))
    offer(N + 'README.md', ('# ' + K + ': aggregate root-dependent spanning-tree hardness\n\n'
        'Status: claimed_solved. Historical author count 2/5 was imported from authenticated QUEUE and two-approach prose. '
        'No original structured ledger was submitted; IMPORT_BASELINE.json is a dated native import, not recovered history. '
        'Additional central proof-search turns: 0.\n\nThe current clarified proof and guards are at PROOF.md/verify.py; '
        'the exact 15 submitted native files remain under historical_original/. The imported prior report remains {}.\n\n'
        'The final source-bound mathematical, priority, package and native reviews are archived under publication/gates/. '
        'The actual published package is https://doi.org/' + doi + '. DOI and tracker receipts are archived separately. '
        'Extensive AI-assisted review is disclosed; conventional human peer review is not claimed.\n').encode())
    offer(N + 'RESEARCH_LOG.md', ('# PR108 native import log\n\n' + now() +
        ': Native integration preparation 95% pending independent bundle review, explicit export, committed-main and service readbacks. '
        'Original submitted author effort 2/5 preserved as an imported historical count; original_structured_ledger_present=false; '
        'new central proof-search turns 0. Literal claimed_solved retained. Mathematical/priority/package clearance is supplied by '
        'the archived final gates and actual DOI/tracker receipts; this preparation has not merged, published, committed or exported.\n').encode())
    final = {'schema': 'pr108-native-review-bundle/v1', 'UTC': now(), 'actual_operator_PID': os.getpid(),
             'main_parent': base, 'original_head': HEAD, 'live_head': live['headRefOid'],
             'config_sha256': sha(cfg_bytes), 'native_status': 'claimed_solved', 'turns_used': 2,
             'original_structured_ledger_present': False, 'new_central_proof_search_turns': 0,
             'unrelated_catalog_projection_drift_preserved': drift, 'DOI': doi,
             'native_assess_executed_in_private_backend': True, 'shared_cache_read_only': True,
             'native_export_executed': False, 'Git_index_branch_remote_or_service_mutated': False,
             'merge_executed': False, 'publication_executed_by_helper': False,
             'affected_paths': affected, 'parent_review_and_explicit_export_required': True}
    (output / 'CANDIDATE_RECEIPT.json').write_bytes(encode(final))
    (output / 'CONFIG.json').write_bytes(cfg_bytes)
    reader.flush()
    print(json.dumps({'candidate': str(output), 'affected_path_count': len(affected), 'native_export_executed': False}))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, required=True)
    args = parser.parse_args()
    prepare(args.config)
