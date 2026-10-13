"""Publish only this program's artifacts without touching the shared index.

Each commit descends from the freshly read remote main. A non-fast-forward push
is retried with a fresh parent; no force push or shared checkout reset occurs.
"""
import datetime
import json
import os
import pathlib
import subprocess
import sys
import tempfile

PROGRAM = pathlib.Path(__file__).resolve().parent
REPO = PROGRAM.parent
RELATIVE = PROGRAM.relative_to(REPO).as_posix()

def run(*args, env=None, data=None):
    return subprocess.check_output(args, cwd=REPO, env=env, input=data, text=True).strip()

def remote_tip():
    # Read-only API lookup also works when Git's HTTP ref advertisement stalls.
    return run('gh', 'api', 'repos/AlecKriebel/Math/git/ref/heads/main', '--jq', '.object.sha')

def main():
    message = sys.argv[1] if len(sys.argv) > 1 else 'Checkpoint actual-claim review for draft PRs #1000–#1100'
    if run('git', 'branch', '--show-current') != 'main':
        raise SystemExit('The shared checkout must remain on main.')
    before = run('git', 'rev-parse', 'HEAD')
    for attempt in range(6):
        parent = remote_tip()
        present = subprocess.run(['git', 'cat-file', '-e', f'{parent}^{{commit}}'], cwd=REPO, capture_output=True)
        if present.returncode:
            subprocess.run(['git', 'fetch', '--quiet', '--no-write-fetch-head', 'origin', parent], cwd=REPO, check=True)
        with tempfile.TemporaryDirectory(prefix='math-pr1000-index-') as tmp:
            env = {**os.environ, 'GIT_INDEX_FILE': str(pathlib.Path(tmp) / 'index')}
            run('git', 'read-tree', parent, env=env)
            run('git', 'add', '--', RELATIVE, env=env)
            tree = run('git', 'write-tree', env=env)
            if tree == run('git', 'rev-parse', f'{parent}^{{tree}}'):
                print(json.dumps({'no_changes': True, 'remote_main': parent}))
                return
            commit = run('git', 'commit-tree', tree, '-p', parent, data=message + '\n')
        changed = run('git', 'diff-tree', '--no-commit-id', '--name-only', '-r', parent, commit).splitlines()
        if not changed or any(not p.startswith(RELATIVE + '/') for p in changed):
            raise SystemExit('Checkpoint would include a path outside this program.')
        result = subprocess.run(['git', 'push', '--porcelain', 'origin', f'{commit}:refs/heads/main'], cwd=REPO, text=True, capture_output=True)
        if result.returncode:
            current = remote_tip()
            if current != parent:
                continue
            raise SystemExit(result.stderr)
        receipt = {'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   'commit': commit, 'parent': parent, 'tree': tree, 'paths': changed,
                   'url': f'https://github.com/AlecKriebel/Math/commit/{commit}',
                   'shared_local_head_before': before,
                   'shared_local_head_after': run('git', 'rev-parse', 'HEAD'),
                   'shared_index_modified': False, 'force_push': False}
        (PROGRAM / 'LATEST_PUSH_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
        print(json.dumps(receipt, indent=2))
        return
    raise SystemExit('Remote main changed during every checkpoint attempt; retry later.')

if __name__ == '__main__':
    main()
