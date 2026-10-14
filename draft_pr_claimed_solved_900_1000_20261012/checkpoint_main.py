#!/usr/bin/env python3
"""Publish only explicitly named effort files to main, preserving shared checkout.

Only the ancestor trees of explicitly named files are rebuilt from remote
main; commits are pushed without force. No index or local HEAD is touched.
A rejected push is rebuilt on the newer remote parent. No branch is created
or checked out. Avoiding a complete alternate index keeps disk use small.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import stat
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
EFFORT = Path(__file__).resolve().parent

def run(args, **kwargs):
    return subprocess.run(args, cwd=ROOT, check=True, text=True,
                          capture_output=True, **kwargs).stdout.strip()

def replace_explicit_files(parent, paths):
    changes = {}
    for path in paths:
        cursor = changes
        parts = path.split('/')
        for part in parts[:-1]:
            cursor = cursor.setdefault(os.fsencode(part), {})
        blob = run(['git', 'hash-object', '-w', '--', path])
        mode = b'100755' if (ROOT / path).stat().st_mode & stat.S_IXUSR else b'100644'
        cursor[os.fsencode(parts[-1])] = (mode, b'blob', blob.encode('ascii'))

    def rebuild(old, updates):
        entries = {}
        if old is not None:
            data = subprocess.run(['git', 'ls-tree', '-z', old], cwd=ROOT,
                                  capture_output=True, check=True).stdout
            for entry in data.split(b'\0'):
                if entry:
                    header, name = entry.split(b'\t', 1)
                    entries[name] = tuple(header.split(b' '))
        for name, value in updates.items():
            if isinstance(value, dict):
                previous = entries.get(name)
                if previous is not None and previous[1] != b'tree':
                    raise ValueError('Non-tree ancestor in remote main')
                child = rebuild(previous[2].decode('ascii') if previous else None, value)
                entries[name] = (b'040000', b'tree', child.encode('ascii'))
            else:
                entries[name] = value
        payload = b''.join(b' '.join(header)+b'\t'+name+b'\0'
                           for name, header in entries.items())
        return subprocess.run(['git', 'mktree', '-z'], cwd=ROOT, input=payload,
                              capture_output=True, check=True).stdout.decode('ascii').strip()
    return rebuild(parent, changes)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--message', required=True)
    ap.add_argument('--receipt', required=True)
    ap.add_argument('paths', nargs='+')
    args = ap.parse_args()
    prefix = EFFORT.relative_to(ROOT).as_posix() + '/'
    for path in args.paths:
        p = ROOT / path
        if not path.startswith(prefix) or not p.is_file() or p.is_symlink():
            raise ValueError('Path outside own regular-file allowlist: ' + path)
    receipt = EFFORT / 'checkpoints' / args.receipt
    receipt.parent.mkdir(exist_ok=True)
    for attempt in range(1, 7):
        parent = run(['git', 'ls-remote', 'origin', 'refs/heads/main']).split()[0]
        run(['git', 'fetch', '--no-write-fetch-head', 'origin', parent])
        for path in args.paths:
            if '\n' in path or '\t' in path or any(part in ('', '.', '..') for part in path.split('/')):
                raise ValueError('Noncanonical checkpoint path')
        tree = replace_explicit_files(parent, args.paths)
        staged = run(['git', 'diff', '--name-only', parent, tree]).splitlines()
        if set(staged) - set(args.paths):
            raise ValueError('Unexpected changed path')
        sha = run(['git', 'commit-tree', tree, '-p', parent], input=args.message+'\n')
        push = subprocess.run(['git', 'push', 'origin', sha+':refs/heads/main'],
                              cwd=ROOT, text=True, capture_output=True)
        if push.returncode == 0:
            record = {'utc': datetime.now(timezone.utc).isoformat(), 'parent': parent,
                      'commit': sha, 'tree': tree, 'attempt': attempt,
                      'paths': staged, 'push_confirmed': True,
                      'shared_index_and_local_head_untouched': True,
                      'construction': 'explicit blobs and ancestor trees; no index allocated',
                      'push_output': push.stdout + push.stderr}
            receipt.write_text(json.dumps(record, indent=2)+'\n')
            print(json.dumps(record, indent=2))
            return
        if 'non-fast-forward' not in push.stderr and 'fetch first' not in push.stderr:
            raise RuntimeError(push.stderr)
    raise RuntimeError('main advanced on each attempt; checkpoint not pushed')

if __name__ == '__main__':
    main()
