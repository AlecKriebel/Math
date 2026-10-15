#!/usr/bin/env python3
"""Exact-head one-row priority correction; no action without a final review gate."""
import argparse
import base64
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import urllib.parse

PROGRAM = Path(__file__).resolve().parent
AUDIT = PROGRAM / 'audits/pr463_6000016'
REPO = 'AlecKriebel/Math'
ORIGINAL = '982fcf87d60c9f8d4ec853d5dd5f4ad6021a6649'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def api(endpoint, payload=None, method='POST'):
    cmd = ['gh', 'api', 'repos/' + REPO + '/' + endpoint]
    if payload is not None:
        cmd += ['--method', method, '--input', '-']
    result = subprocess.run(cmd, input=None if payload is None else json.dumps(payload), capture_output=True, text=True)
    require(result.returncode == 0, result.stderr.strip())
    return json.loads(result.stdout)

def output_path(name):
    path = AUDIT / name
    require(AUDIT.resolve() == AUDIT and not AUDIT.is_symlink(), 'Output directory alias')
    require(not path.is_symlink(), 'Output symlink')
    if path.exists():
        require(path.is_file() and path.stat().st_nlink == 1, 'Nonregular or hardlinked output')
    return path

def dump(name, value):
    path = output_path(name)
    # Each fixed destination was checked before dispatch; writes stay in the audit folder.
    path.write_text(json.dumps(value, indent=2) + '\n')

def eligible(branch):
    pr = api('pulls/463')
    require(pr['state'] == 'open' and pr['draft'] is True and pr['head']['sha'] == ORIGINAL
            and pr['head']['ref'] == branch and pr['head']['repo']['full_name'] == REPO
            and pr['base']['ref'] == 'main' and pr['base']['repo']['full_name'] == REPO,
            'Original open draft head/repository/base changed')
    require(api('git/ref/heads/' + urllib.parse.quote(branch, safe=''))['object']['sha'] == ORIGINAL,
            'Original branch ref changed')
    return pr

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    for name in ['STATUS_REPAIR_PREFLIGHT.json', 'STATUS_REPAIR_OPERATION.json', 'STATUS_REPAIR_RECEIPT.json']:
        output_path(name)
    gate = json.loads((AUDIT / 'PRIORITY_DISPOSITION_GATE.json').read_text())
    require(gate.get('verdict') == 'ACCEPTED_PRIORITY_CLASSIFICATION' and gate.get('pr') == 463
            and gate.get('problem_id') == '6000016' and gate.get('original_head') == ORIGINAL
            and gate.get('recommended_status') == 'already_solved', 'Final exact priority gate absent')
    require(gate.get('root_read_entire_final_reports') is True and gate.get('helper_sha256') == sha(Path(__file__)),
            'Root acceptance or reviewed helper binding absent')
    reviews = gate['reviews']
    families = {r['family'] for r in reviews}
    require(len(reviews) == len(families) and {'source_topology', 'global_obstruction', 'reproduction',
            'priority', 'candidate_adversary', 'disposition_adversary'}.issubset(families), 'Distinct complete reviews absent')
    for review in reviews:
        require(type(review.get('blocking_issues')) is int and review['blocking_issues'] == 0
                and type(review.get('unresolved_disposition_issues')) is int
                and review['unresolved_disposition_issues'] == 0, 'Unresolved review issue')
    for entry in gate['reviewed_files']:
        path = AUDIT / entry['path']
        require(path.resolve().is_relative_to(AUDIT) and path.is_file() and not path.is_symlink()
                and sha(path) == entry['sha256'], 'Accepted evidence drift')
    link = gate['published_disposition_url']
    require(link.startswith('https://github.com/' + REPO + '/blob/') and '/DISPOSITION_SYNTHESIS.md' in link,
            'Published immutable disposition link absent')
    branch = json.loads((AUDIT / 'pr_metadata.json').read_text())['headRefName']
    eligible(branch)
    original = api('git/commits/' + ORIGINAL)
    tree_sha = original['tree']['sha']
    for part in QUEUE.split('/'):
        matches = [e for e in api('git/trees/' + tree_sha)['tree'] if e['path'] == part]
        require(len(matches) == 1, 'QUEUE Git tree path not unique')
        item = matches[0]
        tree_sha = item['sha']
    require(item['type'] == 'blob' and item['mode'] == '100644', 'QUEUE not regular Git blob')
    before = base64.b64decode(api('git/blobs/' + tree_sha)['content'])
    source = json.loads((AUDIT / 'SOURCE_RECEIPT.json').read_text())
    require(hashlib.sha256(before).hexdigest() == source['queue_sha256'], 'Frozen original QUEUE mismatch')
    lines = before.decode().splitlines(keepends=True)
    headers = [x for x in lines if x.startswith('|') and 'ID / code' in x and 'Status' in x]
    require(len(headers) == 1, 'QUEUE header not unique')
    columns = [x.strip() for x in headers[0].split('|')[1:-1]]
    indices = [i for i, x in enumerate(lines) if x.startswith('|') and x.split('|')[2].strip().startswith('6000016 /')]
    require(len(indices) == 1, 'Selected row not unique')
    index = indices[0]
    old_row = lines[index].rstrip('\r\n')
    cells = old_row.split('|')[1:-1]
    require(len(cells) == len(columns), 'QUEUE schema mismatch')
    require(cells[columns.index('Status')].strip() == 'claimed_solved', 'Excluded status: stop without processing')
    old_cells = list(cells)
    cells[columns.index('Status')] = ' already_solved '
    finding = ('2026-10-12: Priority correction: unrestricted positive Hessian-metric stability has a routine negative answer from the exact Baues-Goldman affine-torus deformation (arXiv v1, 20 Jan 2004, pp.24-25) and Delanoe 1989 Theorem 3 plus Jorgens 1954 Satz 1. The older theorem chain excludes every positive Hessian metric via a constant-volume replacement and full-plane quadratic-potential rigidity; merely excluding parallel candidates would not suffice. Mathematics independently verified. An earlier explicitly printed answer to original item5(b) and a first solver were not established; Shima2007/Cheng-Yau access gaps are not the decisive basis. [Independent disposition audit](' + link + '). Corrected to already_solved and immediately skipped; no paper, DOI or merge.')
    require('|' not in finding and '\n' not in finding, 'Invalid finding cell')
    cells[columns.index('Findings')] = ' ' + finding + ' '
    require([i for i, (a, b) in enumerate(zip(old_cells, cells)) if a != b]
            == sorted([columns.index('Status'), columns.index('Findings')]), 'Unexpected cell alteration')
    ending = '\r\n' if lines[index].endswith('\r\n') else '\n' if lines[index].endswith('\n') else ''
    lines[index] = '|' + '|'.join(cells) + '|' + ending
    after = ''.join(lines).encode()
    require(len(before.decode().splitlines()) == len(after.decode().splitlines())
            and [i for i, (a, b) in enumerate(zip(before.decode().splitlines(), after.decode().splitlines())) if a != b] == indices,
            'Non-target QUEUE alteration')
    summary = {'at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'pr': 463,
               'problem_id': '6000016', 'old_status': 'claimed_solved', 'new_status': 'already_solved',
               'old_head': ORIGINAL, 'branch': branch, 'files_changed': [QUEUE],
               'old_queue_sha256': hashlib.sha256(before).hexdigest(), 'new_queue_sha256': hashlib.sha256(after).hexdigest(),
               'selected_old_row': old_row, 'selected_new_row': lines[index].rstrip('\r\n'),
               'state': 'read_only_preflight', 'shared_checkout_index': 'untouched main',
               'subsequent_scope': 'immediate skip: no paper/Zenodo/tracker/merge/close/comment/further audit'}
    dump('STATUS_REPAIR_PREFLIGHT.json', summary)
    if not args.apply:
        print(json.dumps(summary, indent=2))
        return
    require(not (AUDIT / 'STATUS_REPAIR_OPERATION.json').exists(), 'Prior operation exists: do not repeat mutation')
    blob = api('git/blobs', {'content': base64.b64encode(after).decode(), 'encoding': 'base64'})['sha']
    new_tree = api('git/trees', {'base_tree': original['tree']['sha'],
                    'tree': [{'path': QUEUE, 'mode': '100644', 'type': 'blob', 'sha': blob}]})['sha']
    eligible(branch)
    commit = api('git/commits', {'message': 'Correct Hessian stability priority after independent primary theorem audit',
                               'tree': new_tree, 'parents': [ORIGINAL]})['sha']
    comparison = api('compare/' + ORIGINAL + '...' + commit)
    require([x['filename'] for x in comparison['files']] == [QUEUE], 'Commit changed other paths')
    summary.update(state='commit_created_before_ref_update', repair_commit=commit, queue_git_blob_sha=blob)
    dump('STATUS_REPAIR_OPERATION.json', summary)
    eligible(branch)
    ref = 'git/refs/heads/' + urllib.parse.quote(branch, safe='')
    try:
        api(ref, {'sha': commit, 'force': False}, method='PATCH')
    except RuntimeError:
        require(api('git/ref/heads/' + urllib.parse.quote(branch, safe=''))['object']['sha'] == commit,
                'Branch update uncertain; no retry')
    require(api('git/ref/heads/' + urllib.parse.quote(branch, safe=''))['object']['sha'] == commit,
            'Branch readback differs')
    require(base64.b64decode(api('git/blobs/' + blob)['content']) == after, 'Status blob exact-byte readback differs')
    summary.update(state='status_repair_verified_immediately_excluded',
                   verified_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   readback='Exact selected branch ref and immutable QUEUE blob bytes matched',
                   basis='Routine original-target implication from primary classical theorem chain and exact 2004 family; no earlier explicit answer or first solver certified',
                   concurrency_scope='Exact head/ref checked before nonforced update; Git-data PATCH is not atomic expected-old-SHA CAS')
    dump('STATUS_REPAIR_RECEIPT.json', summary)
    print(json.dumps({'pr': 463, 'new_status': 'already_solved', 'repair_commit': commit,
                      'state': summary['state'], 'subsequent_scope': summary['subsequent_scope']}, indent=2))

if __name__ == '__main__':
    main()
