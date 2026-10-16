"""Independent local custody/structural checks; never import production writers.

No subprocess, Git/service/lock/signal operation is available in this program.
Every write is confined to its own reviewer output directory. Private full-sheet
and process bytes are read for comparison, never copied into reviewer outputs.
"""
from pathlib import Path
from datetime import datetime, timezone
import ast, collections, gzip, hashlib, io, json, re, stat, sys, zipfile

if sys.flags.optimize:
    raise RuntimeError('This independent assertion checker requires normal mode.')
O = Path(__file__).resolve().parent
D = O.parent
A = D.parent
R = Path('/Users/alec/Documents/Math')
P = R / 'draft_pr_descending_audit_20261002'
HEAD = 'cc083024dbd00de06ad444cd4070f51f60d209eb'
BASE = '3311d193e8c124bb97884fbe41710a957d3122c8'
MERGE = 'b3eaf7561c83b37881eec11f5972396dbad9575d'
DOI = '10.5281/zenodo.23149775'
PREFIX = 'problems/5100034_focal_pedal_equality'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'
sha = lambda b: hashlib.sha256(b).hexdigest()
utc = lambda: datetime.now(timezone.utc).isoformat()
inputs = {}
checks = []

def read(p):
    p = Path(p)
    assert p.is_file() and not p.is_symlink(), str(p)
    b = p.read_bytes()
    e = dict(path=str(p), bytes=len(b), sha256=sha(b), mode=stat.S_IMODE(p.stat().st_mode))
    if str(p) in inputs:
        assert inputs[str(p)] == e, 'Immutable input drift: ' + str(p)
    inputs[str(p)] = e
    return b

def load(p):
    return json.loads(read(p))

def check(name, valid, details=None):
    assert valid, name
    checks.append(dict(check=name, passed=True, details=details))

def pinned(p, e):
    b = read(p)
    mode = e.get('mode')
    if isinstance(mode, str):
        mode = int(mode, 8)
    assert len(b) == e['bytes'] and sha(b) == e['sha256'], str(p)
    if mode is not None:
        assert stat.S_IMODE(Path(p).stat().st_mode) == mode, str(p)
    return b

def strings(v, path=''):
    if isinstance(v, dict):
        for k, x in v.items():
            yield from strings(x, path + '/' + k)
    elif isinstance(v, list):
        for n, x in enumerate(v):
            yield from strings(x, path + '/' + str(n))
    elif isinstance(v, str):
        yield path, v

criteria = load(O / 'CRITERIA.json')
plan = load(D / 'completion_preparation/CONTENT_PLAN.json')
check('exact pre-read frozen criteria and packet identity',
      inputs[str(D / 'completion_preparation/CONTENT_PLAN.json')]['sha256'] ==
      'aa3f453d3bdb86d40228dfcca5f9ba6815665e17db1f9ea4f50b1a495230bad2'
      and inputs[str(D / 'completion_preparation/CONTENT_PLAN.json')]['bytes'] == 70884)
targets = plan['targets']
check('88 distinct literal targets; measured total 3,382,769 bytes',
      len(targets) == plan['target_count'] == 88
      and len({x['target'] for x in targets}) == 88
      and sum(x['input']['bytes'] for x in targets) == 3382769)
bodies = []
json_shapes = []
privacy_hits = []
patterns = {
    'private_key': r'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----',
    'literal_bearer': r'(?i)Bearer\s+[a-zA-Z0-9_-]{15,}',
    'github_credential': r'\b(?:ghp_|gho_|github_pat_)[a-zA-Z0-9_]{15,}',
    'api_credential': r'\bsk-(?:proj-)?[a-zA-Z0-9_-]{20,}',
    'url_credentials': r'https?://[^\s/"\']*:[^\s/"\']*@',
    'private_payload_key': r'(?i)"(?:stdout|stderr|stdout_body|stderr_body|raw_body|full_body|raw_diff|patch_body|index_body)"\s*:\s*"',
    'raw_git_diff': r'(?m)^diff --git |^@@ -\d+(?:,\d+)? \+\d+',
    'raw_git_index': r'(?m)^[A-Z] (?:100644|100755) [a-f0-9]{40} [0-3]\t',
}
for n, t in enumerate(targets):
    rel = Path(t['target'])
    check('literal relative target ' + str(n), not rel.is_absolute() and '..' not in rel.parts)
    p = R / t['input']['path']
    b = pinned(p, t['input'])
    bodies.append(b)
    if t['original_target'] is not None:
        pinned(R / t['original_target']['path'], t['original_target'])
    check('owned target scope ' + str(n), str(rel).startswith(str(P.relative_to(R)) + '/'))
    if p.suffix == '.pdf':
        check('only selected PDF is exact authored note',
              p.name == 'focal_pedal_ratios.pdf' and sha(b) ==
              '426e2f9809b6f02bf03ee564cad40ae41cc0cee68dfafb907257bd17c6f04686')
        continue
    text = b.decode('utf-8')
    for kind, pattern in patterns.items():
        for m in re.finditer(pattern, text):
            privacy_hits.append(dict(target=n, kind=kind, line=text.count('\n', 0, m.start()) + 1))
    if p.suffix == '.json':
        j = json.loads(b)
        ss = list(strings(j))
        long_values = [(k, len(s)) for k, s in ss if len(s) > 1000]
        for k, s in ss:
            for kind in ['private_key', 'literal_bearer', 'github_credential', 'api_credential', 'url_credentials', 'raw_git_diff', 'raw_git_index']:
                if re.search(patterns[kind], s):
                    privacy_hits.append(dict(target=n, kind=kind, json_location=k))
        check('long JSON values are only own tracker notes/argv ' + str(n),
              all(n == 19 and k in ['/native_execution_captures/6/argv/8', '/native_execution_captures/7/argv/8']
                  or n == 64 and k == '/row/3' for k, size in long_values))
        json_shapes.append(dict(target=n, strings=len(ss), top_keys=list(j) if isinstance(j, dict) else None,
                                long_value_locations=long_values))
    if p.suffix == '.py':
        ast.parse(text, filename=str(p))
check('all whole selected UTF-8/JSON/Python bodies read; privacy patterns absent', not privacy_hits)

before = load(P / 'inventory.json')
after = json.loads(bodies[0])
check('all inventory item IDs and order unchanged',
      [x['number'] for x in before['items']] == [x['number'] for x in after['items']]
      and len({x['number'] for x in after['items']}) == len(after['items']))
diff_items = [x['number'] for x, y in zip(before['items'], after['items']) if x != y]
check('only PR305 inventory entry changes', diff_items == [305])
changed_keys = {k for k in before if before[k] != after[k]}
check('only expected four inventory fields change', changed_keys ==
      {'items', 'completed_by_descending', 'claimed_solved_published_by_descending', 'claimed_solved_merged_by_descending'})
for k in ['claimed_solved_published_by_descending', 'claimed_solved_merged_by_descending']:
    check(k + ' appended once without reordering prior values',
          after[k] == before[k] + [305] and len(before[k]) == 7 and len(after[k]) == 8
          and len(set(after[k])) == 8 and all(x != 8 for x in after[k]))
check('completed count26→27', before['completed_by_descending'] == 26 and after['completed_by_descending'] == 27)
new305 = next(x for x in after['items'] if x['number'] == 305)
check('history and exact current outcome', new305['submitted_status'] == 'claimed_solved'
      and new305['original_author_turn_count'] == '1/5' and new305['headRefOid'] == HEAD
      and new305['accepted_head'] == HEAD and new305['actual_merge'] == MERGE
      and new305['doi'] == DOI and new305['historical_first_priority_certified'] is False)
for n in [1, 2, 3]:
    previous = read(R / targets[n]['original_target']['path'])
    check('historical narrative prefix preserved ' + str(n), bodies[n].startswith(previous))
    append = bodies[n][len(previous):].decode()
    check('append tells actual completion and retained failed outer ' + str(n),
          DOI in append and MERGE in append and '1/5' in append and 'outerexit1' in append
          and 'no repeated mutation' in append and 'Final' in append or n == 3 and DOI in append)
status = json.loads(bodies[4])
check('prepared current status agrees with plan and native result',
      status['status'] == 'MERGED_PUBLISHED_AND_TRACKER_VERIFIED' and status['doi'] == DOI
      and status['actual_merge'] == MERGE and status['accepted_head'] == HEAD
      and status['completed_by_descending'] == 27 and status['published_by_descending'] == 8
      and status['original_author_turn_count'] == '1/5' and status['persistent_goal_complete'] is False)

science = load(D / 'ROOT_FULL_PREPRINT_PUBLICATION_CLEARANCE.json')
check('current whole-preprint round02 is accepted with no mandatory findings',
      science['status'] == 'PASS_PR305_FULL_PREPRINT_REVISION02_READY'
      and science['new_whole_review_round'] == 2 and science['mandatory_unresolved_findings'] == 0
      and science['original_head'] == HEAD and science['original_author_budget'] == '1/5')
for p, e in science['closed_evidence_bindings'].items():
    pinned(p, e)
for name, e in science['submission_files'].items():
    pinned(D / 'submission_v02' / name, e)
nc = load(D / 'ROOT_PR305_NATIVE_INTEGRATION_CLEARANCE.json')
check('native current round03 accepted; earlier adverse history retained',
      nc['new_clean_native_review_round'] == 3 and nc['unresolved_mandatory_findings'] == 0
      and nc['earlier_adverse_native_reviews_repaired_and_preserved'] is True)
for p, e in nc['closed_review_evidence'].items():
    pinned(p, e)
check('current source never differs from accepted native operator',
      sha(read(D / 'native_integration_preparation/integrate_pr305.py')) == nc['operator']['sha256'] ==
      '0ea02436c0ac1e0070169df466c34ba141c43291e16515b3fd1cce2135071897')
manifest = load(D / 'preprint_review02_candidate_frozen/MANIFEST.json')
check('whole-preprint candidate manifest exact accepted body',
      inputs[str(D / 'preprint_review02_candidate_frozen/MANIFEST.json')]['sha256'] ==
      science['candidate_manifest_sha256'])
for e in manifest['files']:
    b = pinned(D / 'preprint_review02_candidate_frozen' / e['path'], e)
    check('candidate all readonly payloads ' + e['path'],
          stat.S_IMODE((D / 'preprint_review02_candidate_frozen' / e['path']).stat().st_mode) == 0o444)
zbytes = read(D / 'submission_v02/focal-pedal-ratios-verification.zip')
with zipfile.ZipFile(io.BytesIO(zbytes)) as z:
    check('portable24-member ZIP has exact candidate namespace',
          len(z.infolist()) == len(set(z.namelist())) == 24
          and set(z.namelist()) == {e['path'] for e in manifest['files']} | {'MANIFEST.json'}
          and z.testzip() is None)
    for e in z.infolist():
        check('whole portable member ' + e.filename,
              not e.filename.startswith('/') and '..' not in Path(e.filename).parts
              and z.read(e) == read(D / 'preprint_review02_candidate_frozen' / e.filename))
for name in ['focal-pedal-ratios-note.pdf', 'focal-pedal-ratios-verification.zip', 'zenodo-deposit.json']:
    check('native published copy equals reviewed submission ' + name,
          read(R / PREFIX / 'publication' / name) == read(D / 'submission_v02' / name))

tracker = load(D / 'publication_actual/TRACKER_COMPLETE.json')
pub = load(D / 'publication_actual/inspect_published_receipt.json')
check('actual publication and unique own tracker identities agree',
      pub['state'] == 'published' and pub['id'] == 23149775 and pub['doi'] == tracker['doi'] == DOI
      and tracker['status'] == 'PASS_ONE_ROW_APPENDED_AND_EXACT_READBACK'
      and tracker['updatedRange'] == status['tracker_range'] == "'Math Puzzles'!A24:D24"
      and tracker['single_cli_append_invocation'] is True and tracker['automatic_append_retry'] is False)
capture_dir = Path(tracker['private_full_scan_directory'])
before_rows = load(capture_dir / 'existing_rows.stdout')['values']
after_rows = load(capture_dir / 'all_rows_after.stdout')['values']
check('private full43-column history preserved plus exactly own row; no rows copied to outputs',
      len(before_rows) == 23 and len(after_rows) == 24 and after_rows == before_rows + [tracker['row']]
      and sum(DOI in str(x) for x in after_rows[1:]) == 1
      and sum('5100034' in str(x) for x in after_rows[1:]) == 1
      and tracker['all_original_sheet_columns_scanned'] == 43)
check('own four-cell row retains blank chat and exact DOI',
      len(tracker['row']) == 4 and tracker['row'][1] == '' and tracker['row'][2] == 'https://doi.org/' + DOI)
pc = load(D / 'ROOT_ACTUAL_PUBLICATION_TRACKER_FINAL_CUSTODY.json')
for p, e in pc['bindings'].items():
    pinned(p, e)
http = load(D / 'ROOT_ACTUAL_PUBLIC_EVIDENCE_READBACK.json')
for p, e in http['evidence_pins'].items():
    pinned(p, e)
check('root whole HTTP authentication preceded actual tracker append',
      datetime.fromisoformat(http['utc']) <= datetime.fromisoformat(tracker['utc'])
      and http['record_id'] == 23149775 and http['doi'] == DOI)
public = load(D / 'publication_actual/PUBLIC_RECORD_VERIFICATION.json')
public_dir = Path(public['private_capture_directory'])
record = load(public_dir / 'record.stdout')
meta = load(D / 'submission_v02/zenodo-deposit.json')['metadata']
for k, v in meta.items():
    if k == 'upload_type':
        actual = record['metadata']['resource_type']['type']
    elif k == 'publication_type':
        actual = record['metadata']['resource_type']['subtype']
    elif k == 'license':
        actual = record['metadata']['license']['id']
    else:
        actual = record['metadata'][k]
    check('all exact reviewed public metadata ' + k, actual == v)
check('record and exact DOI resolution', record['id'] == 23149775 and record['doi'] == DOI
      and load(public_dir / 'exact_doi_resolution.stdout')['url_effective'] == 'https://zenodo.org/records/23149775')
for e in public['all_file_bytes']:
    downloaded = read(public_dir / ('file_' + e['name'] + '.stdout'))
    check('whole anonymous public bytes ' + e['name'], downloaded == read(D / 'submission_v02' / e['name'])
          and len(downloaded) == e['bytes'] and sha(downloaded) == e['sha256']
          and hashlib.md5(downloaded).hexdigest() == e['md5'])

m = load(D / 'ROOT_PR305_ACTUAL_MERGE_VERIFICATION.json')
check('exact actual merge/historical result', m['status'] == 'PASS_PR305_EXACT_ORIGINAL_HEAD_MERGED_PUBLISHED_TRACKER_VERIFIED'
      and m['actual_merge'] == MERGE and m['parents'] == [BASE, HEAD] and m['original_head'] == HEAD
      and m['original_author_history'] == '1/5' and m['queue_only_cells'] == [8, 9, 11, 12]
      and m['DOI'] == DOI and len(m['owned_paths']) == 34)
recon = m['reconciliation']
check('preserved failed outer and one sole push', recon['original_outer_exit_code'] == 1
      and recon['sole_successful_push_PID'] == 62553 and recon['sole_commit_PID'] == 62318
      and recon['no_merge_commit_stage_push_or_PR_mutation_repeated'] is True)
outerp = D / 'root_runs_private/root_pr305_native_integration_actual001/execution.json'
pinned(outerp, recon['original_outer_capture'])
outer = load(outerp)
for k in ['stdout', 'stderr']:
    b = read(outerp.parent / (k + '.bin'))
    check('preserved actual failed outer full ' + k, len(b) == outer[k + '_bytes'] and sha(b) == outer[k + '_sha256'])
check('failed outer is GitHub recognition lag, not failed push', outer['exit_code'] == 1
      and b'GitHub exact merge readback missing' in read(outerp.parent / 'stderr.bin'))

native = recon['original377_full_actual_captures_authenticated']
check('377 unique actual native operation receipts retained', len(native) == 377 and len({x['actual_PID'] for x in native}) == 377)
native_stream_bytes = 0
push_count = commit_count = 0
for x in native:
    p = Path(x['path']);pinned(p, x['pin']);j = load(p);n = p.name.split('_')[0]
    request = load(p.parent / (n + '_request.json'));started = load(p.parent / (n + '_started.json'))
    assert all(j[k] == v for k, v in request.items()) and all(j[k] == v for k, v in started.items())
    assert j['actual_PID'] == x['actual_PID'] and j['argv'] == x['argv'] and j['exit_code'] == x['exit_code']
    assert j['cwd'] == str(R) and j['cooperative_process_group'] == j['actual_PID']
    assert j['full_stream_capture_complete'] is True and j['parent_reaped'] is True
    assert datetime.fromisoformat(j['end_UTC']) >= datetime.fromisoformat(j['start_UTC'])
    assert j['operator']['sha256'] == nc['operator']['sha256']
    for k in ['stdout', 'stderr']:
        e = j[k];stored = read(e['path']);raw = gzip.decompress(stored)
        assert len(stored) == e['stored_bytes'] and sha(stored) == e['stored_sha256']
        assert len(raw) == e['logical_bytes'] and sha(raw) == e['logical_sha256']
        native_stream_bytes += len(raw)
    if j['argv'][:3] == ['/usr/bin/git', '--no-optional-locks', 'push']:
        push_count += 1
        assert j['actual_PID'] == 62553 and j['exit_code'] == 0 and j['argv'][-1] == MERGE + ':refs/heads/main'
    if j['argv'][:3] == ['/usr/bin/git', '--no-optional-locks', 'commit']:
        commit_count += 1
        assert j['actual_PID'] == 62318 and j['exit_code'] == 0
check('complete original native streams authenticate one commit and one push', push_count == commit_count == 1,
      dict(captures=len(native), logical_stream_bytes=native_stream_bytes))
ops = recon['fresh_readonly_operations']
readback = D / 'actual_merge_reconciliation_readonly_01'
out_by_argv = {}
for n, x in enumerate(ops, 1):
    saved = load(readback / (str(n) + '_execution.json'))
    assert saved == x and saved['exit_code'] == 0 and saved['readonly'] is True and saved['cwd'] == str(R)
    for k in ['stdout', 'stderr']:
        b = gzip.decompress(read(readback / (str(n) + '_' + k + '.gz')))
        assert len(b) == saved[k + '_bytes'] and sha(b) == saved[k + '_sha256']
        if k == 'stdout':
            out_by_argv[tuple(saved['argv'])] = b
check('all84 actual read-only reconciliation captures complete', len(ops) == 84)
freshpr = json.loads(out_by_argv[('/opt/homebrew/bin/gh', 'api', 'repos/AlecKriebel/Math/pulls/305')])
check('actual delayed GitHub MERGED readback agrees', freshpr['merged'] is True and freshpr['state'] == 'closed'
      and freshpr['merge_commit_sha'] == MERGE and freshpr['head']['sha'] == HEAD
      and freshpr['merged_at'] == status['merged_at'])
snap = load(A / 'snapshot_manifest.json')
check('original snapshot history remains exact', snap['head'] == HEAD and snap['original_submitted_status'] == 'claimed_solved'
      and snap['original_author_turn_count'] == '1/5' and len(snap['files']) == 30)
for e in snap['files']:
    original = pinned(A / 'snapshot' / e['path'], e)
    assert hashlib.sha1(b'blob ' + str(len(original)).encode() + b'\0' + original).hexdigest() == e['git_blob_sha']
    if e['path'] != QUEUE:
        check('original historical native body/mode unchanged ' + e['path'],
              read(R / e['path']) == original and stat.S_IMODE((R / e['path']).stat().st_mode) == 0o644)
q0 = out_by_argv[('/usr/bin/git', '--no-optional-locks', 'show', BASE + ':' + QUEUE)]
q1 = out_by_argv[('/usr/bin/git', '--no-optional-locks', 'show', MERGE + ':' + QUEUE)]
row = lambda b: next(x for x in b.splitlines(keepends=True) if b'| 5100034 /' in x)
r0, r1 = row(q0), row(q1)
check('exact native target queue delta and all foreign bytes', q0.replace(r0, b'', 1) == q1.replace(r1, b'', 1)
      and len(r0.split(b'|')) == len(r1.split(b'|')) == 14
      and [i for i, (a, b) in enumerate(zip(r0.split(b'|'), r1.split(b'|'))) if a != b] == [8, 9, 11, 12]
      and r1.split(b'|')[9].strip() == b'1/5' and read(R / QUEUE) == q1)
check('read-only reconciliation source remains exact selected source',
      inputs[str(D / 'root_reconcile_pr305_actual_merge_readonly.py')]['sha256'] == recon['source']['sha256'])

for p, e in list(inputs.items()):
    pinned(p, e)
result = dict(status='PASS_INDEPENDENT_COMPLETION_PACKET_STRUCTURAL_AND_LOCAL_CUSTODY', UTC=utc(),
              exact_plan_sha256=inputs[str(D / 'completion_preparation/CONTENT_PLAN.json')]['sha256'],
              selected_targets=88, selected_body_bytes=3382769, checks=checks, json_shape_summaries=json_shapes,
              credentials_or_private_payload_hits=privacy_hits, authenticated_input_files=len(inputs),
              original_native_captures=377, original_complete_native_logical_stream_bytes=native_stream_bytes,
              fresh_readonly_saved_captures=84, no_production_commands_executed=True,
              all_private_bodies_read_only_and_not_copied=True, source_and_globals_unchanged=True)
(O / 'CHECK_RESULTS.json').write_text(json.dumps(result, indent=2) + '\n')
(O / 'INPUT_INVENTORY.json').write_text(json.dumps(dict(UTC=utc(), files=list(inputs.values()),
    exact_packet_scope_only_not_a_writer_grant=True), indent=2) + '\n')
print(json.dumps({k: v for k, v in result.items() if k not in ['checks', 'json_shape_summaries']}, indent=2))
