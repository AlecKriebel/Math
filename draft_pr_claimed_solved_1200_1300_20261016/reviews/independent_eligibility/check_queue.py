#!/usr/bin/env python3
"""Independently parse exact Status cells at immutable GitHub main/PR head SHAs."""
import base64
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent
METADATA = json.loads((ROOT / 'metadata_receipt.json').read_text())
PATH = 'unsolved_math_prioritization/QUEUE.md'

def fetch_queue(commit):
    endpoint = f'repos/AlecKriebel/Math/contents/{PATH}?ref={commit}'
    raw = subprocess.check_output(['gh', 'api', endpoint])
    response = json.loads(raw)
    assert response['path'] == PATH
    assert response['encoding'] == 'base64'
    content = base64.b64decode(response['content'])
    assert len(content) == response['size']
    git_blob = hashlib.sha1(b'blob ' + str(len(content)).encode() + b'\0' + content).hexdigest()
    assert git_blob == response['sha']
    return content, {
        'commit_sha': commit,
        'endpoint': endpoint,
        'queue_blob_sha': git_blob,
        'size': len(content),
        'content_sha256': hashlib.sha256(content).hexdigest(),
        'obtained_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
    }

def cells(line):
    return [c.strip() for c in re.split(r'(?<!\\)\|', line.strip().removeprefix('|').removesuffix('|'))]

def parse(content):
    rows, headers = {}, []
    active_header = None
    for lineno, line in enumerate(content.decode().splitlines(), 1):
        if not line.lstrip().startswith('|'):
            continue
        values = cells(line)
        if 'Status' in values:
            assert values.count('Status') == 1
            assert 'ID / code' in values, values
            active_header = {
                'line': lineno, 'cells': values,
                'status_column_zero_based': values.index('Status'),
                'id_column_zero_based': values.index('ID / code'),
            }
            headers.append(active_header)
            continue
        if active_header is None:
            continue
        idx = active_header['id_column_zero_based']
        status_idx = active_header['status_column_zero_based']
        if len(values) <= max(idx, status_idx):
            continue
        raw_id = values[idx]
        match = re.match(r'^`?(\d+)(?=[` /]|$)', raw_id)
        if match is None:
            continue
        problem_id = match.group(1)
        assert problem_id not in rows, f'duplicate Problem ID {problem_id}'
        rows[problem_id] = {
            'line': lineno,
            'problem_id': problem_id,
            'raw_problem_id_cell': raw_id,
            'raw_status_cell': values[status_idx],
            'status': values[status_idx].strip('`'),
            'header_line': active_header['line'],
            'status_column_zero_based': status_idx,
        }
    assert headers and rows
    return rows, headers

started = dt.datetime.now(dt.timezone.utc).isoformat()
main_content, main_receipt = fetch_queue(METADATA['main_sha'])
main_rows, main_headers = parse(main_content)
print('Headers', json.dumps(main_headers))
pr_records = []
all_targets = set()
for item in METADATA['pull_requests']:
    p = item['metadata']
    if p is None:
        pr_records.append({'number': item['requested_number'], 'present': False})
        continue
    title_tokens = sorted(set(re.findall(r'(?<!\d)\d{4,8}(?!\d)', p['title'])))
    branch_tokens = sorted(set(re.findall(r'(?<!\d)\d{4,8}(?!\d)', p['headRefName'])))
    targets = sorted((set(title_tokens) | set(branch_tokens)) & set(main_rows), key=int)
    assert targets, f'no problem target for PR{p["number"]}'
    all_targets.update(targets)
    pr_records.append({
        'number': p['number'], 'present': True, 'state': p['state'], 'draft': p['isDraft'],
        'head_sha': p['headRefOid'], 'head_ref': p['headRefName'], 'title': p['title'],
        'title_numeric_tokens': title_tokens, 'branch_numeric_tokens': branch_tokens,
        'problem_ids': targets,
        'main_statuses': {pid: main_rows[pid] for pid in targets},
    })

unique_heads = sorted(set(p['head_sha'] for p in pr_records if p['present']))
head_contents, receipts = {}, []
with ThreadPoolExecutor(max_workers=8) as pool:
    futures = {pool.submit(fetch_queue, sha): sha for sha in unique_heads}
    for future in as_completed(futures):
        sha = futures[future]
        content, receipt = future.result()
        rows, headers = parse(content)
        head_contents[sha] = (rows, headers, receipt)
        receipts.append(receipt)

eligible_heads, eligible_main, mismatches = [], [], []
for p in pr_records:
    if not p['present']:
        continue
    rows, headers, receipt = head_contents[p['head_sha']]
    p['head_queue_blob_sha'] = receipt['queue_blob_sha']
    p['head_statuses'] = {pid: rows.get(pid) for pid in p['problem_ids']}
    assert all(p['head_statuses'].values()), f'missing head target in PR{p["number"]}'
    active = p['state'] == 'OPEN' and p['draft']
    main_ok = any(r['raw_status_cell'] == 'claimed_solved' for r in p['main_statuses'].values())
    head_ok = any(r['raw_status_cell'] == 'claimed_solved' for r in p['head_statuses'].values())
    p['eligible_at_main'] = active and main_ok
    p['eligible_at_head'] = active and head_ok
    if p['eligible_at_main']:
        eligible_main.append(p['number'])
    if p['eligible_at_head']:
        eligible_heads.append(p['number'])
    if {k:v['raw_status_cell'] for k,v in p['main_statuses'].items()} != {k:v['raw_status_cell'] for k,v in p['head_statuses'].items()}:
        mismatches.append(p['number'])
    print(p['number'], ','.join(p['problem_ids']),
          'main=' + ','.join(r['raw_status_cell'] for r in p['main_statuses'].values()),
          'head=' + ','.join(r['raw_status_cell'] for r in p['head_statuses'].values()))

expected = list(range(1200,1301))
assert [p['number'] for p in pr_records] == expected
result = {
    'started_utc': started, 'completed_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
    'coverage': {'first':1200, 'last':1300, 'expected':101, 'actual':len(pr_records),
                 'every_number_exactly_once':True, 'all_present':all(p['present'] for p in pr_records),
                 'open_drafts':sum(p['present'] and p['state']=='OPEN' and p['draft'] for p in pr_records)},
    'status_match_rule':'raw trimmed Markdown Status cell equals claimed_solved; no substring/case matching',
    'main_queue_receipt':main_receipt, 'main_headers':main_headers,
    'main_row_count':len(main_rows), 'unique_problem_count':len(all_targets),
    'unique_head_count':len(unique_heads),
    'unique_queue_blob_count':len({r['queue_blob_sha'] for r in receipts} | {main_receipt['queue_blob_sha']}),
    'head_queue_receipts':sorted(receipts,key=lambda r:r['commit_sha']),
    'head_headers_by_blob':{receipt['queue_blob_sha']:headers for rows,headers,receipt in head_contents.values()},
    'eligible_at_main':eligible_main, 'eligible_at_heads':eligible_heads,
    'main_head_status_mismatch_prs':mismatches,
    'main_status_counts':dict(Counter(r['raw_status_cell'] for p in pr_records if p['present'] for r in p['main_statuses'].values())),
    'head_status_counts':dict(Counter(r['raw_status_cell'] for p in pr_records if p['present'] for r in p['head_statuses'].values())),
    'pull_requests':pr_records,
}
(ROOT / 'independent_eligibility.json').write_text(json.dumps(result,indent=2)+'\n')
print('RESULT', json.dumps({k:result[k] for k in ['coverage','unique_problem_count','unique_head_count','unique_queue_blob_count','eligible_at_main','eligible_at_heads','main_head_status_mismatch_prs','main_status_counts','head_status_counts']}))
