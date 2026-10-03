"""Separate ROOT readonly verifier. Never imports the closer or any other review source."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import stat

F = Path(__file__).absolute().parent
R = F.parents[3]
NAME = 'SELF_MANIFEST.json'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def decode(b):
    def pairs(items):
        out = {}
        for k, v in items:
            require(k not in out, 'Duplicate key')
            out[k] = v
        return out
    def floating(text):
        v = float(text)
        require(math.isfinite(v), 'Nonfinite')
        return v
    return json.loads(b, object_pairs_hook=pairs, parse_float=floating,
                      parse_constant=lambda s: (_ for _ in ()).throw(ValueError(s)))


def path(base, n):
    require(type(n) is str and n and '\\' not in n and '\x00' not in n, 'Literal name')
    p = PurePosixPath(n)
    require(p.as_posix() == n and not p.is_absolute() and n != '.'
            and not {'.', '..', '.git', '__pycache__'}.intersection(p.parts), 'Canonical name')
    q = base / n
    require(not q.is_symlink() and stat.S_ISREG(q.stat().st_mode)
            and all(not a.is_symlink() for a in q.parents), 'Regular literal member')
    return q


def check(base, row, mode):
    require(type(row) is dict and type(row['bytes']) is int and row['bytes'] >= 0
            and type(row['sha256']) is str and re.fullmatch('[0-9a-f]{64}', row['sha256'])
            and type(mode) is int and 0 <= mode <= 0o7777, 'Typed size/digest/fullmode')
    q = path(base, row['path'])
    b = q.read_bytes()
    require(len(b) == row['bytes'] and sha(b) == row['sha256']
            and stat.S_IMODE(q.stat().st_mode) == mode, 'Complete bytes and fullmode')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--expected-manifest-sha256', required=True)
    a = p.parse_args()
    b = path(F, NAME).read_bytes()
    require(sha(b) == a.expected_manifest_sha256, 'ROOT supplied actual closure SHA')
    m = decode(b)
    require(set(m) == {'schema', 'status', 'utc', 'actual_closing_pid', 'self_excluded', 'files_count', 'files',
                       'directories', 'production_imported_compiled_executed', 'future_acceptance_approved',
                       'ROOT_approval_authored', 'mandatory_corrections'}, 'Exact adverse closure schema')
    require(m['schema'] == 'pr48-v2-fresh-source-adversary-closure/v1'
            and m['status'] == 'CLOSED_ADVERSE_SOURCE_REVIEW' and m['self_excluded'] == [NAME]
            and type(m['actual_closing_pid']) is int and m['actual_closing_pid'] > 0
            and m['production_imported_compiled_executed'] is False
            and m['future_acceptance_approved'] is False and m['ROOT_approval_authored'] is False
            and m['mandatory_corrections'] == ['M2'], 'SOURCE adverse meaning only')
    require(type(m['files']) is list and type(m['files_count']) is int
            and len(m['files']) == m['files_count'], 'Typed complete payload count')
    names = set()
    for row in m['files']:
        require(set(row) == {'path', 'bytes', 'sha256'} and row['path'] not in names
                and row['path'] != NAME, 'Literal unique payload')
        check(F, row, 0o444)
        names.add(row['path'])
    names.add(NAME)
    files, dirs = set(), set()
    for q in F.rglob('*'):
        require(not q.is_symlink() and (q.is_file() or q.is_dir()), 'No special/symlink topology')
        (files if q.is_file() else dirs).add(q.relative_to(F).as_posix())
    expected_dirs = {d.as_posix() for n in names for d in PurePosixPath(n).parents if d.as_posix() != '.'}
    require(files == names and dirs == expected_dirs and m['directories'] == sorted(dirs)
            and stat.S_IMODE((F / NAME).stat().st_mode) == 0o444, 'Exact recursive self-only closure')
    refs = decode(path(F, 'INPUT_BINDINGS.json').read_bytes())
    require(refs['schema'] == 'pr48-v2-fresh-source-adversary-fixed-inputs/v1'
            and type(refs['unique_count']) is int and refs['unique_count'] == len(refs['rows']) == 4371
            and refs['dated_native4_pinned_live'] is False and refs['actual_PR47_post_certified'] is False
            and refs['future_acceptance_approved'] is False, 'Exact fixed external context')
    seen = []
    for row in refs['rows']:
        require(type(row) is dict and set(row) == {'path', 'bytes', 'sha256', 'full_mode'}, 'Four-key external row')
        check(R, row, row['full_mode'])
        seen.append(row['path'])
    require(seen == sorted(set(seen)) and set().union(*(set(v) for v in refs['groups'].values())) == set(seen),
            'Unique full external scope and memberships')
    v = decode(path(F, 'VERDICT.json').read_bytes())
    require(v['schema'] == 'pr48-acceptance-source-adversary-verdict/v1'
            and v['verdict'] == 'NEEDS_SOURCE_CORRECTION_SCOPED'
            and v['report_sha256'] == sha(path(F, 'REPORT.md').read_bytes())
            and [z['id'] for z in v['mandatory_corrections']] == ['M2']
            and v['preparation_manifest_sha256'] == '48ddcccb22eb898c42598278fa4914d84fa0da640e098973a1e70d7c60577662', 'Entire adverse report binding')
    print(json.dumps({'status': 'PASS_CLOSED_ADVERSE_SOURCE_REVIEW_READBACK',
                      'actual_readback_pid': os.getpid(), 'payload_files': len(m['files']),
                      'directories': len(dirs), 'external_fixed_inputs': len(seen),
                      'manifest_sha256': sha(b), 'mandatory_corrections': ['M2'],
                      'production_imported_compiled_executed': False, 'future_acceptance_approved': False}, sort_keys=True))


if __name__ == '__main__':
    main()
