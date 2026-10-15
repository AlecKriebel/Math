#!/usr/bin/env python3
"""Publish owned files on remote main, preserving shared checkout and index."""
import argparse, datetime, hashlib, json, os, pathlib, subprocess
ROOT = pathlib.Path(__file__).resolve().parents[2]
PROJECT = pathlib.Path(__file__).resolve().parents[1]
def git(*args, env=None):
    p = subprocess.run(['git', *args], cwd=ROOT, env=env, capture_output=True, check=True)
    return p.stdout.decode().strip()
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('message')
    args = parser.parse_args()
    assert git('branch', '--show-current') == 'main'
    index = PROJECT / 'receipts/isolated.index'
    shared = pathlib.Path(git('rev-parse', '--git-path', 'index'))
    if not shared.is_absolute(): shared = ROOT / shared
    before = hashlib.sha256(shared.read_bytes()).hexdigest()
    git('fetch', 'origin', 'main')
    parent = git('rev-parse', 'origin/main')
    env = os.environ.copy()
    env['GIT_INDEX_FILE'] = str(index)
    if index.exists(): index.unlink()
    git('read-tree', parent, env=env)
    for rel in git('ls-files', '-z', PROJECT.name+'/', env=env).split('\0'):
        if rel and not (ROOT / rel).exists():
            git('update-index', '--force-remove', '--', rel, env=env)
    files = []
    for p in sorted(PROJECT.rglob('*')):
        if not p.is_file() or p.is_symlink(): continue
        rel = p.relative_to(ROOT).as_posix()
        ignore = subprocess.run(['git', 'check-ignore', '-q', '--no-index', rel], cwd=ROOT)
        if ignore.returncode == 0: continue
        blob = git('hash-object', '-w', '--', str(p))
        mode = '100755' if os.access(p, os.X_OK) else '100644'
        git('update-index', '--add', '--cacheinfo', mode, blob, rel, env=env)
        files.append(rel)
    tree = git('write-tree', env=env)
    changed = git('diff-tree', '--no-commit-id', '--name-only', '-r', parent, tree)
    assert all(p.startswith(PROJECT.name+'/') for p in changed.splitlines())
    commit = git('commit-tree', tree, '-p', parent, '-m', args.message)
    git('push', 'origin', commit + ':refs/heads/main')
    after = hashlib.sha256(shared.read_bytes()).hexdigest()
    receipt = {'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'parent':parent, 'commit':commit, 'owned_file_count':len(files),
               'changed_paths':changed.splitlines(), 'shared_index_before':before,
               'shared_index_after':after, 'shared_index_unchanged':after==before,
               'method':'isolated index on current remote main; shared HEAD unchanged'}
    name = PROJECT / ('receipts/checkpoint_' + commit[:12] + '.json')
    name.write_text(json.dumps(receipt, indent=2) + '\n')
    index.unlink()
    print(json.dumps(receipt, indent=2))
if __name__ == '__main__': main()
