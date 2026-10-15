#!/usr/bin/env python3
"""Publish explicitly listed owned files without touching the shared index/HEAD."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

PROJECT = Path(__file__).resolve().parents[1]
REPO = PROJECT.parent


def command(args, env=None):
    return subprocess.check_output(
        ['git', '-c', 'gc.auto=0', *args], cwd=REPO,
        env=env, text=True, stderr=subprocess.PIPE).strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--message', required=True)
    parser.add_argument('--receipt', required=True)
    parser.add_argument('files', nargs='+', help='Paths relative to this project')
    args = parser.parse_args()
    if command(['symbolic-ref', '--short', 'HEAD']) != 'main':
        raise RuntimeError('Expected shared main; no ref changes will be attempted')
    files = []
    hashes = {}
    for relative in args.files:
        path = (PROJECT / relative).resolve(strict=True)
        path.relative_to(PROJECT)
        if not path.is_file():
            raise ValueError('Only explicit regular files may be checkpointed')
        name = str(path.relative_to(REPO))
        files.append(name)
        hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    before_head = command(['rev-parse', 'HEAD'])
    real_index = REPO / '.git' / 'index'
    before_index = hashlib.sha256(real_index.read_bytes()).hexdigest()
    attempts = []
    with tempfile.TemporaryDirectory(prefix='checkpoint-', dir=PROJECT/'receipts') as tmp:
        env = os.environ.copy()
        env['GIT_INDEX_FILE'] = str(Path(tmp)/'index')
        for _ in range(8):
            command(['fetch', 'origin', 'main', '--quiet'])
            base = command(['rev-parse', 'origin/main'])
            command(['read-tree', base], env)
            command(['add', '--', *files], env)
            tree = command(['write-tree'], env)
            commit = command(['commit-tree', tree, '-p', base, '-m', args.message], env)
            changed = command(['diff-tree', '--no-commit-id', '--name-only', '-r', commit])
            if not set(changed.splitlines()).issubset(files):
                raise RuntimeError('Unexpected path in candidate commit')
            # A collaborator may edit a listed file after the initial hash.
            # Check bytes in the commit, rather than trusting working files.
            committed_hashes = {}
            for name in files:
                blob = subprocess.check_output(
                    ['git', '-c', 'gc.auto=0', 'show', commit+':'+name], cwd=REPO)
                committed_hashes[name] = hashlib.sha256(blob).hexdigest()
            if committed_hashes != hashes:
                raise RuntimeError('Owned file changed during checkpoint; no push attempted')
            result = subprocess.run(
                ['git', '-c', 'gc.auto=0', 'push', 'origin', commit+':refs/heads/main'],
                cwd=REPO, capture_output=True, text=True)
            attempts.append({'base':base, 'commit':commit, 'exit_code':result.returncode,
                             'response':result.stderr.strip()})
            if result.returncode == 0:
                break
            if 'fetch first' not in result.stderr and 'non-fast-forward' not in result.stderr:
                raise RuntimeError('Push failed; no unsafe retry: '+result.stderr)
        else:
            raise RuntimeError('Concurrent updates prevented a fast-forward push')
    receipt = {
        'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'commit':commit, 'owned_files':files, 'file_sha256':hashes,
        'committed_blob_sha256':committed_hashes,
        'method':'isolated index, fast-forward hash push to refs/heads/main',
        'shared_head_before':before_head, 'shared_head_after':command(['rev-parse','HEAD']),
        'shared_index_before':before_index,
        'shared_index_after':hashlib.sha256(real_index.read_bytes()).hexdigest(),
        'attempts':attempts,
    }
    target = PROJECT/'receipts'/args.receipt
    target.write_text(json.dumps(receipt, indent=2)+'\n')
    print(json.dumps({'pushed':True,'commit':commit,'receipt':str(target)}))


if __name__ == '__main__':
    main()
