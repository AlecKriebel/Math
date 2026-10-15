"""Build a scoped Git tree without allocating a repository-wide index.

Untouched subtrees retain their exact object IDs. This never changes a ref,
checkout or shared index, and uses ordinary Git objects and commit-tree.
"""
from pathlib import Path
import subprocess


def git_bytes(repo, *args, raw=None):
    result = subprocess.run(['git', *args], cwd=repo, input=raw,
                            capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr.decode('utf-8', errors='replace'))
    return result.stdout


def replace_paths(repo, parent, updates):
    """updates maps relative paths to (mode, object ID), or None for removal."""
    trie = {}
    for path, value in updates.items():
        parts = path.split('/')
        if not parts or any(part in ('', '.', '..') for part in parts):
            raise ValueError('Invalid scoped path')
        node = trie
        for part in parts[:-1]:
            node = node.setdefault(part.encode('utf-8'), {})
            if not isinstance(node, dict):
                raise ValueError('Overlapping scoped paths')
        key = parts[-1].encode('utf-8')
        if key in node:
            raise ValueError('Repeated or overlapping scoped paths')
        node[key] = value

    def build(old_tree, changes):
        entries = {}
        if old_tree:
            for record in git_bytes(repo, 'ls-tree', '-z', old_tree).split(b'\0'):
                if not record:
                    continue
                metadata, name = record.split(b'\t', 1)
                mode, kind, oid = metadata.split(b' ')
                entries[name] = (mode, kind, oid)
        for name, value in changes.items():
            if isinstance(value, dict):
                old = entries.get(name)
                if old and old[1] != b'tree':
                    raise ValueError('Scoped ancestor is not a directory')
                oid = build(old[2].decode('ascii') if old else None, value)
                if oid is None:
                    entries.pop(name, None)
                else:
                    entries[name] = (b'040000', b'tree', oid.encode('ascii'))
            elif value is None:
                if name not in entries:
                    raise ValueError('Cannot remove a missing scoped path')
                del entries[name]
            else:
                mode, oid = value
                kind = b'commit' if mode == '160000' else b'blob'
                entries[name] = (mode.encode('ascii'), kind, oid.encode('ascii'))
        if not entries:
            return None
        records = b''.join(mode + b' ' + kind + b' ' + oid + b'\t' + name + b'\0'
                           for name, (mode, kind, oid) in entries.items())
        return git_bytes(repo, 'mktree', '-z', raw=records).decode('ascii').strip()

    parent_tree = git_bytes(repo, 'rev-parse', parent + '^{tree}').decode('ascii').strip()
    result = build(parent_tree, trie)
    return result if result is not None else git_bytes(repo, 'mktree', raw=b'').decode('ascii').strip()


def selected_working_updates(repo, parent, paths):
    """Match selected tracked/untracked files while honoring ignored scratch."""
    remote = {}
    for record in git_bytes(repo, 'ls-tree', '-r', '-z', parent, '--', *paths).split(b'\0'):
        if not record:
            continue
        metadata, name = record.split(b'\t', 1)
        mode, kind, oid = metadata.split(b' ')
        if kind not in (b'blob', b'commit'):
            raise ValueError('Unexpected remote selected object')
        remote[name.decode('utf-8')] = (mode.decode('ascii'), oid.decode('ascii'))
    local_names = git_bytes(repo, 'ls-files', '--cached', '--others',
                            '--exclude-standard', '-z', '--', *paths).split(b'\0')
    names = set(remote) | {name.decode('utf-8') for name in local_names if name}
    updates = {}
    for name in names:
        path = Path(repo) / name
        if path.is_symlink():
            raw = str(path.readlink()).encode('utf-8')
            mode = '120000'
        elif path.is_file():
            raw = path.read_bytes()
            mode = '100755' if path.stat().st_mode & 0o111 else '100644'
        elif not path.exists() and name in remote:
            updates[name] = None
            continue
        else:
            raise ValueError('Unsupported scoped working path: ' + name)
        oid = git_bytes(repo, 'hash-object', '-w', '--stdin', raw=raw).decode('ascii').strip()
        value = (mode, oid)
        if remote.get(name) != value:
            updates[name] = value
    return updates
