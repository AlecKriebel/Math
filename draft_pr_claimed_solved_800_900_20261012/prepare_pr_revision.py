#!/usr/bin/env python3
"""Prepare a scoped PR revision atop current main without changing the checkout.

Input mapping enumerates reviewed local files, expected SHA256 values and exact
repository paths. Preview is the default. Updating the existing PR branch
requires --push and a recorded clear final review. No new branch is created.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
QUEUE = 'unsolved_math_prioritization/QUEUE.md'


def git(*args, env=None, input=None):
    return subprocess.check_output(['git', *args], cwd=REPO, env=env,
                                   input=input, text=True).strip()


def row_info(text, pid):
    hits = []
    for line in text.splitlines(keepends=True):
        c = [x.strip() for x in line.split('|')]
        if len(c) >= 13 and c[2].split(' / ')[0] == str(pid):
            hits.append((line, c))
    if len(hits) != 1:
        raise RuntimeError('Expected exactly one target QUEUE row')
    return hits[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mapping')
    ap.add_argument('--push', action='store_true')
    a = ap.parse_args()
    mapping = json.loads(Path(a.mapping).read_text())
    pid, number = mapping['problem_id'], mapping['pr']
    if not 800 <= number <= 900:
        raise RuntimeError('PR outside assigned shard')
    if a.push and mapping['final_review_status'] != 'CLEAR':
        raise RuntimeError('Final review is not clear')
    snap = json.loads(subprocess.check_output([
        'gh', 'pr', 'view', str(number), '--repo', 'AlecKriebel/Math',
        '--json', 'headRefOid,headRefName,state,isDraft'], text=True))
    if snap['state'] != 'OPEN' or snap['headRefOid'] != mapping['expected_head']:
        raise RuntimeError('PR state or expected head changed')
    old = snap['headRefOid']
    head_queue = subprocess.check_output(['git', 'show', old + ':' + QUEUE],
                                         cwd=REPO).decode('utf-8')
    if row_info(head_queue, pid)[1][8] != 'claimed_solved':
        raise RuntimeError('Exact-head status is no longer claimed_solved')
    git('fetch', '--no-tags', 'origin', 'main')
    base = git('rev-parse', 'origin/main')
    current = subprocess.check_output(['git', 'show', base + ':' + QUEUE],
                                     cwd=REPO).decode('utf-8')
    oldrow, cells = row_info(current, pid)
    if cells[8] not in ('queued', 'claimed_solved') or cells[12]:
        raise RuntimeError('Current main target has conflicting disposition/DOI')
    cells[8] = 'claimed_solved'
    cells[9] = mapping['original_turns']
    cells[11] = mapping['findings']
    replacement = '| ' + ' | '.join(cells[1:-1]) + ' |'
    if oldrow.endswith('\r\n'):
        replacement += '\r\n'
    elif oldrow.endswith('\n'):
        replacement += '\n'
    updated = current.replace(oldrow, replacement, 1)
    if updated.replace(replacement, oldrow, 1) != current:
        raise RuntimeError('Queue bytes outside target row changed')
    prefix = 'unsolved_math_prioritization/attempts/' + str(pid) + '/'
    local_work = ROOT / 'local_tools'
    local_work.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(dir=local_work) as tmp:
        env = dict(os.environ, GIT_INDEX_FILE=str(Path(tmp) / 'index'))
        git('read-tree', base, env=env)
        seen = set()
        for f in mapping['files']:
            name = f['repo_path']
            if not name.startswith(prefix) or '..' in Path(name).parts or name in seen:
                raise RuntimeError('Unsafe/duplicate/out-of-scope mapped path')
            seen.add(name)
            local = Path(f['local_path'])
            raw = local.read_bytes()
            if local.is_symlink() or hashlib.sha256(raw).hexdigest() != f['sha256']:
                raise RuntimeError('Reviewed file changed: ' + name)
            blob = git('hash-object', '-w', str(local))
            git('update-index', '--add', '--cacheinfo', '100644', blob, name, env=env)
        blob = git('hash-object', '-w', '--stdin', input=updated)
        git('update-index', '--add', '--cacheinfo', '100644', blob, QUEUE, env=env)
        changed = git('diff', '--cached', '--name-only', base, env=env).splitlines()
        if any(n != QUEUE and not n.startswith(prefix) for n in changed):
            raise RuntimeError('Unexpected prepared diff scope')
        tree = git('write-tree', env=env)
        commit = git('commit-tree', tree, '-p', old, '-p', base,
                     input=mapping['commit_message'] + '\n')
    receipt = {'pr': number, 'problem_id': pid, 'old_head': old,
               'main_base': base, 'prepared_commit': commit,
               'changed_paths_vs_main': changed, 'queue_before': oldrow,
               'queue_after': replacement, 'pushed': False}
    out = Path(mapping['receipt_path'])
    out.write_text(json.dumps(receipt, indent=2) + '\n')
    if a.push:
        receipt['push_target'] = 'refs/heads/' + snap['headRefName']
        try:
            subprocess.run(['git', 'push', 'origin',
                            commit + ':' + receipt['push_target']],
                           cwd=REPO, check=True)
        except subprocess.CalledProcessError:
            receipt['push_outcome'] = 'failed_or_unknown; reconcile remote before retry'
            out.write_text(json.dumps(receipt, indent=2) + '\n')
            raise
        receipt['pushed'] = True
        receipt['head_readback_status'] = 'pending'
        receipt['head_readback_observations'] = []
        out.write_text(json.dumps(receipt, indent=2) + '\n')
        # PR metadata can lag a successful Git ref update. Only reads repeat.
        for attempt in range(4):
            actual = json.loads(subprocess.check_output([
                'gh', 'pr', 'view', str(number), '--repo', 'AlecKriebel/Math',
                '--json', 'headRefOid'], text=True))['headRefOid']
            receipt['head_readback_observations'].append(actual)
            if actual == commit:
                receipt['head_readback_status'] = 'confirmed'
                break
            out.write_text(json.dumps(receipt, indent=2) + '\n')
            if attempt < 3:
                time.sleep(3)
        if actual != commit:
            receipt['head_readback_status'] = 'mismatch; reconcile before further mutation'
            out.write_text(json.dumps(receipt, indent=2) + '\n')
            raise RuntimeError('PR head readback mismatch; successful push receipt retained')
    out.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt))


if __name__ == '__main__':
    main()
