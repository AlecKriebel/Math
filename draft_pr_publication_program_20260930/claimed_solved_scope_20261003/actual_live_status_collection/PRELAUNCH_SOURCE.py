"""Read-only current draft/status projection; no science or PR body review.

Writes only this dedicated administrative folder. QUEUE blob text is read only
to identify target status scalars, then discarded. Whole responses are hashed in
memory, explicitly not retained. This is dated eligibility, not math acceptance.
"""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import re
import stat
import subprocess
import traceback

R = Path('/Users/alec/Documents/Math')
D = R / 'draft_pr_publication_program_20260930/claimed_solved_scope_20261003'
C = D / 'actual_live_status_collection'
Q = 'unsolved_math_prioritization/QUEUE.md'
COMMANDS = []
FIELDS = 'number,title,state,isDraft,headRefName,headRefOid,baseRefName,url,mergedAt,closedAt,mergeCommit,createdAt,updatedAt'

def utc(): return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def dump(path, value):
    with path.open('x') as f:
        json.dump(value, f, indent=2, sort_keys=True)
        f.write('\n')
def pin(path):
    b = path.read_bytes()
    return {'path': str(path), 'bytes': len(b), 'sha256': sha(b), 'full_mode': stat.S_IMODE(path.lstat().st_mode)}
def run(argv, retain=True):
    n = len(COMMANDS) + 1
    start = utc()
    p = subprocess.Popen(argv, cwd=R, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    end = utc()
    ep = C / f'{n:02d}.stderr.bin';ep.write_bytes(err)
    row = {'argv': argv, 'cwd': str(R), 'actual_pid': p.pid, 'started_utc': start, 'ended_utc': end,
           'exit_code': p.returncode, 'stderr': pin(ep), 'stdout_bytes': len(out), 'stdout_sha256': sha(out)}
    if retain:
        op = C / f'{n:02d}.stdout.bin';op.write_bytes(out)
        row.update(stdout=pin(op), stdout_custody='ENTIRE_RAW_STREAM_RETAINED')
    else:
        row.update(stdout_custody='ENTIRE_RAW_STREAM_OBSERVED_HASHED_IN_MEMORY_NOT_RETAINED',
                   reason='Status-only QUEUE projection; excluded descriptions/findings are not retained.')
    COMMANDS.append(row);dump(C / f'{n:02d}.COMMAND.json', row)
    if p.returncode: raise RuntimeError(f'read-only child {p.pid} exit {p.returncode}')
    return out

def list_open():
    values = json.loads(run(['gh', 'pr', 'list', '--repo', 'AlecKriebel/Math', '--state', 'open', '--limit', '2000', '--json', FIELDS]))
    assert len(values) < 2000, 'query cap reached: coverage incomplete'
    assert len(values) == len({v['number'] for v in values})
    return {v['number']: v for v in values if v['number'] >= 9 and v['number'] != 8 and v['isDraft'] and v['state'] == 'OPEN'}

def project(body, blob, metadata, original_id=None):
    text = body.decode('utf8')
    header = next(line for line in text.splitlines() if line.startswith('| Rank |'))
    cells = [c.strip() for c in header.split('|')[1:-1]]
    si = cells.index('Status');ti = cells.index('Turns')
    scalar_rows = []
    linked = []
    link = re.compile(r'https://github\.com/AlecKriebel/Math/pull/' + str(metadata['number']) + r'(?![0-9])')
    for line in text.splitlines():
        if not line.startswith('|'): continue
        values = [c.strip() for c in line.split('|')[1:-1]]
        if len(values) <= ti: continue
        pid = values[1].split(' / ')[0]
        if not re.fullmatch(r'[0-9]+', pid): continue
        scalar = {'problem_id': pid, 'code': values[1], 'status': values[si], 'turns': values[ti],
                  'selected_row_sha256': sha(line.encode())}
        scalar_rows.append(scalar)
        if link.search(line): linked.append(scalar)
    if original_id is not None:
        selected = [r for r in scalar_rows if r['problem_id'] == original_id]
        method = 'dated_original_inventory_exact_problem_id'
    elif linked:
        selected = linked;method = 'literal_exact_PR_URL_in_QUEUE_row'
    else:
        ids = set(re.findall(r'[0-9]{4,}', metadata['headRefName'] + ' ' + metadata['title']))
        selected = [r for r in scalar_rows if r['problem_id'] in ids]
        method = 'QUEUE_ID_intersection_with_branch_and_title_numeric_metadata'
    return {'targets': selected, 'target_selection_method': method, 'git_blob_oid': blob,
            'whole_QUEUE_bytes': len(body), 'whole_QUEUE_sha256': sha(body),
            'science_findings_or_QUEUE_full_body_retained': False,
            'target_ambiguity': not selected or len({r['problem_id'] for r in selected}) != len(selected)}

def fresh_projections(entries, original_ids):
    result = {}
    items = list(entries.values())
    for offset in range(0, len(items), 12):
        selected = items[offset:offset + 12]
        aliases = ' '.join(f'q{j}:object(expression:"{v["headRefOid"]}:{Q}"){{... on Blob{{oid byteSize text}}}}' for j, v in enumerate(selected))
        query = 'query{repository(owner:"AlecKriebel",name:"Math"){' + aliases + '}}'
        response = json.loads(run(['gh', 'api', 'graphql', '-f', 'query=' + query], retain=False))
        assert not response.get('errors'), response.get('errors')
        for j, m in enumerate(selected):
            v = response['data']['repository'][f'q{j}']
            if v is None or v.get('text') is None:
                result[m['number']] = {'targets': [], 'target_ambiguity': True, 'status_gap': 'literal head QUEUE blob unavailable',
                                       'science_findings_or_QUEUE_full_body_retained': False}
                continue
            body = v['text'].encode();assert len(body) == v['byteSize']
            assert hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest() == v['oid']
            result[m['number']] = project(body, v['oid'], m, original_ids.get(m['number']))
    return result

def main():
    start = utc();C.mkdir(mode=0o755)
    (C / 'PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes())
    original = json.loads((D / 'SCOPE_LEDGER.json').read_text())
    original_rows = {r['pr']: r for r in original['rows']}
    original_ids = {n: r['problem_id'] for n, r in original_rows.items()}
    current = list_open()
    cached = {}
    pending = {}
    for n, m in current.items():
        old = original_rows.get(n)
        if old and old['inventory_head'] == m['headRefOid']:
            source = old['submitted_QUEUE']
            cached[n] = {'targets': [{k: source[k] for k in ['problem_id','code','status','turns','selected_row_sha256']}],
                         'target_selection_method': 'exact_head_equal_dated_roster_status_projection',
                         'git_blob_oid': source['git_blob_oid'], 'whole_QUEUE_bytes': source['whole_QUEUE_bytes'],
                         'whole_QUEUE_sha256': source['whole_QUEUE_sha256'], 'target_ambiguity': False,
                         'science_findings_or_QUEUE_full_body_retained': False}
        else: pending[n] = m
    cached.update(fresh_projections(pending, original_ids))
    observations = [{'utc': utc(), 'open_draft_count': len(current), 'numbers': sorted(current)}]
    # Reconcile arrivals/closures/head changes twice; do not claim a timeless snapshot.
    for _ in range(2):
        after = list_open()
        changed = {n: m for n, m in after.items() if n not in current or m['headRefOid'] != current[n]['headRefOid']}
        cached.update(fresh_projections(changed, original_ids))
        observations.append({'utc': utc(), 'open_draft_count': len(after), 'numbers': sorted(after), 'new_or_changed_heads': sorted(changed)})
        current = after
        if not changed: break
    final_rows = []
    for n, m in sorted(current.items()):
        projection = cached[n]
        statuses = [r['status'] for r in projection['targets']]
        if projection.get('target_ambiguity'):
            action = 'METADATA_TARGET_GAP_NO_PROCESSING'
        elif statuses and all(s == 'claimed_solved' for s in statuses):
            action = 'ELIGIBLE_CLAIMED_SOLVED_ORDERED_WORKFLOW'
        elif 'claimed_solved' in statuses:
            action = 'MIXED_TARGET_STATUS_GAP_NO_PROCESSING'
        else: action = 'SKIP_ENTIRELY_NONCLAIM_STATUS'
        final_rows.append({'pr': n, 'url': m['url'], 'title': m['title'], 'state': m['state'], 'isDraft': m['isDraft'],
                           'headRefOid': m['headRefOid'], 'headRefName': m['headRefName'], 'updatedAt': m['updatedAt'],
                           'in_original_180_roster': n in original_rows, 'status_projection': projection,
                           'action': action, 'new_science_review_or_repair_or_PR_write': False})
    eligible = [r['pr'] for r in final_rows if r['action'] == 'ELIGIBLE_CLAIMED_SOLVED_ORDERED_WORKFLOW']
    gaps = [r['pr'] for r in final_rows if 'GAP' in r['action']]
    old_closed_claims = [r['pr'] for r in original['rows'] if r['submitted_status_exactly_claimed_solved']
                         and r['current_GitHub_metadata']['state'] != 'OPEN' and r['pr'] not in [9,16]]
    ledger = {'schema': 'claimed-solved-only-live-draft-eligibility-registry/v1', 'status': 'READY_STATUS_ONLY_WITH_DATED_COVERAGE',
              'actual_collector_pid': os.getpid(), 'started_utc': start, 'ended_utc': utc(),
              'dated_180_roster': pin(D / 'SCOPE_LEDGER.json'),
              'dated_180_preliminary_action_labels_superseded': True,
              'dated_original_submitted_status_counts': original['submitted_status_counts'],
              'historical_completed_partial_and_publication_count': 37,
              'historical_count_is_not_current_eligible_denominator': True,
              'dated_already_published_eligible_PRs': [9,16],
              'dated_merged_nonpublication_original_claims_excluded_from_draft_workflow': old_closed_claims,
              'current_open_draft_count': len(final_rows), 'current_eligible_open_draft_count': len(eligible),
              'current_eligible_open_draft_order': eligible, 'first_unpublished_eligible_PR': eligible[0] if eligible else None,
              'metadata_target_gaps': gaps, 'metadata_observations': observations,
              'known_published_plus_current_eligible_denominator': 2 + len(eligible),
              'known_published_percent_of_dated_current_eligible_registry': 200 / (2 + len(eligible)),
              'estimate_denominator_excludes_status_gaps_and_future_arrivals': True,
              'scope_inventory_completion_percent': 100 if not gaps else 95,
              'scope_only_no_new_mathematical_or_priority_clearance': True,
              'external_PR_writes_native_Git_index_ref_body_mutations': False,
              'coverage_limit': 'Only OPEN drafts returned by exact paginated gh query during this observation interval. Later arrivals, non-draft open PRs, and target/status gaps require separate metadata checks; no eternal all-repo coverage claimed.',
              'rows': final_rows}
    dump(D / 'LIVE_DRAFT_ELIGIBILITY_REGISTRY.json', ledger)
    dump(C / 'COMPLETE_COMMANDS.json', COMMANDS)
    dump(C / 'COLLECTION_RECEIPT.json', {'schema': 'claimed-solved-live-status-administrative-actual-collection/v1',
             'status': 'PASS_STATUS_COLLECTION', 'actual_pid': os.getpid(), 'started_utc': start, 'ended_utc': utc(),
             'source': pin(Path(__file__)), 'prelaunch_source': pin(C / 'PRELAUNCH_SOURCE.py'),
             'registry': pin(D / 'LIVE_DRAFT_ELIGIBILITY_REGISTRY.json'), 'command_count': len(COMMANDS),
             'production_mathematical_helpers_imported_compiled_executed': False})
    print(json.dumps({k: ledger[k] for k in ['actual_collector_pid','current_open_draft_count','current_eligible_open_draft_count','current_eligible_open_draft_order','metadata_target_gaps','known_published_percent_of_dated_current_eligible_registry']}))

if __name__ == '__main__':
    try: main()
    except BaseException:
        if C.exists():
            dump(C / 'FAILED_COMPLETE_COMMANDS.json', COMMANDS)
            (C / 'COLLECTION_FAILURE.txt').write_text(traceback.format_exc())
        raise
