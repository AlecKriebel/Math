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
import stat

PROGRAM = pathlib.Path(__file__).resolve().parent
REPO = PROGRAM.parent
RELATIVE = PROGRAM.relative_to(REPO).as_posix()

def run(*args, env=None, data=None):
    return subprocess.check_output(args, cwd=REPO, env=env, input=data, text=True).strip()

def remote_tip():
    # Read-only API lookup also works when Git's HTTP ref advertisement stalls.
    return run('gh', 'api', 'repos/AlecKriebel/Math/git/ref/heads/main', '--jq', '.object.sha')

def byte_run(*args, data=None):
    return subprocess.check_output(args, cwd=REPO, input=data)

def program_tree():
    """Build just our subtree, without allocating the repository-wide index.

    Respect Git's actual ignore rules even for previously tracked private
    files. Every byte written belongs to this program; no shared index or
    checkout file is opened for mutation.
    """
    paths = []
    for base, dirs, files in os.walk(PROGRAM, followlinks=False):
        # os.walk puts symlink directories in dirs even with followlinks=False.
        for name in list(dirs):
            p = pathlib.Path(base) / name
            if p.is_symlink():
                paths.append(p)
                dirs.remove(name)
        paths.extend(pathlib.Path(base) / name for name in files)
    rels = [p.relative_to(REPO).as_posix() for p in paths]
    request = b'\0'.join(os.fsencode(n) for n in rels) + b'\0'
    ignored = subprocess.run(['git', 'check-ignore', '--no-index', '-z', '--stdin'],
                             cwd=REPO, input=request, capture_output=True)
    if ignored.returncode not in (0, 1):
        raise RuntimeError(ignored.stderr.decode(errors='replace'))
    ignored_paths = set(ignored.stdout.rstrip(b'\0').split(b'\0')) if ignored.stdout else set()
    nodes = {}
    for p, rel in zip(paths, rels):
        if os.fsencode(rel) in ignored_paths:
            continue
        mode = p.lstat().st_mode
        if stat.S_ISLNK(mode):
            git_mode, payload = '120000', os.fsencode(os.readlink(p))
        elif stat.S_ISREG(mode):
            git_mode = '100755' if mode & 0o111 else '100644'
            payload = p.read_bytes()
        else:
            raise RuntimeError('Unsupported checkpoint file: ' + str(p))
        oid = byte_run('git', 'hash-object', '-w', '--stdin', data=payload).decode().strip()
        parts = p.relative_to(PROGRAM).parts
        node = nodes
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = (git_mode, 'blob', oid)
    def write(node):
        entries = []
        for name, value in node.items():
            if isinstance(value, dict):
                mode, kind, oid = '040000', 'tree', write(value)
            else:
                mode, kind, oid = value
            entries.append(f'{mode} {kind} {oid}\t'.encode() + os.fsencode(name) + b'\0')
        return byte_run('git', 'mktree', '-z', data=b''.join(entries)).decode().strip()
    return write(nodes)

def graft_program(parent, subtree):
    if '/' in RELATIVE:
        raise RuntimeError('This graft requires the dedicated top-level program folder.')
    entries = byte_run('git', 'ls-tree', '-z', parent).rstrip(b'\0').split(b'\0')
    preserved = [e for e in entries if e.split(b'\t', 1)[1] != os.fsencode(RELATIVE)]
    preserved.append(f'040000 tree {subtree}\t{RELATIVE}'.encode())
    return byte_run('git', 'mktree', '-z', data=b'\0'.join(preserved) + b'\0').decode().strip()

def main():
    message = sys.argv[1] if len(sys.argv) > 1 else 'Checkpoint actual-claim review for draft PRs #1000–#1100'
    if run('git', 'branch', '--show-current') != 'main':
        raise SystemExit('The shared checkout must remain on main.')
    before = run('git', 'rev-parse', 'HEAD')
    index_before = pathlib.Path(run('git', 'rev-parse', '--git-path', 'index')).read_bytes()
    # Capture our artifacts once. A racing remote push changes only the parent
    # graft, not the content of this local checkpoint.
    subtree = program_tree()
    for attempt in range(6):
        parent = remote_tip()
        present = subprocess.run(['git', 'cat-file', '-e', f'{parent}^{{commit}}'], cwd=REPO, capture_output=True)
        if present.returncode:
            subprocess.run(['git', 'fetch', '--quiet', '--no-write-fetch-head', 'origin', parent], cwd=REPO, check=True)
        tree = graft_program(parent, subtree)
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
                   'shared_index_modified': False,
                   'shared_index_bytes_unchanged': index_before == pathlib.Path(run('git', 'rev-parse', '--git-path', 'index')).read_bytes(),
                   'checkpoint_method': 'index-free isolated subtree graft',
                   'force_push': False}
        (PROGRAM / 'LATEST_PUSH_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
        print(json.dumps({**{k: v for k, v in receipt.items() if k != 'paths'},
                          'path_count': len(changed)}, indent=2))
        return
    raise SystemExit('Remote main changed during every checkpoint attempt; retry later.')

if __name__ == '__main__':
    main()
