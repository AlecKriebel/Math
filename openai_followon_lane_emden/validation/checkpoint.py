#!/usr/bin/env python3
"""Publish only explicitly named project files on current remote main.

Uses a private index and commit-tree; never alters the shared index, checkout,
HEAD, or a local branch. Push is a normal fast-forward compare-and-swap; a
concurrent remote update causes failure and a fresh run is then required.
"""
from pathlib import Path
import argparse, datetime, json, os, subprocess, tempfile

ROOT = Path(__file__).resolve().parents[2]
PROJECT = Path(__file__).resolve().parents[1]

def run(*args, env=None):
    return subprocess.check_output(args, cwd=ROOT, env=env, text=True).strip()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--message', required=True)
    parser.add_argument('--receipt', required=True)
    parser.add_argument('paths', nargs='+')
    args = parser.parse_args()
    for name in args.paths:
        path = (ROOT / name).resolve()
        if not path.is_relative_to(PROJECT) or not path.exists():
            raise SystemExit('Refusing a missing or non-project path: ' + name)
    if run('git', 'branch', '--show-current') != 'main':
        raise SystemExit('Shared checkout must stay on main')
    branch_before = run('git', 'rev-parse', 'HEAD')
    index_path = Path(run('git', 'rev-parse', '--git-path', 'index'))
    if not index_path.is_absolute():
        index_path = ROOT / index_path
    import hashlib
    index_before = hashlib.sha256(index_path.read_bytes()).hexdigest()
    run('git', 'fetch', '--no-write-fetch-head', 'origin', 'refs/heads/main')
    remote = run('git', 'ls-remote', 'origin', 'refs/heads/main').split()[0]
    fd, private_index = tempfile.mkstemp(prefix='checkpoint-index-', dir=PROJECT/'receipts')
    os.close(fd)
    os.unlink(private_index)
    env = os.environ.copy()
    env['GIT_INDEX_FILE'] = private_index
    try:
        run('git', 'read-tree', remote, env=env)
        run('git', 'add', '--', *args.paths, env=env)
        tree = run('git', 'write-tree', env=env)
        changed = run('git', 'diff-tree', '--no-commit-id', '--name-only', '-r', remote, tree)
        if not changed:
            raise SystemExit('No project changes to publish')
        if any(not p.startswith(PROJECT.name + '/') for p in changed.splitlines()):
            raise SystemExit('Private tree contains unexpected changes')
        commit = run('git', 'commit-tree', tree, '-p', remote, '-m', args.message)
        run('git', 'push', 'origin', commit + ':refs/heads/main')
        public_tip = run('git', 'ls-remote', 'origin', 'refs/heads/main').split()[0]
        receipt = {'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   'parent':remote, 'commit':commit, 'remote_tip_after':public_tip,
                   'files':changed.splitlines(), 'shared_head_before':branch_before,
                   'shared_head_after':run('git','rev-parse','HEAD'),
                   'shared_index_before_sha256':index_before,
                   'shared_index_after_sha256':hashlib.sha256(index_path.read_bytes()).hexdigest(),
                   'method':'private index; commit-tree on remote main; normal push; no checkout mutation'}
        receipt_path = (ROOT / args.receipt).resolve()
        if not receipt_path.is_relative_to(PROJECT):
            raise SystemExit('Receipt must stay in project')
        receipt_path.write_text(json.dumps(receipt,indent=2)+'\n')
        print(json.dumps(receipt,indent=2))
    finally:
        Path(private_index).unlink(missing_ok=True)

if __name__ == '__main__':
    main()
