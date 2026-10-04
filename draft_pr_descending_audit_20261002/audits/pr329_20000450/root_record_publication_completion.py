"""Record actual publication without changing any cleared scientific artifact."""
from root_submission_gate import *

assert not (A/'CURRENT_PUBLICATION_STATUS.json').exists()
assert not (A/'published_pr_body_update_preexecution.json').exists()
clear=current_clearance();window();cap=Capture('publication_completion')
merged=load(A/'ACTUAL_MERGE_VERIFICATION.json')
post=load(A/'ROOT_POST_MERGE_VERIFICATION.json')
pub=load(A/'publication/inspect_published_receipt.json')
public=load(A/'publication/PUBLIC_RECORD_VERIFICATION.json')
tracker=load(A/'publication/TRACKER_COMPLETE.json')
assert merged['status']=='PASS_PR329_EXACT_MERGE'
assert post['status']=='PASS_PR329_POST_MERGE_EXACT_SUBMISSION'
assert post['actual_merge']==merged['actual_merge']
assert pub['state']=='published' and pub['environment']=='production'
assert pub['doi']=='10.5281/zenodo.23137834' and pub['id']==23137834
assert public['status']=='PASS_PUBLIC_RECORD_EXACT_METADATA_AND_ALL_FILE_BYTES'
assert public['doi']==tracker['doi']==pub['doi']
assert len(public['all_reviewed_metadata_keys_compared'])==11
assert len(public['all_file_bytes'])==2 and all(x['entire_public_download_equals_reviewed_local_file'] for x in public['all_file_bytes'])
assert tracker['status']=='PASS_ONE_ROW_APPENDED_AND_EXACT_READBACK'
assert tracker['updatedRange']=="'Math Puzzles'!A21:D21"
assert pub['doi_resolution']['http_status']==200
assert cap.git('rev-parse','HEAD').decode().strip()==merged['actual_merge']
assert cap.git('branch','--show-current')==b'main\n'
api=json.loads(cap.run('actual_merged_pr',['gh','api','repos/AlecKriebel/Math/pulls/329']).stdout)
assert api['merged'] and api['merge_commit_sha']==merged['actual_merge'] and api['head']['sha']==merged['accepted_head']
oldbody=(A/'accepted_pr_body.txt').read_text()
assert api['body'].strip()==oldbody.strip()
needle='The exact qualified PDF and verification ZIP are ready for production Zenodo publication and subsequent DOI tracker registration.'
assert oldbody.count(needle)==1
newbody=oldbody.replace(needle,'The exact qualified PDF and verification ZIP are published at '+pub['doi_url']+' (record '+str(pub['id'])+'). All eleven reviewed metadata fields and both complete public downloads match exactly. The DOI and paper details are registered in the Math Puzzles tracker, row A21:D21, with exact readback.')
(A/'published_pr_body.txt').write_text(newbody)
request=cap.directory/'body_update_request.json';request.write_text(json.dumps({'body':newbody})+'\n')
argv=['gh','api','--method','PATCH','repos/AlecKriebel/Math/pulls/329','--input',str(request)]
(A/'published_pr_body_update_preexecution.json').write_text(json.dumps(dict(utc=utc(),argv=argv,published_body=pin(A/'published_pr_body.txt'),automatic_retry=False),indent=2)+'\n')
updated=json.loads(cap.run('update_own_merged_pr_body',argv).stdout)
assert updated['body'].strip()==newbody.strip() and updated['merged']
again=json.loads(cap.run('readback_own_merged_pr_body',['gh','api','repos/AlecKriebel/Math/pulls/329']).stdout)
assert again['body'].strip()==newbody.strip() and again['merge_commit_sha']==merged['actual_merge']
queue=R/QUEUE;before=queue.read_bytes();assert before==cap.git('show','HEAD:'+QUEUE)
lines=before.splitlines(keepends=True)
hits=[i for i,x in enumerate(lines) if len(x.split(b'|'))>2 and x.split(b'|')[2].strip().split(b' / ')[0]==b'20000450']
assert len(hits)==1;i=hits[0];oldrow=lines[i];cells=oldrow.split(b'|')
assert cells[8].strip()==b'claimed_solved' and cells[9].strip()==b'1/5' and not cells[12].strip()
cells[12]=(' '+pub['doi_url']+' ').encode();newrow=b'|'.join(cells)
lines[i]=newrow;after=b''.join(lines)
assert [j for j,(x,y) in enumerate(zip(oldrow.split(b'|'),newrow.split(b'|'))) if x!=y]==[12]
queue.write_bytes(after)
qrec=dict(utc=utc(),status='PASS_ONLY_OWN_DOI_QUEUE_CELL_CHANGED',queue_physical_line=i+1,only_pipe_cells=[12],
          old_row=oldrow.decode(),new_row=newrow.decode(),all_other_queue_bytes_unchanged=True,
          original_author_turns='1/5',before_sha256=sha(before),after_sha256=sha(after))
(A/'queue_publication_receipt.json').write_text(json.dumps(qrec,indent=2)+'\n')
stamp=utc()
result=dict(utc=stamp,status='MERGED_PUBLISHED_AND_TRACKER_VERIFIED',pr=329,problem='20000450',
    mathematical_verification_percent=100,priority_percent=100,workflow_completion_percent=100,
    actual_merge=merged['actual_merge'],accepted_head=merged['accepted_head'],merged_at=merged['merged_at'],
    zenodo_record=pub['id'],doi=pub['doi'],doi_url=pub['doi_url'],record_url=pub['record_url'],
    tracker_spreadsheet_id=tracker['spreadsheetId'],tracker_gid=tracker['gid'],tracker_range=tracker['updatedRange'],
    formal_submission_files=clear['formal_submission_files'],final_clean_review=2,unresolved_findings=0,
    metadata_semantics_changed=False,all_eleven_public_metadata_fields_equal=True,all_two_public_files_equal=True,
    doi_resolved_http200=True,one_tracker_row_exact_readback=True,original_attempt_files_unchanged=21,
    original_author_turn_count='1/5',first_priority_certified=False,unrefereed=True,extensive_AI_use=True,
    independent_external_human_review=False,formal_proof_assistant_certification=False,
    no_release_or_journal_submission=True,no_person_contacted=True,persistent_goal_complete=False,
    published_pr_body_exact_readback=True,capture_directory=str(cap.directory))
(A/'CURRENT_PUBLICATION_STATUS.json').write_text(json.dumps(result,indent=2)+'\n')
(O/'PUBLICATION_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
publication=('Published '+stamp+' after exact merged-tree and held-review verification.\n\n'
    'Preprint: '+pub['doi_url']+'\n\nRecord: '+pub['record_url']+'\n\n'
    'The seven-page PDF and the 50-payload verification package plus manifest match the reviewed files byte for byte in complete unauthenticated public downloads. All eleven metadata fields match. The DOI resolves with HTTP 200. Exactly one row was appended to the specified Math Puzzles sheet, A21:D21, and read back exactly. No chat was shared and no individual was contacted.\n\n'
    'Mathematical verification 100%; bounded priority audit 100%; this PR review/merge/publication workflow 100%. Two successive new whole-preprint reviews completed; the first attribution finding was repaired globally and the final review has zero unresolved findings. This is an unrefereed preprint with extensive AI use, without independent external human peer review or a first-priority certificate. The original author count 1/5 and all 21 original attempt files are preserved. The persistent descending program remains active.\n')
(O/'PUBLICATION.md').write_text(publication)
with (R/RELEASE).open('a') as f:f.write('\n## Actual publication\n\n'+publication)
for target in [A/'PREPRINT_READINESS.json',O/'READINESS.json']:
    j=load(target);j.update(utc=stamp,status=result['status'],workflow_percent=100,merged=True,published=True,
        tracker_complete=True,doi=pub['doi'],zenodo_record=pub['id'],exact_remaining_gates=[],
        review02_exposure='Source-only and first-candidate independent stages held before full packet; final whole review closed and independently reproduced.',
        persistent_goal_complete=False)
    target.write_text(json.dumps(j,indent=2)+'\n')
inv=load(P/'inventory.json');row=next(x for x in inv['items'] if x['number']==329)
row.update(disposition='merged_claimed_solved_published_zenodo_tracker_verified',workflow_percent=100,
    audit_workflow_percent=100,mathematical_acceptance=True,priority_acceptance=True,preprint_ready=True,
    publication_ready=True,actual_merge=merged['actual_merge'],accepted_head=merged['accepted_head'],
    merged_at=merged['merged_at'],doi=pub['doi'],zenodo_record=pub['id'],final_clean_review=2,
    current_publication_status='audits/pr329_20000450/CURRENT_PUBLICATION_STATUS.json')
for key in ['claimed_solved_published_by_descending','claimed_solved_merged_by_descending']:
    assert 329 not in inv[key];inv[key].append(329)
inv['completed_by_descending']+=1
(P/'inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
shared=load(P/'SHARED_GIT_WINDOW_STATUS.json');shared.update(utc=stamp,descending_329_workflow_percent=100,
    descending_329_complete=True,descending_final_acceptance_preparing=False,descending_git_checkpoint_preparing=True,
    descending_checkpoint_scope='PR329 exact merged preprint published with unchanged metadata and files; DOI tracker row21 confirmed; scoped completion checkpoint preparing.')
(P/'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(shared,indent=2)+'\n')
log=stamp+' — PR329 complete: actual merge '+merged['actual_merge']+'; production DOI '+pub['doi']+'; all11 public metadata fields and both complete public file bytes exact; DOI HTTP200; ONE tracker row A21:D21 exact readback; own merged PR body updated/read back, own QUEUE DOI cell12 only. Current v03 formal files and all held scientific/review evidence unchanged. Math100%, bounded priority100%, PR329 workflow100%; original21 attempt files and author1/5 preserved, two successive NEW whole reviews with global attribution repair and final zero findings. No external human review or firstness certificate; no GitHub release, journal submission, outside person contact or duplicate deposit/append. Persistent goal active; next eligible descending intake after scoped push. Initial post-merge driver call used a relative child path and failed before execution; exact failure retained, corrected absolute-path native call passed.\n'
for target in [P/'RESEARCH_LOG.md',A/'RESEARCH_LOG.md']:
    with target.open('a') as f:f.write('\n'+log)
current_clearance()
print(json.dumps(result,indent=2))
