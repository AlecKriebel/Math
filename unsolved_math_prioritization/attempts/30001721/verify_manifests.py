#!/usr/bin/env python3
"""Strict, portable manifest verification and isolated negative controls."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import re
import tempfile


def verify(directory):
    directory = Path(directory)
    if directory.is_symlink():
        raise ValueError('symlink root')
    entries = {}
    for line in (directory/'SHA256SUMS').read_text().splitlines(keepends=True):
        m = re.fullmatch(r'([0-9a-f]{64})  ([^\n]+)\n', line)
        if m is None:
            raise ValueError('malformed manifest line')
        digest, name = m.groups()
        p = PurePosixPath(name)
        if (p.is_absolute() or name != p.as_posix() or '\\' in name or
            '..' in p.parts or '.' in p.parts or name == 'SHA256SUMS'):
            raise ValueError('unsafe or self-referential path')
        if name in entries:
            raise ValueError('duplicate entry')
        entries[name] = digest
    actual = {}
    for path in sorted(directory.rglob('*')):
        if path.is_symlink():
            raise ValueError('symlink in packet')
        if path.is_file() and path != directory/'SHA256SUMS':
            actual[path.relative_to(directory).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != entries:
        raise ValueError('inventory or digest mismatch')
    return len(entries)


def negative_controls():
    outcomes = {}
    changes = {
        'extra_file': lambda p: (p/'extra').write_text('extra'),
        'missing_file': lambda p: (p/'a.txt').unlink(),
        'altered_bytes': lambda p: (p/'a.txt').write_text('changed'),
        'duplicate_entry': lambda p: (p/'SHA256SUMS').write_text((p/'SHA256SUMS').read_text()*2),
        'absolute_path': lambda p: (p/'SHA256SUMS').write_text('0'*64+'  /absolute\n'),
        'parent_traversal': lambda p: (p/'SHA256SUMS').write_text('0'*64+'  ../escape\n'),
        'noncanonical_path': lambda p: (p/'SHA256SUMS').write_text('0'*64+'  ./a.txt\n'),
        'symlink': lambda p: (p/'link').symlink_to('a.txt'),
        'malformed_hash': lambda p: (p/'SHA256SUMS').write_text('not-a-hash  a.txt\n'),
    }
    for name, mutation in changes.items():
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            (p/'a.txt').write_text('control\n')
            (p/'SHA256SUMS').write_text(hashlib.sha256((p/'a.txt').read_bytes()).hexdigest()+'  a.txt\n')
            assert verify(p) == 1
            mutation(p)
            try:
                verify(p)
            except (ValueError, OSError):
                outcomes[name] = 'rejected'
            else:
                raise AssertionError('negative control accepted: '+name)
    return outcomes


def main():
    root = Path(__file__).resolve().parent
    targets = ['.', 'release-v2', 'release-v2/author', 'release-v2/original-author',
               'release-v2/original-audit', 'supplemental-audit-v2']
    result = {'manifest_entries': {n: verify(root/n) for n in targets},
              'negative_controls': negative_controls()}
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
