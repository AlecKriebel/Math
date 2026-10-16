"""Ordinary scoped Git publication using a GraphQL-read immutable parent.

Writes ordinary Git objects only, never the shared index, checkout, or local
refs. Complete resulting tree is independently verified before normal FF push.
"""
import datetime
import json
import re
import subprocess

from remote_scoped_commit import REPO, need, oid, path_parts
from scoped_tree import git_bytes, replace_paths


def commit_updates(remote, updates, message):
    need(git_bytes(REPO, 'branch', '--show-current').decode().strip() == 'main', 'Must stay on main')
    present = subprocess.run(['git', 'cat-file', '-e', remote.parent + '^{commit}'], cwd=REPO, capture_output=True)
    if present.returncode:
        git_bytes(REPO, 'fetch', '--no-write-fetch-head', 'origin', remote.parent)
    rows, selected = {}, {}
    for path, value in updates.items():
        path_parts(path)
        raw = value.encode() if isinstance(value, str) else value
        expected = oid('blob', raw)
        row = {'mode': '100644', 'type': 'blob', 'sha': expected}
        existing = remote.entry(path)
        need(existing is None or (existing['type'] == 'blob' and existing['mode'] == '100644'), 'Cannot replace nonregular file')
        if existing == row:
            continue
        actual = git_bytes(REPO, 'hash-object', '-w', '--stdin', raw=raw).decode().strip()
        need(actual == expected, 'Blob hash mismatch')
        rows[path], selected[path] = row, ('100644', actual)
    need(bool(rows), 'No changed paths')
    expected_tree = remote.expected_tree(rows)
    tree = replace_paths(REPO, remote.parent, selected)
    need(tree == expected_tree, 'Complete resulting tree mismatch before push')
    commit = git_bytes(REPO, 'commit-tree', tree, '-p', remote.parent,
                       raw=(message + '\n').encode()).decode().strip()
    result = subprocess.run(['git', 'push', 'origin', commit + ':refs/heads/main'],
                            cwd=REPO, capture_output=True, text=True)
    if result.returncode:
        current = git_bytes(REPO, 'ls-remote', 'origin', 'refs/heads/main').decode().split()[0]
        confirmed = current == commit
        if not confirmed:
            present = subprocess.run(['git', 'cat-file', '-e', current + '^{commit}'], cwd=REPO, capture_output=True)
            if present.returncode:
                git_bytes(REPO, 'fetch', '--no-write-fetch-head', 'origin', current)
            confirmed = subprocess.run(['git', 'merge-base', '--is-ancestor', commit, current], cwd=REPO, capture_output=True).returncode == 0
        if not confirmed:
            race = re.search(r"cannot lock ref 'refs/heads/main': is at [0-9a-f]{40} but expected [0-9a-f]{40}", result.stderr)
            if 'fetch first' in result.stderr or 'non-fast-forward' in result.stderr or race:
                return None
            raise RuntimeError('Push unconfirmed; inspect before repeat: ' + result.stderr)
    receipt = {'status': 'pushed', 'commit': commit, 'parent': remote.parent,
               'pushed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'paths': list(rows), 'message': message,
               'backend': 'ordinary Git objects and normal fast-forward push; immutable parent read using GraphQL',
               'entire_resulting_tree_sha_computed_and_verified_before_push': True,
               'shared_checkout_index_and_local_refs_untouched': True}
    print(json.dumps(receipt), flush=True)
    return receipt
