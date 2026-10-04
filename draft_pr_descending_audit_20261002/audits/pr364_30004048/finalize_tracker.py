"""Finish the previously published PR364 after its first successful sheet append."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

A = Path(__file__).resolve().parent
P = A.parents[1]
D = A / 'publication'
load = lambda p: json.loads(p.read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
t = datetime.now(timezone.utc).isoformat()
old_bytes = (A / 'PUBLICATION_RESULT.json').read_bytes()
old = json.loads(old_bytes)
clear = load(A / 'PUBLISHING_CLEARANCE.json')
merged = load(A / 'ACTUAL_MERGE_VERIFICATION.json')
post = load(A / 'ROOT_POST_MERGE_VERIFICATION.json')
published = load(D / 'inspect_published_receipt.json')
public = load(D / 'PUBLIC_RECORD_VERIFICATION.json')
tracker = load(D / 'TRACKER_COMPLETE.json')
assert old['status'] == 'MERGED_AND_ZENODO_PUBLISHED_TRACKER_AUTH_PENDING'
assert old['workflow_completion_percent'] == 95 and old['tracker_mutation_attempted'] is False
assert clear['status'] == 'READY_AFTER_TWO_SEQUENTIAL_FRESH_PREPRINT_REVIEWS'
assert clear['second_review_mandatory_findings'] == 0
assert merged['status'] == 'claimed_solved' and merged['turns'] == '3/5'
assert merged['all_expected_paths_exact'] == 42 and merged['all_target_file_hashes_exact'] == 41
assert post['status'] == 'PASS_FRESH_POST_MERGE_ALL_SOURCE_AND_SUBMISSION_BINDINGS'
assert post['actual_merge'] == merged['actual_merge'] == old['actual_merge']
assert post['all41_mathematical_files_unchanged'] and post['all_five_family_namespaces_unchanged']
assert published['state'] == 'published' and published['environment'] == 'production'
assert published['metadata_normalizations'] == []
assert published['doi_resolution']['status'] == 'resolved' and published['doi_resolution']['http_status'] == 200
assert public['status'] == 'PASS_PUBLIC_RECORD_EXACT_METADATA_AND_ALL_FILE_BYTES'
assert public['doi'] == published['doi'] == old['doi'] == tracker['doi']
assert len(public['all_file_bytes']) == 2
assert all(e['entire_public_download_equals_reviewed_local_file'] for e in public['all_file_bytes'])
assert tracker['status'] == 'PASS_ONE_ROW_APPENDED_AND_EXACT_READBACK' and tracker['gid'] == 1254632077
for e in clear['sealed_submission_files']:
    b = (A / 'preprint' / e['path']).read_bytes()
    assert len(b) == e['bytes'] and sha(b) == e['sha256']
assert old['all_four_submission_files'] == clear['sealed_submission_files']
history = A / 'private_publication_history'
history.mkdir(exist_ok=True)
archive = history / ('PUBLICATION_RESULT_pending95_' + sha(old_bytes) + '.json')
assert not archive.exists()
archive.write_bytes(old_bytes)
current = {**old, 'utc': t, 'status': 'MERGED_PUBLISHED_AND_TRACKER_VERIFIED',
           'workflow_completion_percent': 100, 'tracker_append_pending': False,
           'tracker_mutation_attempted': True, 'tracker_exact_readback': True,
           'tracker_gid': tracker['gid'], 'tracker_updated_range': tracker['updatedRange'],
           'tracker_completion_receipt': 'publication/TRACKER_COMPLETE.json',
           'tracker_failure': None, 'earlier_auth_failure_preserved_as_history': True,
           'previous_publication_result_sha256': sha(old_bytes),
           'previous_publication_result_archive': str(archive.relative_to(A)),
           'extensive_AI_use_disclosed': True, 'external_human_peer_review_received': False}
(A / 'PUBLICATION_RESULT.json').write_text(json.dumps(current, indent=2) + '\n')
c = load(A / 'acceptance_criteria.json')
c.update(utc=t, workflow_completion_percent=100, tracker_append_pending=False,
         tracker_exact_readback=True, tracker_updated_range=tracker['updatedRange'])
(A / 'acceptance_criteria.json').write_text(json.dumps(c, indent=2) + '\n')
inv = load(P / 'inventory.json')
row = next(x for x in inv['items'] if x['number'] == 364)
assert row['actual_merge'] == merged['actual_merge']
row.update(disposition='merged_claimed_solved_published_zenodo_tracker_verified',
           audit_workflow_percent=100, tracker_pending_auth=False,
           tracker_updated_range=tracker['updatedRange'],
           current_publication_status='audits/pr364_30004048/PUBLICATION_RESULT.json')
pending = inv['claimed_solved_tracker_pending_by_descending']
assert 364 in pending
pending.remove(364)
(P / 'inventory.json').write_text(json.dumps(inv, indent=2) + '\n')
line = ('\n' + t + ': PR364 tracker completion: the existing Google Workspace CLI authorization now works. '
        + 'The guarded first append passed duplicate/header checks and was independently read back at '
        + tracker['updatedRange'] + ' with DOI `' + tracker['doi'] + '`. No previous tracker write existed; '
        + 'the initial failed read-only capture remains untouched and the successful metadata retry uses a distinct capture label. '
        + 'No Zenodo operation or paper edit was repeated. Mathematics/preprint100%; acceptance/publication workflow100%. '
        + 'Earlier95% pending receipts remain dated history. Bounded priority, inaccessible2019 thesis, AI/unrefereed/no external human review disclosures remain.\n')
for path in [A / 'README.md', A / 'RESEARCH_LOG.md', A / 'ACCEPTANCE_DECISION.md', D / 'README.md', P / 'RESEARCH_LOG.md']:
    with path.open('a') as f:
        f.write(line)
print(json.dumps({k: v for k, v in current.items() if k != 'all_four_submission_files'}, indent=2))
