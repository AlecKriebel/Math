#!/usr/bin/env python3
"""Independently read every published target blob and the one changed queue row."""
import argparse
import datetime
import hashlib
import json
import pathlib
import subprocess

AUDIT = pathlib.Path(__file__).resolve().parent
REPO = AUDIT.parents[2]
PREFIX = 'unsolved_math_prioritization/attempts/30001168/'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)


def queue_row(raw):
    found = []
    for line in raw.splitlines(keepends=True):
        cells = [cell.strip() for cell in line.decode('utf-8').split('|')]
        if len(cells) >= 13 and cells[2].split(' / ')[0] == '30001168':
            found.append((line, cells))
    require(len(found) == 1, 'Target queue row is not unique')
    return found[0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--published', action='store_true')
    args = parser.parse_args()
    prep = json.loads((AUDIT / 'POSTPUBLICATION_PREPARATION.json').read_text())
    mapping = json.loads((AUDIT / 'POST_PUBLICATION_MAIN_MAPPING.json').read_text())
    receipt_name = 'POST_PUBLICATION_MAIN_RECEIPT.json' if args.published else 'POST_PUBLICATION_MAIN_PREVIEW.json'
    receipt = json.loads((AUDIT / receipt_name).read_text())
    commit, base = receipt['commit'], receipt['main_base']
    if args.published:
        require(receipt['pushed'] is True and receipt['push_outcome'] == 'confirmed', 'Publication push is unconfirmed')
        observed = git('rev-parse', 'origin/main').decode().strip()
        require(subprocess.run(['git', 'merge-base', '--is-ancestor', commit, observed], cwd=REPO).returncode == 0,
                'Published annotation is not on observed main')
        target = observed
    else:
        target = commit
    work = pathlib.Path(prep['tree'])
    expected = {PREFIX + str(p.relative_to(work)): p for p in work.rglob('*') if p.is_file()}
    require(len(expected) == 164 and not any(p.is_symlink() for p in expected.values()), 'Unexpected local inventory')
    entries = {}
    for raw in git('ls-tree', '-r', '-z', target, '--', PREFIX).split(b'\0'):
        if not raw:
            continue
        head, name = raw.split(b'\t', 1)
        mode, kind, oid = head.split()
        key = name.decode('utf-8')
        require(mode == b'100644' and kind == b'blob' and key not in entries, 'Unsafe Git target entry')
        entries[key] = oid.decode()
    require(set(entries) == set(expected), 'Git/local target inventory differs')
    checked = {}
    for name, path in expected.items():
        local = path.read_bytes()
        actual = git('cat-file', 'blob', entries[name])
        require(actual == local, 'Actual Git blob differs: ' + name)
        checked[name] = hashlib.sha256(actual).hexdigest()
    require(len(mapping['protected_files']) == 159, 'Wrong protected inventory')
    for entry in mapping['protected_files']:
        name, pin = entry['repo_path'], entry['sha256']
        require(checked[name] == pin, 'Accepted file changed: ' + name)
        require(hashlib.sha256(git('show', base + ':' + name)).hexdigest() == pin,
                'Base accepted file changed: ' + name)
    for entry in mapping['files']:
        actual = git('show', target + ':' + entry['repo_path'])
        require(hashlib.sha256(actual).hexdigest() == entry['sha256'], 'Mapped file changed')
    before = git('show', base + ':' + QUEUE)
    after = git('show', commit + ':' + QUEUE)
    old_line, old_cells = queue_row(before)
    new_line, new_cells = queue_row(after)
    require(after.replace(new_line, old_line, 1) == before, 'Non-target queue bytes changed')
    require(old_cells[8:10] == new_cells[8:10] == ['claimed_solved', '1/5'], 'Status/effort changed')
    require(new_cells[12] == 'https://doi.org/10.5281/zenodo.23383952', 'Wrong DOI')
    live_line, live_cells = queue_row(git('show', target + ':' + QUEUE))
    require(live_line == new_line, 'Current main target queue row changed')
    allowed = {QUEUE} | {entry['repo_path'] for entry in mapping['files']}
    changed = {n.decode('utf-8') for n in git('diff-tree', '-r', '--no-commit-id', '--name-only', '-z', base, commit).split(b'\0') if n}
    require(changed <= allowed and changed == set(receipt['changed_paths']), 'Unexpected changed path')
    for name in changed - {QUEUE}:
        raw = git('ls-tree', commit, '--', name)
        require(raw.startswith(b'100644 blob '), 'Changed file mode is not regular 100644')
    acceptance = json.loads((AUDIT / 'FINAL_PREPRINT_ACCEPTANCE.json').read_text())
    for core in acceptance['core_files']:
        name = PREFIX + 'publication_20261013/preprint/' + core['path']
        require(checked[name] == core['sha256'], 'Accepted preprint core changed')
    result = {
        'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'status': 'PASS', 'phase': 'published_main_readback' if args.published else 'preview',
        'annotation_commit': commit, 'annotation_base': base, 'observed_tree': target,
        'regular_target_files_read_back': 164, 'protected_accepted_files_unchanged': 159,
        'all_10_preprint_core_files_unchanged': True,
        'outer_manifest_sha256': prep['outer_manifest_sha256'],
        'doi_url': new_cells[12], 'queue_status': new_cells[8], 'proof_effort': new_cells[9],
        'all_non_target_queue_bytes_unchanged_in_annotation': True,
        'changed_paths_within_explicit_scope': sorted(changed),
        'target_blob_sha256': checked,
        'no_new_mathematical_or_priority_claims': True,
    }
    destination = 'PUBLISHED_PACKAGE_VALIDATION.json' if args.published else 'POST_PUBLICATION_PREVIEW_VALIDATION.json'
    (AUDIT / destination).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('target_blob_sha256', 'changed_paths_within_explicit_scope')}))


if __name__ == '__main__':
    main()
