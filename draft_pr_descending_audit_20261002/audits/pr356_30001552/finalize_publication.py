"""Record actual publication; retain a failed read-only tracker attempt honestly."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

A = Path(__file__).resolve().parent
P = A.parents[1]
R = P.parent
D = A / 'publication'
load = lambda p: json.loads(p.read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
utc = lambda: datetime.now(timezone.utc).isoformat()

clear = load(A / 'PUBLISHING_CLEARANCE.json')
merged = load(A / 'ACTUAL_MERGE_VERIFICATION.json')
post = load(A / 'ROOT_POST_MERGE_VERIFICATION.json')
published = load(D / 'inspect_published_receipt.json')
public = load(D / 'PUBLIC_RECORD_VERIFICATION.json')
assert clear['status'] == 'READY_AFTER_TWO_SEQUENTIAL_FRESH_PREPRINT_REVIEWS'
assert merged['status'] == 'claimed_solved' and merged['turns'] == '1/5'
assert not (A/'CURRENT_PUBLICATION_STATUS.json').exists(), 'Finalization already recorded; preserve original event'
assert merged['all_expected_paths_exact'] == 22 and merged['all_target_file_hashes_exact'] == 21
assert merged['all_other_queue_bytes_equal']
assert post['status'] == 'PASS_COMPLETE_PR356_POST_MERGE'
assert post['actual_merge'] == merged['actual_merge'] and post['closed_namespaces_unchanged']
assert post['all_22_source_bindings_exact'] and post['all_16_original_math_files_unchanged']
assert published['state'] == 'published' and published['environment'] == 'production'
assert published['metadata_normalizations'] == []
assert published['doi_resolution']['status'] == 'resolved'
assert published['doi_resolution']['http_status'] == 200
assert public['status'] == 'PASS_PUBLIC_RECORD_EXACT_METADATA_AND_ALL_FILE_BYTES'
assert public['doi'] == published['doi'] and public['record_id'] == published['id']
assert len(public['all_file_bytes']) == 2
assert all(e['entire_public_download_equals_reviewed_local_file'] for e in public['all_file_bytes'])
for e in clear['sealed_submission_files']:
    b = (A / 'preprint' / e['path']).read_bytes()
    assert len(b) == e['bytes'] and sha(b) == e['sha256']
    assert b == (R / 'problems/30001552_antimorphic_periods/preprint' / e['path']).read_bytes()
original = load(A / 'snapshot_manifest.json')
for e in original['files']:
    if e['path'].endswith('/QUEUE.md'):
        continue
    b = (R / e['path']).read_bytes()
    assert len(b) == e['bytes'] and sha(b) == e['sha256']
assert len(original['files']) == 17

tracker_path = D / 'TRACKER_COMPLETE.json'
if tracker_path.exists():
    tracker = load(tracker_path)
    assert tracker['status'] == 'PASS_ONE_ROW_APPENDED_AND_EXACT_READBACK'
    assert tracker['doi'] == published['doi'] and tracker['gid'] == 1254632077
    tracker_complete, percent = True, 100
    disposition = 'merged_claimed_solved_published_zenodo_tracker_verified'
else:
    assert not (D / 'tracker_append_response.stdout').exists(), 'Uncertain append: inspect before any further action'
    failed = D / 'private_tracker/before_append_sheet_metadata_execution.json'
    rec = load(failed)
    assert rec['exit_code'] != 0 and rec['argv'][:4] == ['gws', 'sheets', 'spreadsheets', 'get']
    streams = []
    for name in ['stdout', 'stderr']:
        b = (failed.parent / ('before_append_sheet_metadata.' + name)).read_bytes()
        assert len(b) == rec[name + '_bytes'] and sha(b) == rec[name + '_sha256']
        streams.append(b)
    assert b'invalid_grant' in b'\n'.join(streams)
    pending = {'utc': utc(), 'status': 'ZENODO_PUBLISHED_TRACKER_PENDING_GWS_AUTH',
               'doi': published['doi'], 'record_url': published['record_url'],
               'tracker_mutation_attempted': False,
               'failed_operation': 'gws sheets spreadsheets get (read-only target metadata)',
               'failure': 'invalid_grant: Token has been expired or revoked',
               'native_capture_directory': 'publication/private_tracker',
               'next_action': 'Reconnect the existing Google Workspace CLI login, then execute the guarded append once. Do not duplicate the Zenodo deposit.',
               'mathematical_resolution_percent': 100, 'preprint_preparation_percent': 100,
               'acceptance_publication_workflow_percent': 95,
               'persistent_goal_remains_active': True, 'native_failure': rec}
    assert not (D / 'TRACKER_PENDING.json').exists()
    (D / 'TRACKER_PENDING.json').write_text(json.dumps(pending, indent=2) + '\n')
    tracker_complete, percent = False, 95
    disposition = 'merged_claimed_solved_published_zenodo_tracker_pending_auth'

t = utc()
status = {'utc': t, 'status': 'MERGED_PUBLISHED_AND_TRACKER_VERIFIED' if tracker_complete else 'MERGED_PUBLISHED_TRACKER_PENDING_AUTH',
          'workflow_completion_percent': percent, 'mathematical_resolution_percent': 100,
          'preprint_preparation_percent': 100, 'accepted_status': 'claimed_solved', 'author_turns': '1/5',
          'original_head': original['head'], 'accepted_head': merged['reviewed_head'],
          'actual_merge': merged['actual_merge'], 'merged_at': merged['merged_at'],
          'zenodo_record': published['id'], 'doi': published['doi'], 'doi_url': published['doi_url'],
          'record_url': published['record_url'], 'doi_resolves': True,
          'tracker_gid': 1254632077, 'tracker_exact_readback': tracker_complete,
          'tracker_mutation_attempted': tracker_complete,
          'sealed_submission_files': clear['sealed_submission_files'],
          'two_sequential_fresh_preprint_reviews_cleared': True,
          'all_16_original_math_files_unchanged': True,
          'all_public_metadata_and_download_bytes_verified': True,
          'historical_novelty_or_first_priority_certified': False,
          'external_human_peer_review_received': False, 'extensive_AI_use_disclosed': True,
          'journal_submission': False, 'GitHub_release': False,
          'no_person_contact_or_conversation_shared': True,
          'earlier_pending_records_are_immutable_dated_history': True}
if tracker_complete:
    status['tracker_updated_range'] = tracker['updatedRange']
(A / 'CURRENT_PUBLICATION_STATUS.json').write_text(json.dumps(status, indent=2) + '\n')
(R/'problems/30001552_antimorphic_periods/preprint/PUBLICATION_RESULT.json').write_text(json.dumps(status,indent=2)+'\n')
c = load(A / 'acceptance_criteria.json')
c.update(utc=t, updated_utc=t, acceptance_publication_workflow_percent=percent, candidate_accepted=True, independently_accepted=True,
         workflow_completion_percent=percent, publication_workflow_percent=percent,
         actual_merge_pending=False, zenodo_publication_pending=False,
         tracker_append_pending=not tracker_complete, doi=published['doi'],
         zenodo_record=published['id'], current_publication_status='CURRENT_PUBLICATION_STATUS.json',
         exposure_disclosure='The exact original mathematical scope passed root review, three independent mathematical families, a bounded primary-source priority audit, and two sequential fresh preprint reviews. Actual merge and whole public-file/metadata checks passed. External human peer review and universal historical novelty are not certified.')
(A / 'acceptance_criteria.json').write_text(json.dumps(c, indent=2) + '\n')
inv = load(P / 'inventory.json')
row = next(x for x in inv['items'] if x['number'] == 356)
assert row['actual_merge'] == merged['actual_merge']
row.update(disposition=disposition, audit_workflow_percent=percent, doi=published['doi'],
           zenodo_record=published['id'], tracker_pending_auth=not tracker_complete,
           current_publication_status='audits/pr356_30001552/CURRENT_PUBLICATION_STATUS.json')
inv.setdefault('claimed_solved_published_by_descending', [])
assert 356 not in inv['claimed_solved_published_by_descending']
inv['claimed_solved_published_by_descending'].append(356)
if not tracker_complete:
    inv.setdefault('claimed_solved_tracker_pending_by_descending', [])
    if 356 not in inv['claimed_solved_tracker_pending_by_descending']:
        inv['claimed_solved_tracker_pending_by_descending'].append(356)
(P / 'inventory.json').write_text(json.dumps(inv, indent=2) + '\n')
tracker_text = ('One Google Workspace CLI row was appended and independently read back at ' + tracker['updatedRange'] + '.') if tracker_complete else 'The first read-only Google Workspace CLI request failed with invalid_grant; no tracker write was attempted. The DOI row remains pending the existing CLI login reconnect.'
(D / 'README.md').write_text('# Verified preprint publication\n\n'
    + 'Published version 1.0: [Zenodo record](' + published['record_url'] + '), [DOI ' + published['doi'] + '](' + published['doi_url'] + '). The DOI resolves with HTTP 200. Both complete public downloads and all ten supplied metadata fields match the cleared local submission; no metadata normalization occurred.\n\n'
    + 'The three-page note proves the exact original alternating antimorphic gcd conjecture, including equality and partial terminal blocks. The reversal witness abb gives only uniform one-letter-lower obstruction. The 69-member verification archive binds68 payloads, preserves16 original research files, and includes signed-graph, word-overlap, definition and bounded-priority evidence. Current portable68408 output is reproduced; historical optional five-source68413 mode remains unreproduced. Both sequential fresh preprint adversaries and the complete root exact-live/post-merge checks passed. AI use, the unrefereed status, and lack of external human peer review are disclosed. Fine-Wilf, the originating Nowotka/Bischoff contribution and Bischoff thesis reflection/doubled-period mechanism are credited. Bounded priority access/version gaps remain; universal novelty or first discovery is not certified.\n\n'
    + tracker_text + '\n\n'
    + 'Actual PR #356 merge: `' + merged['actual_merge'] + '`. Current workflow ' + str(percent) + '%, mathematics and preprint preparation 100%. Earlier dated pending receipts remain immutable history. No journal submission, GitHub release, person contact or conversation sharing occurred. Do not repeat the Zenodo deposit.\n')
(R/'problems/30001552_antimorphic_periods/preprint/PUBLICATION.md').write_bytes((D/'README.md').read_bytes())
line = ('\n' + t + ': PR356 accepted and published: actual merge `' + merged['actual_merge']
        + '`, DOI `' + published['doi'] + '` (' + published['record_url'] + '). All original16 mathematical files unchanged; final4 submission pins, complete public PDF/ZIP bytes and all10 metadata fields exact, zero normalization, DOI200. Two sequential fresh adversaries clean. Mathematics/preprint100%, acceptance/publication workflow'
        + str(percent) + '%. ' + tracker_text
        + ' Bounded priority only, extensive AI use, unrefereed/no external human review. Persistent claimed_solved-only descending goal remains active; PR8 excluded.\n')
for path in [A / 'README.md', A / 'RESEARCH_LOG.md', A / 'ACCEPTANCE_DECISION.md', P / 'RESEARCH_LOG.md',
             A / 'publication/FINAL_RESEARCH_CHECKPOINT.md']:
    with path.open('a') as f:
        f.write(line)
print(json.dumps({k: v for k, v in status.items() if k != 'sealed_submission_files'}, indent=2))
