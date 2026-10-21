#!/usr/bin/env python3
"""Publish only explicitly selected audit files on main, without touching shared index/HEAD.

Creates a commit atop the freshly fetched remote main using a private temporary
index. Push is a normal fast-forward push. If main advances concurrently, rebuild
the same selected-file overlay atop the new main, at most three attempts.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

REPO = Path(__file__).resolve().parent.parent
ROOT = Path(__file__).resolve().parent


def run(args, *, env=None, data=None):
    return subprocess.run(args, cwd=REPO, env=env, input=data, text=True,
                          capture_output=True, check=True).stdout.strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--message', required=True)
    parser.add_argument('--force-authored', action='append', default=[], metavar='PATH',
                        help='Explicit reviewed authored evidence otherwise ignored by Git; must also be selected below')
    parser.add_argument('paths', nargs='+')
    args = parser.parse_args()
    paths = []
    for name in args.paths:
        p = (REPO / name).resolve()
        if not p.is_relative_to(ROOT) or not p.exists():
            raise ValueError(f'Only existing files in this effort may be selected: {name}')
        paths.append(str(p.relative_to(REPO)))
    forced = []
    for name in args.force_authored:
        p = (REPO / name).resolve()
        rel = str(p.relative_to(REPO))
        if not p.is_relative_to(ROOT) or not p.is_file() or rel not in paths:
            raise ValueError('Forced authored evidence must be an explicitly selected effort file: ' + name)
        forced.append(rel)
    if run(['git', 'branch', '--show-current']) != 'main':
        raise RuntimeError('Shared checkout is not on main; no action taken')
    scratch = ROOT / 'tmp'
    scratch.mkdir(exist_ok=True)
    for attempt in range(1, 4):
        run(['git', 'fetch', 'origin', 'main'])
        parent = run(['git', 'rev-parse', 'refs/remotes/origin/main'])
        with tempfile.TemporaryDirectory(dir=scratch) as d:
            env = dict(os.environ, GIT_INDEX_FILE=str(Path(d) / 'index'))
            run(['git', 'read-tree', parent], env=env)
            ordinary = [name for name in paths if name not in forced]
            if ordinary:
                run(['git', 'add', '--', *ordinary], env=env)
            if forced:
                run(['git', 'add', '-f', '--', *forced], env=env)
            tree = run(['git', 'write-tree'], env=env)
            if tree == run(['git', 'rev-parse', f'{parent}^{{tree}}']):
                print(json.dumps({'status': 'already_present', 'commit': parent}))
                return
            commit = run(['git', 'commit-tree', tree, '-p', parent],
                         data=args.message + '\n')
        result = subprocess.run(['git', 'push', 'origin', f'{commit}:refs/heads/main'],
                                cwd=REPO, text=True, capture_output=True)
        if result.returncode == 0:
            print(json.dumps({'status': 'pushed', 'commit': commit, 'parent': parent,
                              'attempt': attempt, 'paths': paths}))
            return
        if 'non-fast-forward' not in result.stderr and 'fetch first' not in result.stderr:
            raise RuntimeError(result.stderr)
    raise RuntimeError('Main advanced during three push attempts; local findings preserved')


if __name__ == '__main__':
    main()
