#!/usr/bin/env python3
"""Authenticate selected immutable Git blobs against disk; default stdout only."""
import argparse
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[4]
PREFIX = 'unsolved_math_prioritization/attempts/30003634'
SNAP = HERE.parents[1] / 'original'
COMMIT = '2b3ea2de7a9a9ea4fa8cba9a34cbdb01063bda3b'
PROOF_SHA256 = '0492e0e0de785be263174e86d69855120b2f5c24b105c6479739cd72d64abe3b'
OUTER_SHA256 = '149e6144f0ad90ee12945c29155318100b65c6faee8ba2661d2c09db58b9ae30'

class VerificationError(RuntimeError):
    """A provenance check failed; active under all optimization settings."""

def require(condition, message):
    if not condition:
        raise VerificationError(str(message))

def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])

def sha(data):
    return hashlib.sha256(data).hexdigest()

def authenticate(expected_proof_sha256=PROOF_SHA256):
    rows = []
    for line in git('ls-tree', '-r', COMMIT, PREFIX).decode().splitlines():
        meta, name = line.split('\t')
        mode, kind, oid = meta.split()
        require(kind == 'blob', 'Selected Git tree contains a non-blob')
        require(mode in ('100644', '100755'), 'Unexpected selected Git file mode')
        raw = git('cat-file', 'blob', oid)
        disk = SNAP / name
        require(disk.is_file() and not disk.is_symlink(), 'Selected disk file missing or symlink: ' + name)
        body = disk.read_bytes()
        rows.append(dict(path=name, mode=mode, git_oid=oid, bytes=len(raw), sha256=sha(raw), disk_sha256=sha(body), equal=raw == body, symlink=disk.is_symlink(), disk_mode=oct(disk.stat().st_mode & 0o777)))
    require(len(rows) == 44, 'Selected Git inventory count is not 44')
    require(all(x['equal'] and not x['symlink'] for x in rows), 'Selected Git/disk bytes or file types differ')
    disk_paths = {str(f.relative_to(SNAP)) for f in (SNAP / PREFIX).rglob('*') if f.is_file() or f.is_symlink()}
    require(disk_paths == {x['path'] for x in rows}, 'Closed disk inventory differs from selected Git tree')
    require(all(x['disk_mode'] == ('0o755' if x['mode'] == '100755' else '0o644') for x in rows), 'Selected disk/Git modes differ')
    pinned = {'original/PROOF.md': expected_proof_sha256, 'PUBLICATION_MANIFEST.json': OUTER_SHA256}
    for name, digest in pinned.items():
        require(sha((SNAP / PREFIX / name).read_bytes()) == digest, 'Pinned authentication digest mismatch: ' + name)
    branch = git('branch', '--show-current').decode().strip()
    require(branch == 'main', 'Shared working branch is not main')
    return dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), selected_commit=COMMIT, workspace_head=git('rev-parse', 'HEAD').decode().strip(), branch=branch, prefix=PREFIX, count=len(rows), disk_file_count=len(disk_paths), closed_disk_inventory_equal=True, all_equal=True, pins=pinned, files=rows)

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=pathlib.Path, help='Explicit result destination; omitted means stdout only.')
    args = parser.parse_args(argv)
    payload = json.dumps(authenticate(), indent=2) + '\n'
    if args.output is not None:
        args.output.write_text(payload)
    sys.stdout.write(payload)

if __name__ == '__main__':
    try:
        main()
    except VerificationError as exc:
        print('Verification failed: ' + str(exc), file=sys.stderr)
        sys.exit(1)
