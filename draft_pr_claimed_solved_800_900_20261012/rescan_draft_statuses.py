#!/usr/bin/env python3
"""Read-only final PR800--900 metadata gate; never inspect mathematical files.

Unchanged commits reuse the authenticated initial QUEUE status. Changed draft
heads fetch only their QUEUE.md. Every other status is a metadata-only skip.
The caller must finish all returned pending PRs before completing the goal.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse
import base64
import datetime
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parent
BASELINE_SHA = '3c50ddb1b333d0b6865681acb64cee79c7b75cace7ef9c8c3b30a287ef9d3609'
REPO = 'AlecKriebel/Math'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def api(args, body=None):
    return subprocess.check_output(['gh', 'api', *args], input=body,
                                   stderr=subprocess.PIPE)


def changed_queue(head, pid):
    require(re.fullmatch('[0-9a-f]{40}', head), 'Invalid head object ID')
    raw = api(['-H', 'Accept: application/vnd.github.raw+json',
               f'repos/{REPO}/contents/{QUEUE}?ref={head}'])
    expected_oid = None
    if raw.lstrip().startswith(b'{'):
        meta = json.loads(raw)
        require(meta.get('type') == 'file', 'QUEUE file metadata required')
        expected_oid = meta['sha']
        if meta.get('encoding') != 'base64':
            meta = json.loads(api([f'repos/{REPO}/git/blobs/{expected_oid}']))
        require(meta.get('encoding') == 'base64', 'Complete QUEUE body required')
        raw = base64.b64decode(''.join(meta['content'].split()), validate=True)
        require(len(raw) == meta['size'], 'Complete QUEUE byte count')
    oid = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    require(expected_oid is None or oid == expected_oid, 'QUEUE Git identity')
    matches = []
    for line in raw.decode('utf-8').splitlines():
        cells = [cell.strip() for cell in line.split('|')]
        if line.startswith('|') and len(cells) > 9 and cells[2].split(' / ', 1)[0] == pid:
            matches.append(cells)
    require(len(matches) == 1, 'Unique exact problem QUEUE row required')
    return {'problem_status': matches[0][8], 'original_turns': matches[0][9],
            'queue_git_blob': oid, 'queue_bytes': len(raw),
            'queue_sha256': hashlib.sha256(raw).hexdigest(),
            'gate_evidence': 'Fresh QUEUE body at exact current PR head'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path, help='Fresh JSON output inside this program folder')
    args = parser.parse_args()
    destination = args.output.absolute()
    require(destination.is_relative_to(ROOT) and not destination.exists(), 'Fresh scoped output required')
    raw = (ROOT / 'eligibility_inventory.json').read_bytes()
    require(hashlib.sha256(raw).hexdigest() == BASELINE_SHA, 'Initial inventory external pin')
    original = {entry['number']: entry for entry in json.loads(raw)['entries']}
    require(set(original) == set(range(800, 901)), 'Complete initial 101-number inventory')
    completed = set(json.loads((ROOT / 'CURRENT_STATE.json').read_bytes())['completed_prs'])
    fields = 'number title url state isDraft headRefOid headRefName mergedAt mergeCommit{oid}'
    parts = [f'p{n}:pullRequest(number:{n}){{{fields}}}' for n in range(800, 901)]
    query = 'query{repository(owner:"AlecKriebel",name:"Math"){' + ' '.join(parts) + '}}'
    response = json.loads(api(['graphql', '--input', '-'], json.dumps({'query': query}).encode()))
    require(not response.get('errors') and response.get('data', {}).get('repository'), 'Complete PR metadata query')
    repository = response['data']['repository']

    def gate(number):
        current = repository.get('p' + str(number))
        require(current and current['number'] == number, 'PR metadata identity')
        entry = {'pr': number, 'problem_id': original[number]['problem_id'], **current}
        if current['state'] != 'OPEN' or not current['isDraft']:
            entry['action'] = 'metadata_only_not_open_draft'
            return entry
        if current['headRefOid'] == original[number]['headRefOid']:
            entry.update(problem_status=original[number]['head_queue_status'],
                         gate_evidence='Same immutable head as authenticated initial inventory')
        else:
            entry.update(changed_queue(current['headRefOid'], entry['problem_id']))
        if entry['problem_status'] != 'claimed_solved':
            entry['action'] = 'metadata_only_skip_non_claimed_status'
        else:
            entry['action'] = ('eligible_reopened_or_changed_after_completion' if number in completed
                               else 'eligible_unprocessed_claimed_solved_draft')
        return entry

    with ThreadPoolExecutor(max_workers=4) as pool:
        entries = list(pool.map(gate, range(800, 901)))
    pending = [entry['pr'] for entry in entries if entry['action'].startswith('eligible_')]
    result = {'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'status': 'PENDING_CLAIMED_SOLVED_DRAFTS' if pending else 'NO_UNPROCESSED_CLAIMED_SOLVED_DRAFTS',
              'completion_estimate_percent': 98,
              'scope': 'Only PR metadata and exact QUEUE status; no mathematical/source audit or remote mutation.',
              'range': [800, 900], 'direction': 'ascending', 'initial_inventory_sha256': BASELINE_SHA,
              'fresh_PR_metadata_count': len(entries), 'pending_prs_ascending': pending,
              'skip_rule': 'Every status other than exact claimed_solved is skipped entirely.',
              'entries': entries}
    with destination.open('x') as stream:
        stream.write(json.dumps(result, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'status': result['status'], 'metadata_count': len(entries),
                      'pending_prs_ascending': pending}))


if __name__ == '__main__':
    main()
