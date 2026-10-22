#!/usr/bin/env python3
"""Authenticate the complete frozen PR932 packet before executing any of its code.

Bootstrap this file and PINNED_SNAPSHOT.json from an independent trusted digest.
This is a serial local integrity check, not protection from concurrent attackers.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat
import subprocess

HEAD = 'c09ef9df8b1f4642be0396ba6343344be8fa25b0'
PREFIX = 'unsolved_math_prioritization/attempts/30003471'
OUTER_PIN = 'd1b3a0528bf518640a117c2cfecff5bc81d21f58632f7b4f647ae998eb4dcedd'
PROOF_PIN = '6015fcacefd914217ddadc816a5c84c1be250ec58838df891f267835f9198415'
HEX = re.compile(r'[0-9a-f]{64}')


class Rejected(Exception):
    pass


def need(condition, message):
    if not condition:
        raise Rejected(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, 'duplicate JSON key')
            result[key] = value
        return result

    def bad(value):
        raise Rejected('nonfinite JSON constant: ' + value)

    def finite(value):
        if type(value) is float:
            need(math.isfinite(value), 'nonfinite JSON number')
        elif type(value) is dict:
            for entry in value.values():
                finite(entry)
        elif type(value) is list:
            for entry in value:
                finite(entry)

    try:
        value = json.loads(raw, object_pairs_hook=pairs, parse_constant=bad)
    except (ValueError, UnicodeError) as error:
        raise Rejected('malformed JSON') from error
    finite(value)
    return value


def typed_equal(left, right):
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return left.keys() == right.keys() and all(typed_equal(left[k], right[k]) for k in left)
    if type(left) is list:
        return len(left) == len(right) and all(typed_equal(x, y) for x, y in zip(left, right))
    return left == right


def canonical_root(raw):
    need(type(raw) is str and raw.startswith('/') and '\\' not in raw and '\x00' not in raw,
         'absolute canonical root required')
    parts = raw.split('/')
    need(all(part and part not in ('.', '..') for part in parts[1:]), 'noncanonical root')
    root = Path(raw)
    for parent in reversed([root, *root.parents]):
        mode = parent.lstat().st_mode
        need(stat.S_ISDIR(mode) and not stat.S_ISLNK(mode), 'non-directory or symlink ancestor: ' + str(parent))
    return root


def regular(path, limit=10_000_000):
    need(stat.S_ISREG(path.lstat().st_mode), 'nonregular file: ' + str(path))
    descriptor = os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0))
    try:
        need(stat.S_ISREG(os.fstat(descriptor).st_mode), 'nonregular opened file')
        with os.fdopen(descriptor, 'rb', closefd=False) as stream:
            raw = stream.read(limit + 1)
        need(len(raw) <= limit, 'oversized file')
        return raw
    finally:
        os.close(descriptor)


def snapshot_schema(snapshot):
    need(type(snapshot) is dict and set(snapshot) == {'schema', 'head', 'prefix', 'files', 'directories'}, 'snapshot schema')
    need(snapshot['schema'] == 'pr932-complete-git-snapshot-v1' and snapshot['head'] == HEAD and snapshot['prefix'] == PREFIX,
         'snapshot identity')
    records = snapshot['files']
    need(type(records) is dict and len(records) == 29, 'snapshot file count')
    for name, record in records.items():
        need(type(name) is str and all(re.fullmatch(r'[A-Za-z0-9_.-]+', p) and p not in ('.', '..') for p in name.split('/')),
             'unsafe snapshot member')
        need(type(record) is dict and set(record) == {'bytes', 'sha256', 'git_blob', 'git_mode'}, 'snapshot record')
        need(type(record['bytes']) is int and record['bytes'] >= 0, 'snapshot byte type')
        need(type(record['sha256']) is str and HEX.fullmatch(record['sha256']) is not None, 'snapshot hash')
        need(type(record['git_blob']) is str and re.fullmatch(r'[0-9a-f]{40}', record['git_blob']) is not None, 'snapshot Git blob')
        need(record['git_mode'] == '100644', 'snapshot Git mode')
    directories = sorted({str(parent) for name in records for parent in Path(name).parents if str(parent) != '.'})
    need(typed_equal(snapshot['directories'], directories), 'snapshot directories')
    need(records['PUBLICATION_MANIFEST.json']['sha256'] == OUTER_PIN and records['public/PROOF.md']['sha256'] == PROOF_PIN,
         'frozen anchor disagreement')
    return records


def load_snapshot(path, external_digest):
    need(type(external_digest) is str and HEX.fullmatch(external_digest) is not None, 'external snapshot digest required')
    raw = regular(path)
    need(sha(raw) == external_digest, 'snapshot anchor mismatch')
    snapshot = strict_json(raw)
    snapshot_schema(snapshot)
    return snapshot


def authenticate(raw_root, snapshot, profile='baseline'):
    records = snapshot_schema(snapshot)
    root = canonical_root(raw_root)
    expected_file, expected_dir = (0o644, 0o755) if profile == 'baseline' else (0o444, 0o555)
    need(profile in ('baseline', 'readonly'), 'unknown filesystem profile')
    need(stat.S_IMODE(root.lstat().st_mode) == expected_dir, 'packet root mode')
    files, directories = {}, []

    def descend(directory):
        for entry in sorted(os.scandir(directory), key=lambda item: item.name):
            path = Path(entry.path)
            relative = path.relative_to(root).as_posix()
            mode = entry.stat(follow_symlinks=False).st_mode
            if stat.S_ISDIR(mode):
                need(relative in snapshot['directories'], 'unexpected directory: ' + relative)
                need(stat.S_IMODE(mode) == expected_dir, 'directory mode: ' + relative)
                directories.append(relative)
                descend(path)
            else:
                need(stat.S_ISREG(mode), 'symlink or special entry: ' + relative)
                need(relative in records, 'unexpected file: ' + relative)
                need(stat.S_IMODE(mode) == expected_file, 'file mode: ' + relative)
                raw = regular(path, records[relative]['bytes'])
                need(len(raw) == records[relative]['bytes'] and sha(raw) == records[relative]['sha256'],
                     'byte identity: ' + relative)
                files[relative] = {'bytes': len(raw), 'sha256': sha(raw), 'mode': format(stat.S_IMODE(mode), '04o')}

    descend(root)
    need(files.keys() == records.keys() and sorted(directories) == snapshot['directories'], 'closed inventory differs')
    return {'files': files, 'directories': sorted(directories), 'root_mode': format(expected_dir, '04o')}


def authenticate_git(repository, snapshot):
    records = snapshot_schema(snapshot)
    command = ['git', '-C', str(repository)]
    tree = subprocess.run(command + ['ls-tree', '-r', '-z', HEAD, '--', PREFIX], check=True, capture_output=True, timeout=30).stdout
    found = {}
    for entry in tree.split(b'\0'):
        if not entry:
            continue
        header, raw_path = entry.split(b'\t', 1)
        mode, kind, oid = header.decode().split()
        path = raw_path.decode()
        need(path.startswith(PREFIX + '/') and kind == 'blob' and mode == '100644', 'unexpected Git member')
        relative = path[len(PREFIX) + 1:]
        raw = subprocess.run(command + ['cat-file', 'blob', oid], check=True, capture_output=True, timeout=30).stdout
        found[relative] = {'bytes': len(raw), 'sha256': sha(raw), 'git_blob': oid, 'git_mode': mode}
    need(typed_equal(found, records), 'actual Git objects differ from pinned snapshot')
    return {'head': HEAD, 'files': len(found), 'actual_git_blobs_authenticated': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet', required=True)
    parser.add_argument('--snapshot', type=Path, required=True)
    parser.add_argument('--snapshot-sha256', required=True)
    parser.add_argument('--profile', choices=['baseline', 'readonly'], default='baseline')
    parser.add_argument('--repository', type=Path)
    args = parser.parse_args()
    try:
        snapshot = load_snapshot(args.snapshot, args.snapshot_sha256)
        inventory = authenticate(args.packet, snapshot, args.profile)
        out = {'status': 'PASS', 'files': len(inventory['files']), 'directories': inventory['directories'],
               'head': HEAD, 'analytic_proof_certified': False}
        if args.repository is not None:
            out['git'] = authenticate_git(args.repository, snapshot)
        print(json.dumps(out, sort_keys=True))
    except (Rejected, OSError, ValueError, subprocess.SubprocessError) as error:
        print('GUARD_REJECT: ' + str(error))
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
