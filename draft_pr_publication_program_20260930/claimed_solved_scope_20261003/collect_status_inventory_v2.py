"""Administrative status inventory only; no proof/helper/PR-body processing.

Only this dedicated folder is written. Git reads literal QUEUE snapshots without
fetching or changing refs/index. Large QUEUE batch streams are hashed in memory,
not represented as retained full streams. GitHub queries request metadata only.
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
P = R / 'draft_pr_publication_program_20260930'
D = P / 'claimed_solved_scope_20261003'
Q = 'unsolved_math_prioritization/QUEUE.md'
OBJECTIVE = Path('/Users/alec/.codex/attachments/4df73d3d-641f-4907-b9ad-c47c468f2589/goal-objective.md')
C = D / 'actual_status_collection_v2'
COMMANDS = []

def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def sha(b):
    return hashlib.sha256(b).hexdigest()

def write_json(path, value):
    with path.open('x', encoding='utf8') as f:
        json.dump(value, f, indent=2, sort_keys=True)
        f.write('\n')

def pin(path):
    b = path.read_bytes()
    return {'path': str(path), 'bytes': len(b), 'sha256': sha(b), 'full_mode': stat.S_IMODE(path.lstat().st_mode)}

def run(argv, data=None, retain_stdout=True):
    n = len(COMMANDS) + 1
    start = utc()
    proc = subprocess.Popen(argv, cwd=R, stdin=subprocess.PIPE if data is not None else subprocess.DEVNULL,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate(data)
    end = utc()
    ep = C / f'{n:02d}.stderr.bin'
    ep.write_bytes(err)
    row = {'argv': argv, 'cwd': str(R), 'actual_pid': proc.pid, 'started_utc': start, 'ended_utc': end,
           'exit_code': proc.returncode, 'stderr': pin(ep), 'stdout_bytes': len(out), 'stdout_sha256': sha(out),
           'stdin_bytes': len(data) if data is not None else 0, 'stdin_sha256': sha(data or b'')}
    if retain_stdout:
        op = C / f'{n:02d}.stdout.bin'
        op.write_bytes(out)
        row['stdout'] = pin(op)
        row['stdout_custody'] = 'ENTIRE_RAW_STREAM_RETAINED'
    else:
        row['stdout_custody'] = 'ENTIRE_RAW_STREAM_OBSERVED_AND_HASHED_IN_MEMORY_NOT_RETAINED'
        row['reason'] = 'QUEUE snapshots contain excluded mathematical descriptions; only status scalar projections are retained.'
    COMMANDS.append(row)
    # Write a distinct per-command record before any decoding or interpretation.
    write_json(C / f'{n:02d}.COMMAND.json', row)
    if proc.returncode:
        raise RuntimeError(f'read-only child {proc.pid} refused: exit {proc.returncode}')
    return out

def queue_projection(body, problem_id, git_blob=None):
    text = body.decode('utf8')
    header = next(line for line in text.splitlines() if line.startswith('| Rank |'))
    headers = [c.strip() for c in header.split('|')[1:-1]]
    status_at = headers.index('Status')
    turns_at = headers.index('Turns')
    matches = []
    for line in text.splitlines():
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if len(cells) > 1 and cells[1].split(' / ')[0] == problem_id:
            matches.append((line, cells))
    if len(matches) != 1:
        raise ValueError(f'{problem_id}: selected QUEUE status row count {len(matches)}')
    line, cells = matches[0]
    return {'problem_id': problem_id, 'code': cells[1], 'status': cells[status_at], 'turns': cells[turns_at],
            'git_blob_oid': git_blob, 'whole_QUEUE_bytes': len(body), 'whole_QUEUE_sha256': sha(body),
            'selected_row_sha256': sha(line.encode('utf8')), 'science_or_findings_body_retained': False}

def batch_queue(heads):
    refs = [h + ':' + Q for h in heads]
    out = run(['git', 'cat-file', '--batch'], ('\n'.join(refs) + '\n').encode(), retain_stdout=False)
    at = 0
    results = []
    for ref in refs:
        nl = out.index(b'\n', at)
        header = out[at:nl].decode('ascii')
        at = nl + 1
        if header.endswith(' missing'):
            results.append(None)
            continue
        oid, kind, length = header.split(' ')
        assert kind == 'blob'
        size = int(length)
        body = out[at:at + size]
        assert len(body) == size and out[at + size:at + size + 1] == b'\n'
        at += size + 1
        assert hashlib.sha1(b'blob ' + str(size).encode() + b'\0' + body).hexdigest() == oid
        results.append((body, oid))
    assert at == len(out)
    return results

def remote_immutable_queues(heads):
    values = {}
    for offset in range(0, len(heads), 12):
        selected = heads[offset:offset + 12]
        aliases = ' '.join(f'q{j}:object(expression:"{h}:{Q}"){{... on Blob{{oid byteSize text}}}}' for j, h in enumerate(selected))
        query = 'query{repository(owner:"AlecKriebel",name:"Math"){' + aliases + '}}'
        response = json.loads(run(['gh', 'api', 'graphql', '-f', 'query=' + query], retain_stdout=False))
        assert not response.get('errors'), response.get('errors')
        for j, h in enumerate(selected):
            value = response['data']['repository'][f'q{j}']
            assert value is not None and value['text'] is not None, h
            b = value['text'].encode('utf8')
            assert len(b) == value['byteSize']
            assert hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest() == value['oid']
            values[h] = (b, value['oid'])
    return values

def current_remote_queue(head):
    # Only eligible originally-claimed heads can enter this fallback.
    return run(['gh', 'api', f'repos/AlecKriebel/Math/contents/{Q}?ref={head}',
                '-H', 'Accept: application/vnd.github.raw+json'], retain_stdout=False)

def main():
    start = utc()
    C.mkdir(mode=0o755)
    (C / 'PRELAUNCH_SOURCE.py').write_bytes(Path(__file__).read_bytes())
    inv_body = (P / 'inventory.json').read_bytes()
    inventory = json.loads(inv_body)
    items = inventory['items']
    assert len(items) == 180 and len({i['number'] for i in items}) == 180
    assert [i['number'] for i in items] == list(range(9, 189))
    branch = run(['git', 'branch', '--show-current']).decode().strip()
    assert branch == 'main'
    head = run(['git', 'rev-parse', 'HEAD']).decode().strip()
    problem_ids = [i['headRefName'].split('dot/math-', 1)[1] for i in items]
    assert all(re.fullmatch(r'[0-9]+', i) for i in problem_ids)
    original_queues = batch_queue([i['headRefOid'] for i in items])
    missing_heads = [i['headRefOid'] for i, value in zip(items, original_queues) if value is None]
    remote_original = remote_immutable_queues(missing_heads)
    original_methods = ['local_immutable_Git_QUEUE_blob' if value is not None else 'fresh_GitHub_immutable_head_QUEUE_Blob_API_status_projection_only' for value in original_queues]
    original_queues = [value if value is not None else remote_original[i['headRefOid']] for i, value in zip(items, original_queues)]
    original = [queue_projection(v[0], pid, v[1]) for v, pid in zip(original_queues, problem_ids)]
    for value, method in zip(original, original_methods):
        value['method'] = method
    # Exact numbered metadata queries avoid a recent-first list cap omitting PR9–188.
    metadata = {}
    for offset in range(0, len(items), 60):
        aliases = ' '.join(
            f'p{i["number"]}:pullRequest(number:{i["number"]}){{number title state isDraft headRefName headRefOid baseRefName url createdAt updatedAt closedAt mergedAt mergeCommit{{oid}}}}'
            for i in items[offset:offset + 60])
        query = 'query{repository(owner:"AlecKriebel",name:"Math"){' + aliases + '}}'
        response = json.loads(run(['gh', 'api', 'graphql', '-f', 'query=' + query]))
        assert not response.get('errors'), response.get('errors')
        for value in response['data']['repository'].values():
            assert value is not None
            metadata[value['number']] = value
    assert set(metadata) == {i['number'] for i in items}
    original_eligible = [i for i, row in zip(items, original) if row['status'] == 'claimed_solved']
    eligible_current = batch_queue([metadata[i['number']]['headRefOid'] for i in original_eligible])
    current_status = {}
    for item, value in zip(original_eligible, eligible_current):
        h = metadata[item['number']]['headRefOid']
        if value is None and h in remote_original:
            value = remote_original[h]
        if value is None:
            b = current_remote_queue(h)
            git_blob = hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
            value = (b, git_blob)
            method = 'fresh_GitHub_contents_API_at_literal_metadata_head'
        else:
            method = 'immutable_Git_QUEUE_blob_body_at_fresh_GitHub_metadata_head_local_or_prior_same_literal_API_observation'
        cur = queue_projection(value[0], item['headRefName'].split('dot/math-', 1)[1], value[1])
        cur['method'] = method
        current_status[item['number']] = cur
    rows = []
    for item, submitted in zip(items, original):
        number = item['number']
        remote = metadata[number]
        cur = current_status.get(number)
        rows.append({'pr': number, 'url': remote['url'], 'problem_id': submitted['problem_id'],
                     'inventory_head': item['headRefOid'], 'submitted_QUEUE': submitted,
                     'submitted_status_exactly_claimed_solved': submitted['status'] == 'claimed_solved',
                     'current_GitHub_metadata': remote, 'current_head_equals_inventory_head': remote['headRefOid'] == item['headRefOid'],
                     'eligible_current_head_QUEUE': cur,
                     'current_status_exactly_claimed_solved': cur['status'] == 'claimed_solved' if cur is not None else None,
                     'historical_stage': item.get('stage'), 'historical_outcome': item.get('outcome'),
                     'historical_DOI': item.get('doi'),
                     'revised_action': ('ALREADY_PUBLISHED_PRESERVE' if item.get('doi') and submitted['status'] == 'claimed_solved'
                                        else 'ELIGIBLE_CURRENT_CLAIM_ORDERED_REVIEW' if cur and cur['status'] == 'claimed_solved'
                                        else 'SKIP_ENTIRELY_NONCLAIM_STATUS'),
                     'excluded_science_processed': False})
    status_counts = {}
    for row in rows:
        s = row['submitted_QUEUE']['status']
        status_counts[s] = status_counts.get(s, 0) + 1
    published = [r['pr'] for r in rows if r['revised_action'] == 'ALREADY_PUBLISHED_PRESERVE']
    pending = [r['pr'] for r in rows if r['revised_action'] == 'ELIGIBLE_CURRENT_CLAIM_ORDERED_REVIEW']
    ledger = {'schema': 'claimed-solved-only-status-inventory/v1', 'status': 'READY_ADMINISTRATIVE_SCOPE_ONLY',
              'actual_collector_pid': os.getpid(), 'started_utc': start, 'ended_utc': utc(),
              'objective': pin(OBJECTIVE), 'original_inventory': pin(P / 'inventory.json'),
              'main_branch_observed': branch, 'dated_local_HEAD': head,
              'original_inventory_readback_unchanged': (P / 'inventory.json').read_bytes() == inv_body,
              'original_inventory_count': 180, 'original_inventory_historical_completed_count': inventory['completed_count'],
              'historical_acceptance_count_is_not_revised_publication_count': True,
              'submitted_status_counts': status_counts, 'submitted_claimed_solved_count': len(original_eligible),
              'already_published_eligible_prs': published, 'already_published_eligible_count': len(published),
              'current_eligible_unpublished_order': pending,
              'revised_eligible_publication_percent': 100 * len(published) / len(original_eligible),
              'scope_inventory_completion_percent': 100, 'new_mathematics_or_priority_audit': False,
              'GitHub_writes': False, 'native_acceptance_or_Git_index_ref_body_writes': False,
              'rows': rows}
    write_json(D / 'SCOPE_LEDGER.json', ledger)
    write_json(C / 'COMPLETE_COMMANDS.json', COMMANDS)
    write_json(C / 'COLLECTION_RECEIPT.json', {'schema': 'claimed-solved-status-administrative-actual-collection/v1',
             'actual_pid': os.getpid(), 'started_utc': start, 'ended_utc': utc(), 'status': 'PASS_STATUS_COLLECTION',
             'command_count': len(COMMANDS), 'scope_ledger': pin(D / 'SCOPE_LEDGER.json'),
             'source': pin(Path(__file__)), 'source_prelaunch': pin(C / 'PRELAUNCH_SOURCE.py'),
             'production_or_mathematical_helpers_executed': False})
    print(json.dumps({k: ledger[k] for k in ['status','actual_collector_pid','submitted_status_counts','submitted_claimed_solved_count','already_published_eligible_prs','current_eligible_unpublished_order','revised_eligible_publication_percent']}))

if __name__ == '__main__':
    try:
        main()
    except BaseException:
        if C.exists():
            write_json(C / 'FAILED_COMPLETE_COMMANDS.json', COMMANDS)
            (C / 'COLLECTION_FAILURE.txt').write_text(traceback.format_exc())
        raise
