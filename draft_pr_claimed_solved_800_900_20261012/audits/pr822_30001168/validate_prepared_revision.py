#!/usr/bin/env python3
"""Independent readback of exact prepared Git bytes and non-target queue scope."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]


def need(ok, reason):
    if not ok:
        raise RuntimeError(reason)


def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', default='R1')
    args = parser.parse_args()
    if not args.label.isalnum():
        raise RuntimeError('unsafe label')
    receipt = json.loads((HERE / ('PREPARED_PR_REVISION_RECEIPT_' + args.label + '.json')).read_bytes())
    mapping = json.loads((HERE / ('PREPARED_PR_MAPPING_' + args.label + '.json')).read_bytes())
    commit, base = receipt['prepared_commit'], receipt['main_base']
    prefix = 'unsolved_math_prioritization/attempts/30001168/'
    raw = git('ls-tree', '-r', '-z', commit, '--', prefix)
    entries = {}
    for item in raw.split(b'\0'):
        if not item:
            continue
        meta, name = item.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        need(mode == '100644' and kind == 'blob', 'regular mapped Git entry')
        entries[name.decode()] = oid
    rows = mapping['files']
    need(set(entries) == {row['repo_path'] for row in rows}, 'exact mapped Git inventory')
    for row in rows:
        local = Path(row['local_path']).read_bytes()
        blob = git('cat-file', 'blob', entries[row['repo_path']])
        need(blob == local and hashlib.sha256(blob).hexdigest() == row['sha256'],
             'exact blob readback: ' + row['repo_path'])
    queue = 'unsolved_math_prioritization/QUEUE.md'
    before, after = git('show', base + ':' + queue), git('show', commit + ':' + queue)
    oldrow, newrow = receipt['queue_before'].encode(), receipt['queue_after'].encode()
    need(before.count(oldrow) == 1 and after.count(newrow) == 1, 'unique target queue rows')
    need(before.replace(oldrow, newrow, 1) == after, 'only target queue bytes changed')
    need(newrow.decode().split('|')[8].strip() == 'claimed_solved', 'exact resulting queue status')
    changed = git('diff-tree', '-r', '--no-commit-id', '--name-only', '-z', base, commit)
    names = [x.decode() for x in changed.split(b'\0') if x]
    need(all(n == queue or n.startswith(prefix) for n in names), 'only authorized target paths changed')
    parents = git('show', '-s', '--format=%P', commit).decode().strip().split()
    need(parents == [mapping['expected_head'], base], 'original-head/current-main parents')
    out = {'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'status': 'PASS', 'prepared_commit': commit, 'main_base': base,
           'mapped_files_byte_exact': len(rows), 'non_target_queue_bytes_unchanged': True,
           'foreign_tree_unchanged_vs_main': True, 'changed_paths': len(names),
           'read_only_validation': True}
    (HERE / ('PREPARED_GIT_BYTES_VALIDATION_' + args.label + '.json')).write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps(out))


if __name__ == '__main__':
    main()
