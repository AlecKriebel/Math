#!/usr/bin/env python3
"""Reproduce the exact-status gate without opening any PR research content."""
import collections
import hashlib
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent


def queue_rows(raw):
    result = []
    for line_number, line in enumerate(raw.decode('utf-8').splitlines(), 1):
        if not line.startswith('|'):
            continue
        cells = [part.strip() for part in line.split('|')[1:-1]]
        if len(cells) < 9 or not re.fullmatch(r'\d+', cells[0]):
            continue
        identifier = cells[1].split(' / ')[0].strip()
        if not identifier.isdecimal():
            continue
        result.append({
            'problem_id': identifier,
            'code': cells[1].partition(' / ')[2].strip(),
            'title': cells[2],
            'status': cells[7],
            'line_number': line_number,
            'row_sha256': hashlib.sha256(line.encode()).hexdigest(),
        })
    return result


def match_row(pr, rows):
    # Titles identify the problem; branch names contain unrelated dates/numbers.
    title_numbers = set(re.findall(r'(?<!\d)\d+(?!\d)', pr['title']))
    matched = [r for r in rows if r['problem_id'] in title_numbers]
    if not matched:
        matched = [r for r in rows if r['code'] and r['code'] in pr['title']]
    if len(matched) != 1:
        raise ValueError(f"Ambiguous/missing queue mapping for PR {pr['number']}: {matched}")
    return matched[0]


def reproduce():
    prs = json.loads((ROOT / 'PR_METADATA.json').read_text())['prs']
    numbers = [p['number'] for p in prs]
    if numbers != list(range(1100, 1201)):
        raise ValueError('Metadata does not cover each PR number exactly once in ascending order')
    receipt = json.loads((ROOT / 'evidence/QUEUE_SNAPSHOT_RECEIPT.json').read_text())
    queues = {}
    for source in ('local', 'remote_main'):
        raw = (ROOT / f'evidence/QUEUE.{source}.md').read_bytes()
        expected = receipt[f"{'remote' if source == 'remote_main' else 'local'}_queue_sha256"]
        if hashlib.sha256(raw).hexdigest() != expected:
            raise ValueError(f'{source} queue snapshot checksum mismatch')
        queues[source] = queue_rows(raw)
    head_gate = json.loads((ROOT / 'evidence/HEAD_QUEUE_GATE.json').read_text())
    head_checks = head_gate['checks']
    if [c['pr'] for c in head_checks] != numbers:
        raise ValueError('PR-head queue evidence does not cover each PR exactly once')
    dispositions = []
    for pr, head in zip(prs, head_checks):
        remote = match_row(pr, queues['remote_main'])
        local = match_row(pr, queues['local'])
        if remote['problem_id'] != local['problem_id'] or remote['status'] != local['status']:
            raise ValueError(f"Live workspace versus remote queue disagreement for PR {pr['number']}")
        parsed_head_rows = queue_rows(head['exact_queue_row'].encode())
        if len(parsed_head_rows) != 1:
            raise ValueError(f"Invalid PR-head queue row for PR {pr['number']}")
        parsed_head = parsed_head_rows[0]
        expected_head_source = (
            f"https://github.com/AlecKriebel/Math/blob/{pr['headRefOid']}/"
            'unsolved_math_prioritization/QUEUE.md'
        )
        if (head['head_sha'] != pr['headRefOid'] or
                head['queue_source'] != expected_head_source or
                parsed_head['problem_id'] != remote['problem_id'] or
                parsed_head['status'] != remote['status'] or
                any(parsed_head[key] != head['row'][key]
                    for key in ('problem_id', 'code', 'title', 'status', 'row_sha256'))):
            raise ValueError(f"PR-head versus main queue disagreement or invalid evidence for PR {pr['number']}")
        eligible = pr['state'] == 'OPEN' and pr['isDraft'] and remote['status'] == 'claimed_solved'
        dispositions.append({
            'pr': pr['number'], 'url': pr['url'], 'head_sha': pr['headRefOid'],
            'problem_id': remote['problem_id'], 'problem_code': remote['code'],
            'pr_state': pr['state'], 'is_draft': pr['isDraft'],
            'remote_queue_status': remote['status'], 'local_queue_status': local['status'],
            'head_queue_status': parsed_head['status'],
            'remote_queue_line': remote['line_number'], 'remote_queue_row_sha256': remote['row_sha256'],
            'eligible': eligible,
            'disposition': 'eligible_for_review' if eligible else 'skipped_status_not_claimed_solved',
        })
    return {
        'scope': {'first_pr': 1100, 'last_pr': 1200, 'order': 'ascending', 'required_status': 'claimed_solved'},
        'queue_sources': 'Workspace, pinned remote main, and pinned PR heads; all 101 relevant statuses agree',
        'remote_main_sha': receipt['remote_main_sha'],
        'counts': {'total': len(dispositions), 'eligible': sum(d['eligible'] for d in dispositions),
                   'skipped': sum(not d['eligible'] for d in dispositions)},
        'status_counts': dict(collections.Counter(d['remote_queue_status'] for d in dispositions)),
        'dispositions': dispositions,
    }


if __name__ == '__main__':
    result = reproduce()
    expected = ROOT / 'DISPOSITIONS.json'
    if expected.exists() and json.loads(expected.read_text()) != result:
        raise SystemExit('Saved dispositions differ from reproduced gate')
    print(json.dumps({'verified': True, 'counts': result['counts'], 'status_counts': result['status_counts']}, indent=2))
