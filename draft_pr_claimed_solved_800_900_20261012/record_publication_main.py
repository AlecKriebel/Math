#!/usr/bin/env python3
"""Preview/push reviewed publication receipts and one queue row after a merge.

All files are explicit, hash checked, and restricted to this shard's effort or
the selected problem's attempt folder. The shared checkout/index stays intact.
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
QUEUE = 'unsolved_math_prioritization/QUEUE.md'
from importlib.util import spec_from_file_location, module_from_spec
_tree_spec = spec_from_file_location('scoped_git_tree', ROOT / 'scoped_git_tree.py')
_tree_module = module_from_spec(_tree_spec)
_tree_spec.loader.exec_module(_tree_module)
patch_tree = _tree_module.patch_tree


def git(*args, env=None, input=None):
    return subprocess.check_output(['git', *args], cwd=REPO, env=env,
                                   input=input, text=True).strip()


def row(text, pid):
    matches = []
    for line in text.splitlines(keepends=True):
        cells = [c.strip() for c in line.split('|')]
        if len(cells) >= 13 and cells[2].split(' / ')[0] == str(pid):
            matches.append((line, cells))
    if len(matches) != 1:
        raise RuntimeError('Expected exactly one target queue row')
    return matches[0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mapping')
    parser.add_argument('--push', action='store_true')
    args = parser.parse_args()
    mapping = json.loads(Path(args.mapping).read_text())
    pid, pr = mapping['problem_id'], mapping['pr']
    if type(pid) is not int or type(pr) is not int or pid <= 0:
        raise RuntimeError('PR and problem ID must be positive integer keys')
    if not 800 <= pr <= 900 or mapping['final_review_status'] != 'CLEAR':
        raise RuntimeError('Out of scope or missing final acceptance')
    publication = mapping['published_record']
    if publication['environment'] != 'production' or publication['state'] != 'published':
        raise RuntimeError('No confirmed production publication')
    doi = publication['doi_url']
    if not doi.startswith('https://doi.org/10.5281/zenodo.'):
        raise RuntimeError('Unexpected/missing Zenodo DOI')
    merged = json.loads(subprocess.check_output([
        'gh', 'pr', 'view', str(pr), '--repo', 'AlecKriebel/Math',
        '--json', 'state,mergeCommit'], text=True))
    if merged['state'] != 'MERGED':
        raise RuntimeError('PR is not merged')
    # Keep PR872's verified legacy root; other targets retain the default scope.
    # This literal exception never permits arbitrary caller-selected prefixes.
    prefix = ('random_property_t_30006628/' if (pr, pid) == (872, 30006628)
              else 'unsolved_math_prioritization/attempts/' + str(pid) + '/')
    seen = set()
    for entry in mapping['files']:
        name, local = entry['repo_path'], Path(entry['local_path'])
        if (not (name.startswith(prefix) or name.startswith(ROOT.name + '/'))
                or '..' in Path(name).parts or name in seen or local.is_symlink()):
            raise RuntimeError('Unsafe/duplicate/out-of-scope path')
        seen.add(name)
        if hashlib.sha256(local.read_bytes()).hexdigest() != entry['sha256']:
            raise RuntimeError('Mapped file changed: ' + name)
    history = []
    work = ROOT / 'local_tools'
    work.mkdir(exist_ok=True)
    for attempt in range(5):
        git('fetch', '--no-tags', 'origin', 'main')
        base = git('rev-parse', 'origin/main')
        if subprocess.run(['git', 'merge-base', '--is-ancestor',
                           merged['mergeCommit']['oid'], base], cwd=REPO).returncode:
            raise RuntimeError('Merged PR is not in current main')
        for entry in mapping['protected_files']:
            if not entry['repo_path'].startswith(prefix):
                raise RuntimeError('Protected file outside target attempt')
            raw = subprocess.check_output(['git', 'show', base + ':' + entry['repo_path']], cwd=REPO)
            if hashlib.sha256(raw).hexdigest() != entry['sha256']:
                raise RuntimeError('Accepted core changed on main')
            if entry['repo_path'] in seen:
                raise RuntimeError('Publication receipts may not modify accepted core')
        current = subprocess.check_output(['git', 'show', base + ':' + QUEUE], cwd=REPO).decode('utf-8')
        before, cells = row(current, pid)
        if cells[8] != 'claimed_solved' or cells[12] not in ('', doi):
            raise RuntimeError('Target status/DOI conflicts with accepted outcome')
        cells[11], cells[12] = mapping['findings'], doi
        ending = '\r\n' if before.endswith('\r\n') else '\n' if before.endswith('\n') else ''
        after = '| ' + ' | '.join(cells[1:-1]) + ' |' + ending
        updated = current.replace(before, after, 1)
        if updated.replace(after, before, 1) != current:
            raise RuntimeError('Queue changed outside target row')
        entries = mapping['files']
        blobs = git('hash-object', '-w', '--no-filters', '--',
                    *(entry['local_path'] for entry in entries)).splitlines() if entries else []
        if len(blobs) != len(entries):
            raise RuntimeError('Batch blob inventory mismatch')
        updates = {entry['repo_path']: blob for blob, entry in zip(blobs, entries)}
        updates[QUEUE] = git('hash-object', '-w', '--stdin', input=updated)
        tree = patch_tree(REPO, base, updates)
        changed = git('diff-tree', '-r', '--no-commit-id', '--name-only', base, tree).splitlines()
        if any(p != QUEUE and p not in seen for p in changed):
            raise RuntimeError('Unexpected diff path')
        commit = git('commit-tree', tree, '-p', base,
                     input=mapping['commit_message'] + '\n') if changed else base
        receipt = {'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   'pr': pr, 'problem_id': pid, 'main_base': base, 'commit': commit,
                   'doi_url': doi, 'changed_paths': changed, 'pushed': False,
                   'shared_checkout_index_branch_unchanged': True}
        if not args.push or not changed:
            Path(mapping['receipt_path']).write_text(json.dumps(receipt, indent=2) + '\n')
            print(json.dumps(receipt))
            return
        receipt.update(push_outcome='pending', attempts=history)
        Path(mapping['receipt_path']).write_text(json.dumps(receipt, indent=2) + '\n')
        pushed = subprocess.run(['git', 'push', 'origin', commit + ':refs/heads/main'],
                                cwd=REPO, capture_output=True, text=True)
        history.append({'base': base, 'commit': commit, 'push_exit': pushed.returncode})
        if pushed.returncode == 0:
            receipt.update(pushed=True, push_outcome='confirmed', attempts=history)
            Path(mapping['receipt_path']).write_text(json.dumps(receipt, indent=2) + '\n')
            print(json.dumps(receipt))
            return
        concurrent_ref_rejection=("cannot lock ref 'refs/heads/main'" in pushed.stderr
                                  and 'is at ' in pushed.stderr and 'but expected ' in pushed.stderr)
        receipt.update(push_outcome='failed_or_unknown; reconcile before any non-rejection retry', attempts=history)
        Path(mapping['receipt_path']).write_text(json.dumps(receipt, indent=2) + '\n')
        if not concurrent_ref_rejection and not any(s in pushed.stderr for s in ('non-fast-forward', 'fetch first', 'failed to update ref')):
            raise RuntimeError(pushed.stderr)
    raise RuntimeError('Five main advances prevented publication-receipt push; commits retained')


if __name__ == '__main__':
    main()
