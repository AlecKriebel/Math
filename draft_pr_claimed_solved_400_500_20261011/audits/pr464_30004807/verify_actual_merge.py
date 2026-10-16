#!/usr/bin/env python3
"""Read-only independent final merge/ancestry/content verification; no service writes."""
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'operations'))
import common as c


def main():
    context = c.validate_gate()
    installed = c.read_json(ROOT, 'BRANCH_INTEGRATION_RECEIPT.json')
    c.require(installed.get('state') == 'branch_updated_verified', 'Verified install receipt absent')
    pr = c.github('pulls/464')
    c.require(pr.get('merged') is True and pr.get('state') == 'closed' and pr.get('draft') is False
              and pr['head']['sha'] == installed['commit_sha'] and pr['head']['ref'] == c.BRANCH
              and pr['head']['repo']['full_name'] == c.REPO and pr['base']['ref'] == 'main'
              and pr['base']['repo']['full_name'] == c.REPO, 'Actual merged PR identity differs')
    merge = pr['merge_commit_sha']; reader = c.GitReader(); commit = reader.commit(merge)
    c.require(len(commit['parents']) == 2 and commit['parents'][1]['sha'] == installed['commit_sha'],
              'Merge commit does not have exact accepted branch parent')
    previous_main = commit['parents'][0]['sha']
    comparison = c.github('compare/' + previous_main + '...' + merge)
    changes = comparison.get('files')
    c.require(type(changes) is list and len(changes) < 300
              and len({x['filename'] for x in changes}) == len(changes)
              and {x['filename'] for x in changes} == set(installed['expected_changed_paths'])
              and all(x['status'] in {'added', 'modified'} and 'previous_filename' not in x for x in changes),
              'Actual merge changed unexpected files')
    verified = []
    for path, spec in installed['files'].items():
        entry = reader.entry(path, merge)
        c.require(entry is not None and entry['type'] == 'blob' and entry['mode'] == '100644', 'Merged leaf type differs')
        if path != c.QUEUE:
            c.require(entry['sha'] == spec['git_blob_sha'], 'Merged immutable blob differs: ' + path)
        verified.append({'path': path, 'actual_git_blob_sha': entry['sha'],
                         'accepted_git_blob_sha': spec['git_blob_sha'],
                         'matches_accepted_blob': entry['sha'] == spec['git_blob_sha']})
    queue = reader.read(c.QUEUE, merge)
    _, row, cells, columns = c.queue_row(queue)
    c.require(cells[columns.index('Status')].strip() == 'claimed_solved'
              and cells[columns.index('Turns')].strip() == '1/5'
              and cells[columns.index('DOI')].strip() == installed['doi_url'], 'Actual merged selected QUEUE row differs')
    before = reader.read(c.QUEUE, previous_main).decode().splitlines(keepends=True)
    after = queue.decode().splitlines(keepends=True)
    c.require(len(before) == len(after) and [i for i, (a, b) in enumerate(zip(before, after)) if a != b] == [row],
              'Merge changed an unrelated QUEUE row')
    actual_downloads = []
    for name in ['manuscript.pdf', c.ZIP_NAME, 'manuscript.tex', 'metadata.json']:
        data = reader.read(c.PREPRINT + name, merge); spec = context['freeze']['files'][name]
        c.require(len(data) == spec['bytes'] and c.sha(data) == spec['sha256'], 'Merged public/source artifact differs')
        actual_downloads.append({'path': c.PREPRINT + name, 'sha256': c.sha(data), 'bytes': len(data)})
    latest = c.github('git/ref/heads/main')['object']['sha']
    ancestry = c.github('compare/' + merge + '...' + latest)
    c.require(ancestry.get('status') in {'identical', 'ahead'}
              and ancestry.get('merge_base_commit', {}).get('sha') == merge, 'Actual merge is not ancestor of current main')
    _, _, latest_cells, latest_columns = c.queue_row(reader.read(c.QUEUE, latest))
    c.require(latest_cells[latest_columns.index('Status')].strip() == 'claimed_solved'
              and latest_cells[latest_columns.index('DOI')].strip() == installed['doi_url'], 'Current main disposition differs')
    receipt = {'verified_at_utc': c.now(), 'pr': 464, 'problem_id': c.PROBLEM, 'merged': True,
               'accepted_branch_head': installed['commit_sha'], 'merge_commit_sha': merge,
               'previous_main_sha': previous_main, 'observed_current_main_sha': latest,
               'merge_ancestor_of_current_main': True, 'selected_queue_status': 'claimed_solved',
               'selected_queue_turns': '1/5', 'doi': installed['doi'], 'doi_url': installed['doi_url'],
               'verified_file_count': len(verified), 'verified_files': verified,
               'exact_immutable_blob_identity_for_all_nonqueue_installed_files': True,
               'fully_downloaded_artifacts': actual_downloads, 'merge_changed_queue_rows': 1,
               'verification_basis': 'Integration independently verified full accepted blob bytes before and after branch update; this fresh merge check verifies immutable blob identity for all payloads and downloads four public/source files. QUEUE is checked against merge parent and latest main to permit unrelated later row changes.',
               'shared_checkout_and_index': 'untouched', 'external_writes': 0}
    c.dump('ACTUAL_MERGE_READBACK.json', receipt)
    print(json.dumps({k: receipt[k] for k in ['merged', 'merge_commit_sha', 'verified_file_count', 'doi', 'merge_changed_queue_rows']}, indent=2))


if __name__ == '__main__': main()
