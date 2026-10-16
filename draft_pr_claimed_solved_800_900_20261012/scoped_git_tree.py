"""Patch explicit Git tree entries without a checkout or full index.

Uses Git's tree parser/writer. Unchanged entries retain exact modes and OIDs;
only ancestors of the named regular-file entries are reconstructed.
"""
from pathlib import PurePosixPath
import subprocess


def patch_tree(repo, base, updates):
    def git(*args, input=None):
        return subprocess.check_output(['git', *args], cwd=repo, input=input)
    edits = {}
    for name, oid in updates.items():
        p = PurePosixPath(name)
        if (not isinstance(name, str) or name != str(p) or p.is_absolute()
                or not p.parts or any(x in ('', '.', '..') for x in p.parts)
                or '\x00' in name or '\\' in name):
            raise RuntimeError('Unsafe scoped tree path')
        if len(oid) != 40 or any(c not in '0123456789abcdef' for c in oid):
            raise RuntimeError('Invalid blob OID')
        if git('cat-file', '-t', oid).strip() != b'blob':
            raise RuntimeError('Entry must be a blob')
        node = edits
        for part in p.parts[:-1]:
            child = node.setdefault(part, {})
            if not isinstance(child, dict):
                raise RuntimeError('File/directory edit collision')
            node = child
        leaf = p.parts[-1]
        if leaf in node:
            raise RuntimeError('Duplicate or directory/file edit collision')
        node[leaf] = oid
    root_oid = git('rev-parse', base + '^{tree}').decode().strip()
    def walk(old, node):
        entries = {}
        if old:
            for row in git('ls-tree', '-z', old).split(b'\x00'):
                if not row:
                    continue
                header, name = row.split(b'\t', 1)
                mode, kind, oid = header.split(b' ')
                entries[name] = (mode, kind, oid)
        for name, change in node.items():
            key = name.encode('utf-8')
            existing = entries.get(key)
            if isinstance(change, dict):
                if existing and existing[1] != b'tree':
                    raise RuntimeError('Cannot traverse a non-tree entry')
                oid = walk(existing[2].decode() if existing else None, change)
                entries[key] = (b'040000', b'tree', oid.encode())
            else:
                if existing and existing[1] == b'tree':
                    raise RuntimeError('Cannot replace a directory with a file')
                entries[key] = (b'100644', b'blob', change.encode())
        payload = b''.join(mode + b' ' + kind + b' ' + oid + b'\t' + name + b'\x00'
                           for name, (mode, kind, oid) in entries.items())
        return git('mktree', '-z', input=payload).decode().strip()
    return walk(root_oid, edits)
