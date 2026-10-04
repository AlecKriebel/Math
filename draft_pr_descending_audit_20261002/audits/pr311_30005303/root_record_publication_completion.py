"""Record actual publication without changing any cleared scientific artifact."""
from root_submission_gate import *
import copy

assert not (A/'CURRENT_PUBLICATION_STATUS.json').exists()
assert not (A/'published_pr_body_update_preexecution.json').exists()
clear = current_clearance()
window()
cap = Capture('publication_completion')
merged = load(A/'ACTUAL_MERGE_VERIFICATION.json')
post = load(A/'ROOT_POST_MERGE_VERIFICATION.json')
pub = load(A/'publication/inspect_published_receipt.json')
public = load(A/'publication/PUBLIC_RECORD_VERIFICATION.json')
tracker = load(A/'publication/TRACKER_COMPLETE.json')
assert merged['status'] == 'PASS_PR311_EXACT_MERGE'
assert post['status'] == 'PASS_PR311_POST_MERGE_EXACT_SUBMISSION' and post['actual_merge'] == merged['actual_merge']
assert pub['state'] == 'published' and pub['environment'] == 'production'
assert type(pub['id']) is int and pub['id'] > 0 and pub['doi_url'] == 'https://doi.org/'+pub['doi']
assert pub['record_url'] == 'https://zenodo.org/records/'+str(pub['id'])
assert public['status'] == 'PASS_PUBLIC_RECORD_EXACT_METADATA_AND_ALL_FILE_BYTES'
assert public['doi'] == tracker['doi'] == pub['doi']
assert len(public['all_reviewed_metadata_keys_compared']) == 11
assert len(public['all_file_bytes']) == 2 and all(x['entire_public_download_equals_reviewed_local_file'] for x in public['all_file_bytes'])
assert tracker['status'] == 'PASS_ONE_ROW_APPENDED_AND_EXACT_READBACK'
assert tracker['spreadsheetId'] == '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20' and tracker['gid'] == 1254632077
assert pub['doi_resolution']['http_status'] == 200
assert cap.git('branch','--show-current') == b'main\n'
cap.git('merge-base','--is-ancestor',merged['actual_merge'],'HEAD')
api = json.loads(cap.run('actual_merged_pr',['/opt/homebrew/bin/gh','api','repos/AlecKriebel/Math/pulls/311']).stdout)
assert api['merged'] and api['merge_commit_sha'] == merged['actual_merge'] and api['head']['sha'] == merged['accepted_head']
oldbody = (A/'accepted_pr_body.txt').read_text()
assert api['body'] == oldbody
newbody = oldbody+'\nActual publication: '+pub['doi_url']+' ([Zenodo record '+str(pub['id'])+']('+pub['record_url']+')). All eleven reviewed metadata fields and both complete public file downloads match the cleared submission. The DOI resolves with HTTP 200. Exactly one row was appended to the specified Math Puzzles tracker, '+tracker['updatedRange']+', and read back exactly.\n'
(A/'published_pr_body.txt').write_text(newbody)
request = cap.directory/'body_update_request.json'
request.write_text(json.dumps({'body':newbody})+'\n')
argv = ['/opt/homebrew/bin/gh','api','--method','PATCH','repos/AlecKriebel/Math/pulls/311','--input',str(request)]
(A/'published_pr_body_update_preexecution.json').write_text(json.dumps({'utc':utc(),'argv':argv,
    'published_body':pin(A/'published_pr_body.txt'),'automatic_retry':False},indent=2)+'\n')
window()
updated = json.loads(cap.run('update_own_merged_pr_body',argv).stdout)
assert updated['body'] == newbody and updated['merged']
again = json.loads(cap.run('readback_own_merged_pr_body',['/opt/homebrew/bin/gh','api','repos/AlecKriebel/Math/pulls/311']).stdout)
assert again['body'] == newbody and again['merge_commit_sha'] == merged['actual_merge']
queue = R/QUEUE
before = queue.read_bytes()
assert before == cap.git('show','HEAD:'+QUEUE)
lines = before.splitlines(keepends=True)
i = ownrow(lines)
oldrow = lines[i]
cells = oldrow.split(b'|')
assert cells[8].strip() == b'claimed_solved' and cells[9].strip() == b'2/5' and not cells[12].strip()
cells[12] = (' '+pub['doi_url']+' ').encode()
newrow = b'|'.join(cells)
lines[i] = newrow
after = b''.join(lines)
assert [j for j,(x,y) in enumerate(zip(oldrow.split(b'|'),newrow.split(b'|'))) if x != y] == [12]
window()
queue.write_bytes(after)
qrec = {'utc':utc(),'status':'PASS_ONLY_OWN_DOI_QUEUE_CELL_CHANGED','queue_physical_line':i+1,
    'only_pipe_cells':[12],'old_row':oldrow.decode(),'new_row':newrow.decode(),'all_other_queue_bytes_unchanged':True,
    'original_author_turns':'2/5','before_sha256':sha(before),'after_sha256':sha(after)}
(A/'queue_publication_receipt.json').write_text(json.dumps(qrec,indent=2)+'\n')
stamp = utc()
result = {'utc':stamp,'status':'MERGED_PUBLISHED_AND_TRACKER_VERIFIED','pr':311,'problem':'30005303',
    'mathematical_verification_percent':100,'bounded_priority_percent':100,'workflow_completion_percent':100,
    'actual_merge':merged['actual_merge'],'accepted_head':merged['accepted_head'],'merged_at':merged['merged_at'],
    'zenodo_record':pub['id'],'doi':pub['doi'],'doi_url':pub['doi_url'],'record_url':pub['record_url'],
    'tracker_spreadsheet_id':tracker['spreadsheetId'],'tracker_gid':tracker['gid'],'tracker_range':tracker['updatedRange'],
    'formal_submission_files':clear['formal_submission_files'],'final_clean_review':clear['final_clean_review'],
    'unresolved_findings':0,'metadata_semantics_changed':False,'all_eleven_public_metadata_fields_equal':True,
    'both_whole_public_files_equal':True,'doi_resolved_http200':True,'one_tracker_row_exact_readback':True,
    'original_attempt_files_unchanged':29,'original_author_turn_count':'2/5','historical_first_priority_certified':False,
    'unrefereed':True,'extensive_AI_use':True,'independent_external_human_review':False,
    'formal_proof_assistant_certification':False,'no_release_or_journal_submission':True,'no_person_contacted':True,
    'persistent_goal_complete':False,'published_pr_body_exact_readback':True,'capture_directory':str(cap.directory)}
(A/'CURRENT_PUBLICATION_STATUS.json').write_text(json.dumps(result,indent=2)+'\n')
publication = ('Published '+stamp+' after exact merged-tree and complete fresh-review verification.\n\n'
    'Preprint: '+pub['doi_url']+'\n\nRecord: '+pub['record_url']+'\n\n'
    'The five-page PDF and portable verification ZIP match the cleared submission byte for byte in complete unauthenticated public downloads. All eleven metadata fields match. The DOI resolves with HTTP 200. Exactly one row was appended to the specified Math Puzzles sheet, '+tracker['updatedRange']+', and read back exactly. No chat was shared and no individual was contacted.\n\n'
    'Mathematical verification100%; bounded priority audit100%; this PR review/merge/publication workflow100%. Successive NEW whole-preprint reviews completed with global provenance/count corrections and final zero unresolved findings. The general binary MTP2 original-edge closure and attractive-approximation characterization answers source Conjecture1; the earlier Gandolfi–Lenarda witness for Conjectures2/3 is credited. This is an unrefereed preprint with extensive AI use, without external human peer review or a historical first-priority certificate. The author count2/5 and all29 original attempt files are preserved. The persistent descending program remains active.\n')
(A/'publication/PUBLICATION.md').write_text(publication)
native = R/RELEASE
original_release = cap.git('show','HEAD:'+RELEASE)
assert native.read_bytes() == original_release
window()
with native.open('a') as f:
    f.write('\n## Actual publication\n\n'+publication)
(A/'native_publication_note_receipt.json').write_text(json.dumps({'utc':utc(),'path':RELEASE,
    'original_release_sha256':sha(original_release),'published_release_sha256':sha(native.read_bytes()),
    'only_actual_publication_section_appended':True,'original29_attempt_files_unchanged':True},indent=2)+'\n')
status = load(A/'CURRENT_PACKAGE_STATUS.json')
status.update(recorded_utc=stamp,status=result['status'],workflow_percent=100,publication_ready=True,
    second_full_review_active=False,merge_performed=True,zenodo_upload_performed=True,tracker_append_performed=True,
    doi=pub['doi'],zenodo_record=pub['id'],tracker_range=tracker['updatedRange'],persistent_goal_complete=False)
(A/'CURRENT_PACKAGE_STATUS.json').write_text(json.dumps(status,indent=2)+'\n')
inv = load(P/'inventory.json')
before_inv = copy.deepcopy(inv)
row = next(x for x in inv['items'] if x['number'] == 311)
assert row['submitted_status'] == row['original_submitted_status'] == 'claimed_solved'
assert 311 not in inv['claimed_solved_published_by_descending'] and 311 not in inv['claimed_solved_merged_by_descending']
row.update(disposition='merged_claimed_solved_published_zenodo_tracker_verified',workflow_percent=100,
    audit_workflow_percent=100,mathematical_acceptance=True,priority_acceptance=True,preprint_ready=True,
    publication_ready=True,actual_merge=merged['actual_merge'],accepted_head=merged['accepted_head'],
    merged_at=merged['merged_at'],doi=pub['doi'],zenodo_record=pub['id'],final_clean_review=clear['final_clean_review'],
    current_publication_status='audits/pr311_30005303/CURRENT_PUBLICATION_STATUS.json')
for key in ['claimed_solved_published_by_descending','claimed_solved_merged_by_descending']:
    inv[key].append(311)
inv['completed_by_descending'] += 1
assert all(x == y for x,y in zip(before_inv['items'],inv['items']) if x['number'] != 311)
window()
(P/'inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
shared = load(P/'SHARED_GIT_WINDOW_STATUS.json')
shared.update(utc=stamp,descending_311_workflow_percent=100,descending_311_complete=True,
    descending_final_acceptance_preparing=False,descending_git_checkpoint_preparing=True,
    descending_checkpoint_scope='PR311 exact accepted note published; public metadata and whole files equal; DOI tracker row verified; scoped completion checkpoint preparing.')
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(shared,indent=2)+'\n')
log = stamp+' — PR311 complete: actual merge '+merged['actual_merge']+'; production DOI '+pub['doi']+'; all11 public metadata fields and both complete public file bytes exact; DOI HTTP200; ONE tracker row '+tracker['updatedRange']+' exact readback; own merged PR body updated/read back, only own QUEUE DOI cell12 changed and current native publication note appended. Cleared v02 formal files and closed scientific/review evidence unchanged. Math100%,boundedpriority100%,PR311workflow100%; original29 files and author2/5 preserved, successive NEWfull reviews after global provenance/count repairs with final zero findings. C2/C3 exact old witness credited; no human review or historical-first certificate, GitHub release, journal submission, person contact, duplicate deposit or append. Persistent goal remains active; next eligible descending intake after scoped push.\n'
for target in [P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']:
    with target.open('a') as f:
        f.write('\n'+log)
current_clearance()
print(json.dumps(result,indent=2))
