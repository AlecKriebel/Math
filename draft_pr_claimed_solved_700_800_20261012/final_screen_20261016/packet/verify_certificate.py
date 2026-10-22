"""Verify the closed certificate inventory and optionally replay 90 source blobs.

Usage: python -I -S -B verify_certificate.py PACKET MANIFEST_SHA CHECKER_SHA REPO [--replay-blobs]
All operations, including optional Git cat-file, are read-only. No network calls.
The externally supplied manifest/checker hashes are the trust anchors.
"""
import collections
import datetime
import hashlib
import json
import pathlib
import re
import stat
import subprocess
import sys

QUEUE = 'unsolved_math_prioritization/QUEUE.md'
NUMBERS = list(range(700, 801))
FIELDS = 'number title state isDraft merged headRefOid headRefName closedAt url mergeCommit { oid }'
PROCESSED = [718, 734, 742, 764, 765, 767, 778, 781, 786, 788, 789]
CURRENT = [799]


def need(test, message):
    if not test:
        raise RuntimeError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def blob_oid(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()


def read_json(root, name):
    return json.loads((root / name).read_bytes())


def own_row(raw, problem):
    pattern = re.compile(rb'^\|\s*\d+\s*\|\s*' + problem.encode() + rb'\s*(?:/|\|)')
    rows = [r.decode() for r in raw.splitlines() if pattern.match(r)]
    need(len(rows) == 1, 'Missing/duplicate own queue row')
    cells = [c.strip() for c in rows[0].strip('|').split('|')]
    need(len(cells) == 12, 'Wrong own-row schema')
    return rows[0], cells[7], cells[8]


def main():
    need(len(sys.argv) in (5, 6), 'Expected PACKET MANIFEST_SHA CHECKER_SHA REPO [--replay-blobs]')
    root = pathlib.Path(sys.argv[1])
    need(root.is_absolute() and root.is_dir() and not root.is_symlink(), 'Absolute nonsymlink packet required')
    mp, cp = sys.argv[2:4]
    repo = pathlib.Path(sys.argv[4])
    replay = len(sys.argv) == 6
    need(not replay or sys.argv[5] == '--replay-blobs', 'Unknown option')
    need(repo.is_absolute() and repo.is_dir(), 'Absolute repository directory required')
    need(sha((root / 'MANIFEST.json').read_bytes()) == mp, 'Manifest external pin mismatch')
    need(sha((root / 'verify_certificate.py').read_bytes()) == cp, 'Checker external pin mismatch')
    need(pathlib.Path(__file__).resolve() == (root / 'verify_certificate.py').resolve(), 'Checker execution path mismatch')
    manifest = read_json(root, 'MANIFEST.json')
    need(manifest['schema'] == 'closed-regular-file-inventory-v1', 'Manifest schema')
    files = manifest['files']
    need(set(p.name for p in root.iterdir()) == set(files) | {'MANIFEST.json', 'verify_certificate.py'}, 'Closed inventory mismatch')
    for p in root.iterdir():
        need(stat.S_ISREG(p.lstat().st_mode), 'Nonregular entry')
    for name, digest in files.items():
        need('/' not in name and '\\' not in name and name not in ('.', '..'), 'Noncanonical manifest name')
        need(sha((root / name).read_bytes()) == digest, 'Inventory hash mismatch: ' + name)
    cert = read_json(root, 'CERTIFICATE.json')
    need(cert['schema'] == 'read-only-final-eligibility-screen-v1', 'Certificate schema')
    need(cert['repository'] == 'AlecKriebel/Math' and cert['range_inclusive'] == [700, 800] and cert['order'] == 'ascending', 'Scope mismatch')
    need(cert['expected_numbers'] == NUMBERS and cert['coverage_complete'] is True and cert['numbers_accounted'] == 101, 'Complete range not certified')
    rows = cert['rows']
    need([r['number'] for r in rows] == NUMBERS, 'Coverage missing/duplicate/reordered number')
    initial_raw = (root / 'INITIAL_INVENTORY.json').read_bytes()
    need(sha(initial_raw) == cert['initial_mapping_sha256'], 'Initial mapping source mismatch')
    initial_rows = read_json(root, 'INITIAL_INVENTORY.json')['range_prs']
    need([r['number'] for r in initial_rows] == NUMBERS, 'Initial coverage mismatch')
    initial = {r['number']: r for r in initial_rows}
    metadata = {}
    for prefix in ('metadata_before', 'metadata_after'):
        combined = []
        for index, start in enumerate(range(700, 801, 25)):
            numbers = list(range(start, min(start + 25, 801)))
            doc = read_json(root, f'{prefix}_{index:02d}.json')
            aliases = ' '.join(f'p{n}:pullRequest(number:{n}){{{FIELDS}}}' for n in numbers)
            expected_query = 'query { repository(owner:"AlecKriebel",name:"Math") { ' + aliases + ' } }'
            need(doc['query'] == expected_query, 'Metadata query differs from complete alias query')
            need(not doc['response'].get('errors'), 'Captured metadata API errors')
            result = doc['response']['data']['repository']
            need(set(result) == {f'p{n}' for n in numbers}, 'Metadata alias coverage')
            for number in numbers:
                row = result[f'p{number}']
                need(row is not None and row['number'] == number, 'Missing/misnumbered metadata')
                combined.append(row)
        metadata[prefix] = combined
    need(metadata['metadata_before'] == metadata['metadata_after'], 'Before/after metadata changed')
    need(cert['metadata_stable_across_complete_before_after_inventories'] is True, 'Unstable certificate')
    meta = metadata['metadata_before']
    open_drafts = [r for r in meta if r['state'] == 'OPEN' and r['isDraft']]
    source_oids = {}
    for index, start in enumerate(range(0, len(open_drafts), 20)):
        group = open_drafts[start:start + 20]
        doc = read_json(root, f'queue_oids_{index:02d}.json')
        aliases = ' '.join(f'q{r["number"]}:object(expression:"{r["headRefOid"]}:{QUEUE}")'
                           '{ ... on Blob { oid byteSize } }' for r in group)
        expected = 'query { repository(owner:"AlecKriebel",name:"Math") { ' + aliases + ' } }'
        need(doc['query'] == expected and not doc['response'].get('errors'), 'Queue query binding mismatch')
        result = doc['response']['data']['repository']
        need(set(result) == {f'q{r["number"]}' for r in group}, 'Queue alias coverage')
        for r in group:
            source_oids[r['number']] = result[f'q{r["number"]}']
    replayed = 0
    for index, record in enumerate(rows):
        number = record['number']
        need(all(record[k] == v for k, v in meta[index].items()), 'Certificate differs from authenticated metadata')
        need(record['problem_id'] == initial[number]['problem_id'], 'Initial own problem mapping mismatch')
        if record['state'] != 'OPEN' or not record['isDraft']:
            need(record['queue_inspected'] is False and record['disposition'] == 'not_open_draft_metadata_only', 'Non-open-draft processed')
            need(not any(k.startswith('queue_') and k != 'queue_inspected' for k in record), 'Out-of-scope source read')
            continue
        need(record['queue_inspected'] is True, 'Missing required own-row screen')
        problem = record['problem_id']
        need(problem in re.findall(r'(?<!\d)\d{4,8}(?!\d)', record['headRefName']), 'Current branch/mapping mismatch')
        source = source_oids[number]
        need(record['queue_blob_oid'] == source['oid'] and record['queue_blob_bytes'] == source['byteSize'], 'Authenticated blob identity mismatch')
        need(record['queue_path'] == QUEUE, 'Wrong queue source path')
        parsed_row, status, turns = own_row((record['own_row'] + '\n').encode(), problem)
        need(parsed_row == record['own_row'] and status == record['queue_status'] and turns == record['queue_turns'], 'Own-row status extraction mismatch')
        need(sha(record['own_row'].encode()) == record['own_row_sha256'], 'Own-row byte hash mismatch')
        need(record['disposition'] == ('eligible_current' if status == 'claimed_solved' else 'skipped_out_of_scope'), 'Wrong exact-status scope')
        need(record['initial_head_unchanged'] == (record['headRefOid'] == initial[number]['headRefOid']), 'Initial head comparison wrong')
        need(record['initial_status_unchanged'] == (status == initial[number]['queue_status']), 'Initial status comparison wrong')
        if replay:
            result = subprocess.run(['git', 'cat-file', 'blob', record['headRefOid'] + ':' + QUEUE],
                                    capture_output=True, cwd=repo, check=True)
            raw = result.stdout
            need(blob_oid(raw) == record['queue_blob_oid'] and sha(raw) == record['queue_blob_sha256'] and len(raw) == record['queue_blob_bytes'], 'Replayed complete source bytes differ')
            need(own_row(raw, problem) == (record['own_row'], status, turns), 'Replayed own source row differs')
            replayed += 1
    eligible = [r['number'] for r in rows if r['disposition'] == 'eligible_current']
    need(cert['merged_numbers'] == [r['number'] for r in rows if r['merged']], 'Merged summary mismatch')
    need(cert['closed_unmerged_numbers'] == [r['number'] for r in rows if r['state'] == 'CLOSED' and not r['merged']], 'Closed summary mismatch')
    need(cert['metadata_state_counts'] == dict(collections.Counter(r['state'] for r in rows)), 'Metadata counts mismatch')
    need(cert['open_draft_count'] == len(open_drafts), 'Open draft count mismatch')
    need(cert['open_draft_status_counts'] == dict(collections.Counter(r['queue_status'] for r in rows if r['queue_inspected'])), 'Status counts mismatch')
    need(cert['already_processed_numbers_supplied_by_parent'] == PROCESSED and cert['currently_in_review_numbers_supplied_by_parent'] == CURRENT, 'Parent supplied case accounting mismatch')
    need(cert['current_exact_claimed_solved_numbers'] == eligible, 'Current eligible list mismatch')
    unprocessed = sorted(set(eligible) - set(PROCESSED))
    need(cert['eligible_not_yet_processed_numbers'] == unprocessed, 'Unprocessed list mismatch')
    newly = sorted(set(unprocessed) - set(CURRENT))
    need(cert['newly_eligible_outside_known_current_case_numbers'] == newly, 'New eligibility list mismatch')
    need(datetime.datetime.fromisoformat(cert['started_at']) <= datetime.datetime.fromisoformat(cert['finished_at']), 'Timestamp order')
    print(json.dumps({'status': 'PASS', 'coverage': 101, 'open_drafts': len(open_drafts),
                      'statuses': cert['open_draft_status_counts'], 'current_eligible': eligible,
                      'newly_eligible_outside_known_current': newly,
                      'source_blobs_replayed': replayed, 'network_calls': 0,
                      'scope': 'metadata and own queue row only; no mathematical review'}))


if __name__ == '__main__':
    main()
