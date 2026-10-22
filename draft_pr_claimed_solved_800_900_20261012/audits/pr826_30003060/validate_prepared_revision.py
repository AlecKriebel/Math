#!/usr/bin/env python3
"""Read all prepared Git blobs independently of the tree-writing helper."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import subprocess

AUDIT = Path(__file__).resolve().parent
REPO = AUDIT.parents[2]
PREFIX = 'unsolved_math_prioritization/attempts/30003060/'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)


def row(raw):
    rows = []
    for line in raw.splitlines(keepends=True):
        cells = [c.strip() for c in line.decode().split('|')]
        if len(cells) >= 13 and cells[2].split(' / ')[0] == '30003060':
            rows.append((line, cells))
    need(len(rows) == 1, 'Queue target not unique')
    return rows[0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    args = parser.parse_args()
    label = args.label.upper()
    mapping = json.loads((AUDIT / ('PREPARED_PR_MAPPING_' + label + '.json')).read_text())
    receipt = json.loads((AUDIT / ('PREPARED_PR_REVISION_RECEIPT_' + label + '.json')).read_text())
    assembly = json.loads((AUDIT / ('LOCAL_PR_ASSEMBLY_' + label + '.json')).read_text())
    commit, base = receipt['prepared_commit'], receipt['main_base']
    entries = {}
    for raw in git('ls-tree', '-r', '-z', commit, '--', PREFIX).split(b'\0'):
        if not raw:
            continue
        head, name = raw.split(b'\t', 1)
        mode, kind, oid = head.split()
        key = name.decode()
        need(mode == b'100644' and kind == b'blob' and key not in entries, 'Unsafe Git entry')
        entries[key] = oid.decode()
    need(set(entries) == {f['repo_path'] for f in mapping['files']}, 'Prepared inventory differs')
    hashes = {}
    for entry in mapping['files']:
        raw = git('cat-file', 'blob', entries[entry['repo_path']])
        pin = hashlib.sha256(raw).hexdigest()
        need(pin == entry['sha256'] and raw == Path(entry['local_path']).read_bytes(), 'Actual Git bytes differ')
        hashes[entry['repo_path']] = pin
    before, after = git('show', base + ':' + QUEUE), git('show', commit + ':' + QUEUE)
    old_line, old_cells = row(before)
    new_line, cells = row(after)
    need(after.replace(new_line, old_line, 1) == before, 'Non-target queue bytes changed')
    need(cells[8:10] == ['claimed_solved', '1/5'] and cells[12] == '', 'Status, effort or DOI changed')
    need(all(cells[i] == old_cells[i] for i in range(len(cells)) if i not in {8, 9, 11}), 'Other target fields changed')
    paths = {p.decode() for p in git('diff-tree', '-r', '--no-commit-id', '--name-only', '-z', base, commit).split(b'\0') if p}
    need(paths <= {QUEUE} | set(entries), 'Unrelated Git tree path changed')
    parents = git('rev-list', '--parents', '-n', '1', commit).decode().split()[1:]
    need(len(parents) == 2 and set(parents) == {receipt['old_head'], base}, 'Prepared ancestry differs')
    pre = PREFIX + 'publication_20261014/preprint/'
    for core in assembly['core_files']:
        need(hashes[pre + core['path']] == core['sha256'], 'Preprint core differs')
    result = {'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'status': 'PASS', 'label': label, 'prepared_commit': commit, 'main_base': base,
              'frozen_old_head': receipt['old_head'], 'actual_target_blobs_read': len(hashes),
              'all_10_core_files_exact': True, 'all_non_target_queue_bytes_unchanged': True,
              'all_changed_paths_within_explicit_scope': True, 'parents_exact': parents,
              'outer_manifest_sha256': assembly['outer_manifest_sha256'],
              'git_blob_sha256': hashes, 'pushed_by_this_validator': False}
    (AUDIT / ('PREPARED_GIT_BYTES_VALIDATION_' + label + '.json')).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k != 'git_blob_sha256'}))


if __name__ == '__main__':
    main()
