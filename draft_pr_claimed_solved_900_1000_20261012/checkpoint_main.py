#!/usr/bin/env python3
"""Publish only explicitly named effort files to main, preserving shared checkout.

An alternate index derives from current remote main; commits are pushed without
force. Neither the shared index nor local HEAD is touched. A rejected push is
rebuilt on the newer remote parent. No branch is created or checked out.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
EFFORT = Path(__file__).resolve().parent

def run(args, **kwargs):
    return subprocess.run(args, cwd=ROOT, check=True, text=True,
                          capture_output=True, **kwargs).stdout.strip()

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
        with tempfile.TemporaryDirectory(prefix='math-pr900-main-') as td:
            env = dict(os.environ, GIT_INDEX_FILE=str(Path(td) / 'index'))
            run(['git', 'read-tree', parent], env=env)
            run(['git', 'add', '--', *args.paths], env=env)
            staged = run(['git', 'diff', '--cached', '--name-only', parent], env=env).splitlines()
            if set(staged) - set(args.paths):
                raise ValueError('Unexpected staged path')
            tree = run(['git', 'write-tree'], env=env)
            sha = run(['git', 'commit-tree', tree, '-p', parent], input=args.message+'\n')
        push = subprocess.run(['git', 'push', 'origin', sha+':refs/heads/main'],
                              cwd=ROOT, text=True, capture_output=True)
        if push.returncode == 0:
            record = {'utc': datetime.now(timezone.utc).isoformat(), 'parent': parent,
                      'commit': sha, 'tree': tree, 'attempt': attempt,
                      'paths': staged, 'push_confirmed': True,
                      'shared_index_and_local_head_untouched': True,
                      'push_output': push.stdout + push.stderr}
            receipt.write_text(json.dumps(record, indent=2)+'\n')
            print(json.dumps(record, indent=2))
            return
        if 'non-fast-forward' not in push.stderr and 'fetch first' not in push.stderr:
            raise RuntimeError(push.stderr)
    raise RuntimeError('main advanced on each attempt; checkpoint not pushed')

if __name__ == '__main__':
    main()
