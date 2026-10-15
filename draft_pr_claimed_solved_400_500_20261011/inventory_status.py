#!/usr/bin/env python3
"""Read only draft metadata and exact QUEUE status; never inspect skipped work."""
import concurrent.futures
import datetime
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = 'AlecKriebel/Math'

def gh(*args):
    return subprocess.check_output(['gh', *args])

def status_at_head(pr):
    if not pr['isDraft']:
        return {**pr, 'scope': 'skip_non_draft'}
    raw = gh('api', f'repos/{REPO}/contents/unsolved_math_prioritization/QUEUE.md?ref={pr["headRefOid"]}',
             '-H', 'Accept: application/vnd.github.raw+json')
    rows = {}
    status_column = None
    for line in raw.decode().splitlines():
        if not line.startswith('|'):
            continue
        cells = [s.strip() for s in line.split('|')[1:-1]]
        if 'Status' in cells and 'ID / code' in cells:
            status_column = cells.index('Status')
        if status_column is None or len(cells) <= status_column:
            continue
        m = re.match(r'(\d{4,9})(?:\s|/|$)', cells[1])
        if m:
            rows[m.group(1)] = cells[status_column]
    ids = re.findall(r'(?<!\d)\d{4,9}(?!\d)', pr['title'] + ' ' + pr['headRefName'])
    ids = list(dict.fromkeys(i for i in ids if i in rows))
    statuses = {i: rows[i] for i in ids}
    return {**pr, 'problem_ids': ids, 'queue_statuses': statuses,
            'queue_sha256': hashlib.sha256(raw).hexdigest(),
            'status_basis': 'QUEUE.md at exact PR head SHA',
            'scope': 'eligible' if ids and all(s == 'claimed_solved' for s in statuses.values()) else 'skip'}

def main():
    prs = json.loads(gh('pr', 'list', '--repo', REPO, '--state', 'open', '--limit', '1000',
                       '--json', 'number,title,isDraft,headRefName,headRefOid,baseRefName,url'))
    prs = sorted((p for p in prs if 400 <= p['number'] <= 500), key=lambda p: p['number'], reverse=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        checked = list(pool.map(status_at_head, prs))
    receipt = {'captured_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'repository': REPO, 'range_inclusive': [400, 500], 'order': 'descending',
               'strict_filter': 'exactly claimed_solved in the selected PR head QUEUE.md', 'prs': checked}
    out = ROOT / 'inventory' / 'head_status_inventory.json'
    out.write_text(json.dumps(receipt, indent=2) + '\n')
    eligible = [p for p in checked if p['scope'] == 'eligible']
    print(json.dumps({'open_in_range': len(checked), 'eligible': [{'pr': p['number'], 'ids': p['problem_ids'], 'title': p['title']} for p in eligible],
                      'skipped_count': len(checked) - len(eligible)}, indent=2))

if __name__ == '__main__':
    main()
