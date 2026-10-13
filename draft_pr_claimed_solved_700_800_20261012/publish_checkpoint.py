"""Push only this shard's selected files onto remote main, preserving shared checkout.

The local checkout has independent unpublished commits and unrelated dirty files.
An isolated temporary index avoids staging, resetting, or rebasing others' work.
No branches are created or switched. Each push is a normal fast-forward on main.
"""
import datetime
import json
import os
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parent


def git(*args, env=None, input=None):
    return subprocess.run(['git', *args], cwd=REPO, env=env, input=input,
                          capture_output=True, text=True, check=True).stdout.strip()


def publish(message, paths):
    if git('branch', '--show-current') != 'main':
        raise RuntimeError('Expected shared checkout to remain on main')
    relative = []
    for path in paths:
        resolved = (REPO / path).resolve()
        resolved.relative_to(ROOT)
        if not resolved.exists():
            raise ValueError(f'Missing checkpoint path: {path}')
        relative.append(str(resolved.relative_to(REPO)))
    with tempfile.TemporaryDirectory(prefix='math-pr700-checkpoint-') as temp:
        env = os.environ.copy()
        env['GIT_INDEX_FILE'] = str(pathlib.Path(temp) / 'index')
        for attempt in range(3):
            git('fetch', 'origin', 'main')
            parent = git('rev-parse', 'origin/main')
            git('read-tree', parent, env=env)
            git('add', '--', *relative, env=env)
            changed = git('diff', '--cached', '--name-only', parent, env=env).splitlines()
            if not changed:
                print(json.dumps({'status': 'no_changes', 'remote_main': parent}))
                return
            for name in changed:
                (REPO / name).resolve().relative_to(ROOT)
            tree = git('write-tree', env=env)
            commit = git('commit-tree', tree, '-p', parent, input=message + '\n')
            result = subprocess.run(['git', 'push', 'origin', commit + ':refs/heads/main'],
                                    cwd=REPO, capture_output=True, text=True)
            if result.returncode == 0:
                receipt = {'status': 'pushed', 'pushed_at': datetime.datetime.now(
                    datetime.timezone.utc).isoformat(), 'commit': commit, 'parent': parent,
                    'changed_files': changed, 'message': message,
                    'shared_checkout_and_index_untouched': True}
                receipts = ROOT / 'checkpoint_receipts.jsonl'
                with receipts.open('a') as stream:
                    stream.write(json.dumps(receipt) + '\n')
                print(json.dumps(receipt, indent=2))
                return
            if 'fetch first' not in result.stderr and 'non-fast-forward' not in result.stderr:
                raise RuntimeError(result.stderr)
        raise RuntimeError('Remote main advanced during all three checkpoint attempts')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise SystemExit('Usage: publish_checkpoint.py MESSAGE PATH [PATH ...]')
    publish(sys.argv[1], sys.argv[2:])
