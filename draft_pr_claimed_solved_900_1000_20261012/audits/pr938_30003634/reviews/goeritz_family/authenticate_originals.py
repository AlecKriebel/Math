#!/usr/bin/env python3
"""Read-only authentication against actual immutable Git objects.

Writes a review receipt only if --output is explicitly supplied.
"""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import subprocess


def require(ok, reason):
    if not ok:
        raise RuntimeError(reason)


def main(output=None):
    folder = Path(__file__).resolve().parent
    repo = Path(subprocess.check_output(['git', 'rev-parse', '--show-toplevel'],
                                       cwd=folder, text=True).strip())
    disk = folder.parents[1] / 'original'
    head = '2b3ea2de7a9a9ea4fa8cba9a34cbdb01063bda3b'
    prefix = 'unsolved_math_prioritization/attempts/30003634'

    def git(*args):
        return subprocess.check_output(['git', *args], cwd=repo)

    paths = git('ls-tree', '-r', '--name-only', head, '--', prefix).decode().splitlines()
    require(len(paths) == 44, 'Original path count mismatch')
    rows = []
    for path in paths:
        blob = git('show', head + ':' + path)
        raw = (disk / path).read_bytes()
        require(raw == blob, 'Original disk/Git mismatch: ' + path)
        rows.append({'path': path, 'bytes': len(blob),
                     'sha256': hashlib.sha256(blob).hexdigest(), 'disk_equal': True})
    pins = {r['path']: r['sha256'] for r in rows}
    require(pins[prefix + '/original/PROOF.md'] ==
            '0492e0e0de785be263174e86d69855120b2f5c24b105c6479739cd72d64abe3b',
            'Proof pin mismatch')
    require(pins[prefix + '/PUBLICATION_MANIFEST.json'] ==
            '149e6144f0ad90ee12945c29155318100b65c6faee8ba2661d2c09db58b9ae30',
            'Outer manifest pin mismatch')
    branch = git('branch', '--show-current').decode().strip()
    require(branch == 'main', 'Shared branch is no longer main')
    out = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'git_commit': head, 'branch': branch, 'count': len(rows),
           'all_equal': True, 'files': rows}
    body = json.dumps(out, indent=2) + '\n'
    if output:
        Path(output).write_text(body)
        print(json.dumps({'count': len(rows), 'all_equal': True, 'branch': branch}))
    else:
        print(body, end='')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', help='Explicit receipt output file')
    main(parser.parse_args().output)
