"""Prepared final event record, requiring actual merge, publication and tracker."""
from pathlib import Path
import json
from root_submission_gate import (A, P, R, TARGET, current_clearance, load, pin, utc)

D = A / 'publication'
assert not (A / 'CURRENT_PUBLICATION_STATUS.json').exists()
clear = current_clearance()
merged = load(A / 'ACTUAL_MERGE_VERIFICATION.json')
post = load(A / 'ROOT_POST_MERGE_VERIFICATION.json')
published = load(D / 'inspect_published_receipt.json')
public = load(D / 'PUBLIC_RECORD_VERIFICATION.json')
tracker = load(D / 'TRACKER_COMPLETE.json')
assert merged['status'] == 'claimed_solved' and merged['turns'] == '1/5'
assert merged['all_expected_paths_exact'] == 21 and merged['all_target_file_hashes_exact'] == 20
assert merged['all_other_queue_bytes_equal']
assert post['status'] == 'PASS_COMPLETE_PR344_POST_MERGE'
assert post['actual_merge'] == merged['actual_merge'] and post['closed_namespaces_unchanged']
assert post['all_21_source_bindings_exact'] and post['all_15_original_math_files_unchanged']
assert published['state'] == 'published' and published['environment'] == 'production'
assert published['metadata_normalizations'] == []
assert published['doi_resolution']['status'] == 'resolved'
assert published['doi_resolution']['http_status'] == 200
assert public['status'] == 'PASS_PUBLIC_RECORD_EXACT_METADATA_AND_ALL_FILE_BYTES'
assert public['doi'] == published['doi'] and public['record_id'] == published['id']
assert len(public['all_reviewed_metadata_keys_compared']) == 11
assert len(public['all_file_bytes']) == 2
assert all(row['entire_public_download_equals_reviewed_local_file'] for row in public['all_file_bytes'])
assert tracker['status'] == 'PASS_ONE_ROW_APPENDED_AND_EXACT_READBACK'
assert tracker['doi'] == published['doi'] and tracker['gid'] == 1254632077
for entry in clear['sealed_submission_files']:
    assert pin(A / 'preprint' / entry['path']) == {key: entry[key] for key in ('bytes', 'sha256', 'mode')}
    assert (A / 'preprint' / entry['path']).read_bytes() == (R / TARGET / 'preprint' / entry['path']).read_bytes()
original = load(A / 'snapshot_manifest.json')
assert len(original['files']) == 16
for entry in original['files']:
    if entry['path'].endswith('/QUEUE.md'):
        continue
    assert {key: pin(R / entry['path'])[key] for key in ('bytes', 'sha256')} == {
        key: entry[key] for key in ('bytes', 'sha256')}

time = utc()
status = dict(utc=time, status='MERGED_PUBLISHED_AND_TRACKER_VERIFIED',
              workflow_completion_percent=100, mathematical_resolution_percent=100,
              bounded_priority_percent=100, preprint_preparation_percent=100,
              accepted_status='claimed_solved', author_turns='1/5',
              original_head=original['head'], accepted_head=merged['reviewed_head'],
              actual_merge=merged['actual_merge'], merged_at=merged['merged_at'],
              zenodo_record=published['id'], doi=published['doi'], doi_url=published['doi_url'],
              record_url=published['record_url'], doi_resolves=True,
              tracker_gid=1254632077, tracker_exact_readback=True,
              tracker_updated_range=tracker['updatedRange'],
              sealed_submission_files=clear['sealed_submission_files'],
              sealed_author_inputs=clear['sealed_author_inputs'],
              successive_new_full_preprint_reviews=3, final_clean_review=3,
              historical_adverse_reviews_retained=True,
              historical_supporting_findings_repaired=['B1', 'F01/root B2'],
              all_15_original_math_files_unchanged=True,
              all_public_metadata_and_download_bytes_verified=True,
              first_priority_certified=False, first_application_certified=False,
              continuing_openness_certified=False, external_human_peer_review_received=False,
              extensive_AI_use_disclosed=True, journal_submission=False, GitHub_release=False,
              no_person_contact_or_conversation_shared=True,
              earlier_pending_records_are_immutable_dated_history=True,
              persistent_descending_goal_remains_active=True)
(A / 'CURRENT_PUBLICATION_STATUS.json').write_text(json.dumps(status, indent=2) + '\n')
(R / TARGET / 'preprint/PUBLICATION_RESULT.json').write_text(json.dumps(status, indent=2) + '\n')
criteria = load(A / 'acceptance_criteria.json')
criteria.update(updated_utc=time, candidate_accepted=True, independently_accepted=True,
                workflow_completion_percent=100, publication_workflow_percent=100,
                preprint_preparation_percent=100, actual_merge_pending=False,
                zenodo_publication_pending=False, tracker_append_pending=False,
                doi=published['doi'], zenodo_record=published['id'],
                current_publication_status='CURRENT_PUBLICATION_STATUS.json')
(A / 'acceptance_criteria.json').write_text(json.dumps(criteria, indent=2) + '\n')
inventory = load(P / 'inventory.json')
item = next(row for row in inventory['items'] if row['number'] == 344)
assert item['actual_merge'] == merged['actual_merge']
item.update(disposition='merged_claimed_solved_published_zenodo_tracker_verified',
            audit_workflow_percent=100, doi=published['doi'], zenodo_record=published['id'],
            current_publication_status='audits/pr344_30005649/CURRENT_PUBLICATION_STATUS.json')
inventory.setdefault('claimed_solved_published_by_descending', [])
assert 344 not in inventory['claimed_solved_published_by_descending']
inventory['claimed_solved_published_by_descending'].append(344)
(P / 'inventory.json').write_text(json.dumps(inventory, indent=2) + '\n')
prose = ('# Verified preprint publication\n\nPublished version 1.0: [Zenodo record]('
         + published['record_url'] + '), [DOI ' + published['doi'] + '](' + published['doi_url']
         + '). The DOI resolves with HTTP200. Both complete public downloads and all11 supplied metadata fields match the cleared local submission, with no normalization.\n\n'
         'The four-page note gives an explicit negative answer to Takao\'s higher-rank self-duality question in OWR42/2023, printed2479. For every p>3 and n>=3 over k=an algebraic closure of F_p, both the quasi-supersingular special fiber and its p-killed finite flat W(k)-lift of rank p^(2n) fail Cartier self-duality. The definition uses actual supersingular elliptic p-torsion factors over k. No quasi-supersingular Witt-ring filtration, universal perfect-field descent, polarization, Jacobian or Coleman result is asserted.\n\n'
         'The33-member verification ZIP has32 payloads. Three independent mathematical approach families and a bounded primary-literature audit were completed. Established cyclic-word, supersingular, Dieudonne and finite Honda mechanisms are credited. Source/access/version limitations remain; first discovery, first application and worldwide continuing openness are not certified.\n\n'
         'Three successive NEW full preprint adversaries were used. Historical B1 and F01/root B2 remain adverse records. Their supporting-software defects were repaired globally in the current public derivative: interpreter-independent mathematical output and opposite squared-Frobenius twists in the generic dual kernel formula. Dense nonprime basis changes, separate reviewer arithmetic and targeted negative controls were checked. The third NEW full review closed with zero unresolved mandatory findings. All15 original research files remain byte-identical; original progress remains1/5.\n\n'
         'Extensive AI use is disclosed. This is an unrefereed preprint without independent external human peer review. No journal submission, GitHub release, person contact or conversation sharing occurred.\n\n'
         'One Google Workspace CLI row was appended and read back exactly at ' + tracker['updatedRange']
         + '. Actual PR344 merge: `' + merged['actual_merge'] + '`. Publication workflow100%; the descending claimed_solved-only goal remains active. Do not repeat this deposit or tracker append.\n')
(D / 'README.md').write_text(prose)
(R / TARGET / 'preprint/PUBLICATION.md').write_text(prose)
line = ('\n' + time + ': PR344 accepted and published: actual merge `' + merged['actual_merge']
        + '`, DOI `' + published['doi'] + '` (' + published['record_url'] + '). All15 original mathematical files unchanged; exact reviewed v04 eight-author-input/four-formal-file custody retained, both complete public PDF/ZIP bytes and all11 metadata fields exact, zero normalization, DOI200. Third NEW full adversary clean after two preserved adverse reviews and global supporting-code repairs. ONE tracker row exact at ' + tracker['updatedRange']
        + '. Mathematics/preprint100%, bounded priority100%, publication workflow100%. Extensive AI use; unrefereed, no external human review or first-priority certificate. Persistent descending claimed_solved-only goal remains active; PR8 excluded.\n')
for path in [A / 'README.md', A / 'RESEARCH_LOG.md', A / 'ACCEPTANCE_DECISION.md',
             P / 'RESEARCH_LOG.md', D / 'FINAL_RESEARCH_CHECKPOINT.md']:
    with path.open('a') as file:
        file.write(line)
print(json.dumps({key: value for key, value in status.items()
                  if key not in ('sealed_submission_files', 'sealed_author_inputs')}, indent=2))
