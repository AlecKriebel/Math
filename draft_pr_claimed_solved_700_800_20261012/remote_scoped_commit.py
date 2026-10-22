"""Memory-only, scoped ordinary fast-forward checkpoints during ENOSPC.

No local Git object, index, worktree, or ref is written. The expected complete
Git tree SHA is computed before the remote ref update, retaining every entry
outside the explicit updates. No deletion, force update, or branch creation.
"""
import base64
import datetime
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import time

REPO = Path(__file__).resolve().parent.parent
PROGRAM = Path(__file__).resolve().parent.name
ALLOWED = (PROGRAM, 'unsolved_math_prioritization')


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def oid(kind, raw):
    return hashlib.sha1(kind.encode() + b' ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def api(path, method='GET', body=None, check=True):
    args = ['gh', 'api', 'repos/AlecKriebel/Math/' + path, '--method', method]
    if body is not None:
        args += ['--input', '-']
    for attempt in range(3 if method == 'GET' else 1):
        result = subprocess.run(args, input=None if body is None else json.dumps(body),
                                text=True, capture_output=True, cwd=REPO)
        if result.returncode == 0:
            return json.loads(result.stdout)
        if method == 'GET' and attempt < 2:
            time.sleep(attempt + 1)
    if check:
        raise RuntimeError(result.stderr)
    return {'_error': result.stderr, '_exit': result.returncode}


def path_parts(path):
    parts = PurePosixPath(path).parts
    need(parts and parts[0] in ALLOWED and all(p not in ('', '.', '..', '/') for p in parts),
         'Path outside authorized scoped roots: ' + path)
    need('/'.join(parts) == path and '\\' not in path and '\0' not in path, 'Noncanonical path')
    return parts


def tree_oid(entries):
    ordered = sorted(entries.items(), key=lambda item: item[0].encode() +
                     (b'/' if item[1]['type'] == 'tree' else b''))
    raw = b''.join(row['mode'].lstrip('0').encode() + b' ' + name.encode() + b'\0' +
                   bytes.fromhex(row['sha']) for name, row in ordered)
    return oid('tree', raw)


class Remote:
    def __init__(self, parent):
        self.parent = parent
        self.root = api('git/commits/' + parent)['tree']['sha']
        self.cache = {}

    def entries(self, sha):
        if sha is None:
            return {}
        if sha not in self.cache:
            result = api('git/trees/' + sha)
            need(not result.get('truncated'), 'Truncated nonrecursive tree')
            rows = {r['path']: {k: r[k] for k in ('mode', 'type', 'sha')} for r in result['tree']}
            need(len(rows) == len(result['tree']), 'Duplicate tree names')
            need(tree_oid(rows) == sha, 'Downloaded tree Merkle hash mismatch')
            self.cache[sha] = rows
        return dict(self.cache[sha])

    def entry(self, path):
        parts = path_parts(path)
        sha = self.root
        for i, name in enumerate(parts):
            row = self.entries(sha).get(name)
            if row is None:
                return None
            if i == len(parts) - 1:
                return row
            need(row['type'] == 'tree', 'Non-tree path ancestor')
            sha = row['sha']

    def read(self, path):
        row = self.entry(path)
        need(row is not None and row['type'] == 'blob' and row['mode'] == '100644',
             'Expected regular native text file: ' + path)
        result = api('git/blobs/' + row['sha'])
        need(result['encoding'] == 'base64', 'Unsupported blob encoding')
        raw = base64.b64decode(result['content'])
        need(oid('blob', raw) == row['sha'], 'Downloaded blob hash mismatch')
        return raw.decode()

    def expected_tree(self, updates):
        trie = {}
        for path, row in updates.items():
            node = trie
            parts = path_parts(path)
            for name in parts[:-1]:
                node = node.setdefault(name, {})
            need(parts[-1] not in node, 'Conflicting updates')
            node[parts[-1]] = ('blob', row)

        def walk(sha, changes):
            rows = self.entries(sha)
            for name, change in changes.items():
                if isinstance(change, tuple):
                    need(name not in rows or rows[name]['type'] == 'blob', 'Overwrite non-blob')
                    rows[name] = change[1]
                else:
                    old = rows.get(name)
                    need(old is None or old['type'] == 'tree', 'Ancestor collision')
                    rows[name] = {'mode': '040000', 'type': 'tree',
                                  'sha': walk(None if old is None else old['sha'], change)}
            return tree_oid(rows)
        return walk(self.root, trie)


def commit_updates(remote, updates, message):
    """Return confirmed receipt, or None after a verified competing FF update."""
    need(subprocess.check_output(['git', 'branch', '--show-current'], cwd=REPO,
                                 text=True).strip() == 'main', 'Shared checkout must remain on main')
    rows = {}
    for path, value in updates.items():
        path_parts(path)
        raw = value.encode() if isinstance(value, str) else value
        row = {'mode': '100644', 'type': 'blob', 'sha': oid('blob', raw)}
        if remote.entry(path) == row:
            continue
        result = api('git/blobs', 'POST', {'content': base64.b64encode(raw).decode(), 'encoding': 'base64'})
        need(result['sha'] == row['sha'], 'Uploaded blob hash mismatch')
        rows[path] = row
    need(rows, 'No changed paths')
    expected = remote.expected_tree(rows)
    result = api('git/trees', 'POST', {'base_tree': remote.root,
                                    'tree': [dict(path=p, **r) for p, r in rows.items()]})
    need(result['sha'] == expected, 'Full resulting tree differs from computed exact Merkle tree')
    commit = api('git/commits', 'POST', {'message': message, 'tree': expected,
                                     'parents': [remote.parent]})['sha']
    result = api('git/refs/heads/main', 'PATCH', {'sha': commit, 'force': False}, check=False)
    confirmed = result.get('object', {}).get('sha') == commit
    if not confirmed:
        current = api('git/ref/heads/main')['object']['sha']
        confirmed = current == commit or api('compare/' + commit + '...' + current).get('status') in ('ahead', 'identical')
        if not confirmed:
            need(current != remote.parent, 'Ref update failed without competing main advancement: ' + result.get('_error', 'unknown'))
            return None
    receipt = {'status': 'pushed', 'commit': commit, 'parent': remote.parent,
               'pushed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'paths': list(rows), 'message': message,
               'backend': 'GitHub Git API; force:false ordinary fast-forward',
               'entire_resulting_tree_sha_computed_and_verified': True,
               'shared_checkout_index_objects_and_local_refs_untouched': True}
    print(json.dumps(receipt), flush=True)
    return receipt
