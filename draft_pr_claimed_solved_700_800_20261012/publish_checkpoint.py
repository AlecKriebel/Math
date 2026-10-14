"""Push only this shard's selected files onto remote main, preserving shared checkout.

The local checkout has independent unpublished commits and unrelated dirty files.
Scoped tree construction avoids allocating or changing the shared Git index.
No branches are created or switched. Each push is a normal fast-forward on main.
"""
import datetime
import json
import pathlib
import re
import subprocess
import sys
from scoped_tree import replace_paths, selected_working_updates

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parent


def git(*args, env=None, input=None):
    result = subprocess.run(['git', *args], cwd=REPO, env=env, input=input,
                            capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr)
    return result.stdout.strip()


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
    for attempt in range(3):
        # Resolve main without writing any shared fetch/reference state.
        parent = subprocess.run(
            ['gh', 'api', 'repos/AlecKriebel/Math/git/ref/heads/main',
             '--jq', '.object.sha'], cwd=REPO, capture_output=True,
            text=True, check=True).stdout.strip()
        present = subprocess.run(['git', 'cat-file', '-e', parent + '^{commit}'],
                                 cwd=REPO, capture_output=True)
        if present.returncode:
            git('fetch', '--no-write-fetch-head', 'origin', parent)
        updates = selected_working_updates(REPO, parent, relative)
        tree = replace_paths(REPO, parent, updates)
        changed = git('diff', '--name-only', parent, tree).splitlines()
        if not changed:
            print(json.dumps({'status': 'no_changes', 'remote_main': parent}))
            return
        for name in changed:
            (REPO / name).resolve().relative_to(ROOT)
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
        ref_race = re.search(
            r"cannot lock ref 'refs/heads/main': is at [0-9a-f]{40} but expected [0-9a-f]{40}",
            result.stderr)
        if ('fetch first' not in result.stderr and 'non-fast-forward' not in result.stderr
                and not ref_race):
            raise RuntimeError(result.stderr)
    raise RuntimeError('Remote main advanced during all three checkpoint attempts')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise SystemExit('Usage: publish_checkpoint.py MESSAGE PATH [PATH ...]')
    publish(sys.argv[1], sys.argv[2:])
