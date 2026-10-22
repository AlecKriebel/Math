"""Read-only exact-head eligibility below completed PR210; no science on skipped statuses."""
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
import base64
import hashlib
import json
import re
import subprocess

HERE = Path(__file__).resolve().parent
PRIVATE = HERE / 'private_transport/gate_01'
assert __import__('json').loads((HERE.parent/'audits/pr210_5100033/initial_review_20261015/FINAL_COMPLETION_CHECKPOINT_PUBLICATION_RECEIPT.json').read_text())['actual_publication_tracker_native_merge_complete'] is True
PRIVATE.mkdir(parents=True,exist_ok=False)
GH = '/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
B = 'repos/AlecKriebel/Math/'


def get(path, target):
    r = subprocess.run([GH, 'api', B + path], capture_output=True, timeout=60)
    target.write_bytes(r.stdout)
    target.with_suffix('.stderr.txt').write_bytes(r.stderr)
    assert r.returncode == 0, str(target)
    return json.loads(r.stdout)


query = '''query($cursor:String){repository(owner:"AlecKriebel",name:"Math"){
 pullRequests(first:100,after:$cursor,states:OPEN,orderBy:{field:CREATED_AT,direction:ASC}){
 nodes{number title isDraft headRefOid headRefName}
 pageInfo{hasNextPage endCursor}}}}'''
cursor = None
nodes = []
pages = []
while True:
    request = PRIVATE / f'inventory_{len(pages)+1}_request.json'
    request.write_text(json.dumps({'query': query, 'variables': {'cursor': cursor}}))
    r = subprocess.run([GH, 'api', 'graphql', '--input', str(request)], capture_output=True, timeout=60)
    (PRIVATE / f'inventory_{len(pages)+1}_response.json').write_bytes(r.stdout)
    assert r.returncode == 0
    response = json.loads(r.stdout)
    assert not response.get('errors')
    page = response['data']['repository']['pullRequests']
    rows = page['nodes']
    nodes += rows
    numbers = [x['number'] for x in rows]
    pages.append({'items': len(rows), 'minimum': min(numbers) if numbers else None,
                  'maximum': max(numbers) if numbers else None, 'has_next_page': page['pageInfo']['hasNextPage']})
    if not page['pageInfo']['hasNextPage']:
        break
    cursor = page['pageInfo']['endCursor']
inventory = {x['number']: x for x in nodes}
lower = sorted([x for x in inventory.values() if x['isDraft'] and x['number'] < 210 and x['number'] != 8], key=lambda x: -x['number'])
(HERE / 'OPEN_DRAFT_BOUNDARY_INVENTORY.json').write_text(json.dumps(lower, indent=2) + '\n')
(HERE / 'INVENTORY_RECEIPT.json').write_text(json.dumps({
    'utc': datetime.now(timezone.utc).isoformat(), 'method': 'Native GraphQL complete OPEN pagination, then descending draft filter below completed210',
    'pages': pages, 'lower_open_drafts': len(lower), 'PR8_excluded': True,
    'read_only': True}, indent=2) + '\n')


def gate(item):
    n = item['number']
    T = PRIVATE / str(n)
    T.mkdir()
    pr = get('pulls/' + str(n), T / 'PR.json')
    result = {'utc': datetime.now(timezone.utc).isoformat(), 'PR': n, 'title': pr['title'],
              'head': pr['head']['sha'], 'state': pr['state'], 'draft': pr['draft'],
              'merged': pr['merged'], 'read_only_gate': True}
    if pr['state'] != 'open' or not pr['draft'] or pr['merged']:
        result.update(eligible=False, reason='not_current_open_draft')
    else:
        ids = re.findall(r'\d{4,}', pr['head']['ref'])
        assert len(ids) == 1, (n, pr['head']['ref'])
        pid = ids[0]
        q = get('contents/unsolved_math_prioritization/QUEUE.md?ref=' + pr['head']['sha'], T / 'QUEUE.json')
        raw = base64.b64decode(q['content'])
        rows = [s for s in raw.decode().splitlines() if re.match(r'\|\s*\d+\s*\|\s*' + pid + r'\s*/', s)]
        assert len(rows) == 1, (n, pid)
        row = rows[0]
        status = row.split('|')[8].strip()
        result.update(problem_id=pid, branch=pr['head']['ref'], Queue_path='unsolved_math_prioritization/QUEUE.md',
                      Queue_blob=q['sha'], Queue_sha256=hashlib.sha256(raw).hexdigest(), queue_row=row,
                      status=status, eligible=status == 'claimed_solved', reason='exact_current_PR_head_queue_status')
    (HERE / f'PR{n}_ELIGIBILITY.json').write_text(json.dumps(result, indent=2) + '\n')
    return result


results = []
selected = None
for item in lower:
    result=gate(item);results.append(result)
    if result['eligible']:
        selected=result
        break
decision = {'utc': datetime.now(timezone.utc).isoformat(), 'from_cursor': 209,
            'previous_complete_PR': 210, 'previous_DOI': '10.5281/zenodo.23398175',
            'program_counts': [44, 21, 21, 0], 'held_uncompleted_PRs': [293, 292, 280, 239],
            'PR8_excluded': True, 'read_only_current_head_gates': results, 'selected': selected,
            'no_science_review_or_mutation_of_non_claimed_status': True,
            'all_current_lower_open_drafts_exhausted': selected is None,
            'goal_complete_or_blocked_not_inferred': True}
(HERE / 'SELECTION.json').write_text(json.dumps(decision, indent=2) + '\n')
print(json.dumps({'gates': [{'PR': x['PR'], 'status': x.get('status'), 'eligible': x['eligible']} for x in results],
                  'selected': selected, 'lower_open_drafts': len(lower)}, indent=2))
