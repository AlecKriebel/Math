"""Record actual PR210 completion only after guarded native merged readback."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,importlib.util,json,os
D=Path(__file__).resolve().parent;C=D.parent;P=D.parents[2];PUB=C/'publication';R=C/'preprint'
load=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=load(PUB/'PR_MERGED.json');prepared=load(PUB/'PR_PREPARED.json')
assert m['merged'] is True and m['PR']==210 and m['program_counts']==[44,21,21,0]
assert m['reviewed_head']==prepared['prepared_head']
assert m['doi_url']=='https://doi.org/10.5281/zenodo.23398175'
assert m['tracker_range']=="'Math Puzzles'!A113:D113"
readback=load(PUB/'NATIVE_SCIENTIFIC_READBACK.json')
assert readback['status']=='PASS' and readback['head']==m['reviewed_head']
assert all(row['byte_identical'] is True for row in readback['actual_current_source_original_archive_and_submission_readbacks'])
assert all(row['native_tree_identity_verified'] is True for row in readback['all_included_owned_native_tree_identities'])
assert len(readback['all_included_owned_native_tree_identities'])==len(prepared['included_owned_pins'])
spec=importlib.util.spec_from_file_location('final_pr210_pure_binding',PUB/'release_binding.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
ctx=g.context(R);z=g.publication(R,PUB,ctx);t=g.tracker(R,PUB,ctx,z)
assert m['release_binding']==g.binding(ctx)
reconciliation=load(PUB/'RELEASE_BINDING_RECONCILIATION.json')
assert reconciliation['verified'] is True and reconciliation['additional_stage_publish_append_update_or_native_mutations']==0
assert t['append_count']==1 and t['additional_append_or_update_calls']==0
assert z['single_publish_attempt'] is True and z['additional_stage_or_publish_calls']==0
initial=C/'initial_review_20261015/history/release_helpers_review03_frozen'
originals=load(D/'INTAKE.json')['original_source_files'];F=PUB/'native_current_source'
original_checks=[]
for row in originals:
    rel=row['native_path'].removeprefix('unsolved_math_prioritization/attempts/5100033/')
    p=F/'history/original_submission_20261015'/rel
    assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256']
    original_checks.append(dict(path=rel,sha256=row['sha256'],byte_exact=True))
assert len(original_checks)==20
qpin=next(row for row in prepared['included_owned_pins'] if row['path']=='unsolved_math_prioritization/QUEUE.md')
utc=datetime.now(timezone.utc).isoformat()
def atomic(path,value):
    temp=path.with_name(path.name+'.finalize-tmp')
    with temp.open('x') as f:f.write(json.dumps(value,indent=2)+'\n');f.flush();os.fsync(f.fileno())
    os.replace(temp,path);g.sync_directory(path.parent)
receipt=dict(utc=utc,case_completion_percent=100,PR=210,problem_id=5100033,
    actual_publication_tracker_native_merge_complete=True,
    original_head=prepared['original_head'],accepted_head=m['reviewed_head'],merge_commit=m['merge_commit'],
    accepted_queue_blob=qpin['git_blob_sha1'],accepted_queue_row=prepared['target_queue_row'],
    exact_source_specific_odd_outer_focal_pedal_theorem_verified=True,
    primitive_star_domain_repetitions_circle_and_even_boundary_explicit=True,
    author_proof_turns='1/5',original20_native_archives=original_checks,
    mathematical_source_reconstruction_families=3,independent_priority_families=2,
    new_sequential_whole_manuscript_reviews=3,final_frozen_clean_whole_review='whole_manuscript_adversary_03',
    supporting_source_reviews=5,final_clean_supporting_source_review='release_helpers_adversary_05',
    final_supporting_controls_root_reproduced=218,mandatory_findings=[],optional_findings=[],
    final_clearance_sha256=sha(R/'FINAL_CLEARANCE.json'),release_binding=g.binding(ctx),
    DOI=z['doi'],record_url=z['record_url'],actual_both_public_size_SHA256_verified=True,
    exact_metadata_verified=True,tracker_range=t['updated_range'],single_append_all_four_cells_verified=True,
    original_publish_and_append_once_only_intents_preserved=True,extra_publish_or_append_calls=0,
    native_owned_tree_identities_verified=len(readback['all_included_owned_native_tree_identities']),
    native_actual_current_source_archive_and_submission_body_readbacks=len(readback['actual_current_source_original_archive_and_submission_readbacks']),
    all_scientific_claims_reproduced_before_release=True,AI_assistance_extensive=True,unrefereed=True,
    independent_human_peer_review=False,formal_proof_assistant_verification=False,
    no_absolute_priority_first_proof_new_general_method_or_current_world_open_claim=True,
    bounded_priority_and_documented_source_access_limits_preserved=True,
    counts=[44,21,21,0],goal_active_incomplete=True,next_descending_cursor=209,
    excluded_PR8=True,held_uncompleted_PRs=[293,292,280,239],local_Git_index_or_ref_mutations=0)
out=D/'ROOT_FINAL_CASE_ACCEPTANCE.json';assert not out.exists();atomic(out,receipt)
for path in [D/'CURRENT_AUDIT_STATE.json',P/'CURRENT_GOAL_SELECTION_20261013.json']:
    value=load(path);value.update(utc=utc,stage='complete_verified_publication_tracker_and_native_merge',
        current_stage='complete_verified_publication_tracker_and_native_merge',completion_percent=100,
        case_completion_percent=100,current_case_completion_percent=100,counts=[44,21,21,0],program_counts=[44,21,21,0],
        goal_active_incomplete=True,overall_goal_active_incomplete=True,preprint_upload_cleared=True,
        native_merge_complete=True,actual_publication_tracker_native_merge_complete=True,
        renewed_release_binding_reconciliation_pending=False,renewed_release_binding_reconciliation_verified=True,
        current_DOI=z['doi'],current_tracker_range=t['updated_range'],actual_native_merge=m['merge_commit'],
        accepted_PR_head=m['reviewed_head'],accepted_PR_queue_blob=qpin['git_blob_sha1'],
        whole_manuscript_reviews_completed=3,release_helper_source_reviews_completed=5,
        final_clean_reviews=1,unresolved_review_findings=[],
        third_new_whole_manuscript_review_active=False,release_helper_source_review_active=False,
        release_helper_source_review04_active=False,release_helper_source_review05_active=False,
        current_PR_head=m['reviewed_head'],original_PR_head=prepared['original_head'],
        final_clearance_sha256=sha(R/'FINAL_CLEARANCE.json'),final_case_acceptance=str(out.relative_to(P)),
        storage_wait_for_this_case_resolved=True)
    if path.parent==P:
        value.update(previous_completed_PR=210,previous_completed_DOI=z['doi'],previous_completion_counts=[44,21,21,0],
            last_native_merge=m['merge_commit'],Queue_blob=qpin['git_blob_sha1'],next_descending_cursor=209)
    atomic(path,value)
line='\n- '+utc+' — PR210100%: actual expected-head native merge '+m['merge_commit']+' accepted head '+m['reviewed_head']+'. All'+str(receipt['native_owned_tree_identities_verified'])+' included owned blob identities and'+str(receipt['native_actual_current_source_archive_and_submission_body_readbacks'])+' current-source/original-archive/PDF/ZIP body readbacks verified; all20originals exact. Published same reviewed PDF/181ZIP at '+z['doi']+', exact metadata, actualDOI200 and both publicSHA; exactly1GWS append/all4cells '+t['updated_range']+'. Three fresh sequential whole-package reviews and five supporting workflow reviews/global repairs complete; zero unresolved mandatory/optional findings. ExtensiveAI/unrefereed/nohumanpeerreview/noformalproof; historical priority undetermined and source-access limits retained, no first/newgeneralmethod/worldopen claim. Counts44completed/21preprints/21merges/0pendingtracker. Held293/292/280/239 unchanged; goalACTIVE/INCOMPLETE; next exact-status descent below210 after final completion checkpoint.\n'
for path in [D/'RESEARCH_LOG.md',P/'RESEARCH_LOG.md']:
    with path.open('a') as f:f.write(line)
print(json.dumps({k:v for k,v in receipt.items() if k not in ['original20_native_archives']},indent=2))
