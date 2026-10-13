"""Status-only intake; never reads PR bodies, proofs, or verification files."""
import base64
import collections
import datetime
import hashlib
import json
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent
REPO = 'AlecKriebel/Math'

def gh(*args):
    return json.loads(subprocess.check_output(['gh', *args], text=True))

def queue_rows(text):
    rows = {}
    for number, line in enumerate(text.splitlines(), 1):
        cells = [c.strip() for c in line.split('|')]
        if len(cells) < 10 or not re.fullmatch(r'\d+ / [^|]+', cells[2]):
            continue
        problem_id = cells[2].split(' / ')[0]
        # Status precedes the turns column. This avoids pipes within titles.
        status_match = re.search(r'\|\s*([a-z][a-z0-9_]*)\s*\|\s*(?:\d+/\d+|—|-)\s*\|', line)
        if not status_match:
            raise ValueError(f'Cannot parse queue status for {problem_id}, line {number}')
        if problem_id in rows:
            raise ValueError(f'Duplicate queue ID {problem_id}')
        rows[problem_id] = {'status': status_match.group(1), 'line': number}
    return rows

def main():
    captured = datetime.datetime.now(datetime.timezone.utc).isoformat()
    main_sha = gh('api', f'repos/{REPO}/commits/main')['sha']
    queue_api = gh('api', f'repos/{REPO}/contents/unsolved_math_prioritization/QUEUE.md?ref={main_sha}')
    queue = base64.b64decode(queue_api['content'])
    (ROOT / 'queue_remote_main.md').write_bytes(queue)
    rows = queue_rows(queue.decode())
    prs = gh('pr', 'list', '--repo', REPO, '--state', 'all', '--limit', '2500',
             '--json', 'number,title,state,isDraft,headRefName,headRefOid,baseRefName,url')
    prs = sorted((p for p in prs if 1000 <= p['number'] <= 1100), key=lambda p: p['number'])
    (ROOT / 'pr_metadata.json').write_text(json.dumps(prs, indent=2) + '\n')
    inventory = []
    for p in prs:
        if p['state'] != 'OPEN' or not p['isDraft']:
            inventory.append({**p, 'disposition': 'skip_not_open_draft'})
            continue
        candidates = [pid for pid in rows if re.search(r'(?<!\d)' + re.escape(pid) + r'(?!\d)', p['title'] + ' ' + p['headRefName'])]
        if len(candidates) != 1:
            # File paths identify the problem; file contents are never fetched here.
            files = gh('api', f'repos/{REPO}/pulls/{p["number"]}/files?per_page=100')
            paths = [f['filename'] for f in files]
            candidates = sorted(set(re.findall(r'^unsolved_math_prioritization/attempts/(\d+)/', '\n'.join(paths), re.M)))
        if len(candidates) != 1 or candidates[0] not in rows:
            raise ValueError(f'Ambiguous problem identity for PR {p["number"]}: {candidates}')
        pid = candidates[0]
        row = rows[pid]
        inventory.append({**p, 'problem_id': pid, 'queue_status': row['status'],
                          'queue_line': row['line'],
                          'disposition': 'eligible_pending_audit' if row['status'] == 'claimed_solved' else 'skip_status'})
    document = {'captured_utc': captured, 'repository': REPO, 'direction': 'ascending',
                'range_inclusive': [1000, 1100], 'queue_main_commit': main_sha,
                'queue_blob_sha': queue_api['sha'], 'queue_sha256': hashlib.sha256(queue).hexdigest(),
                'gate': 'queue_status == claimed_solved AND OPEN AND draft', 'prs': inventory}
    (ROOT / 'inventory.json').write_text(json.dumps(document, indent=2) + '\n')
    counts = collections.Counter(p.get('queue_status', p['disposition']) for p in inventory)
    eligible = [{k: p[k] for k in ('number', 'problem_id', 'queue_status', 'headRefOid', 'title')}
                for p in inventory if p['disposition'] == 'eligible_pending_audit']
    state = {'phase': 'status_intake_complete', 'estimated_completion_percent': 5,
             'next_pr': eligible[0]['number'] if eligible else None, 'eligible_count': len(eligible),
             'eligible_completed': [], 'counts': dict(counts), 'captured_utc': captured}
    (ROOT / 'STATE.json').write_text(json.dumps(state, indent=2) + '\n')
    print(json.dumps({'counts': dict(counts), 'eligible': eligible, 'main_sha': main_sha}, indent=2))

if __name__ == '__main__':
    main()
